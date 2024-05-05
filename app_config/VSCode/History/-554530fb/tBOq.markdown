# Diffusion工作名录

图像生成：NCSN 、DDPM、DDIM

文生图：

- Classifier guidance:
  - 按类生成: Diffusion Models Beat GANs on Image Synthesis
  - 按图像、按文本和多模态条件来生成: More Control for Free! Image Synthesis with Semantic Diffusion Guidance
- Classifier-free guidance: GLIDE→{DALLE2、Imagen}, stable diffusion, Midjourney

图生图/Image Editing：SDEdit、Depth-to-image、ControlNet

# Diffusion 论文汇总

Diffusion Models从入门到放弃：必读的10篇经典论文(2023-01-01) https://zhuanlan.zhihu.com/p/595866176

- DDPM奠基之作：《Denoising Diffusion Probabilistic Models》
- 从DDPM到DDIM：《Denoising Diffusion Implicit Models》
- 第一波高潮！首次击败GANs：《Diffusion Models Beat GANs on Image Synthesis》
- 条件分类器技术进一步发展：《Classifier-Free Diffusion Guidance》
- Image-to-Image经典之作《Palette: Image-to-Image Diffusion Models》
- 畅游多模态领域：GLIDE
- stable diffusion的原型：《High-Resolution Image Synthesis with Latent Diffusion Models》
- 高调进军视频领域：《Video Diffusion Models》
- 了不起的attention：《Prompt-to-Prompt Image Editing with Cross Attention Control》
- Unet已死，transformer当立！《Scalable Diffusion Models with Transformers》

2023年Diffusion Models还有哪些方向值得研究(好发论文)？ https://zhuanlan.zhihu.com/p/566059899

扩散模型汇总——从DDPM到DALLE2 https://juejin.cn/post/7181011684041949240

Difffusion学习笔记 https://www.zhihu.com/column/c_1712921480839639040

# 各种生成模型比较

各种生成模型：VAE、GAN、flow、DDPM、autoregressive models https://blog.csdn.net/zephyr_wang/article/details/126588478

# 待读资料

diffusion合集 https://github.com/heejkoo/Awesome-Diffusion-Models

ControlNet star量破万！2023年，AI绘画杀疯了 -机器之心 https://mp.weixin.qq.com/s/lkR03NnKSF00q6W_Lc9D1w

适配Diffusers框架的全套教程来了！从T2I-Adapter到大热ControlNet https://mp.weixin.qq.com/s/3cIr0KWrIE9TaVYV-6q4gQ

OpenAI用GPT-4解释了GPT-2三十万个神经元：智慧原来是这个样子 https://mp.weixin.qq.com/s/ZG5ZUDmpok9Ct4ecM56JXw

分解大模型的神经元！Claude团队最新研究火了，网友：打开黑盒 https://mp.weixin.qq.com/s/FAz3MjN5uRFo9xVpqbgebw

# 待查简介

文本反转： https://textual-inversion.github.io ：图像转为一个词，学到该词的embedding，而后带入propmt中，去生成图像。An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion。

Hypernetwork是一种微调Stable Diffusion的技术，它通过干预交叉注意力网络来插入风格。

LoRA 模型修改交叉注意力模块的权重以更改风格。仅修改此模块就可以微调 Stabe Diffusion模型这一事实说明了该模块的重要性。

ControlNet 通过检测到的轮廓、人体姿势等来调节噪声预测器，并实现对图像生成的出色控制。

下文来自： https://zhuanlan.zhihu.com/p/627133524

[SDEdit](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2108.01073)：图像到图像，可用于任何扩散模型。故有Stable Diffusion的图像到图像的功能。

[Depth-to-image](https://stable-diffusion-art.com/depth-to-image/)：图像到图像的diffusion中，使用深度图prompt+文本prompt去预测噪声，去生成新图像，让新图像的深度图和输入的深度图尽可能一致。问题：depth map如何处理后才输入到denoiser？

Stable diffusion的版本

Stable diffusion v1 和 v2 差异详见 https://zhuanlan.zhihu.com/p/627133524

V1.4: https://huggingface.co/CompVis

V2.0: https://stable-diffusion-art.com/how-to-run-stable-diffusion-2-0/

V2.1: https://huggingface.co/stabilityai/stable-diffusion-2-1
