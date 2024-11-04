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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Method
    parser.add_argument('--config', type=str, choices=['gradtts', 'bridgetts-i2sb', 'bridgetts', 'bridgetts-fg'])
    # Data
    parser.add_argument('--test_filelist_path', type=str, required=True)
    parser.add_argument('--file', type=str, required=True, help='path to a file with texts to synthesize')
    parser.add_argument('--total_test_samples', type=int, default=20)
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
    parser.add_argument('--f', type=float, default=-0.01)
    parser.add_argument('--g', type=float, default=8.2793)
    parser.add_argument('--predictor', type=str, default="noise_hpsi")
    parser.add_argument('--n_spks', type=int, default=1)
    # Sampling
    parser.add_argument('--sampler', type=str, required=False, default='euler_sde', help='sampler for reverse diffusion')
    parser.add_argument('--timesteps', type=int, required=False, default=10, help='number of timesteps of reverse diffusion')
    parser.add_argument('--speaker_id', type=int, required=False, default=None, help='speaker id for multispeaker model')
    parser.add_argument('--output_dir', type=str, required=True)
    parser.add_argument('--plot_latent', action='store_true', help='plot latent space trajectory')
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
        decoder = decoder_dict[args.config](f=args.f, g=args.g, predictor=args.predictor, offset=args.offset)
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

        # This is the reserved test text
    with open(args.file, 'r', encoding='utf-8') as f:
        texts = [line.strip() for line in f.readlines()]

    test_dataset = TextMelDataset(args.test_filelist_path, args.cmudict_path, args.add_blank,
                                  args.n_fft, args.n_feats, args.sample_rate, args.hop_length,
                                  args.win_length, args.f_min, args.f_max)

    test_samples_x = []
    test_samples_y = []
    test_samples_text = []

    # Search some reserved test data
    for idx in range(len(test_dataset)):
        raw_text = test_dataset.get_raw_text(idx)
        if raw_text in texts:
            test_samples_x.append(test_dataset[idx]['x'])
            test_samples_y.append(test_dataset[idx]['y'])
            test_samples_text.append(raw_text)
        if len(test_samples_x) == len(texts):
            break

    if len(test_samples_x) < args.total_test_samples:
        for idx in range(len(test_dataset)):
            raw_text = test_dataset.get_raw_text(idx)
            if raw_text not in test_samples_text:
                test_samples_x.append(test_dataset[idx]['x'])
                test_samples_y.append(test_dataset[idx]['y'])
                test_samples_text.append(raw_text)
            if len(test_samples_x) == args.total_test_samples:
                break

    cmu = cmudict.CMUDict('./resources/cmu_dictionary')

    output_dir = os.path.join(args.output_dir, model_name, f"n_epoch={ckpt_step}", args.sampler, f"nfe={args.timesteps}")
    check_dir(output_dir)

    with torch.no_grad():
        for i in range(len(test_samples_x)):
            print(f'Synthesizing {i} text...', end=' ')
            x = test_samples_x[i].cuda()[None]
            x_lengths = torch.LongTensor([x.shape[-1]]).cuda()

            t = dt.datetime.now()
            y_enc, y_dec, attn, y_dec_xs = model.forward(x, x_lengths,
                                            n_timesteps=args.timesteps, sampler=args.sampler,
                                            spk=spk, clip_denoise=False,
                                            verbose=True, length_scale=0.91)
            t = (dt.datetime.now() - t).total_seconds()
            print(f'Bridge-TTS RTF: {t * 22050 / (y_dec.shape[-1] * 256)}')
            y_dec = y_dec.cuda()
            audio = (vocoder.forward(y_dec).cpu().squeeze().clamp(-1, 1).numpy() * 32768).astype(np.int16)

            write(os.path.join(output_dir, f"sample_{i}_text={test_samples_text[i]}.wav"), 22050, audio)

            if args.plot_latent:
                traj_output_dir = os.path.join(args.output_dir, model_name, f"n_epoch={ckpt_step}", args.sampler, f"nfe={args.timesteps}", f"sample_{i}_text={test_samples_text[i]}")
                check_dir(traj_output_dir)
                for j in range(y_dec_xs.shape[1]):
                    save_plot_final(y_dec_xs[:, j].squeeze().cpu(),
                                    f"{traj_output_dir}/step={j}.png")


    print(f'Done. Check out {output_dir} folder for samples.')
