# 有待调研

* [ ] DALLE
* [ ] DALLE2
* [ ] Imagen
* [ ] eDiff-l
* [ ] Stable diffusion
* [ ] ERRNIE-ViLG
* [ ] Midjourney

# 条件diffusion的类型

Classifier Guidance：加一个分类器

Classifier-Free Guidance：不加分类器，而是把送y到denoiser中

# DALLE 2及其前置工作

### CLIP

[[GIthub]](https://github.com/openai/CLIP) [[Blog]](https://openai.com/blog/clip/) [[Paper]](https://arxiv.org/abs/2103.00020) [[Model Card]](https://github.com/openai/CLIP/blob/main/model-card.md) [[Colab]](https://colab.research.google.com/github/openai/clip/blob/master/notebooks/Interacting_with_CLIP.ipynb)

CLIP（**C**ontrastive **L**anguage-**I**mage **P**re-training）学习的。

CLIP接受过数亿张图片及其相关文字的训练，学习到了给定文本片段与图像的关联。

也就是说，CLIP并不是试图预测给定图像的对应文字说明，而是只学习任何给定文本与图像之间的关联。CLIP做的是对比性而非预测性的工作。

整个DALL-E 2模型依赖于CLIP从自然语言学习语义的能力，所以让我们看看如何训练CLIP来理解其内部工作。

训练CLIP的基本原则非常简单:

1. 首先，所有图像及其相关文字说明都通过各自的编码器，将所有对象映射到m维空间。
2. 然后，计算每个(图像，文本)对的cos值相似度。
3. 训练目标是使N对正确编码的图像/标题对之间的cos值相似度最大化，同时使N2 - N对错误编码的图像/标题对之间的cos值相似度最小化。

训练过程如下图所示:

![1707203764014](assets/1707203764014.png)

### GLIDE

GLIDE：Classifier-Free Guidance 文生图

**GLIDE最大的贡献是开始用文本作为条件引导图像的生成**，下图是其训练过程，和之前工作差异主要有以下几点：

- **分词后将文本送入transformer（bert），生成文本的embedding**
- **文本embedding中最后一个token的特征作为扩散模型中classifier-free     guidance中的条件c**

原文：

[Classifier-free Diffusion Guidance, Jonathan Ho, Tim Salimans](https://arxiv.org/pdf/2207.12598.pdf)

[GLIDE: Towards Photorealistic Image Generation and Editing with Text-Guided Diffusion Models](https://arxiv.org/pdf/2112.10741.pdf)

参考：

[通俗理解Classifier Guidance 和 Classifier-Free Guidance 的扩散模型](https://zhuanlan.zhihu.com/p/640631667)

贝叶斯定理

$$
P(y|x_t)=\frac{P(x_t|y)P(y)}{P(x_t))}
$$

对其取导数

$$
\nabla_{x_t} \log P(y|x_t)=\nabla_{x_t} \log P(x_t|y)-\nabla_{x_t} \log P(x_t)
$$

由于$\nabla_{x_t} \log P(x_t)=-\frac{\epsilon_\theta(x_t,t)}{\sqrt{1-\bar{\alpha}_t}}$，故

$$
\nabla_{x_t} \log P(y|x_t)=-\frac{\epsilon_\theta(x_t,t,y)-\epsilon_\theta(x_t,t)}{\sqrt{1-\bar{\alpha}_t}}
$$

将前式改写为

$$
\nabla_{x_t} \log P(x_t|y)=\nabla_{x_t} \log P(x_t)+\nabla_{x_t} \log P(y|x_t)
$$

并在将右侧的第二项前加上系数$\omega>0$，$\omega$越大则条件项的比重越大，当$\omega=0$则为无条件生成

$$
\nabla_{x_t} \log P(x_t|y)=\nabla_{x_t} \log P(x_t)+\omega\nabla_{x_t} \log P(y|x_t)
$$

向上式中带入

$$
\begin{aligned}
\nabla_{x_t} \log P(x_t)&=-\frac{\epsilon_\theta(x_t,t)}{\sqrt{1-\bar{\alpha}_t}}\\
\nabla_{x_t} \log P(x_t|y)&=-\frac{\epsilon_\theta(x_t,t,y)}{\sqrt{1-\bar{\alpha}_t}}\\
\nabla_{x_t} \log P(y|x_t)&=-\frac{\epsilon_\theta(x_t,t,y)-\epsilon_\theta(x_t,t)}{\sqrt{1-\bar{\alpha}_t}}
\end{aligned}
$$

则得到校准后的有条件的噪声估计$\bar{\boldsymbol{\epsilon}}_\theta\left(\mathbf{x}_t, t, y\right)$为

$$
\begin{aligned} \bar{\boldsymbol{\epsilon}}_\theta\left(\mathbf{x}_t, t, y\right) & =\boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t, y\right)+w\left(\boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t\right)-\boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t\right)\right) \\ & =(1-w) \boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t, y\right)+w \boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t\right)\end{aligned}
$$

