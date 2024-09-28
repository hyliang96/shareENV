## Token Merge

**ToMe**：Token Merge用在Diffusion上搞可解释模型

Token Merge：用在ViT上，用于加速：https://arxiv.org/pdf/2210.09461.pdf

已经有人搞了Token Merge+diffusion，发了个workshop，Token Merging for Fast Stable Diffusion https://arxiv.org/pdf/2303.17604.pdf

他们的侧重点都在加速，不在可解释性、可控性。

需要自己再想想有差异性的idea。

[Token Merge 加速Diffusion模型推理 | OpenMMLab MMagic实现](https://zhuanlan.zhihu.com/p/625899991)

## graph和diffusion结合

**diffusionSeg：2023年3月，用stable diffusion产生的feature，经过graph Net，去做分割。**

UniGS：统一分割和生成

我的idea：在UniGS基础上加个graph，就像diffusionSeg那样

## Diffusion相关的论文

去看看controlNet

adobe已经有可交互（用户不断调整）地生成图像的

diffusion中用transformer替代unet，适合diffusion的transformer架构

* U-ViT：鲍凡做的，最早的diffusion transformer，其中的transformer有skip connection
* DiT：2022年12月出来的，没有skip connection，只有往每一层注入条件

去看看主流的diffusion schedule：Karras, T., Aittala, M., Aila, T., Laine, S., 2022. Elucidating the Design Space of Diffusion-Based Generative Models. https://doi.org/10.48550/arXiv.2206.00364

* AnimateDiff

## 双向Diffusion

苏老师：将图像识别和图像生成用同一个模型去做

我的问题：

* 用可逆网络做吗？
* 还是像GAN那样，生成用diffusion，识别用另一个网络？

LLaVA是李春元在微软时做的，后来做了许多后续工作：

图像交互编辑 LLaVa， interactive LLaVa 在intreactive LLaVa中，会给半成品图像生成文字评论，指出当中还需要进一步改进的点，若用户同意，则进一步编辑图像。这样的可解释性、可控性大大增强。

LLaVa-plus, 刘世隆做，李春元（在字节）指导。从LLM到LMM，并调用多种tools。

LLaVa-1.5

open sora：https://github.com/hpcaitech/Open-Sora， 卡少的小作坊联合开源复刻sora

mira (mini-sore),  https://github.com/mini-sora/minisora
