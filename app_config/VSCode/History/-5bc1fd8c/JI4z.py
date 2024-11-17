# Bridge TTS: Chen, Z., He, G., Zheng, K., Tan, X., & Zhu, J. (2023). Schrodinger Bridges Beat Diffusion Models on Text-to-Speech Synthesis (No. arXiv:2312.03491). arXiv. https://doi.org/10.48550/arXiv.2312.03491

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


class Diffusion_SB_VP(BaseModule):
    # vp: 见11页 / Table 1 / Bridge-VP: variance perserving.
    # dx = - beta_t/2 * x_t dt + sqrt(beta_t) dW_t
    # beta(t) = beta_0 + (beta_1 - beta_0) * t
    # beta_0 = beta_min
    # beta_1 = beta_max

    def __init__(self, n_feats=80, dim=64,
                 n_spks=1, spk_emb_dim=64,
                 beta_min=0.01, beta_max=20, pe_scale=1000, predictor="hpsi", offset=1e-5, sampling_temp=2.0, sde_lambda=0.1):
        super(Diffusion_SB_VP, self).__init__()

        self.n_feats = n_feats
        self.dim = dim
        self.n_spks = n_spks
        self.spk_emb_dim = spk_emb_dim
        self.beta_min = beta_min
        self.beta_max = beta_max
        self.pe_scale = pe_scale

        self.total_cul_beta = (self.beta_min + self.beta_max) / 2
        # total_cul_beta = int_0^1 beta(s) ds = get_cul_beta(1) = int_0^1 beta(s) ds
        self.alpha_1 = math.exp(-0.5 * self.total_cul_beta)
        # alpha_1 = exp(-0.5 * total_cul_beta)
        self.sigma2_1 = math.exp(self.total_cul_beta) - 1
        # sigma^2_1 = int_0^1 beta_s/alpha^2_s ds = int_0^1 beta_s exp(int_0^s beta_u du) ds =exp(int_0^1 beta_u du)-1

        self.predictor = predictor
        self.offset = offset

        self.sampling_temp = sampling_temp
        self.sde_lambda2 = sde_lambda ** 2
        # self.total_noise = (self.beta_min + self.beta_max) / 2

        self.estimator = GradLogPEstimator2d(dim, n_spks=n_spks,
                                             spk_emb_dim=spk_emb_dim,
                                             pe_scale=pe_scale)

    def get_cul_beta(self, t):
        # cul: cumulative, 积累，积分
        # int_0^t beta(s) ds = beta_0 * t + (beta_1 - beta_0) * t^2 / 2
        return self.beta_min * t + 0.5 * (self.beta_max - self.beta_min) * (t**2)

    # 式(12):
    def get_alpha(self, t):
        # alpha_t = exp(-1/2 * int_0^t beta(s) ds)
        cul_beta = self.get_cul_beta(t)
        return torch.exp(-0.5 * cul_beta)
    # 式(12):
    def get_bar_alpha(self, t):
        # bar_alpha_t = exp(1/2 * (int_t^1 beta(s) ds) ) = alpha_1 *  alpha_t = exp(-1/2 * (int_0^1 beta(s) ds - int_0^t beta(s) ds) )
        # bar_alpha_t = alpha_1 * alpha_t
        cul_bar_beta = self.total_cul_beta - self.get_cul_beta(t)
        return torch.exp(0.5 * cul_bar_beta)
    # 式(12):
    def get_sigma2(self, t):
        # sigma^2_t = int_0^t beta_s/alpha^2_s ds = int_0^t beta_s exp(int_0^s beta_u du) ds =exp(int_0^s beta_u du)-1
        cul_beta = self.get_cul_beta(t)
        return torch.exp(cul_beta) - 1
    # 式(12):
    def get_bar_sigma2(self, t):
        # bar_sigma^2_t = int_t^1 beta_s/alpha^2_s ds = sigma^2_1 - sigma^2_t
        return self.sigma2_1 - self.get_sigma2(t)


    def forward_diffusion(self, x0, mask, x1, t):
        time = t.unsqueeze(-1).unsqueeze(-1)
        alpha_t = self.get_alpha(time)
        bar_alpha_t = self.get_bar_alpha(time)
        sigma2_t = self.get_sigma2(time)
        bar_sigma2_t = self.get_bar_sigma2(time)

        z = torch.randn(x0.shape, dtype=x0.dtype, device=x0.device, requires_grad=False)
        xt = (alpha_t*bar_sigma2_t*x0 + bar_alpha_t*sigma2_t*x1)/(bar_sigma2_t + sigma2_t) + torch.sqrt((alpha_t**2 * sigma2_t * bar_sigma2_t)/(bar_sigma2_t + sigma2_t)) * z
        # 式(25), bar_sigma2_t + sigma2_t = sigma^2_1
        xt.detach()

        if self.predictor == "hpsi":
            target = (xt - alpha_t * x0) / (alpha_t * torch.sqrt(sigma2_t))
            # 式(36)(67), eps^psi_theta -> target

            # Control the variance of the input to 1
            xt = (xt - alpha_t/self.alpha_1*x1) / (alpha_t * torch.sqrt(bar_sigma2_t))
            # 这是在干啥？
            xt.detach()
            target.detach()
            weight = 1

        elif self.predictor == "x0":
            # 式(67), x_theta -> x_0
            target = x0
            target.detach()
            weight = 1

        else:
            raise NotImplementedError(f"Unsupported predictor {self.predictor}")
        target.detach()
        return xt * mask, target * mask, weight


    @torch.no_grad()
    def data_estimation(self, xt, mask, x1, t, spk):
        # 返回x_0的估计值: hat_x0
        time = t.unsqueeze(-1).unsqueeze(-1)

        if self.predictor == "hpsi":
            alpha_t = self.get_alpha(time)
            sigma_t = torch.sqrt(self.get_sigma2(time))
            bar_sigma_t = torch.sqrt(self.get_bar_sigma2(time))

            normalized_x1 = (x1 + 5.0) / 5.0
            xt_input = (xt - alpha_t/self.alpha_1*x1) / (alpha_t * bar_sigma_t)
            # alpha_t/self.alpha_1 = bar_alpha_t
            # 式(24): Psi_t: x_t = bar_alpha_t*x1 + eps_psi * alpha_t * bar_sigma_t, xi ~ N(0,1)
            # xt_input 即 eps_psi
            # 但为什么要把 eps_psi 输入到 estimator，去估计 eps_hat_psi ？
            eps_t = self.estimator(xt_input, mask, normalized_x1, t, spk)

            hat_x0 = xt/alpha_t - sigma_t * eps_t
            # 式(24): Psi: x_t = alpha_t*x0 + eps_hat_psi * alpha_t * sigma_t, xi ~ N(0,1)
            # 式(36)变形得: 估计值 hat_x0 = xt/alpha_t - sigma_t * epsilon_theta^{hat_phi}

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
            xt = (alpha_t*bar_sigma2_t*x0_s + bar_alpha_t*sigma2_t*x1)/(bar_sigma2_t + sigma2_t) + torch.sqrt((alpha_t**2 * sigma2_t * bar_sigma2_t)/(bar_sigma2_t + sigma2_t)) * z / 2
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