其中，$\boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t,y\right)$为未校准的有条件噪声估计，$\boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t\right)$为无条件的噪声估计，它俩都使用同一个网络去估计，即$\boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t\right)$由$\boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t,y=∅\right)$来给出。





原文推导错了，不是

$$
\begin{aligned} \bar{\boldsymbol{\epsilon}}_\theta\left(\mathbf{x}_t, t, y\right) & =\boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t, y\right)-\sqrt{1-\bar{\alpha}_t} w \nabla_{\mathbf{x}_t} \log p\left(y \mid \mathbf{x}_t\right) \\ & =\boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t, y\right)+w\left(\boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t, y\right)-\boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t\right)\right) \\ & =(w+1) \boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t, y\right)-w \boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t\right)\end{aligned}
$$

而是




$$
\begin{array}{l}\bar{\epsilon}_\theta\left(x_t, t, y\right)=\epsilon_\theta\left(x_t, t\right)-\sqrt{1-\bar{\alpha}_t} \omega \nabla_{x_t} \log p\left(y \mid x_t\right)\ \ \ \ //故意取系数为\sqrt{1-\bar{\alpha}_t} \omega, 带入上式即可消掉\sqrt{1-\bar{\alpha}_t} \\ =\epsilon_\theta\left(x_t, t\right)+\omega\left(\epsilon_\theta\left(x_t, t, y\right)-\epsilon_\theta\left(x_t, t\right)\right) \\ =(1-\omega) \epsilon_\theta\left(x_t, t\right)+\omega \epsilon_\theta\left(x_t, t, y\right)\end{array}
$$

