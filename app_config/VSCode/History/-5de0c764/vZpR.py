# 使用 grad-vc (即Vadim Popov, Ivan Vovk, Vladimir Gogoryan,DIFFUSION-BASED VOICE CONVERSION WITH FAST  MAXIMUM LIKELIHOOD SAMPLING SCHEME)

# Copyright (C) 2021. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

import math
import torch
from einops import rearrange

from model.base import BaseModule
from model.unet import GradLogPEstimator2d

def get_noise(t, beta_init, beta_term, cumulative=False):

    if cumulative:
    # int_0^t beta_s ds=beta_0 t+(beta_1-beta_0)t^2/2
        noise = beta_init*t + 0.5*(beta_term - beta_init)*(t**2)
    else:
    # beta_t=beta_0+(beta_1-beta_0)t
        noise = beta_init + (beta_term - beta_init)*t
    return noise


class Diffusion_Grad(BaseModule):
    def __init__(self, n_feats=80, dim=64,
                 n_spks=1, spk_emb_dim=64,
                 beta_min=0.05, beta_max=20, pe_scale=1000, offset=1e-5, **kwargs):
        super(Diffusion_Grad, self).__init__()
        self.n_feats = n_feats
        self.dim = dim
        self.n_spks = n_spks
        self.spk_emb_dim = spk_emb_dim
        self.beta_min = beta_min
        self.beta_max = beta_max
        self.pe_scale = pe_scale
        self.offset = offset

        self.estimator = GradLogPEstimator2d(dim, n_spks=n_spks,
                                             spk_emb_dim=spk_emb_dim,
                                             pe_scale=pe_scale)

    def get_beta(self, t):
        beta = self.beta_min + (self.beta_max - self.beta_min) * t
        return beta

    def get_gamma(self, s, t, p=1.0, use_torch=False):
        beta_integral = self.beta_min + 0.5*(self.beta_max - self.beta_min)*(t + s)
        beta_integral *= (t - s)
        if use_torch:
            gamma = torch.exp(-0.5*p*beta_integral).unsqueeze(-1).unsqueeze(-1)
        else:
            gamma = math.exp(-0.5*p*beta_integral)
        return gamma

    # get_mu,get_nu,get_sigma 见式(9)
    def get_mu(self, s, t):
        a = self.get_gamma(s, t)
        b = 1.0 - self.get_gamma(0, s, p=2.0)
        c = 1.0 - self.get_gamma(0, t, p=2.0)
        return a * b / c

    def get_nu(self, s, t):
        a = self.get_gamma(0, s)
        b = 1.0 - self.get_gamma(s, t, p=2.0)
        c = 1.0 - self.get_gamma(0, t, p=2.0)
        return a * b / c

    def get_sigma(self, s, t):
        a = 1.0 - self.get_gamma(0, s, p=2.0)
        b = 1.0 - self.get_gamma(s, t, p=2.0)
        c = 1.0 - self.get_gamma(0, t, p=2.0)
        return math.sqrt(a * b / c)


    def forward_diffusion(self, x0, mask, mu, t):
        # 式(3)
        time = t.unsqueeze(-1).unsqueeze(-1)
        cum_noise = get_noise(time, self.beta_min, self.beta_max, cumulative=True)
        mean = x0*torch.exp(-0.5*cum_noise) + mu*(1.0 - torch.exp(-0.5*cum_noise))
        variance = 1.0 - torch.exp(-cum_noise)
        z = torch.randn(x0.shape, dtype=x0.dtype, device=x0.device,
                        requires_grad=False)
        xt = mean + z * torch.sqrt(variance)
        return xt * mask, z * mask

    @torch.no_grad()
    def reverse_diffusion(self, z, mask, mu, n_timesteps, sampler="pf_ode_euler", spk=None):
        h = 1.0 / n_timesteps
        xt = z * mask
        xt_traj = [xt.cpu().detach()]
        for i in range(n_timesteps):
            t = (1.0 - (i + 0.5)*h) * torch.ones(z.shape[0], dtype=z.dtype, device=z.device)
            # t = (1.0 - self.offset - i*h) * torch.ones(z.shape[0], dtype=z.dtype, device=z.device)
            time = t.unsqueeze(-1).unsqueeze(-1)
            noise_t = get_noise(time, self.beta_min, self.beta_max, cumulative=False)

            if sampler == "sde_euler":  # adds stochastic term
                # x_{t-h} = x_t - h * dx_t
                # dx_t = 0.5 * (mu - x_t) - s_θs_o g
                dxt_det = 0.5 * (mu - xt) - self.estimator(xt, mask, mu, t, spk)
                dxt_det = dxt_det * noise_t * h
                dxt_stoc = torch.randn(z.shape, dtype=z.dtype, device=z.device,
                                       requires_grad=False)
                dxt_stoc = dxt_stoc * torch.sqrt(noise_t * h)
                if i < n_timesteps - 1:
                    dxt = dxt_det + dxt_stoc
                else:
                    dxt = dxt_det
                xt = (xt - dxt) * mask

            elif sampler == "pf_ode_euler":
                dxt = 0.5 * (mu - xt - self.estimator(xt, mask, mu, t, spk))
                dxt = dxt * noise_t * h
                xt = (xt - dxt) * mask

            elif sampler == "sde_ml":
                # t -> s
                t = (1.0 - self.offset - (i*h)) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                s = max(self.offset, 1.0 - self.offset - (i+1)*h) * torch.ones(xt.shape[0], dtype=xt.dtype, device=xt.device)
                gamma_0t = self.get_gamma(0, t, p=1)
                mu_st = self.get_mu(s, t)
                nu_st = self.get_nu(s, t)
                sigma_st = self.get_sigma(s, t)
                score_est = self.estimator(xt, mask, mu, t, spk)
                E = mu + 1/gamma_0t * ((1 - gamma_0t**2) * score_est  + xt - mu)
                xt = mu_st * xt + nu_st * E + (1 - mu_st - nu_st) * mu
                if i < n_timesteps - 1:
                    z = torch.randn(xt.shape, dtype=xt.dtype, device=xt.device,
                                    requires_grad=False)
                    xt = xt + sigma_st * z
                xt = xt * mask


            else:
                raise NotImplementedError(f"Unsupported sampler {sampler}")
            xt_traj.append(xt.cpu().detach())

        xt_traj = torch.stack(xt_traj, dim=1)
        return xt_traj

    @torch.no_grad()
    def forward(self, z, mask, mu, n_timesteps, sampler="pf_ode_euler", spk=None):
        return self.reverse_diffusion(z, mask, mu, n_timesteps, sampler, spk)

    def loss_t(self, x0, mask, mu, t, spk=None):
        xt, z = self.forward_diffusion(x0, mask, mu, t)
        time = t.unsqueeze(-1).unsqueeze(-1)
        cum_noise = get_noise(time, self.beta_min, self.beta_max, cumulative=True)
        noise_estimation = self.estimator(xt, mask, mu, t, spk)
        noise_estimation *= torch.sqrt(1.0 - torch.exp(-cum_noise))
        loss = torch.sum((noise_estimation + z)**2) / (torch.sum(mask)*self.n_feats)
        return loss, xt

    def compute_loss(self, x0, mask, mu, spk=None, offset=1e-5):
        t = torch.rand(x0.shape[0], dtype=x0.dtype, device=x0.device,
                       requires_grad=False)
        t = torch.clamp(t, self.offset, 1.0 - self.offset)
        return self.loss_t(x0, mask, mu, t, spk)
