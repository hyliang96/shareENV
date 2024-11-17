# 可能是I2SB: Liu, G.-H., Vahdat, A., Huang, D.-A., Theodorou, E. A., Nie, W., & Anandkumar, A. (2023). I2SB: Image-to-Image Schrödinger Bridge (No. arXiv:2302.05872). arXiv. https://doi.org/10.48550/arXiv.2302.05872

# Copyright (C) 2021. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

import math
from tqdm import tqdm
import numpy as np
import torch
import torch.nn.functional as F
from einops import rearrange
from functools import partial

from model.base import BaseModule
from model.unet import GradLogPEstimator2d


def make_beta_schedule(n_timestep=1000, linear_start=1e-4, linear_end=3e-2):
    # return np.linspace(linear_start, linear_end, n_timestep)
    betas = (
        torch.linspace(linear_start ** 0.5, linear_end ** 0.5, n_timestep, dtype=torch.float64) ** 2
    )
    return betas.numpy()

def compute_gaussian_product_coef(sigma1, sigma2):
    """ Given p1 = N(x_t|x_0, sigma_1**2) and p2 = N(x_t|x_1, sigma_2**2)
        return p1 * p2 = N(x_t| coef1 * x0 + coef2 * x1, var) """

    denom = sigma1**2 + sigma2**2
    coef1 = sigma2**2 / denom
    coef2 = sigma1**2 / denom
    var = (sigma1**2 * sigma2**2) / denom
    return coef1, coef2, var

def space_indices(num_steps, count):
    assert count <= num_steps

    if count <= 1:
        frac_stride = 1
    else:
        frac_stride = (num_steps - 1) / (count - 1)

    cur_idx = 0.0
    taken_steps = []
    for _ in range(count):
        taken_steps.append(round(cur_idx))
        cur_idx += frac_stride

    return taken_steps


