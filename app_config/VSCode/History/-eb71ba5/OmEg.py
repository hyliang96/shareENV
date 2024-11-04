# Copyright (C) 2021. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

import argparse
import os
import numpy as np
from tqdm import tqdm

import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from configs import decoder_dict
from model import TextEncoder, Diffusion_SB, Diffusion_Grad, Diffusion_I2SB, TTS, TTS_Encoder
from model.utils import fix_len_compatibility
from data import TextMelDataset, TextMelBatchCollate
from utils import plot_tensor, save_plot
from file_utils import check_dir
from text.symbols import symbols

OUT_SIZE = fix_len_compatibility(2*22050//256)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Method
    parser.add_argument('--config', type=str, choices=['encoder', 'gradtts', 'bridgetts-i2sb', 'bridgetts', 'bridgetts-fg', 'bridgetts-beta', 'bridgetts-vp'])
    # Data
    parser.add_argument('--train_filelist_path', type=str)
    parser.add_argument('--valid_filelist_path', type=str)
    parser.add_argument('--cmudict_path', type=str, default="./resources/cmu_dictionary")
    parser.add_argument('--add_blank', type=bool, default=True)
    parser.add_argument('--n_feats', type=int, default=80)
    parser.add_argument('--n_fft', type=int, default=1024)
    parser.add_argument('--sample_rate', type=int, default=22050)
    parser.add_argument('--hop_length', type=int, default=256)
    parser.add_argument('--win_length', type=int, default=1024)
    parser.add_argument('--f_min', type=int, default=0)
    parser.add_argument('--f_max', type=int, default=8000)
    parser.add_argument('--cache_dataset', action='store_true')
    # Encoder
    parser.add_argument('--load_encoder', action='store_true')
    parser.add_argument('--encoder_ckpt_path', type=str, required=False)
    # Decoder
    parser.add_argument('--offset', type=float, default=1e-5)
    parser.add_argument('--beta_min', type=float, default=100, help='minimum beta')
    parser.add_argument('--beta_max', type=float, default=100, help='maximum beta')
    parser.add_argument('--f', type=float, default=-0.01, help='drift')
    parser.add_argument('--g', type=float, default=0.7297, help='schedule')
    parser.add_argument('--predictor', type=str, required=False, default="hpsi")
    # Training
    parser.add_argument('--n_spks', type=int, default=1)
    parser.add_argument('--test_size', type=int, default=4)
    parser.add_argument('--n_epochs', type=int, default=2280)
    parser.add_argument('--batch_size', type=int, default=16)
    parser.add_argument('--learning_rate', type=float, default=1e-4)
    parser.add_argument('--seed', type=int, default=37)
    parser.add_argument('--save_every', type=int, default=20)
    parser.add_argument('--resume_from_ckpt', type=int, default=-1)
    parser.add_argument('--log_dir', type=str)
    args = parser.parse_args()

    check_dir(os.path.join(args.log_dir, "figs"))
    check_dir(os.path.join(args.log_dir, "ckpts"))

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    print("args:", args)

    print('Initializing logger...')
    logger = SummaryWriter(log_dir=args.log_dir)

    print('Initializing data loaders...')
    train_dataset = TextMelDataset(args.train_filelist_path, args.cmudict_path, args.add_blank,
                                   args.n_fft, args.n_feats, args.sample_rate, args.hop_length,
                                   args.win_length, args.f_min, args.f_max, use_cache=args.cache_dataset)
    batch_collate = TextMelBatchCollate()
    loader = DataLoader(dataset=train_dataset, batch_size=args.batch_size,
                        collate_fn=batch_collate, drop_last=True,
                        num_workers=4, shuffle=False)
    # test_dataset = TextMelDataset(args.valid_filelist_path, args.cmudict_path, args.add_blank,
                                #   args.n_fft, args.n_feats, args.sample_rate, args.hop_length,
                                #   args.win_length, args.f_min, args.f_max)

    print('Initializing model...')
    nsymbols = len(symbols) + 1 if args.add_blank else len(symbols)
    encoder = TextEncoder(nsymbols, n_feats=args.n_feats, n_spks=args.n_spks)

    if args.config == "encoder":
        model = TTS_Encoder(encoder, n_feats=args.n_feats, n_spks=args.n_spks)
    else:
        if args.config == "bridgetts-fg":
            decoder = decoder_dict[args.config](f=args.f, g=args.g, n_spks=args.n_spks, predictor=args.predictor, offset=args.offset)
        elif args.config == "bridgetts":
            decoder = decoder_dict[args.config](g2_min=args.beta_min, g2_max=args.beta_max, n_spks=args.n_spks, predictor=args.predictor, offset=args.offset)
        else:
            decoder = decoder_dict[args.config](beta_min=args.beta_min, beta_max=args.beta_max, n_spks=args.n_spks, predictor=args.predictor, offset=args.offset)

        model = TTS(encoder, decoder, n_feats=args.n_feats, n_spks=args.n_spks, pre_trained_enc=args.load_encoder)

        if args.load_encoder:
            # assert os.path.isdir(args.encoder_ckpt_path)
            tmp_encoder = TextEncoder(nsymbols)
            # tmp_decoder = decoder_dict[args.config]()
            # tmp_model = TTS(tmp_encoder, tmp_decoder)
            tmp_model = TTS_Encoder(tmp_encoder, n_feats=args.n_feats, n_spks=args.n_spks)
            tmp_model.load_state_dict(torch.load(args.encoder_ckpt_path))

            model.encoder = tmp_model.encoder

            for param in model.encoder.parameters():
                param.requires_grad = False

        if args.resume_from_ckpt > 0:
            model.load_state_dict(torch.load(os.path.join(args.log_dir, f"ckpts/grad_{args.resume_from_ckpt}.pt")))

    model.cuda()
    # print('Number of encoder + duration predictor parameters: %.2fm' % (model.encoder.nparams/1e6))
    # print('Number of decoder parameters: %.2fm' % (model.decoder.nparams/1e6))
    # print('Total parameters: %.2fm' % (model.nparams/1e6))

    print('Initializing optimizer...')
    optimizer = torch.optim.Adam(params=model.parameters(), lr=args.learning_rate)

    # print('Logging test batch...')
    # test_batch = test_dataset.sample_test_batch(size=args.test_size)
    # for i, item in enumerate(test_batch):
    #     mel = item['y']
    #     logger.add_image(f'image_{i}/ground_truth', plot_tensor(mel.squeeze()),
    #                      global_step=0, dataformats='HWC')
    #     save_plot(mel.squeeze(), f'{args.log_dir}/figs/original_{i}.png')

    print('Start training...')
    iteration = 0
    start_epoch = 1

    if args.resume_from_ckpt > 0:
        for epoch in tqdm(range(1, args.resume_from_ckpt + 1), desc='resuming training states...'):
            for batch_idx, batch in enumerate(loader):
                iteration += 1
        start_epoch = args.resume_from_ckpt + 1


    for epoch in range(start_epoch, args.n_epochs + 1):

        model.train()
        dur_losses = []
        prior_losses = []
        diff_losses = []
        with tqdm(loader, total=len(train_dataset)//args.batch_size) as progress_bar:
            for batch_idx, batch in enumerate(progress_bar):
                model.zero_grad()
                x, x_lengths = batch['x'].cuda(), batch['x_lengths'].cuda()
                y, y_lengths = batch['y'].cuda(), batch['y_lengths'].cuda()
                if args.config != "encoder":
                    dur_loss, prior_loss, diff_loss = model.compute_loss(x, x_lengths,
                                                                        y, y_lengths,
                                                                        out_size=OUT_SIZE)
                    if args.load_encoder:
                        loss = diff_loss
                    else:
                        loss = dur_loss + prior_loss + diff_loss

                    loss.backward()

                    if not args.load_encoder:
                        enc_grad_norm = torch.nn.utils.clip_grad_norm_(model.encoder.parameters(),
                                                                    max_norm=1)
                    dec_grad_norm = torch.nn.utils.clip_grad_norm_(model.decoder.parameters(),
                                                                max_norm=1)
                    optimizer.step()

                    if not args.load_encoder:
                        logger.add_scalar('training/duration_loss', dur_loss.item(),
                                        global_step=iteration)
                        logger.add_scalar('training/prior_loss', prior_loss.item(),
                                        global_step=iteration)
                    logger.add_scalar('training/diffusion_loss', diff_loss.item(),
                                    global_step=iteration)
                else:
                    dur_loss, prior_loss = model.compute_loss(x, x_lengths,
                                                              y, y_lengths,
                                                              out_size=OUT_SIZE)
                    diff_loss = torch.zeros(1)
                    loss = dur_loss + prior_loss
                    loss.backward()
                    enc_grad_norm = torch.nn.utils.clip_grad_norm_(model.encoder.parameters(),
                                                                   max_norm=1)
                    optimizer.step()
                # logger.add_scalar('training/encoder_grad_norm', enc_grad_norm,
                #                   global_step=iteration)
                # logger.add_scalar('training/decoder_grad_norm', dec_grad_norm,
                #                   global_step=iteration)

                if args.load_encoder:
                    dur_losses.append(torch.zeros(1))
                    prior_losses.append(torch.zeros(1))
                else:
                    dur_losses.append(dur_loss.item())
                    prior_losses.append(prior_loss.item())
                diff_losses.append(diff_loss.item())

                if batch_idx % 5 == 0:
                    msg = f'Epoch: {epoch}, iteration: {iteration}'
                    progress_bar.set_description(msg)

                iteration += 1

        # log_msg = 'Epoch %d: duration loss = %.3f ' % (epoch, np.mean(dur_losses))
        # log_msg += '| prior loss = %.3f ' % np.mean(prior_losses)
        # log_msg += '| diffusion loss = %.3f\n' % np.mean(diff_losses)
        # with open(f'{args.log_dir}/train.log', 'a') as f:
        #     f.write(log_msg)

        if epoch % args.save_every == 0:
            ckpt = model.state_dict()
            torch.save(ckpt, f=f"{args.log_dir}/ckpts/grad_{epoch}.pt")
