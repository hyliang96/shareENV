# Copyright (C) 2021. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

import numpy as np
import torch
from functools import partial


from model.base import BaseModule
from model.unet import GradLogPEstimator2d


def compute_gaussian_product_coef(sigma1, sigma2):
    """ Given p1 = N(x_t|x_0, sigma_1**2) and p2 = N(x_t|x_1, sigma_2**2)
        return p1 * p2 = N(x_t| coef1 * x0 + coef2 * x1, var) """

    denom = sigma1**2 + sigma2**2
    coef1 = sigma2**2 / denom
    coef2 = sigma1**2 / denom
    var = (sigma1**2 * sigma2**2) / denom
    return coef1, coef2, var


class Diffusion_SB_Beta(BaseModule):
    def __init__(self, n_feats=80, dim=64,
                 n_spks=1, spk_emb_dim=64,
                 beta_min=1e-1, beta_max=3e1, pe_scale=1000, predictor="noise_hpsi", offset=1e-5, sampling_temp=1.5):
        super(Diffusion_SB_Beta, self).__init__()

        self.n_feats = n_feats
        self.dim = dim
        self.n_spks = n_spks
        self.spk_emb_dim = spk_emb_dim
        self.beta_min = beta_min
        self.beta_max = beta_max
        self.pe_scale = pe_scale

        self.predictor = predictor
        self.offset = offset

        # \sigma^2_1
        self.total_noise = (self.beta_min + self.beta_max) / 2

        self.sampling_temp = sampling_temp

        self.estimator = GradLogPEstimator2d(dim, n_spks=n_spks,
                                             spk_emb_dim=spk_emb_dim,
                                             pe_scale=pe_scale)

    def get_symmetric_noise(self, t, cumulative=False):
        # t    beta_t
        # --------------
        # 0    beta_min
        # 0.5  beta_max
        # 1    beta_min
        # 分段线性
        '''
        return \beta_t or (\sigma_t / \bar\sigma_t)
        '''
        half_flag = t <= 0.5
        beta = torch.zeros_like(t)
        beta[half_flag] = self.beta_min + 2 * (self.beta_max - self.beta_min) * t[half_flag]
        beta[~half_flag] = self.beta_max - 2 * (self.beta_max - self.beta_min) * (t[~half_flag]-0.5)
        if not cumulative:
            return beta
        else:
            var = torch.zeros_like(t)
            var[half_flag] = (self.beta_min + beta[half_flag]) * t[half_flag] / 2
            var[~half_flag] = self.total_noise/2 + (self.beta_max + beta[~half_flag]) * (t[~half_flag]-0.5) / 2
            return var.sqrt()

    def forward_diffusion(self, x0, mask, x1, t):
        time = t.unsqueeze(-1).unsqueeze(-1)
        std_fwd = self.get_symmetric_noise(time, cumulative=True)
        std_bwd = torch.sqrt(self.total_noise - std_fwd**2)
        mu_x0, mu_x1, var = compute_gaussian_product_coef(std_fwd, std_bwd)
        z = torch.randn(x0.shape, dtype=x0.dtype, device=x0.device, requires_grad=False)
        xt = mu_x0 * x0 + mu_x1 * x1 + torch.sqrt(var) * z
        xt.detach()

        if self.predictor == "hpsi":
            target = (xt - x0) / std_fwd
            weight = 1
            # coeff = std_fwd

        elif "hpsi_var" in self.predictor:
            assert self.beta_min == self.beta_max
            assert self.beta_min == 0.5325
            target = (xt - x0) / std_fwd
            # Control the variance of the input to 1
            xt = (xt - x1) / std_bwd
            xt = xt.detach()
            if self.predictor == "hpsi_var_3":
                weight = 1 / time
            else:
                weight = 1

        elif self.predictor == "hpsi_const":
            assert self.beta_min == self.beta_max
            target = torch.sqrt(time) * (x1 - x0) / torch.sqrt(self.beta_max) + torch.sqrt(1-time) * z
            weight = 1

        elif self.predictor == "x0":
            target = x0
            weight = 1

        elif self.predictor == "psb":
            var_fwd = std_fwd**2
            var_bwd = std_bwd**2
            target = (xt - (var_bwd * x0 + var_fwd * x1 )/(var_bwd + var_fwd)) / torch.sqrt((var_bwd * var_fwd)/(var_bwd + var_fwd))
            weight = 1
            # coeff = torch.sqrt((var_bwd * var_fwd)/(var_bwd + var_fwd))

        elif self.predictor == "velocity":
            beta_t = self.get_symmetric_noise(time, cumulative=False)
            var_fwd = std_fwd**2
            var_bwd = std_bwd**2
            target = 1/2 * beta_t * ((xt - x0)/var_fwd - (xt - x1)/var_bwd)
            weight = 1
            # coeff = var_fwd * var_bwd

        elif self.predictor == "psb_const":
            assert self.beta_min == self.beta_max
            target = z
            weight = 1/(1-time)

        elif self.predictor == "velocity_const":
            assert self.beta_min == self.beta_max
            target = ((1-2*time) * xt - (1-time)*x0 + time*x1) / (2*time*(1-time))
            weight = (4*time)/self.beta_max

        elif self.predictor == "velocity_normalized_const":
            assert self.beta_min == self.beta_max
            var_lj = 0.5325
            var_0 = (1-2*time)**2 * self.beta_max / (4 * time * (1-time))
            target = ((1-2*time) * xt - (1-time)*x0 + time*x1) / (2*time*(1-time))
            target /= torch.sqrt(var_lj + var_0)
            weight = (4*time)/self.beta_max * (var_lj + var_0)

        else:
            raise NotImplementedError(f"Unsupported predictor {self.predictor}")
        target.detach()
        return xt * mask, target * mask, weight

    @torch.no_grad()
    def score_estimation(self, xt, mask, x1, t, spk):
        time = t.unsqueeze(-1).unsqueeze(-1)

        if self.predictor == "hpsi":
            eps_t = self.estimator(xt, mask, x1, t, spk)
            std_t = self.get_symmetric_noise(time, cumulative=True)
            score_t = -eps_t / std_t

        elif self.predictor == "psb_const":
            assert self.beta_min == self.beta_max

        elif self.predictor == "velocity_const":
            assert self.beta_min == self.beta_max

        elif self.predictor == "hpsi_const":
            assert self.beta_min == self.beta_max
        # elif self.predictor == "hpsi":
        #     score_t = self.estimator(xt, mask, x1, t, spk)

        elif self.predictor == "psb":
            score_t_psb = self.estimator(xt, mask, x1, t, spk)
            var_bwd_t = self.get_symmetric_noise(1-time, cumulative=True)**2
            score_t_psi = -(xt - x1) / var_bwd_t
            score_t = score_t_psb - score_t_psi

        elif self.predictor == "noise_psb":
            var_fwd_t = self.get_symmetric_noise(time, cumulative=True)**2
            var_bwd_t = self.total_noise - var_fwd_t
            eps_t = self.estimator(xt, mask, x1, t, spk)
            std_marginal_t = torch.sqrt((var_bwd_t*var_fwd_t)/(var_bwd_t + var_fwd_t))
            score_t_psb = -eps_t / std_marginal_t
            score_t_Psi = -(xt - x1) / var_bwd_t
            score_t = score_t_psb - score_t_Psi

        elif self.predictor == "velocity":
            beta_t = self.get_symmetric_noise(time, cumulative=False)
            var_bwd_t = self.get_symmetric_noise(1-t, cumulative=True)**2
            v_t = self.estimator(xt, mask, x1, t, spk)
            score_t = -(2*v_t)/beta_t - (xt - x1)/var_bwd_t

        else:
            raise NotImplementedError()

        return score_t

    @torch.no_grad()
    def data_estimation(self, xt, mask, x1, t, spk):
        time = t.unsqueeze(-1).unsqueeze(-1)

        if self.predictor == "hpsi":
            # score estimation
            # score_t = self.estimator(xt, mask, x1, t, spk)
            # hat_x0 = xt + score_t * self.get_symmetric_noise(t, cumulative=true)**2

            # noise estimation
            eps_t = self.estimator(xt, mask, x1, t, spk)
            std_t = self.get_symmetric_noise(time, cumulative=True)
            score_t = -eps_t / std_t
            hat_x0 = xt + score_t * std_t**2

        elif self.predictor == "hpsi_var":
            assert self.beta_min == self.beta_max == 0.5325
            std_fwd = self.get_symmetric_noise(time, cumulative=True)
            std_bwd = torch.sqrt(self.total_noise - std_fwd**2)
            xt_input = (xt - x1) / std_bwd
            eps_t = self.estimator(xt_input, mask, x1, t, spk)
            score_t = -eps_t / std_fwd
            hat_x0 = xt + score_t * std_fwd**2

        elif "hpsi_var" in self.predictor:
            assert self.beta_min == self.beta_max == 0.5325
            std_fwd = self.get_symmetric_noise(time, cumulative=True)
            std_bwd = torch.sqrt(self.total_noise - std_fwd**2)
            xt_input = (xt - x1) / std_bwd
            normalized_x1 = (x1 + 5.0) / 5.0
            eps_t = self.estimator(xt_input, mask, normalized_x1, t, spk)
            score_t = -eps_t / std_fwd
            hat_x0 = xt + score_t * std_fwd**2

        elif self.predictor == "hpsi_score":
            # score estimation
            score_t = self.estimator(xt, mask, x1, t, spk)
            hat_x0 = xt + score_t * self.get_symmetric_noise(t, cumulative=True)**2

        elif self.predictor == "x0":
            return self.estimator(xt, mask, x1, t, spk)

        elif self.predictor == "psb_const":
            assert self.beta_min == self.beta_max
            eps_t = self.estimator(xt, mask, x1, t, spk)
            hat_x0 = (xt - t*x1)/(1-t) - torch.sqrt(self.beta_min * t /(1-t)) * eps_t

        elif self.predictor == "velocity_const":
            assert self.beta_min == self.beta_max
            v_t = self.estimator(xt, mask, x1, t, spk)
            hat_x0 = ((1-2*t)*xt + t*x1)/(1-t) - 2*t*v_t

        elif self.predictor == "velocity_normalized_const":
            assert self.beta_min == self.beta_max
            var_lj = 0.5325
            var_0 = (1-2*time)**2 * self.beta_max / (4 * time * (1-time))
            v_t = self.estimator(xt, mask, x1, t, spk) * torch.sqrt(var_lj + var_0)
            hat_x0 = ((1-2*t)*xt + t*x1)/(1-t) - 2*t*v_t

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

        xt = x1
        if "second" in sampler:
            assert n_timesteps % 2 == 0 and n_timesteps > 1
            n_timesteps = n_timesteps // 2
        elif "n2" in sampler:
            assert n_timesteps > 1
            init_s = (1.0 - self.offset) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
            x0_s = self.data_estimation(xt, mask, x1, init_s, spk)
            alpha_t = 1
            bar_alpha_t = 1
            sigma2_t = self.get_symmetric_noise(init_s, cumulative=True)**2
            bar_sigma2_t = self.get_symmetric_noise(1-init_s, cumulative=True)**2
            z = torch.randn(x1.shape, dtype=x1.dtype, device=x1.device, requires_grad=False)
            xt = (alpha_t*bar_sigma2_t*x0_s + bar_alpha_t*sigma2_t*x1)/(bar_sigma2_t + sigma2_t) + torch.sqrt((alpha_t**2 * sigma2_t * bar_sigma2_t)/(bar_sigma2_t + sigma2_t)) * z
            n_timesteps -= 1

        h = 1.0 / n_timesteps
        xt = xt * mask
        xt_traj = [xt.detach().cpu()]
        for i in range(n_timesteps):

            if sampler == "sde_euler":
                # t = (1.0 - (i+0.5)*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                t = (1.0 - self.offset - i*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                time = t.unsqueeze(-1).unsqueeze(-1)
                beta_t = self.get_symmetric_noise(time, cumulative=False)
                score_t = self.score_estimation(xt, mask, x1, t, spk)

                dxt_det = -score_t
                dxt_det = dxt_det * beta_t * h
                dxt_stoc = torch.randn(x1.shape, dtype=x1.dtype, device=x1.device, requires_grad=False)
                dxt_stoc = dxt_stoc * torch.sqrt(beta_t * h)
                if i != n_timesteps - 1:
                    dxt = dxt_det + dxt_stoc
                else:
                    dxt = dxt_det
                xt = (xt - dxt) * mask

            elif sampler == "pf_ode_euler":
                # t = (1.0 - (i+0.5)*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                t = (1.0 - self.offset - i*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                time = t.unsqueeze(-1).unsqueeze(-1)
                beta_t = self.get_symmetric_noise(time, cumulative=False)

                bar_std_t = self.get_symmetric_noise(1-t, cumulative=True)
                score_t_Psi = -(xt - x1) / (bar_std_t**2)
                score_t = self.score_estimation(xt, mask, x1, t, spk)

                dxt = 0.5 * (score_t_Psi - score_t)
                dxt = dxt * beta_t * h
                xt = (xt - dxt) * mask

            elif sampler == "pf_ode_euler_v":
                assert "velocity" in self.predictor
                t = (1.0 - self.offset - i*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                time = t.unsqueeze(-1).unsqueeze(-1)

                vt = self.estimator(xt, mask, x1, t, spk)
                dxt = vt * h
                xt = (xt - dxt) * mask

            elif sampler == 'sde_first_order':
                # s -> t
                s = (1.0 - self.offset - (i*h)) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                t = max(self.offset, 1.0 - self.offset - (i+1)*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                # Prepare all needed variables
                std_s = self.get_symmetric_noise(s, cumulative=True)
                std_t = self.get_symmetric_noise(t, cumulative=True)
                bar_std_s = self.get_symmetric_noise(1-s, cumulative=True)
                bar_std_t = self.get_symmetric_noise(1-t, cumulative=True)

                xs = xt
                hat_x0 = self.data_estimation(xs, mask, x1, s, spk)
                # score_t = self.score_estimation(xs, mask, x1, s, spk)
                # hat_x0 = xs + std_t**2 * score_t

                coeff = (std_t**2)/(std_s**2)
                xt = coeff * xs + (1-coeff) * hat_x0
                if i != n_timesteps - 1:
                    eps = torch.randn(x1.shape, dtype=x1.dtype, device=x1.device, requires_grad=False) / self.sampling_temp
                    xt += std_t * torch.sqrt(1 - coeff) * eps
                xt = xt * mask

            elif sampler == 'pf_ode_first_order' or sampler == 'pf_ode_first_order_n2':
                # s -> t
                s = (1.0 - self.offset - (i*h)) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                t = max(self.offset, 1.0 - self.offset - (i+1)*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                # Prepare all needed variables
                std_s = self.get_symmetric_noise(s, cumulative=True)
                std_t = self.get_symmetric_noise(t, cumulative=True)
                bar_std_s = self.get_symmetric_noise(1-s, cumulative=True)
                bar_std_t = self.get_symmetric_noise(1-t, cumulative=True)
                var_1 = self.total_noise

                xs = xt
                hat_x0 = self.data_estimation(xs, mask, x1, s, spk)
                # score_t = self.score_estimation(xs, mask, x1, s, spk)
                # hat_x0 = xs + std_t**2 * score_t

                xt = (std_t*bar_std_t)/(std_s*bar_std_s) * xs + 1/var_1 * ((bar_std_t**2 - (bar_std_s*std_t*bar_std_t)/(std_s)) * hat_x0 + (std_t**2 - (std_s*std_t*bar_std_t)/(bar_std_s)) * x1)
                xt = xt * mask

            elif sampler == "sde_second_order":
                # s -> t
                s = (1.0 - self.offset - (i*h)) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                t = max(self.offset, 1.0 - self.offset - (i+1)*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                # Prepare all needed variables
                std_s = self.get_symmetric_noise(s, cumulative=True)
                std_t = self.get_symmetric_noise(t, cumulative=True)
                bar_std_s = self.get_symmetric_noise(1-s, cumulative=True)
                bar_std_t = self.get_symmetric_noise(1-t, cumulative=True)

                # Predictor
                xs = xt.detach().clone()
                hat_x0_s = self.data_estimation(xs, mask, x1, s, spk)
                coeff = (std_t**2)/(std_s**2)
                xt_pred = coeff * xs + (1 - coeff) * hat_x0_s
                eps = torch.randn(x1.shape, dtype=x1.dtype, device=x1.device, requires_grad=False)
                xt_pred += std_t * torch.sqrt(1 - coeff) * eps

                # Correction
                hat_x0_t = self.data_estimation(xt_pred, mask, x1, t, spk)
                xt = coeff * xs + (1 - coeff) * ((hat_x0_s + hat_x0_t)/2)
                if i != n_timesteps - 1:
                    eps = torch.randn(x1.shape, dtype=x1.dtype, device=x1.device, requires_grad=False)
                    xt += std_t * torch.sqrt(1 - coeff) * eps
                xt = xt * mask



            elif sampler == "pf_ode_second_order":
                # s -> t
                s = (1.0 - self.offset - (i*h)) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                t = max(self.offset, 1.0 - self.offset - (i+1)*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                # Prepare all needed variables
                std_s = self.get_symmetric_noise(s, cumulative=True)
                std_t = self.get_symmetric_noise(t, cumulative=True)
                bar_std_s = self.get_symmetric_noise(1-s, cumulative=True)
                bar_std_t = self.get_symmetric_noise(1-t, cumulative=True)
                var_1 = self.total_noise

                # Prediction
                xs = xt.detach().clone()
                hat_x0_s = self.data_estimation(xs, mask, x1, s, spk)
                xt_pred = (std_t*bar_std_t)/(std_s*bar_std_s) * xs + 1/var_1 * ((bar_std_t**2 - (bar_std_s*std_t*bar_std_t)/(std_s))*hat_x0_s + (std_t**2 - (std_s*std_t*bar_std_t)/(bar_std_s)) * x1)

                # Correction
                hat_x0_t = self.data_estimation(xt_pred, mask, x1, t, spk)
                xt = (std_t*bar_std_t)/(std_s*bar_std_s) * xs + 1/var_1 * ((bar_std_t**2 - (bar_std_s*std_t*bar_std_t)/(std_s))*((hat_x0_s + hat_x0_t)/2) + (std_t**2 - (std_s*std_t*bar_std_t)/(bar_std_s)) * x1)
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

    def loss_t(self, x0, mask, mu, t, spk=None):
        # score estimator
        # xt, target, coeff = self.forward_diffusion(x0, mask, mu, t)
        # pred = self.estimator(xt, mask, mu, t, spk)
        # loss = torch.sum((pred*coeff + target)**2) / (torch.sum(mask)*self.n_feats)

        # noise estimator
        xt, target, weight = self.forward_diffusion(x0, mask, mu, t)


        # Normalize x1
        if "hpsi_var" in self.predictor:
            normalized_mu = (mu + 5.0) / 5.0
            pred = self.estimator(xt, mask, normalized_mu, t, spk)
        else:
            pred = self.estimator(xt, mask, mu, t, spk)
        loss = torch.sum((pred - target)**2 * weight)  / (torch.sum(mask)*self.n_feats)

        return loss, xt

    def compute_loss(self, x0, mask, mu, spk=None, offset=1e-5):
        t = torch.rand(x0.shape[0], dtype=x0.dtype, device=x0.device,
                       requires_grad=False)
        t = torch.clamp(t, self.offset, 1.0 - self.offset)
        return self.loss_t(x0, mask, mu, t, spk)






