# lj: LJ Speech Dataset, 用于TTS训练的语音数据集

# Copyright (C) 2021. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

import argparse
import os
import json
import datetime as dt
import numpy as np
from scipy.io.wavfile import write

import torch

from configs import decoder_dict
from data import TextMelDataset
from model import TextEncoder, Diffusion_SB, TTS
from text import text_to_sequence, cmudict
from text.symbols import symbols
from utils import intersperse, save_plot_final
from file_utils import check_dir

import sys
sys.path.append('./hifi-gan/')
from env import AttrDict
from models import Generator as HiFiGAN


HIFIGAN_CONFIG = './checkpts/hifigan-config.json'
HIFIGAN_CHECKPT = './checkpts/hifigan.pt'

# HIFIGAN_CONFIG = './checkpts/config.json'
# HIFIGAN_CHECKPT = './checkpts/generator_v1.pt'
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Method
    parser.add_argument('--config', type=str, choices=['gradtts', 'bridgetts-i2sb', 'bridgetts', 'bridgetts-fg', 'bridgetts-beta', 'bridgetts-vp'])
    # Data
    parser.add_argument('--test_filelist_path', type=str, required=True)
    parser.add_argument('--num_test_examples', type=int, default=-1)
    parser.add_argument('--cmudict_path', type=str, default="./resources/cmu_dictionary")
    parser.add_argument('--add_blank', type=bool, default=True)
    parser.add_argument('--n_feats', type=int, default=80)
    parser.add_argument('--n_fft', type=int, default=1024)
    parser.add_argument('--sample_rate', type=int, default=22050)
    parser.add_argument('--hop_length', type=int, default=256)
    parser.add_argument('--win_length', type=int, default=1024)
    parser.add_argument('--f_min', type=int, default=0)
    parser.add_argument('--f_max', type=int, default=8000)
    # Model
    parser.add_argument('--ckpt_dir', type=str, required=True)
    parser.add_argument('--model_name', type=str, required=True, help='path to a checkpoint of Grad-TTS')
    parser.add_argument('--ckpt_step', type=str, required=True, help='path to a checkpoint of Grad-TTS')
    parser.add_argument('--offset', type=float, default=1e-5)
    parser.add_argument('--beta_min', type=float, default=100, help='beta_min for reverse diffusion')
    parser.add_argument('--beta_max', type=float, default=100, help='beta_max for reverse diffusion')
    parser.add_argument('--f', type=float, default=-0.01, help='beta_min for reverse diffusion')
    parser.add_argument('--g', type=float, default=10, help='beta_max for reverse diffusion')
    parser.add_argument('--sampling_temp', default=1.5, type=float, help='temperature of sampling')
    parser.add_argument('--sde_lambda', default=0.5, type=float, help='temperature of sampling')
    parser.add_argument('--predictor', type=str, default="noise_hpsi")
    parser.add_argument('--n_spks', type=int, default=1)
    # Sampling
    parser.add_argument('--sampler', type=str, required=False, default='euler_sde', help='sampler for reverse diffusion')
    parser.add_argument('--timesteps', type=int, required=False, default=10, help='number of timesteps of reverse diffusion')
    parser.add_argument('--speaker_id', type=int, required=False, default=None, help='speaker id for multispeaker model')
    parser.add_argument('--output_dir', type=str, required=True)
    parser.add_argument('--plot_latent', action='store_true')
    args = parser.parse_args()

    if not isinstance(args.speaker_id, type(None)):
        assert args.n_spks > 1, "Ensure you set right number of speakers in `params.py`."
        spk = torch.LongTensor([args.speaker_id]).cuda()
    else:
        spk = None


    print('Initializing TTS Model...')
    nsymbols = len(symbols) + 1
    encoder = TextEncoder(nsymbols)
    if args.config == "bridgetts-fg":
        decoder = decoder_dict[args.config](f=args.f, g=args.g, predictor=args.predictor, offset=args.offset, sampling_temp=args.sampling_temp, sde_lambda=args.sde_lambda)
    elif args.config == "bridgetts":
        decoder = decoder_dict[args.config](g2_min=args.beta_min, g2_max=args.beta_max, predictor=args.predictor, offset=args.offset, sampling_temp=args.sampling_temp, sde_lambda=args.sde_lambda)
    elif args.config == "bridgetts-vp":
        decoder = decoder_dict[args.config](beta_min=args.beta_min, beta_max=args.beta_max, predictor=args.predictor, offset=args.offset, sampling_temp=args.sampling_temp, sde_lambda=args.sde_lambda)
    else:
        decoder = decoder_dict[args.config](beta_min=args.beta_min, beta_max=args.beta_max, predictor=args.predictor, offset=args.offset)
    model = TTS(encoder, decoder)


    ckpt_dir = args.ckpt_dir
    model_name = args.model_name
    ckpt_step = args.ckpt_step
    ckpt_path = os.path.join(ckpt_dir, model_name, "ckpts", f'grad_{ckpt_step}.pt')
    model.load_state_dict(torch.load(ckpt_path, map_location=lambda loc, storage: loc))
    model.cuda().eval()
    print(f'Number of parameters: {model.nparams}')

    print('Initializing HiFi-GAN...')
    with open(HIFIGAN_CONFIG) as f:
        h = AttrDict(json.load(f))
    vocoder = HiFiGAN(h)
    vocoder.load_state_dict(torch.load(HIFIGAN_CHECKPT, map_location=lambda loc, storage: loc)['generator'])
    _ = vocoder.cuda().eval()
    vocoder.remove_weight_norm()

    test_dataset = TextMelDataset(args.test_filelist_path, args.cmudict_path, args.add_blank,
                                  args.n_fft, args.n_feats, args.sample_rate, args.hop_length,
                                  args.win_length, args.f_min, args.f_max, shuffle=False)

    if args.num_test_examples > 0:
        lj2_index = 186
        lj_index = list(range(args.num_test_examples)) + list(range(lj2_index, lj2_index + args.num_test_examples))
    else:
        lj_index = range(len(test_dataset))

    print(lj_index)

    cmu = cmudict.CMUDict('./resources/cmu_dictionary')

    if 'sde' in args.sampler:
        if "lambda" in args.sampler:
            output_dir = os.path.join(args.output_dir, model_name, f"n_epoch={ckpt_step}", args.sampler, f"sde_lamdba={args.sde_lambda}", f"nfe={args.timesteps}")
        else:
            output_dir = os.path.join(args.output_dir, model_name, f"n_epoch={ckpt_step}", args.sampler, f"sampling_temp={args.sampling_temp}", f"nfe={args.timesteps}")
    else:
            output_dir = os.path.join(args.output_dir, model_name, f"n_epoch={ckpt_step}", args.sampler, f"nfe={args.timesteps}")
    check_dir(output_dir)

    with torch.no_grad():
        for i in lj_index:
            lj_file_name, raw_text = test_dataset.get_file_name_and_raw_text(i)

            print(f'Synthesizing {i} text...', end=' ')
            x = test_dataset[i]["x"].cuda()[None]
            x_lengths = torch.LongTensor([x.shape[-1]]).cuda()

            t = dt.datetime.now()
            y_enc, y_dec, attn, y_dec_xs = model.forward(x, x_lengths,
                                            n_timesteps=args.timesteps, sampler=args.sampler,
                                            spk=spk, clip_denoise=False,
                                            verbose=True, length_scale=0.91)
            t = (dt.datetime.now() - t).total_seconds()
            print(f'Bridge-TTS RTF: {t * 22050 / (y_dec.shape[-1] * 256)}')
            y_dec = y_dec.cuda()
            print(np.mean(y_dec.cpu().numpy()))
            print(np.max(y_dec.cpu().numpy()))
            print(np.min(y_dec.cpu().numpy()))
            audio = (vocoder.forward(y_dec).cpu().squeeze().clamp(-1, 1).numpy() * 32768).astype(np.int16)

            if args.plot_latent:
                traj_output_dir = os.path.join(args.output_dir, model_name, f"n_epoch={ckpt_step}", args.sampler, f"nfe={args.timesteps}", f"{lj_file_name[:-4]}")
                check_dir(traj_output_dir)
                for j in range(y_dec_xs.shape[1]):
                    if j >= 100:
                        if j == 0 or (j+1) % 100 == 0:
                            save_plot_final(y_dec_xs[:, j].squeeze().cpu(),
                                        f"{traj_output_dir}/step={j}.png")
                            save_plot_final(y_dec_xs[:, j].squeeze().cpu(),
                                        f"{traj_output_dir}/step={j}.svg")
                    else:
                        save_plot_final(y_dec_xs[:, j].squeeze().cpu(),
                                    f"{traj_output_dir}/step={j}.png")
                        save_plot_final(y_dec_xs[:, j].squeeze().cpu(),
                                    f"{traj_output_dir}/step={j}.svg")

            write(os.path.join(output_dir, f"{lj_file_name}"), 22050, audio)
    print(f'Done. Check out {output_dir} folder for samples.')