class Diffusion_I2SB(BaseModule):
    def __init__(self, n_feats=80, dim=64,
                 n_spks=1, spk_emb_dim=64,
                 beta_min=1e-4, beta_max=3e-2, pe_scale=1000, predictor="noise_hpsi"):
        super(Diffusion_I2SB, self).__init__()

        self.n_feats = n_feats
        self.dim = dim
        self.n_spks = n_spks
        self.spk_emb_dim = spk_emb_dim
        self.beta_min = beta_min
        self.beta_max = beta_max
        self.pe_scale = pe_scale

        self.predictor = predictor


        betas = make_beta_schedule(n_timestep=pe_scale, linear_start=beta_min,
                                        linear_end=beta_max)
        symbetas = np.concatenate([betas[:pe_scale//2], np.flip(betas[:pe_scale//2])])
        # TODO: cumsum is correct for constant beta, implement for the symmetric beta.
        std_fwd = np.sqrt(np.cumsum(symbetas))
        std_bwd = np.sqrt(np.flip(np.cumsum(np.flip(symbetas))))
        mu_x0, mu_x1, var = compute_gaussian_product_coef(std_fwd, std_bwd)
        std_sb = np.sqrt(var)

        self.estimator = GradLogPEstimator2d(dim, n_spks=n_spks,
                                             spk_emb_dim=spk_emb_dim,
                                             pe_scale=pe_scale)
        self.to_torch = partial(torch.tensor, dtype=torch.float32)
        self.betas = self.to_torch(betas)
        self.symbetas = self.to_torch(symbetas)
        self.std_fwd = self.to_torch(std_fwd)
        self.std_bwd = self.to_torch(std_bwd)
        self.mu_x0 = self.to_torch(mu_x0)
        self.mu_x1 = self.to_torch(mu_x1)
        self.var = self.to_torch(var)
        self.std_sb = self.to_torch(std_sb)


    def forward_diffusion(self, x0, mask, x1, step):
        mu_x0_batch = self.mu_x0[step].unsqueeze(-1).unsqueeze(-1).to(x0.device)
        mu_x1_batch = self.mu_x1[step].unsqueeze(-1).unsqueeze(-1).to(x0.device)
        std_sb_batch = self.std_sb[step].unsqueeze(-1).unsqueeze(-1).to(x0.device)

        xt = mu_x0_batch * x0 + mu_x1_batch * x1                    #[B, 0, 0] * [B, C, T]

        z = torch.randn(x0.shape, dtype=x0.dtype, device=x0.device,
                        requires_grad=False)
        xt = xt + std_sb_batch * z                              #[B, 0, 0] * [B, C, T]
        xt.detach()

        std_fwd_batch = self.std_fwd[step].unsqueeze(-1).unsqueeze(-1).to(x0.device)
        std_bwd_batch = self.std_bwd[step].unsqueeze(-1).unsqueeze(-1).to(x0.device)

        if self.predictor == "noise_hpsi":
            target = (xt - x0) / std_fwd_batch                           #[B, C ,T] / [B, 0, 0]

        elif self.predictor == "noise_psb":
            var_fwd = std_fwd_batch**2
            var_bwd = std_bwd_batch**2
            target = (xt - (var_bwd * x0 + var_fwd * x1 )/(var_bwd + var_fwd)) / torch.sqrt((var_bwd * var_fwd)/(var_bwd + var_fwd))

        elif self.predictor == "velocity":
            beta_t = self.symbetas[step].unsqueeze(-1).unsqueeze(-1).to(x0.device)
            var_fwd = std_fwd_batch**2
            var_bwd = std_bwd_batch**2
            target = 1/2 * beta_t * ((xt - x0)/var_fwd - (xt - x1)/var_bwd)

        elif self.predictor == "velocity_normalized":
            #NOTE: Only support constant beta for now
            beta_t = self.symbetas[step].unsqueeze(-1).unsqueeze(-1).to(x0.device)
            var_fwd = std_fwd_batch**2
            var_bwd = std_bwd_batch**2
            target = 1/2 * beta_t * ((xt - x0)/var_fwd - (xt - x1)/var_bwd)
            var_0 = (self.pe_scale - 2 * step) ** 2 / (4 * step * (self.pe_scale - step)) * beta_t
            var_data = torch.var_mean(x1 - x0)
            target = target / torch.sqrt(var_0 + var_data)


        else:
            raise NotImplementedError()

        target.detach()
        return xt * mask, target * mask

    @torch.no_grad()
    def score_estimation(self, xt, mask, x1, step, spk):
        step_netin = step * torch.ones(x1.shape[0], dtype=torch.long, device=x1.device)

        if self.predictor == "noise_hpsi":
            eps_t = self.estimator(xt, mask, x1, step_netin, spk)
            std_t = self.std_fwd[step].to(xt.device)
            score_t = -eps_t / std_t

        elif self.predictor == "noise_psb":
            var_fwd_t = self.std_fwd[step].to(xt.device)**2
            var_bwd_t = self.std_bwd[step].to(xt.device)**2
            eps_t = self.estimator(xt, mask, x1, step_netin, spk)
            std_marginal_t = torch.sqrt((var_bwd_t*var_fwd_t)/(var_bwd_t + var_fwd_t))
            score_t_psb = -eps_t / std_marginal_t
            score_t_Psi = -(xt - x1) / var_bwd_t
            score_t = score_t_psb - score_t_Psi

        elif self.predictor == "velocity":
            beta_t = self.symbetas[step].to(xt.device)
            var_bwd_t = self.std_bwd[step].to(xt.device)**2
            v_t = self.estimator(xt, mask, x1, step_netin, spk)
            score_t = -(2*v_t)/beta_t - (xt - x1)/var_bwd_t

        else:
            raise NotImplementedError()

        return score_t

    @torch.no_grad()
    def reverse_diffusion(self, x1, mask, n_timesteps, sampler="pf_ode_euler",
                          spk=None, clip_denoise=False, verbose=True):

        nfe = n_timesteps or self.pe_scale - 1
        assert 0 < nfe < self.pe_scale == len(self.symbetas)
        steps = space_indices(self.pe_scale, nfe+1)

        xt = x1 * mask
        xt_traj = [xt.detach().cpu()]
        steps = steps[::-1]
        pair_steps = zip(steps[1:], steps[:-1])
        pair_steps = tqdm(pair_steps, desc='Sampling', total=len(steps)-1) if verbose else pair_steps

        with torch.no_grad():
            if sampler == "sde_euler":
                for prev_step, step in pair_steps:
                    score_t = self.score_estimation(xt, mask, x1, step, spk)
                    beta_t = self.symbetas[step].to(x1.device)
                    mean_xt = xt + beta_t * score_t * (step - prev_step)
                    xt = mean_xt + math.sqrt(step - prev_step) * torch.sqrt(beta_t) * torch.randn_like(xt)

                    mean_xt = mean_xt * mask
                    xt = xt * mask
                    if prev_step > 0:
                        xt_traj.append(xt.detach().cpu())
                    else:
                        xt_traj.append(mean_xt.detach().cpu())

            elif sampler == 'sde_first_order':
                for prev_step, step in pair_steps:
                    score_t = self.score_estimation(xt, mask, x1, step, spk)
                    std_fwd_step = self.std_fwd[step].item()
                    hat_x0 = xt + (std_fwd_step**2) * score_t

                    if clip_denoise:
                        hat_x0.clamp_(-1.,1.)

                    std_fwd_prev_step = self.std_fwd[prev_step].item()
                    std_delta = math.sqrt(std_fwd_step**2 - std_fwd_prev_step**2)
                    mu_x0_gen, mu_xn_gen, var_gen = compute_gaussian_product_coef(std_fwd_prev_step, std_delta)
                    xt = mu_x0_gen * hat_x0 + mu_xn_gen * xt
                    if prev_step > 0:
                        xt = xt + math.sqrt(var_gen) * torch.randn_like(xt)
                    xt = xt * mask
                    xt_traj.append(xt.detach().cpu())

            elif sampler == 'pc_sde_euler':
                snr = 1e-2
                for prev_step, step in pair_steps:
                    # Corrector step
                    score_t = self.score_estimation(xt, mask, x1, step, spk)
                    score_norm = torch.norm(score_t.reshape(score_t.shape[0], -1), dim=-1).mean()
                    noise_norm = torch.sqrt(torch.prod(torch.tensor(xt.shape[1:], device=xt.device)))
                    langevin_step_size = 2 * (snr * noise_norm / score_norm)**2
                    xt = xt + langevin_step_size * score_t + torch.sqrt(2 * langevin_step_size) * torch.randn_like(xt)
                    # Predictor step
                    beta_t = self.symbetas[step].to(xt.device)
                    score_t = self.score_estimation(xt, mask, x1, step, spk)
                    mean_xt = xt + beta_t * score_t * (step - prev_step)
                    xt = mean_xt + math.sqrt(step - prev_step) * torch.sqrt(beta_t) * torch.randn_like(xt)

                    mean_xt = mean_xt * mask
                    xt = xt * mask
                    if prev_step > 0:
                        xt_traj.append(xt.detach().cpu())
                    else:
                        xt_traj.append(mean_xt.detach().cpu())

            elif sampler == 'pf_ode_euler':
                '''
                PF-ODE for SB: dxt = (f + 1/2 * g^2 * (score_Psi - score_HatPsi))dt
                '''
                for prev_step, step in pair_steps:
                    score_t = self.score_estimation(xt, mask, x1, step, spk)

                    bar_std_t = self.std_bwd[step].to(x1.device)
                    score_t_Psi = -(xt - x1) / (bar_std_t**2)

                    beta_t = self.symbetas[step].to(x1.device)
                    mean_xt = xt + 0.5 * beta_t * (score_t - score_t_Psi) * (step - prev_step)
                    xt = mean_xt
                    mean_xt = mean_xt * mask
                    xt = xt * mask
                    xt_traj.append(xt.detach().cpu())

            elif sampler == 'pf_ode_first_order':
                for prev_step, step in pair_steps:
                    score_t = self.score_estimation(xt, mask, x1, step, spk)
                    std_fwd_step = self.std_fwd[step].item()
                    hat_x0 = xt + (std_fwd_step**2) * score_t
                    if clip_denoise:
                        hat_x0.clamp_(-1.,1.)

                    # t -> s
                    var_1 = self.std_fwd[-1].item()**2
                    std_t = self.std_fwd[step].item()
                    bar_std_t = self.std_bwd[step].item()
                    std_s = self.std_fwd[prev_step].item()
                    bar_std_s = self.std_bwd[prev_step].item()

                    xt = (std_s * bar_std_s)/(std_t * bar_std_t) * xt + 1/(var_1) * ((bar_std_s**2 - (bar_std_t*std_s*bar_std_s)/(std_t)) * hat_x0 + (std_s**2 - (std_t*std_s*bar_std_s)/(bar_std_t)) * x1)
                    xt = xt * mask
                    xt_traj.append(xt.detach().cpu())

            else:
                raise NotImplementedError()

        xt_traj = torch.stack(xt_traj, dim=1)
        return xt_traj


    @torch.no_grad()
    def forward(self, x1, mask, n_timesteps, sampler="posterior", spk=None, clip_denoise=False, verbose=True):
        return self.reverse_diffusion(x1, mask, n_timesteps, sampler, spk, clip_denoise, verbose)

    def loss_t(self, x0, mask, x1, step, spk=None):
        xt, target = self.forward_diffusion(x0, mask, x1, step)
        assert x0.shape == x1.shape == xt.shape == target.shape

        pred = self.estimator(xt, mask, x1, step, spk)
        loss = torch.sum((pred - target)**2) / (torch.sum(mask)*self.n_feats)
        return loss, xt

    def compute_loss(self, x0, mask, x1, spk=None, offset=1e-5):
        step = torch.randint(0, self.pe_scale, (x0.shape[0],),
                            dtype=torch.long, device=x0.device,
                            requires_grad=False)
        return self.loss_t(x0, mask, x1, step, spk)
