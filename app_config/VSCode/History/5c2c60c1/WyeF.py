# Copyright (C) 2021. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

import math
import numpy as np
import torch
from functools import partial


from model.base import BaseModule
from model.unet import GradLogPEstimator2d


class Diffusion_SB(BaseModule):
    # Bridge-gmax:
    # g2_t即beta_t;  g2_min,g2_max即beta_0,beta_1 (但谁对应谁，不明)
    # f(t)=0, g^2(t)= (g2_max-g2_min)*t + g2_min, alpha_t=1, sigma2_t= (g2_max-g2_min)*t^2/2 + g2_min*t
    # 故 t=1时, sigma2_1 = (g2_max+g2_min)/2
    def __init__(self, n_feats=80, dim=64,
                 n_spks=1, spk_emb_dim=64,
                 g2_min=0.01, g2_max=8, g2_max_t=1, pe_scale=1000, predictor="hpsi", offset=1e-5, sampling_temp=2.0, sde_lambda=0.1):
        super(Diffusion_SB, self).__init__()

        self.n_feats = n_feats
        self.dim = dim
        self.n_spks = n_spks
        self.spk_emb_dim = spk_emb_dim
        self.pe_scale = pe_scale

        self.g2_min = g2_min
        self.g2_max = g2_max
        self.g2_max_t = g2_max_t
        self.alpha_1 = 1

        self.sampling_temp = sampling_temp
        self.sde_lambda2 = sde_lambda ** 2

        # Linear schedule for g2
        self.k1 = (self.g2_max - self.g2_min) / self.g2_max_t
        if self.g2_max_t < 1:
            self.k2 = (self.g2_max - self.g2_min) / (1 - self.g2_max_t)
        else:
            self.k2 = 0
        self.sigma2_1 = (self.g2_min + self.g2_max) / 2
        self.sigma2_half = (self.g2_min + self.g2_max) * self.g2_max_t / 2

        self.predictor = predictor
        self.offset = offset


        self.estimator = GradLogPEstimator2d(dim, n_spks=n_spks,
                                             spk_emb_dim=spk_emb_dim,
                                             pe_scale=pe_scale)

    def get_alpha(self, t):
        return 1

    def get_bar_alpha(self, t):
        return 1

    def get_sigma2(self, t):
        half_flag = t <= self.g2_max_t
        sigma2 = torch.zeros_like(t)
        sigma2[half_flag] = (self.g2_min + (self.g2_min + t[half_flag] * self.k1)) * t[half_flag] / 2
        sigma2[~half_flag] = self.sigma2_half + (self.g2_max + (self.g2_max - (t[~half_flag] - self.g2_max_t) * self.k2)) * (t[~half_flag] - self.g2_max_t) / 2
        return sigma2

    def get_bar_sigma2(self, t):
        sigma2 = self.sigma2_1 - self.get_sigma2(t)
        return sigma2

    def forward_diffusion(self, x0, mask, x1, t):
        time = t.unsqueeze(-1).unsqueeze(-1)
        alpha_t = self.get_alpha(time)
        bar_alpha_t = self.get_bar_alpha(time)
        sigma2_t = self.get_sigma2(time)
        bar_sigma2_t = self.get_bar_sigma2(time)

        z = torch.randn(x0.shape, dtype=x0.dtype, device=x0.device, requires_grad=False)
        xt = (alpha_t*bar_sigma2_t*x0 + bar_alpha_t*sigma2_t*x1)/(bar_sigma2_t + sigma2_t) + torch.sqrt((alpha_t**2 * sigma2_t * bar_sigma2_t)/(bar_sigma2_t + sigma2_t)) * z
        xt.detach()

        if self.predictor == "hpsi":
            # 预测\nabla\log p\hat{\psi}_t
            target = (xt - alpha_t * x0) / (alpha_t * torch.sqrt(sigma2_t))

            # Control the variance of the input to 1
            xt = (xt - alpha_t/self.alpha_1*x1) / (alpha_t * torch.sqrt(bar_sigma2_t))
            xt.detach()
            target.detach()
            weight = 1

        elif self.predictor == "x0":
            target = x0
            target.detach()
            weight = 1

        else:
            raise NotImplementedError(f"Unsupported predictor {self.predictor}")
        target.detach()
        return xt * mask, target * mask, weight


    @torch.no_grad()
    def data_estimation(self, xt, mask, x1, t, spk):
        time = t.unsqueeze(-1).unsqueeze(-1)

        if self.predictor == "hpsi":
            alpha_t = self.get_alpha(time)
            sigma_t = torch.sqrt(self.get_sigma2(time))
            bar_sigma_t = torch.sqrt(self.get_bar_sigma2(time))

            normalized_x1 = (x1 + 5.0) / 5.0
            xt_input = (xt - alpha_t/self.alpha_1*x1) / (alpha_t * bar_sigma_t)
            eps_t = self.estimator(xt_input, mask, normalized_x1, t, spk)

            hat_x0 = xt/alpha_t - sigma_t * eps_t

        elif self.predictor == "x0":
            normalized_x1 = (x1 + 5.0) / 5.0
            hat_x0 = self.estimator(xt, mask, normalized_x1, t, spk)

        else:
            raise NotImplementedError(f"Unsupported predictor {self.predictor}")


        # elif self.predictor == "velocity":
        #     beta_t = self.get_symmetric_noise(t, cumulative=False)
        #     var_fwd_t = self.get_symmetric_noise(t, cumulative=True)**2
        #     var_bwd_t = self.get_symmetric_noise(1-t, cumulative=True)**2
        #     pred = self.estimator(xt, mask, x1, t, spk)
        #     hat_x0 = xt + (2*pred)/(beta_t * var_bwd_t) - (var_fwd_t)/(var_bwd_t)*(xt - x1)

        return hat_x0

    @torch.no_grad()
    def reverse_diffusion(self, x1, mask, n_timesteps, sampler="pf_ode_euler",
                          spk=None, clip_denoise=False, verbose=True):

        if "second" in sampler:
            assert n_timesteps % 2 == 0 and n_timesteps > 1
            n_timesteps = n_timesteps // 2

        h = 1.0 / n_timesteps
        xt = x1
        # Method1: Calculate the first xs with x1=x0
        if sampler == 'pf_ode_first_order_n':
            init_s = (1.0 - self.offset) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
            alpha_t = self.get_alpha(init_s)
            bar_alpha_t = self.get_bar_alpha(init_s)
            sigma2_t = self.get_sigma2(init_s)
            bar_sigma2_t = self.get_bar_sigma2(init_s)
            z = torch.randn(xt.shape, dtype=xt.dtype, device=xt.device, requires_grad=False)
            xt = (alpha_t*bar_sigma2_t*x1 + bar_alpha_t*sigma2_t*x1)/(bar_sigma2_t + sigma2_t) + torch.sqrt((alpha_t**2 * sigma2_t * bar_sigma2_t)/(bar_sigma2_t + sigma2_t)) * z

        # Method2: Calculate the first xs with an additional NFE step
        elif sampler == 'pf_ode_first_order_n2':
            init_s = (1.0 - self.offset) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
            x0_s = self.data_estimation(xt, mask, x1, init_s, spk)
            alpha_t = self.get_alpha(init_s)
            bar_alpha_t = self.get_bar_alpha(init_s)
            sigma2_t = self.get_sigma2(init_s)
            bar_sigma2_t = self.get_bar_sigma2(init_s)
            z = torch.randn(x1.shape, dtype=x1.dtype, device=x1.device, requires_grad=False)
            xt = (alpha_t*bar_sigma2_t*x0_s + bar_alpha_t*sigma2_t*x1)/(bar_sigma2_t + sigma2_t) + torch.sqrt((alpha_t**2 * sigma2_t * bar_sigma2_t)/(bar_sigma2_t + sigma2_t)) * z
            n_timesteps -= 1

        xt = xt * mask
        xt_traj = [xt.detach().cpu()]
        for i in range(n_timesteps):

            if sampler == 'sde_first_order':
                # s -> t
                s = (1.0 - self.offset - (i*h)) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                t = max(self.offset, 1.0 - self.offset - (i+1)*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                # Prepare all needed variables
                sigma2_t = self.get_sigma2(t)
                sigma2_s = self.get_sigma2(s)
                alpha_t = self.get_alpha(t)
                alpha_s = self.get_alpha(s)

                xs = xt
                hat_x0 = self.data_estimation(xs, mask, x1, s, spk)

                coeff = (sigma2_t)/(sigma2_s)
                xt = (alpha_t/alpha_s)*coeff * xs + alpha_t * (1-coeff) * hat_x0
                if i != n_timesteps - 1:
                    eps = torch.randn(x1.shape, dtype=x1.dtype, device=x1.device, requires_grad=False) / self.sampling_temp
                    xt += alpha_t * torch.sqrt(sigma2_t * (1 - coeff)) * eps
                xt = xt * mask

            elif sampler == 'pf_ode_first_order' or sampler == 'pf_ode_first_order_n' or sampler == 'pf_ode_first_order_n2':
                # s -> t
                s = (1.0 - self.offset - (i*h)) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                t = max(self.offset, 1.0 - self.offset - (i+1)*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                # Prepare all needed variables
                sigma2_t = self.get_sigma2(t)
                bar_sigma2_t = self.get_bar_sigma2(t)
                sigma2_s = self.get_sigma2(s)
                bar_sigma2_s = self.get_bar_sigma2(s)
                sigma_t = torch.sqrt(sigma2_t)
                bar_sigma_t = torch.sqrt(bar_sigma2_t)
                sigma_s = torch.sqrt(sigma2_s)
                bar_sigma_s = torch.sqrt(bar_sigma2_s)
                sigma2_1 = sigma2_t + bar_sigma2_t
                alpha_t = self.get_alpha(t)
                alpha_s = self.get_alpha(s)

                xs = xt
                hat_x0 = self.data_estimation(xs, mask, x1, s, spk)

                xt = (alpha_t*sigma_t*bar_sigma_t)/(alpha_s*sigma_s*bar_sigma_s) * xs + alpha_t/sigma2_1 * ((bar_sigma2_t - (bar_sigma_s*sigma_t*bar_sigma_t)/(sigma_s)) * hat_x0 + (sigma2_t - (sigma_s*sigma_t*bar_sigma_t)/(bar_sigma_s)) * x1/self.alpha_1)
                xt = xt * mask

            elif sampler == 'sde_first_order_lambda':
                # s -> t
                s = (1.0 - self.offset - (i*h)) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                t = max(self.offset, 1.0 - self.offset - (i+1)*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                # Prepare all needed variables
                sigma2_t = self.get_sigma2(t)
                bar_sigma2_t = self.get_bar_sigma2(t)
                sigma2_s = self.get_sigma2(s)
                bar_sigma2_s = self.get_bar_sigma2(s)
                sigma_t = torch.sqrt(sigma2_t)
                bar_sigma_t = torch.sqrt(bar_sigma2_t)
                sigma_s = torch.sqrt(sigma2_s)
                bar_sigma_s = torch.sqrt(bar_sigma2_s)
                sigma2_1 = sigma2_t + bar_sigma2_t
                alpha_t = self.get_alpha(t)
                alpha_s = self.get_alpha(s)
                bar_alpha_t = self.get_bar_alpha(t)

                xs = xt
                hat_x0 = self.data_estimation(xs, mask, x1, s, spk)

                coeff_sigma_t = sigma_t**(1+self.sde_lambda2) * bar_sigma_t**(1-self.sde_lambda2)
                coeff_xs = (alpha_t/alpha_s) * (coeff_sigma_t)/(sigma_s**(1+self.sde_lambda2) * bar_sigma_s**(1-self.sde_lambda2))
                coeff_x1 = (bar_alpha_t * coeff_sigma_t)/sigma2_1 * ((sigma_t**(1-self.sde_lambda2)/bar_sigma_t**(1-self.sde_lambda2)) - (sigma_s**(1-self.sde_lambda2)/bar_sigma_s**(1-self.sde_lambda2)))
                coeff_hat_x0 = (alpha_t * coeff_sigma_t)/sigma2_1 * ((sigma_t**(-1-self.sde_lambda2)/bar_sigma_t**(-1-self.sde_lambda2)) - (sigma_s**(-1-self.sde_lambda2)/bar_sigma_s**(-1-self.sde_lambda2)))
                xt = coeff_xs * xs + coeff_x1 * x1 + coeff_hat_x0 * hat_x0

                if i != n_timesteps - 1:
                    eps = torch.randn(x1.shape, dtype=x1.dtype, device=x1.device, requires_grad=False)
                    coeff_eps = alpha_t * coeff_sigma_t * torch.sqrt(((bar_sigma2_t**self.sde_lambda2/sigma2_t**self.sde_lambda2)-(bar_sigma2_s**self.sde_lambda2/sigma2_s**self.sde_lambda2))/sigma2_1)
                    xt += coeff_eps * eps
                xt = xt * mask
            else:
                raise NotImplementedError()

            xt_traj.append(xt.detach().cpu())

        xt_traj = torch.stack(xt_traj, dim=1)

        return xt_traj

    @torch.no_grad()
    def forward(self, x1, mask, n_timesteps, sampler="pf_ode_euler", spk=None,
                clip_denoise=False, verbose=False):
        return self.reverse_diffusion(x1, mask, n_timesteps, sampler, spk,
                                      clip_denoise, verbose)

    def loss_t(self, x0, mask, x1, t, spk=None):
        # score estimator
        # xt, target, coeff = self.forward_diffusion(x0, mask, mu, t)
        # pred = self.estimator(xt, mask, mu, t, spk)
        # loss = torch.sum((pred*coeff + target)**2) / (torch.sum(mask)*self.n_feats)

        # noise estimator
        xt, target, weight = self.forward_diffusion(x0, mask, x1, t)

        # Normalize x1
        normalized_x1 = (x1 + 5.0) / 5.0

        pred = self.estimator(xt, mask, normalized_x1, t, spk)

        loss = torch.sum((pred - target)**2 * weight)  / (torch.sum(mask)*self.n_feats)

        return loss, xt

    def compute_loss(self, x0, mask, x1, spk=None, offset=1e-5):
        t = torch.rand(x0.shape[0], dtype=x0.dtype, device=x0.device,
                       requires_grad=False)
        t = torch.clamp(t, self.offset, 1.0 - self.offset)
        return self.loss_t(x0, mask, x1, t, spk)