[一文读懂Diffusion Model](https://zhuanlan.zhihu.com/p/599160988)  见 Conditional Diffusion Model

[图像生成别只知道扩散模型，还有基于梯度去噪的分数模型NCSN](https://zhuanlan.zhihu.com/p/597490389)  见 条件生成

[扩散模型汇总——从DDPM到DALLE2](https://zhuanlan.zhihu.com/p/449284962)

[扩散模型应用篇](https://zhuanlan.zhihu.com/p/600804021)

[DALL-E 2的工作原理原来是这样！](https://mp.weixin.qq.com/s/6F4wnzaYF_EMDgfF_Pwd8A)：

GLIDE的目标不是构建一个自编码器并在给定的嵌入条件下精确地重建图像，而是在给定的嵌入条件下生成一个保持原始图像显著特征的图像。为了进行图像生成，GLIDE使用了扩散模型（ **Diffusion Model** ）。

![1707207771557](assets/1707207771557.png)

一只吹喷火喇叭的柯基”一图经过**CLIP的图片编码器**，GLIDE利用这种编码生成保持原图像显著特征的新图像。 [图源](https://arxiv.org/abs/2204.06125)

GLIDE的训练流程：

![iShot_2024-02-06_16.37.38](assets/iShot_2024-02-06_16.37.38.png)

![iShot_2024-02-06_16.37.55](assets/iShot_2024-02-06_16.37.55.png)

![iShot_2024-02-06_16.37.59](assets/iShot_2024-02-06_16.37.59.png)

![iShot_2024-02-06_16.38.03](assets/iShot_2024-02-06_16.38.03.png)

![iShot_2024-02-06_16.38.07](assets/iShot_2024-02-06_16.38.07.png)

![iShot_2024-02-06_16.38.11](assets/iShot_2024-02-06_16.38.11.png)

![iShot_2024-02-06_16.38.15](assets/iShot_2024-02-06_16.38.15.png)

下面是一些使用GLIDE生成的图像示例。作者指出，就照片真实感和文本相似度两方面而言，GLIDE的表现优于DALL-E 1。

【为什么要第五步？】

### DALLE 2

论文信息

* 论文原文：[Hierarchical Text-Conditional Image Generation with CLIP Latent](http://arxiv.org/abs/2204.06125)
* 非官方代码：https://github.com/lucidrains/DALLE2-pytorch
* 作者/单位：Aditya Ramesh et al. / Open AI

简介

* [DALL-E 2的工作原理原来是这样！](https://mp.weixin.qq.com/s/6F4wnzaYF_EMDgfF_Pwd8A)
* [DALL·E 2 解读 | 结合预训练CLIP和扩散模型实现文本-图像生成](https://zhuanlan.zhihu.com/p/526438544)

![640](assets/640.png)

DALL-E 2使用了一种改进的GLIDE模型，这种模型以两种方式使用投影的CLIP文本嵌入：

* 第一种方法是将它们添加到GLIDE现有的**时间步嵌入**中；
* 第二种方法是创建四个额外的**上下文标记**，这些标记连接到GLIDE文本编码器的输出序列。

![img](assets/v2-2cd0e865cb388ba9a2093fc934aacaea_1440w.jpg)

这个模型可以根据CLIP图像编码的$z_i$，还原出具有相同与 $x$ 有相同语义，而又不是与 $x$ 完全一致的图像。

训练：训练好text encoder和img encoder后，将成对的text和文本分别转换为text embed $z_t$和img embed $z_i$，并训练prior模块用text encoder预测img encoder，输出为$z_i'$

![img](assets/v2-9735490632574f482139700d69156f78_1440w.jpg)

在DALL·E 2 模型中，作者团队尝试了两种先验模型：自回归模型（Autoregressive/AR prior) 和扩散模型（Diffusion prior），最终发现它们的性能相差无几。考虑到扩散模型的计算效率更高，因此选择扩散模型作为 DALL-E 2的先验模块。在训练prior模块时，作者使用了主成分分析法PCA来提升训练的稳定性（详见原文）。

# Stable Diffusion

基于LDMs的文图生成（text-to-image）模型。

数据集：在[LAION-5B](https://link.zhihu.com/?target=https%3A//laion.ai/blog/laion-5b/)的一个子集

创新点：

1. 潜在扩散模型（Latent Diffusion Models，LDMs）：加速无条件图像生成。首先用VAE将图像压缩到潜空间中，然后在潜空间使用Diffusion。对比原像素空间，潜空间（latent space）小了 48 倍，故快得多。
2. 条件机制：cross-attention结构（在2020年的论文handwriting     diffusion上就用过，但是当时并没有引起广泛的注意。在这之后cross-attention成为多模态的一种常用方法，成为新的常用条件扩散模型。）

[Stable Diffusion原理详解](https://developer.aliyun.com/article/1215455)

[Stable Diffusion原理解读](https://zhuanlan.zhihu.com/p/583124756)

![image-20240127105327245](assets/image-20240127105327245.png)

普通的扩散模型（Diffusion Models，DM）训练时的目标函数是：

$$
L_{DM}:=\mathbb{E}_{x,\epsilon\sim\mathcal{N}(0,1),t\sim[1,T]}\Vert\epsilon-\epsilon_\theta(x_t,t)\Vert^2_2
$$

潜在的扩散模型（Latent Diffusion Models，LDM）训练时的目标函数，只需将$x$替换为其编码$\mathcal{E}(x)$即可，其中$\mathcal{E}$是将图像转化为潜表示的编码器（详见上图）：

$$
L_{LDM}:=\mathbb{E}_{\mathcal{E}(x),\epsilon\sim\mathcal{N}(0,1),t\sim[1,T]}\Vert\epsilon-\epsilon_\theta(x_t,t)\Vert^2_2
$$

领域专用编码器 ( domain specific encoder) $\tau_\theta$ ，将各种模态 (如文本、类别、layout等 ) 的条件 $y$ ，映射到同一空间内， $\tau_\theta(y) \in R^{M \times d_\tau}$,

$$
\operatorname{Attention}(Q, K, V)=\operatorname{softmax}\left(\frac{Q K^T}{\sqrt{d}}\right) \cdot V, \text{with}
$$

$$
Q=W_Q^{(i)} \cdot \varphi_i\left(z_t\right), K=W_K^{(i)} \cdot \tau_\theta(y), V=W_V^{(i)} \cdot \tau_\theta(y)
$$

其中 $\varphi_i\left(z_t\right) \in \mathbb{R}^{N \times d_e^i}$ 是UNet的一个中间表征。相应的目标函数可以写成如下形式:

$$
L_{L D M}:=\mathbb{E}_{\mathcal{E}(x), y, \epsilon \sim \mathcal{N}(0,1), t\sim[1,T]}\left\|\epsilon-\epsilon_\theta\left(z_t, t, \tau_\theta(y)\right)\right\|_2^2
$$

图片感知压缩 ( Perceptual Image Compression )
给定图像 $x \in R^{H \times W \times 3}$ ，潜表示 $z \in R^{h \times w \times c}$ ，下采样因子的大小为 $f=\frac{H}{h}=\frac{W}{w}=2^m ， m \in R$ 。

**论文：**

Stable diffusion：

**Stable diffusion 开源代码**

内核： https://github.com/CompVis/stable-diffusion

Web-UI： https://github.com/AUTOMATIC1111/stable-diffusion-webui

# 其它条件diffusion模型

图转图（SDEdit）：输入图喂给VAE编码器得带噪声的image latent，作为z_T输给diffusion，反向扩散得到去噪后到image latent，然后过VAE的解码器得到输出图像。diffusion反向扩散，是图像翻译在特征空间的操作。
