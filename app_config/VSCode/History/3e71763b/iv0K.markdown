# 简介

## 文字简介

摘自[【原创】万字长文讲解Stable Diffusion的AI绘画基本技术原理](https://zhuanlan.zhihu.com/p/621493124)

[DDIM 修正主义指南](https://zhuanlan.zhihu.com/p/585785726)

**采样算法加速简介：**

* 不同的采样加速算法，训练过程都一样，都是1000步，可以直接复用DDPM训练的噪声预测网络；
* 不同的采样加速算法，仅在采样时有不同，采样的步数、步长、$x_t$的迭代公式都不同。

以下**采样步数**为NFE（number of function evaluations），即**调用噪声预测网络$\epsilon_\theta(x_t,t)$的次数**，而非$x_t$的迭代公式使用的次数。

**DDPM**（Denoising Diffusion Probabilistic Model），因为传统“扩散模型”是通过朗之万方程从能量模型的采样也有很大的不确定性，得到的往往是带有噪声的采样结果。所以很长时间以来，这种传统路径的扩散模型只是在比较低分辨率的图像上做实验。2020年所提出的DDPM（Denoising Diffusion Probabilistic Model）是一个新的起点、新的篇章。DDPM叫“渐变扩散模型”更为准确一些，DDPM的数学框架其实在ICML2015的论文《Deep Unsupervised Learning using Nonequilibrium Thermodynamics》就已经完成了，但DDPM是首次将它在高分辨率图像生成上调试出来了，从而引导出了后面图片生成的火热，DDPM 默认采用的是线性的加噪采样方案 (linear schedule)。**需要采样1000步。**

**DDIM**（Denoising Diffusion Implicit Models，去噪扩散隐式模型），DDIM和DDPM有相同的训练目标，但是它不再限制扩散过程必须是一个马尔卡夫链，这使得DDIM可以采用更小的采样步数来加速生成过程，DDIM的另外是一个特点是从一个随机噪音生成样本的过程是一个确定的过程。**需要采样250步**。

**PNDM**（Pseudo Numerical methods for Diffusion Models）是一个新的适用于扩散模型的类数值方法，这一方法既不需要重新训练模型，也对模型结构和超参数没有额外的限制，**仅仅通过修改迭代公式**，将扩散模型无任何精度损失加速 20 倍，**迭代 50 步**就可以达到原来 1000 步的 FID 结果。

* **PLMS** (Pseudo Linear Multi-Step method，伪线性多步方法) ：PNDM中的一个步骤，主要是基于diffusion model的原理采样下一步的图片，主要是逐步重建图片的反向去噪过程，对于每一步的图片都应用相应更新diffusion过程的各个参数生成下一步图片，主要是一个**类似于线性的采样方法**。

**DPM-Solver**（Diffusion Process Model Solver，扩散处理模型求解器）是清华大学**朱军**教授带领的TSAIL团队所提出的，一种针对于扩散模型特殊设计的高效求解器：该算法无需任何额外训练，**同时适用于离散时间与连续时间**的扩散模型，可以在 **20 到 25 步**内几乎收敛，并且只**用 10 到 15 步**也能获得非常高质量的采样。在 Stable Diffusion 上，25 步的 DPM-Solver 就可以获得优于 50 步 PNDM 的采样质量，因此采样速度直接翻倍。

Analytic-DPM：鲍凡提出，为扩散模型的最优均值和方差给出了简单、令人吃惊的解析形式，获得 ICLR 2022 Outstanding Paper Award。

## 记号约定

$$
\begin{eqnarray}
我起的名字&=我的记号&=DDPM原文中的记号\\
\\
直达信号系数&=a_t&=\sqrt{\bar\alpha_t}\\
直达噪声系数&=b_t&=\sqrt{\bar\beta_t}=\sqrt{1-\bar\alpha_t}，在DDPM论文满足a^2_t+b^2_t=1\\
\\
单步信号系数&=a'_t&=a_{t|t-1}=\sqrt{\alpha_t}\\
单步噪声系数&=b'_t&=b_{t|t-1}=\sqrt{\beta_t}=\sqrt{1-\alpha_t}，在DDPM论文中满足{a'}^2_t+{b'}^2_t=1\\
\\
多步加噪声从\tau到t&\quad\tau&=t-\Delta t\\
多步信号系数&=a_{t|\tau} \\
多步信号系数&=b_{t|\tau} \\
\\
信号强度&=a_t^2&=\bar\alpha_t\\
噪声强度&=b_t^2&=\bar\beta_t\\
信噪比(SNR)&=\frac{a_t^2}{b_t^2}&=\frac{\bar\alpha_t}{\bar\beta_t}\\
半对数信噪比&=\lambda_t&=\frac{a_t}{b_t}\\
\\
单步噪声&={\boldsymbol z}'_t&=\boldsymbol \epsilon_t\\
直达噪声&=\boldsymbol  z_t&=\bar{\boldsymbol \epsilon}_t\\
预测单步噪声&=\boldsymbol\epsilon'_\theta(x_t,t)&=无\\
预测直达噪声&=\boldsymbol\epsilon_\theta(x_t,t)&=同左\\
用x_t预测x_0的均值&=\boldsymbol\mu_\theta(x_t,t)&=无\\
用x_t预测x_0的方差&=\sigma_{0|t}\\
\\
生成时噪声&=\boldsymbol z&=\boldsymbol\epsilon\\
生成时噪声的方差&=\sigma_t&=\sigma_t
\end{eqnarray}
$$

用我的记号表示

$$
\begin{eqnarray}
单步加噪&\quad \boldsymbol x_t&=a'_t\boldsymbol  x_{t-1}+b'_t\boldsymbol  z'_{t},\boldsymbol z'_t\sim N(0,I)\\
直达加噪&\quad \boldsymbol x_t&=a_t\boldsymbol  x_{0}+b_t \boldsymbol z_{t},\boldsymbol z_t\sim N(0,I)\\
多步加噪&\quad \boldsymbol x_t&=a_{t|\tau} \boldsymbol  x_{\tau}+b_{t|\tau} \boldsymbol z_{t|\tau} ,\boldsymbol z_{t|\tau} \sim N(0,I)\\
预测x_0的方差&\quad \boldsymbol\mu_\theta(x_t,t)&=\frac{1}{a_t}(\boldsymbol x_t-b_t \boldsymbol \epsilon_\theta(\boldsymbol x_t,t))\\
预测\boldsymbol x_0&\quad \boldsymbol x_0&=\boldsymbol \mu_\theta(x_t,t)+\sigma_{0|t}\boldsymbol  z_{0|t},\boldsymbol  z_{0|t}\sim N(0,I)\\
去噪：预测x_{t-1}&\quad \boldsymbol x_{\tau}&=a_\tau \boldsymbol\mu_\theta(x_t,t)+\sqrt{b^2_{\tau}-\sigma_t^2} \boldsymbol\epsilon_\theta\left(x_t, t\right)+\sigma_t \boldsymbol z, \boldsymbol z\sim N(0,I)\\
\end{eqnarray}
$$

系数的关系式

$$
a_{t|\tau}=\frac{a_t}{a_\tau}\\
b_t^2=b_{t|\tau}^2+a_{t|\tau}^2 b_\tau ^2\\
\
a'_{t}=\frac{a_t}{a_{t-1}}\\
b_t^2={b'_t}^2+{a'_t}^2 b_{t-1} ^2
$$

## 表格对比各种采样方法

| 方法             | 前传的原始设定                                                                     | 前传$p(x_t\vert x_{t-1})$是否确定 | 反传/采样公式，分布$q(x_{x_-\Delta t}\vert x_t,x_0)$                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `<span style="display:inline-block;width:80px">`反传过程是否随机 |
| ---------------- | ---------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| **DDPM类** | $x_t\vert x_{t-1}=a'_t x_{t-1}+b'_{t}z'_t ,z'_t\sim N(0,I)$                      | 是                                  | $\boldsymbol{x}_{t-1}\vert x_t,x_0=\frac{1}{a'_t}\left(\boldsymbol{x}_t-\frac{{b'}_t^2}{b_t}\boldsymbol{\epsilon}_\theta(x_t,t)\right)+\boldsymbol \Sigma_\theta^{\frac{1}{2}}\left(x_t, t\right)\boldsymbol{z},\boldsymbol{z}\sim\mathcal{N}(\boldsymbol{0},\boldsymbol{I})$                                                                                                                                                                                                                                                                                                                                                                        | 随机采样                                                           |
| DDPM             | $x_t=\sqrt{\alpha_t}x_{t-1}+\sqrt{1-\alpha_t}z'_t,z'_t\sim N(0,I)$               | 同上                                | $\boldsymbol{x}_{t-1}\vert x_t,x_0=\frac{1}{\sqrt{\alpha_t}}\left(\boldsymbol{x}_t-\frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}\boldsymbol{\epsilon}_\theta(x_t,t)\right)+\sigma_t\boldsymbol{z},\boldsymbol{z}\sim\mathcal{N}(\boldsymbol{0},\boldsymbol{I})$<br />用固定方差$\sigma^2_t\boldsymbol{I}$代替$\boldsymbol \Sigma_\theta\left(x_t, t\right)$，取$\sigma_t=\tilde b'_t,b'_t$的实验结果接近。 $\tilde{b}'_t:=\frac{b_{t-1}}{b_t} b'_t\approx b'_t$。                                                                                                                                                                               | 同上                                                               |
| GLIDE            | 同上                                                                               | 同上                                | 用网络预测可学习方差$\boldsymbol \Sigma_\theta\left(x_t, t\right)$                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 同上                                                               |
| **DDIM类** | $x_t\vert x_0=a_t x_{0}+b_tz_t, z_t\sim N(0,I)$                                  | 否                                  | $\boldsymbol x_{t-\Delta t}\vert x_t,x_0=\dfrac{a_{t-\Delta t}}{a_t}\left(\boldsymbol x_t-b_t\boldsymbol\epsilon_\theta\left(x_t, t\right)\right)+\sqrt{b^2_{t-\Delta t}-\sigma_t^2} \boldsymbol\epsilon_\theta\left(x_t, t\right)+\sigma_t \boldsymbol z, \boldsymbol z\sim N(0,I)$即<br />$x_{t-\Delta t}\vert x_t,x_0=\frac{\sqrt{\bar\alpha_{t-\Delta t}}}{\sqrt{\bar\alpha_t}}(x_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta(x_t,t))+\sqrt{{1-\bar\alpha_{t-\Delta t}-\sigma^2_t}}\epsilon_\theta(x_t,t)+\sigma_t z,z\sim N(0,I)$ <br />- **DDIM**取$\sigma^2_t=0$，采样是确定过程<br />- DDPM取$\sigma^2_t=\tilde b'_t$，采样是随机过程 | 随机/确定采样                                                      |
| DDIM             | $x_t\vert x_0=\sqrt{\bar\alpha_t}x_{0}+\sqrt{1-\bar\alpha_t} z_t,z_t\sim N(0,I)$ | 否                                  | $x_\tau=\frac{a_\tau}{a_t}x_t-(\frac{a_\tau}{a_t}b_t-b_\tau)\epsilon_\theta(x_t,t)$即<br />$x_\tau=\frac{\sqrt{\bar\alpha_{\tau}}}{\sqrt{\bar\alpha_t}}(x_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta(x_t,t))+\sqrt{{1-\bar\alpha_{\tau}}}\epsilon_\theta(x_t,t)$                                                                                                                                                                                                                                                                                                                                                                                       | 确定采样                                                           |
| DPM-Solver       | 同上                                                                               | 同上                                | DPM-Solver-k:<br />$x_t=\frac{a_t}{b_s}x_s-b_t\sum^{k-1}_{n=0}\frac{\dd{}^n\hat\epsilon_\theta（x_{\lambda_s},\lambda_s)}{\dd \lambda^n} \Phi_{n+1}(h), 误差O(h^{k+1})\\$<br />$\Phi_k(h)=e^h-\sum_{i=1}^{n-1}\frac{h^i}{i!}=\sum_{i=n}^{\infty}\frac{h^i}{i!}$<br />用中间点去数值计算$\frac{\dd{}^n\hat\epsilon_\theta（x_{\lambda_s},\lambda_s)}{\dd\lambda^n}$，并巧设中间点的位置来避免数值计算高阶导<br />通常只用DPM-Solver-1～3<br />DPM-Solver-1即DDIM                                                                                                                                                                                    | 同上                                                               |
| PNDM             | 同上                                                                               | 同上                                | $\begin{array}{l}e_t:=\epsilon_\theta\left(x_t, t\right) \\ \hat e_t=\frac{1}{24}\left(55 e_t-59 e_{t-\Delta t}+37 e_{t-2 \Delta t}-9 e_{t-3 \Delta t}\right) \\ x_{t-\Delta t}=\frac{\sqrt{\bar{\alpha}_{t-\Delta t}}}{\sqrt{\bar{\alpha}_{\mathrm{t}}}}\left(x_t-\sqrt{1-\bar{\alpha}_t} \hat e_t\right)+\sqrt{1-\bar{\alpha}_{t-\Delta t}} \hat e_t\end{array}$                                                                                                                                                                                                                                                                                   | 同上                                                               |

# 论文和代码

## 采样算法加速

- DDPM：Diffusion的基础，推推公式
  - 论文：[Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)
  - 代码：tf version: **https://github.com/hojonathanho/diffusion** | pytorch version: **https://github.com/lucidrains/denoising-diffusion-pytorch**
- DDIM：对DDPM的改进
  - 论文：[Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502)
  - 代码：**https://github.com/ermongroup/ddim**
- PNDM/PLMS：对 DDIM 的数值算法改进
  - 论文：[Pseudo Numerical Methods for Diffusion Models on Manifolds](https://arxiv.org/pdf/2202.09778.pdf)
  - 代码：**https://github.com/luping-liu/PNDM**

* DPM-Solver：

  * 论文：

    * [DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps](https://arxiv.org/abs/2206.00927)
    * [DPM-Solver++: Fast Solver for Guided Sampling of Diffusion Probabilistic Models](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2211.01095)
  * 项目开源代码：[https://github.com/LuChengTHU/dpm-solver](https://link.zhihu.com/?target=https%3A//github.com/LuChengTHU/dpm-solver)
  * 项目在线 Demo：[https://huggingface.co/spaces/LuChengTHU/dpmsolver_sdm](https://link.zhihu.com/?target=https%3A//huggingface.co/spaces/LuChengTHU/dpmsolver_sdm)

## 硬件加速

* NVIDIA 写的论文似乎主要是卖显卡的，但我觉得是大资本产阶级派来劝退的。[Elucidating the Design Space of Diffusion-Based Generative Models](https://arxiv.org/abs/2206.00364)
* 为了加速扩散模型的采样，许多研究者从硬件优化的角度出发，例如 Google 使用 JAX 语言将模型编译运行在 TPU 上，中国的OneFlow （一流）团队使用自研编译器将 Stable Diffusion 做到了“一秒出图”。这些方法都基于 50 步的采样算法 PNDM[2]，该算法在步数减少时采样效果会急剧下降。OneFlow 版本的 Stable-Diffusion：[https://github.com/Oneflow-Inc/diffusers/wiki/How-to-Run-OneFlow-Stable-Diffusion](https://link.zhihu.com/?target=https%3A//github.com/Oneflow-Inc/diffusers/wiki/How-to-Run-OneFlow-Stable-Diffusion)

# DDPM推公式

采样：

$$
\boldsymbol{x}_{t-1}=\frac{1}{\sqrt{\alpha_t}}\left(\boldsymbol{x}_t-\frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}\boldsymbol{\epsilon}_\theta(x_t,t)\right)+\sigma_t\boldsymbol{z},\boldsymbol{z}\sim\mathcal{N}(\boldsymbol{0},\boldsymbol{I})
$$

$\sigma_t$有两种取值方案

$$
标准：\sigma_t=\sqrt{\tilde{\beta}_t}:=\sqrt{\frac{1-\bar{\alpha}_{t-1}}{1-\bar{\alpha}_t}\beta_t}\\
近似：\sigma_t=\sqrt{\beta_t}
$$

二者差别不大。

在DDPM的原论文中，$\beta_t$的取值设定是，将$\beta_1= 10^{−4}$ 到$\beta_T = 0.02$线性等分。$T=1000$。近似是

$$
\beta_t=\frac{0.02t}{T}
$$

## 三种推导DDPM的方式

### 逐步生成：最小二乘，预测单步噪声$z_t$ (从$x_{t-1}$到$x_t$)

* 参考：[苏剑林：生成扩散模型漫谈（一）：DDPM = 拆楼 + 建楼](https://kexue.fm/archives/9119)

> 思想：分步噪声$z_t$如砖块，最终生成结果$x_0$如楼房。拆楼要一块块拆，建楼需要逆过来一块块加砖。因此，需要用网络，基于半成品楼，预测拆楼时这一步所拆掉的砖，用它去重建楼。

目标1：用$\mu_\theta(x_t,t)$预测$x_{t-1}$，损失函数为$\mathbb{E}_{x_t,x_{t-1}}\Vert \mu_\theta(x_t,t) -x_{t-1}\Vert^2$

> **参数化｜只预测增量｜方便拟合**：由于$x_{t-1}=\dfrac{x_t-b'_t z'_t}{a'_t}$，故仿照它搞参数化，$ \mu_\theta(x_t,t)=\dfrac{x_t-b'_t\epsilon'_\theta(x_t,t)}{a'_t}$。利用$f(x)=x+\epsilon'(x)$或其他更精确的参数化关系，网络只预测从输入$x$到输出$f(x)$的增量$\epsilon'(x)$，能够让网络更容易拟合，这和ResNet、UNet的思想一致。

目标2：用$\epsilon'_\theta(x_t,t)$预测单步噪声$z'_t$，损失函数变为$\dfrac{{b'_t}^2}{{a'_t}^2} \mathbb{E}_{x_t,z'_t}\Vert \epsilon'_\theta(x_t,t)-z'_t \Vert^2$

> 由于$x_t=a_tx_0+b_tz_t$，但$z_t$和$z'_t$不独立，无法将$z'_t$期望再从式中消去，需要$z_t,z'_t$分别都进行采样，成本太高。
>
> 故重新表示$x_t=a_tx_0+a_t z_t=a'_t (a_{t-1}x_0+z_{t-1})+z'_t, x_{t-1}$, 则$\mathbb{E}_{x_t,z'_t}$变为$\mathbb{E}_{x_{t-1},z'_t}$再变为$\mathbb{E}_{z_{t-1},z'_t}$。因此，损失函数变为$\dfrac{{b'_t}^2}{{a’_t}^2}\mathbb{E}_{z_{t-1},z'_t} \Vert \epsilon'_\theta(x_t(z_{t-1},z'_t),t)-z'_t \Vert^2$。
>
> 由于$z_{t-1},z'_t$都嵌套在$\epsilon'_\theta$函数中，无法求期望时消去。由于$b_t z_t=b'_tz'_t+a'_{t}b_{t-1}z_{t-1}$，$b^2_t={b'_t}^2+{a'_t}^2b_{t-1}^2$，$z'_t,z_{t-1}$独立同分布，因而，可以构造$b_t w=a_tb_{t-1}z'_t-b'_tz_{t-1}$。用$z'_t,z_{t-1}$表示$z_t,w$：
>
> $$
> _t z_t=b'_tz'_t+a'_{t}b_{t-1}z_{t-1}\\
> b_t w=a_tb_{t-1}z'_t-b'_tz_{t-1}
> $$
>
> 可以得到以下性质：$\mathbb{E}(ww^\top)=I, \mathbb{E}(z_tw^\top)=0$, 因此$w,z_t\stackrel{i.i.d}{\sim} N(0,I)$.
>
> 此时，可以用$z_t,w$表示$z'_t,z_{t-1}$：
>
> $$
> _t z'_t=b'_t z_t+a'_t b_{t-1}w\\
> b_t z_{t-1}=a'_t b_{t-1} z_t-b'_t w
> $$
>
> 因此，损失函数变为$\dfrac{{b'_t}^2}{{a’_t}^2}\mathbb{E}_{z_{t},w} \Vert \epsilon'_\theta(a_{t}x_0+b_{t}z_{t},t)-\frac{1}{b_t}(b'_t z_t+a'_t b_{t-1}w)\Vert^2$
>
> 由于此式中$w$不在$\epsilon'_\theta$函数中，仅为二次函数，故可求期望时消去。于是，损失函数变为 $\dfrac{{b'_t}^2}{{a’_t}^2}\mathbb{E}_{z_{t-1}} \Vert \epsilon'_\theta(a_{t}x_0+b_{t}z_{t},t)-\frac{b'_t}{b_t}z_t \Vert^2$。
>
> 化简后，最终的损失函数为
>
> $$
> dfrac{{b'_t}^4}{{a’_t}^2b_t^2}\mathbb{E}_{z_{t-1}} \Vert \frac{b_t}{b'_t}\epsilon'_\theta(a_{t}x_0+b_{t}z_{t},t)-z_t \Vert^2\label{ddpm-loss-1}
> $$
>
> 实验证明，去掉$\dfrac{{b'_t}^4}{{a’_t}^2b_t^2}$后，表现更好，因而不再带它。

目标3：用$\epsilon_\theta(x_t(z_{t-1})$预测直达噪声$z_t$，损失函数为$\mathbb{E}_{z_{t-1}} \Vert \epsilon_\theta(a_{t}x_0+b_{t}z_{t},t)-z_t \Vert^2$

> 式$\eqref{ddpm-loss-1}$显示，**原本用网络$\epsilon'_\theta(x_t,t)$预测单步噪声$z'_t$，竟等价于用$\frac{b_t}{b'_t}\epsilon'_\theta(x_t,t)$预测直达噪声$z_t$。**
>
> 故不妨直接用网络$\epsilon_\theta(x_t,t)$去预测直达噪声$z_t$。等价关系为
>
> $$
> frac{预测z'_t}{预测z_t}=\frac{\epsilon'_\theta(x_t,t)}{\epsilon_\theta(x_t,t)}=\frac{b'_t}{b_t}
> $$
>
> 由于$b'_t<b_t$，故$\epsilon'_\theta(x_t,t)$比$\epsilon_\theta(x_t,t)$小，也即预测**单步**噪声**同向于且小于**预测**直达**噪声。可以用网络**预测直达噪声后，将直达噪声乘上$\frac{b'_t}{b_t}$缩小后，用以从$x_t$还原$x_{t-1}$**（确切当说，是还原上文所说的$\mu_\theta(x_t,t)$)，即
>
> $$
> mu_\theta(x_t,t)=\frac{1}{a'_t}(x_t-b'_t\epsilon'_\theta(x_t,t))\\
> =\frac{1}{a'_t}(x_t-\frac{{b'}_t^2}{b_t}\epsilon_\theta(x_t,t))
> $$
>
> 然后加上随机项
>
> $$
> _{t-1}=\mu_\theta(x_t,t)+\Sigma_t z,z\sim N(0,I)
> $$

方差$\Sigma_t$怎么取 (详见[方差的两种取值](https://kexue.fm/archives/9164#遗留问题))

* 假设训练集只有一个样本$x_*$，即$q_0(x_0)=\delta(x_0-x_*)$，可以推出$\Sigma_t=\sigma_t^2I, \sigma_t=\dfrac{b_{t-1}}{b_t}b'_t$；
* 假设训练集分布服从标准正态分布，即$q_0(x_0)=N(x_0|0,I)$，可以推出$\Sigma_t=\sigma_t^2I, \sigma_t=b'_t$；

预估-修正思想：解答如下两个疑问 (参考[预估修正](https://kexue.fm/archives/9164#预估修正))

* 为什么不直接用预测直达噪声$\epsilon_\theta(x_t,t)$去重建$x_0$，而是用它重建$x_{t-1}$
* 为什么预测**单步**噪声**同向于且小于**预测**直达**噪声

> **预估-修正**思想：**从模糊的半成品开始，无法一步到位变成品，只能给一个前瞻性的预估增量，朝着这个方向推进一小步**。如此迭代许多步骤，得到精细的成品。
>
> 好比画画、雕刻的途中，看到半成品($x_t$)，创作者只能知道大概还差多少增量(预测$z_t$)能变为成品，由于这个增量是模糊的，若把此增量原封不动画上去/凿下来，就只能得到一个模糊的假“成品”，而非精致的真成品。因此，**只能朝着这个大概增量的方向打些折扣地画/凿，以便之后再一步步细化调整**。
>
> 由此我们还可以联想到Hinton三年前提出的[《Lookahead Optimizer: k steps forward, 1 step back》](https://arxiv.org/abs/1907.08610)，它同样也包含了预估（k steps forward）和修正（1 step back）两部分，原论文将其诠释为“快（Fast）-慢（Slow）”权重的相互结合，快权重就是预估得到的结果，慢权重则是基于预估所做的修正结果。如果愿意，我们也可以用同样的方式去诠释DDPM的“预估-修正”过程。

### 多步VAE：KL散度，预测单步噪声$z_t$ (从$x_{t-1}$到$x_t$)

* 参考：[生成扩散模型漫谈（二）：DDPM = 自回归式VAE](https://kexue.fm/archives/9152)

### 贝叶斯：推导$q\left(\boldsymbol{x}_{t-1} \mid \boldsymbol{x}_t, \boldsymbol{x}_0\right)$以近似 $q\left(\boldsymbol{x}_{t-1} \mid \boldsymbol{x}_t\right)$，预测“直达”噪声$\bar{z}_t$ (从$x_{0}$到$x_t$)

* 参考：[苏剑林：生成扩散模型漫谈（三）：DDPM = 贝叶斯 + 去噪](https://kexue.fm/archives/9164)，原论文推导方法

DDPM原论文的推导过程可以总结成如下步骤

$$
q\left(\boldsymbol{x}_t \mid \boldsymbol{x}_{t-1}\right)
\xrightarrow[重参数化]{\text { 推导 }} q\left(\boldsymbol{x}_t \mid \boldsymbol{x}_0\right) \xrightarrow[贝叶斯]{\text { 推导 }}
q\left(\boldsymbol{x}_{t-1} \mid \boldsymbol{x}_t, \boldsymbol{x}_0\right)
\xrightarrow[用\frac{x_t-b_t\epsilon_\theta(x_t,t)}{a_t}替代x_0]{\text { 近似 }} q\left(\boldsymbol{x}_{t-1} \mid \boldsymbol{x}_t\right)\label{ddpm-framework}
$$

损失函数只依赖于$q\left(\boldsymbol{x}_t \mid \boldsymbol{x}_0\right)$，采样过程只依赖于$q\left(\boldsymbol{x}_{t-1} \mid \boldsymbol{x}_t\right)$。

$$
\begin{align}
q(x_t|x_{t-1}):& x_t=a'_t x_{t-1}+b'_t z'_t, z'_t\sim N(0,I)\\
q(x_t|x_0):&x_t=a_t x_0+b_t z_t, z_t\sim N(0,I)\\
q(x_{t-1}|x_{t},x_0):&x_{t-1}=a'_t\frac{b_{t-1}^2}{b_t^2}x_t+a_{t-1}\frac{{b'_t}^2}{b_t^2}x_0+\dfrac{b_{t-1}}{b_t}b'_t z, z\sim N(0,I)\\
q(x_{t-1}|x_t):&x_{t-1}=\dfrac{1}{a'_t}\big( x_t - \frac{{b'_t}^2}{b_t}\epsilon_\theta(x_t,t)\big)+\dfrac{b_{t-1}}{b_t}b'_t z, z\sim N(0,I)
\end{align}
$$

#### 重参数化

由于$q(x_t|x_{t-1})$重参数化为

$$
x_t=a'_t x_{t-1}+b'_t z'_t, z'_t\sim N(0,I)
$$

迭代起来，由于$z'_1,z'_2,\cdots,z'_t$ iid，故可以合成成一个高斯分布，故得到

$$
\begin{align}
x_t&=a'_t(a'_{t-1}x_{t-2}+b'_{t-1}z'_{t-1})+b'_t z'_t\\
&=a'_ta'_{t-1}x_{t-2}+a'_tb'_{t-1}z'_{t-1}+b'_tz'_t\\
&=a'_ta'_{t-1}x_{t-2}+b_{t|t-2}z_{t|t-2},z_{t|t-2}\sim N(0,I)\\
&\cdots\\
&=a'_ta'_{t-1}\cdots a'_1 x_0+b_{t|0}z_{t|0},z_{t|0}\sim N(0,I)
\end{align}
$$

其中，记$a_t=a'_ta'_{t-1}\cdots a'_1, b_t=b_{t|0}$。故$q(x_t|x_0)=N(x_t|a_t x_0,b_t^2 I)$。

#### 使用贝叶斯公式

$$
q(x_{t-1}|x_t,x_0)=\frac{q(x_{t-1},x_t,x_0)}{q(x_t,x_0)}=\frac{q(x_t|x_{t-1})q(x_{t-1}|x_0)q(x_0)}{q(x_t|x_0)q(x_0)}=\frac{q(x_t|x_{t-1})q(x_{t-1}|x_0)}{q(x_t|x_0)}\\
=C_1 \exp\frac{-1}{2}\big[ \frac{1}{{b'_t }^2}\Vert x_t-a'_t x_{t-1} \Vert^2+\frac{1}{{b_{t-1} }^2}\Vert x_{t-1}-a_{t-1} x_{0} \Vert^2-\frac{1}{{b_t }^2}\Vert x_t-a_t x_{0} \Vert^2\big]\\
=C_1 \exp\frac{-1}{2}\big[ (\frac{{a'_t}^2}{{b'_t}^2}+\frac{1}{b_{t-1}^2})x_{t-1}^2 -2(\frac{a'_t x_{t}}{{b'_t}^2}+\frac{a_{t-1} x_0}{b^2_{t-1}})x_{t-1}+C_2\big]
$$

故$q(x_{t-1}|x_t,x_0)=N(x_{t-1}|\mu_t(x_t,x_0),\sigma_t^2 I)$。 它使用的性质是，各向同性的高斯分布相互乘除后仍是各向同性的高斯分布。

其中两个参数推导如下，

$$
\sigma_t^2 =(\frac{{a'_t}^2}{{b'_t}^2}+\frac{1}{b_{t-1}^2})^{-1}=(\frac{{a'_t}^2b_{t-1}^2+{b'_t}^2}{b_{t-1}^2{b'_t}^2})^{-1}=(\frac{b_t^2}{b_{t-1}^2{b'_t}^2})^{-1}=(\frac{b_{t-1}}{b_t} b'_t)^2={\tilde b'_t}^2\\
即\sigma_t=\dfrac{b_{t-1}}{b_t}b'_t \xlongequal{记作}\tilde b'_t
$$

$$
\mu_t(x_t,x_0)=\sigma_t^2(\frac{a'_t x_{t}}{{b'_t}^2}+\frac{a_{t-1} x_0}{b^2_{t-1}})=a'_t\frac{b_{t-1}^2}{b_t^2}x_t+a_{t-1}\frac{{b'_t}^2}{b_t^2}x_0
$$

重参数化为

$$
x_{t-1}=a'_t\frac{b_{t-1}^2}{b_t^2}x_t+a_{t-1}\frac{{b'_t}^2}{b_t^2}x_0+\dfrac{b_{t-1}}{b_t}b'_t z, z\sim N(0,I)\label{qxt-1-xt-x0}
$$

#### 近似消去$x_0$

此时，还有一个困难，即从$x_t$去采样$x_{t-1}$时，**$q(x_{t-1}|x_t,x_0)$中的$x_0$未知，需要用$x_t$预测$x_0$**。

具体做法是，使用网络$\epsilon_\theta(x_t,t)$去预测$z_t$，并用参数化$x_t=a_t x_0+b_t z_t$，来还原$x_0$:

$$
x_0=\frac{x_t-b_t\epsilon_\theta(x_t,t)}{a_t}
$$

将其带回前一式得，$\mu_t(x_t,x_0)=\dfrac{1}{a'_t}\big( x_t - \dfrac{{b'_t}^2}{b_t}\epsilon_\theta(x_t,t)\big)$

$$
\begin{align}
\mu_t(x_t,x_0)&= a'_t\frac{b_{t-1}^2}{b_t^2}x_t+a_{t-1}\frac{{b'_t}^2}{b_t^2}\frac{x_t-b_t\epsilon_\theta(x_t,t)}{a_t}\\
&=\frac{1}{b_t^2}(a'_t b^2_{t-1}+\frac{a_{t-1}}{a_t}{b'_t}^2)x_t -\frac{a_{t-1}}{a_t}\frac{{b'_t}^2}{b_t}\epsilon_\theta(x_t,t)\\
&=\frac{1}{b_t^2}(a'_t b^2_{t-1}+\frac{1}{a'_t}{b'_t}^2)x_t -\frac{1}{a'_t}\frac{{b'_t}^2}{b_t}\epsilon_\theta(x_t,t)\\
&=\frac{1}{a'_tb_t^2 }({a'_t}^2 b^2_{t-1}+{b'_t}^2)x_t -\frac{1}{a'_t}\frac{{b'_t}^2}{b_t}\epsilon_\theta(x_t,t)\\
&=\frac{1}{a'_t b_t^2}b_t^2 x_t -\frac{1}{a'_t}\frac{{b'_t}^2}{b_t}\epsilon_\theta(x_t,t)\\
&=\frac{1}{a'_t }\big( x_t - \frac{{b'_t}^2}{b_t}\epsilon_\theta(x_t,t)\big)\\
\end{align}
$$

综上，$q(x_{t-1}|x_t,x_0)$近似为$q(x_{t-1}|x_t)$：

$$
q(x_{t-1}|x_t)=N(x_{t-1}|\dfrac{1}{a'_t}\big( x_t - \frac{{b'_t}^2}{b_t}\epsilon_\theta(x_t,t)\big),(\dfrac{b_{t-1}}{b_t}b'_t )^2)
$$

重参数化为

$$
x_{t-1}=\dfrac{1}{a'_t}\big( x_t - \frac{{b'_t}^2}{b_t}\epsilon_\theta(x_t,t)\big)+\dfrac{b_{t-1}}{b_t}b'_t z, z\sim N(0,I)
$$

## 有关资料

* [由浅入深了解Diffusion Model](https://zhuanlan.zhihu.com/p/525106459)
* [生成模型(四):扩散模型](https://zhuanlan.zhihu.com/p/499206074)
* 翁丽莲：[What are Diffusion Models?](https://link.zhihu.com/?target=https%3A//lilianweng.github.io/posts/2021-07-11-diffusion-models/)
* 宋飏： [Generative Modeling by Estimating Gradients of the Data Distribution](https://link.zhihu.com/?target=https%3A//yang-song.github.io/blog/2021/score/)
* 对Diffusion的Bayesian诠释：Understanding Diffusion Models: A Unified Perspective](https://arxiv.org/abs/2208.11970)

用公式解读代码：

* [AIGC爆火的背后——扩散模型DDPM浅析](https://zhuanlan.zhihu.com/p/590840909)
* [一文弄懂 Diffusion Model](https://zhuanlan.zhihu.com/p/586936791)

# DDIM

苏剑林：[生成扩散模型漫谈（四）：DDIM = 高观点DDPM](https://kexue.fm/archives/9181)

DDIM的思路：既然DDPM的推导流程（$\eqref{ddpm-framework}$）中，损失函数、采样过程都跟$q\left(\boldsymbol{x}_t \mid \boldsymbol{x}_{t-1}\right)$无关，那不如干脆“过河拆桥”，将$q\left(\boldsymbol{x}_t \mid \boldsymbol{x}_{t-1}\right)$从整个推导过程中去掉，从$q(\boldsymbol x_{t-1}|\boldsymbol x_0)$开始，这样$q(\boldsymbol x_{t-1}|\boldsymbol x_t,\boldsymbol x_0)$有很多种选择，**不要求$q(x_t|x_{t-1})$像DDPM那样满足马尔可夫性。**

设$\tau=t-\Delta t$，在DDPM中$\Delta t=1$，而下面推导DDIM则无需$\Delta t=1$。

人为规定$q(\boldsymbol x_{\tau}|\boldsymbol x_t,\boldsymbol x_0)$为一个高斯分布（因为在DDPM推导中证明过了，各向同性的高斯分布相互乘除后仍是各向同性的高斯分布），

$$
q\left(\boldsymbol{x}_{\tau} \mid \boldsymbol{x}_t, \boldsymbol{x}_0\right)=\mathcal{N}\left(\boldsymbol{x}_{\tau} ; \kappa_t \boldsymbol{x}_t+\lambda_t \boldsymbol{x}_0, \sigma_t^2 \boldsymbol{I}\right)
$$

使其满足边缘分布$q(\boldsymbol x_{\tau}|\boldsymbol x_0)$和DDPM中的一样即可，

$$
\int q\left(\boldsymbol{x}_{\tau} \mid \boldsymbol{x}_t, \boldsymbol{x}_0\right) q\left(\boldsymbol{x}_t \mid \boldsymbol{x}_0\right) d x_t=q\left(\boldsymbol{x}_{\tau} \mid \boldsymbol{x}_0\right)=\mathcal{N}(\boldsymbol x_{t-1}|a_{\tau}\boldsymbol x_{\tau},b_{\tau}^2I)
$$

### 求解参数

由重参数化表示

$$
\begin{align}
x_{\tau}&=a_{\tau}x_0+b_{\tau}z_{t\tau}\\
x_t&=a_tx_0+b_tz_t\\
&将上两式带入下式\\
x_{\tau}&=\kappa_t x_t+\lambda_tx_0+\sigma_t z
\end{align}
$$

得到

$$
a_{\tau}=\kappa_t a_t+\lambda_t \\
b_{\tau}^2=\sigma_t^2+\kappa_t^2 b^2
$$

两个方程，求解$\kappa_t,\lambda_t,\sigma_t$三个变量，解有无穷个，可见$q(\boldsymbol x_{t-1}|\boldsymbol x_t,\boldsymbol x_0)$有很多种选择。故先将$\sigma_t$当作待定参数，去求余下两个变量。

$$
\kappa_t=\frac{\sqrt{b^2_{\tau}-\sigma_t^2}}{b_t}\\
\lambda_t=a_{\tau}-a_t\kappa_t
$$

故得到**$q(x_\tau|x_t,x_0)$重参数化**表示为

$$
x_\tau=\kappa_t x_t+(a_\tau-a_t \kappa_t)x_0+\sigma_t z, z\sim N(0,I)\\
\kappa_t=\frac{\sqrt{b^2_{\tau}-\sigma_t^2}}{b_t} \label{ddim-repara}
$$

* 当$\sigma_t=0$，为DDIM，上式变为

  $$
  x_\tau=\frac{b_\tau}{b_t}x_t+(a_\tau-a_t \frac{b_\tau}{b_t})x_0
  $$
* 当$\sigma_t=\tilde b'_t$，$\tau=t-1$，为DDPM，上式变为$\eqref{qxt-1-xt-x0}$，即

  $$
  x_{t-1}=a'_t\frac{b_{t-1}^2}{b_t^2}x_t+a_{t-1}\frac{{b'_t}^2}{b_t^2}x_0+\dfrac{b_{t-1}}{b_t}b'_t z, z\sim N(0,I)
  $$

### 近似消去$x_0$

**要将$q(x_\tau|x_t,x_0)$近似为$q(x_\tau|x_t)$，**需要从$x_t$粗糙预测$x_0$，使用重参数化$x_t=a_t x_0+b_t z_t$，$\epsilon_\theta(x_t,t)$预测$z_t$，故

$$
\mu_t(x_t,x_0)=\frac{1}{a_t}(x_t-b_t\epsilon_\theta(x_t,t))
$$

用它替代$x_0$，则得到DDIM问题的普遍解：

$$
\begin{align}
x_\tau &=\kappa_t x_t +(a_\tau-a_t\kappa_t)\frac{1}{a_t}(x_t-b_t\epsilon_\theta(x_t,t))+\sigma_t z_t\\
&=\frac{a_\tau}{a_t}x_t-(\frac{a_\tau}{a_t}b_t-b_t\kappa_t)\epsilon_\theta(x_t,t)+\sigma_t z\\
&=\frac{a_\tau}{a_t}x_t-(\frac{a_\tau}{a_t}b_t-\sqrt{b^2_\tau-\sigma_t^2})\epsilon_\theta(x_t,t)+\sigma_t z\label{ddim-general}
\end{align}
$$

在DDIM原论文中，表示为

$$
x_\tau=\frac{\sqrt{\bar\alpha_{\tau}}}{\sqrt{\bar\alpha_t}}(x_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta(x_t,t))+\sqrt{{1-\bar\alpha_{\tau}-\sigma_t^2}}\epsilon_\theta(x_t,t)+\sigma_t z,z\sim N(0,I)
$$

* 当$\sigma_t=0$，即为DDIM，$q(x_t|x_{t-1})$不满足马尔可夫性，式$\eqref{ddim-general}$变为

  $$
  x_\tau=\frac{a_\tau}{a_t}x_t-(\frac{a_\tau}{a_t}b_t-b_\tau)\epsilon_\theta(x_t,t) \label{ddim}
  $$

  在DDIM原论文中，表示为

  $$
  x_\tau=\frac{\sqrt{\bar\alpha_{\tau}}}{\sqrt{\bar\alpha_t}}(x_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta(x_t,t))+\sqrt{{1-\bar\alpha_{\tau}}}\epsilon_\theta(x_t,t)
  $$

  * 若又$\tau=t-1$，则

  $$
  x_{t-1}=\frac{1}{a'_t}x_t-(\frac{b_{t}}{a'_t}-b_{t-1})\epsilon_\theta(x_t,t)
  $$
* 当$\sigma_t=\tilde b_{t|\tau}:=\dfrac{b_\tau}{b_t}b_{t|\tau}$，为DDPM跳步采样，$q(x_t|x_{t-1})$满足马尔可夫性，式$\eqref{ddim-general}$变为

  $$
  x_\tau=\frac{a_\tau}{a_t} x_t-\frac{b_{t|\tau}^2}{b_t}\epsilon_\theta(x_t,t)+\frac{b_\tau}{b_t}b_{t|\tau}z,z\sim N(0,I)
  $$

  * 若又$\tau=t-1$，即DDPM（默认是半步采样），
    $$
    x_{t-1}=\frac{1}{a'_t} x_t-\frac{{b'_t}^2}{b_t}\epsilon_\theta(x_t,t)+\frac{b_{t-1}}{b_t}b'_t z,z\sim N(0,I)
    $$

**参考资料**：加速Diffusion采样和方差的选择(DDIM) https://zhuanlan.zhihu.com/p/525106459

扩散模型之DDIM https://zhuanlan.zhihu.com/p/565698027

DDIM的改进：

- 加速：DDIM和DDPM有相同的训练目标，但是它不再限制扩散过程必须是一个马尔卡夫链，这使得DDIM可以采用更小的采样步数来加速生成过程
- 确定：DDIM的另外是一个特点是从一个随机噪音生成样本的过程是一个确定的过程，中间没有加入随机噪音

详见：扩散模型之DDIM https://zhuanlan.zhihu.com/p/565698027

# 扩散模型与微分方程

## 为什么DDIM能比DDPM节省采样步数？

为什么DDIM能比DDPM省采样步数？
DDPM反向扩散每步都有噪声，可以转化成SDE（随机微分方程 )，只能用小步长从 $x_{\mathrm{T}}$ 去数值计算 $\mathrm{x}_0$ ，不然求得的 $\mathrm{x}_0$ 误差很大，即生成的图像 $\left(\mathrm{x}_0\right)$ 效果很差。
DDIM反向扩散每步都是确定的，可以转化成ODE ( 常微分方程 ) ，可以用较大的步长从 $\mathrm{x}_{\mathrm{T}}$ 去数值计算 $\mathrm{x}_0$ ，仍得到较准确的 $\mathrm{x}_0$ ，即生成的图像 $\left(\mathrm{x}_0\right)$ 效果还好。

## DDPM的前向传播 ( 加噪 )

在DDPM的原论文中，$\beta_t$的取值设定是，将$\beta_1= 10^{−4}$ 到$\beta_T = 0.02$线性等分。因此，当$T\rightarrow +\infty$时，有$ \forall t\geq 0, \beta_t\ll 1$

$$
\begin{align}
x_t&=\sqrt{1-\beta_t} x_{t-1}+\sqrt{\beta_t} z, \quad z \sim N(\mathbf{0}, \mathbf{I}) \\
&\approx\left(1-\frac{1}{2} \beta_t \right) x_{t-1}+\sqrt{\beta_t } z，若T\rightarrow +\infty\\
&=(1-\beta_t \Delta \mathrm{t}) x_{t-\Delta \mathrm{t}}+\sqrt{\beta_t \Delta \mathrm{t}} z, \Delta t=1 \\
\Rightarrow \mathrm{d} x_t&=-\frac{1}{2} \beta_t x_t \mathrm{~d} t+\sqrt{\beta_t \mathrm{~d} t} z,若取\Delta t 为\dd t\\
&=-\frac{1}{2} \beta_t x_t \mathrm{~d} t+\sqrt{\beta_t}\dd \omega_t,\quad \dd\omega_t:=\sqrt{\mathrm{d} t}z\\
&\quad \quad \omega_t 是一个标准布朗运动（又名标准Wiener过程）, 满足\forall t,\Delta t, \omega_t\sim N(0,\Delta t \mathbf I) \\
\Leftrightarrow d x_t \vert x_t &\sim N\left(-\frac{1}{2} \beta_t x_t \mathrm{~d} t, \beta_t \mathrm{~d} t \mathbf{I}\right)
\end{align}
$$

 它是 DDPM的精确SDE方程（下式）的近似形式

$$
\dd {\boldsymbol x_t}=f_t\boldsymbol x_t\dd t+g_t\dd{\boldsymbol w_t}\\
f_t=\frac{\dd{\log a_t}}{\dd t}\\
g_t^2=-2b_t^2\frac{\dd{ \lambda_t}}{\dd{t}}
$$

这是一个随机微分方程 (SDE), 是马尔可夫过程，称作伊藤(Itô)过程或扩散过程。

DDPM采样不会跳步数，始终是步长为1。

详见：

【理论推导】随机微分方程(SDE)视角下的Diffusion Model与Score-based Model https://blog.csdn.net/fnoi2014xtx/article/details/129871986

## DDIM的反向传播（去噪）

DDIM采样会跳步数，即通常步长$\Delta t>1$

$$
\begin{align}
x_{\tau}&=\frac{a_\tau}{a_t}x_t-(\frac{a_\tau}{a_t}b_t-b_\tau)\epsilon_\theta(x_t,t),\tau=t-\Delta t \\
\Leftrightarrow \frac{x_{\tau}}{a_{\tau}}&=\frac{x_t}{a_t}+\left( \frac{b_{\tau}}{a_{\tau}}- \frac{b_t}{a_t}\right) \epsilon_\theta\left(x_t, t\right),\tau=t-\Delta t \\
\Leftrightarrow \frac{\dd }{\dd t}(\frac{x_t}{a_t})&=\epsilon_\theta(x_t,t)\frac{\dd  }{\dd t}(\frac{b_t}{a_t})
\end{align}
$$

这是一个常微分方程 (ODE) ，详见：扩散模型之DDIM https://zhuanlan.zhihu.com/p/565698027。

该ODE等价于

$$
\begin{align}
概率流ODE：\frac{\dd{\boldsymbol x}_t}{\dd t}&=f_t\boldsymbol x_t-\frac{1}{2}g^2_t\nabla_{\boldsymbol x_t}\log q_t(\boldsymbol x_t), \boldsymbol x_t是概率建模的对象\\
\Rightarrow DDIM采样过程ODE：\frac{\dd{\hat{\boldsymbol x}}_t}{\dd t} & = f_t \hat{\boldsymbol x}_t+\frac{g^2_t}{2b_t}\epsilon_\theta(\hat{\boldsymbol x}_t,t),\hat{\boldsymbol x}_t是采样得到的\\
f_t&=\frac{\dd{\log a_t}}{\dd t}\\
g_t^2&=-2b_t^2\frac{\dd{ \lambda_t}}{\dd{t}}
\end{align}
$$

DDIM的正向过程 ( 加噪 ) $q(x_t \mid x_0) =\mathcal{N}\left(x_t\mid \sqrt{\bar{\alpha}_t} x_0 ，\left(1-\bar{\alpha}_t\right) \mathbf{I}\right)$ 不是马尔可夫过程，且不会跳步数。

## 扩展阅读

[扩散模型与能量模型，Score-Matching和SDE，ODE的关系](https://zhuanlan.zhihu.com/p/576779879)

先修知识 Score-Based Generative Modeling through Stochastic Differential Equations  https://arxiv.org/abs/2011.13456

路橙：DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps https://arxiv.org/abs/2206.00927

# PNDM/PLMS

简介：[AIGC: PNDM (Pseudo Numerical Method for Diffusion Models) 笔记](https://www.bilibili.com/read/cv25507394/)

论文：[Pseudo Numerical Methods for Diffusion Models on Manifolds](https://arxiv.org/pdf/2202.09778.pdf)

在DDIM的设定下，使用线性多步法（Linear Multistep Method）去数值求解DDIM的ODE。

每步的采样公式是：

$$
\begin{array}{l}
e_t:=\epsilon_\theta\left(x_t, t\right) \\
\hat e_t=\frac{1}{24}\left(55 e_t-59 e_{t-\Delta t}+37 e_{t-2 \Delta t}-9 e_{t-3 \Delta t}\right) \\
x_{t-\Delta t}=\frac{\sqrt{\bar{\alpha}_{t-\Delta t}}}{\sqrt{\bar{\alpha}_{\mathrm{t}}}}\left(x_t-\sqrt{1-\bar{\alpha}_t} \hat e_t\right)+\sqrt{1-\bar{\alpha}_{t-\Delta t}} \hat e_t
\end{array}
$$

# DPM-Solver

一种**在DDIM的设定**下的高阶采样加速方法。DDIM是1阶的DPM-Solver。

简介：[Stable Diffusion采样速度翻倍！仅需10到25步的扩散模型采样算法](https://zhuanlan.zhihu.com/p/583367414)

论文：

* [DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps](https://arxiv.org/abs/2206.00927)
* [DPM-Solver++: Fast Solver for Guided Sampling of Diffusion Probabilistic Models](https://arxiv.org/abs/2211.01095)

项目开源代码：[https://github.com/LuChengTHU/dpm-solver](https://github.com/LuChengTHU/dpm-solver)

项目在线 Demo：[https://huggingface.co/spaces/LuChengTHU/dpmsolver_sdm](https://huggingface.co/spaces/LuChengTHU/dpmsolver_sdm)

## ODE形式

在DDIM的**Diffusion的反向传播（去噪），其ODE方程如下**

$$
\begin{align}
\frac{\dd x_t}{\dd t}=f(t)x_t+G(x_t,t)\label{ode} \\
G(t,x_t):=\frac{ g^2(t)}{2 b_t}\epsilon_\theta(x_t,t)\\
x_T\sim\mathcal{N}(0,I)\\
\end{align}
$$

* DDIM是对其的离散化。
* PNDM对上式直接求积分，

  $$
  x_t=x_s+\int_s^t\left(f(\tau)x_\tau+\frac{ g^2(\tau)}{2 b_\tau}\epsilon_\theta(x_\tau,\tau) \right)\dd \tau
  $$

  PDNDM把$\phi(x_t,\epsilon,t):=f(t)x_t+\frac{ g^2(\tau)}{2 b_\tau}\epsilon$看作一个整体黑盒，只利用了$\phi$关于$\epsilon$线性的性质，对$\epsilon$进行了更细致的估计；却没有利用ODE关于$x_t$的半线性结构去获得更精确的积分形式的解，因而在小于50步时难以收敛。
* DPM-Solver：利用ODE关于$x_t$的半线性结构去获得更精确的积分形式的解，以减少收敛所需步数

## 更精确的积分形式的解

上述ODE $\eqref{ode}$，更精确的积分形式的解为，

$$
\begin{align}
x_t&=e^{F|^\tau_s}x_s+\int_s^t e^{F|^t_\tau} G(x_\tau,\tau) \dd \tau \label{int}\\
F|^\tau_s&:=\int^\tau_s f(r)\dd r
\end{align}
$$

**证明：**

> 当$G=0$时，ODE蜕化为$\dfrac{\dd x}{\dd t}=fx$，解为$x_t=x_s e^{F|^t_s}$。
>
> 因此，为化简ODE$\eqref{ode}$，现在定义辅助变量$y_t:=e^{-F|^t_s}x_t$
>
> 则
>
> $$
> begin{align}
> \frac{\dd y_t}{\dd t} &= -e^{-F|^t_s}f(t)x_t+e^{-F|^t_s}\frac{\dd x_t}{\dd t}\\
> &= -e^{-F|^t_s}f(t)x_t+e^{-F|^t_s}{\left(f(t)x_t+G(x_t,t)\right)}\\
> &=e^{-F|^t_s}G(x_t,t)
> \end{align}
> $$
>
> 其积分形式的解为
>
> $$
> _t=y_s+\int_s^te^{-F|^\tau_s}G(x_\tau,\tau)\dd \tau
> $$
>
> 再带入$y_t$的定义，得
>
> $$
> ^{-F|^t_s}x_t=e^{-F|^s_s}x_s+\int_s^te^{-F|^\tau_s}G(x_\tau,\tau)\dd \tau
> $$
>
> 左右同乘$e^{F|^t_s}$即得
>
> $$
> _t=e^{F|^t_s}x_s+\int_s^te^{F|^t_\tau}G(x_\tau,\tau)\dd \tau. \ \ \ \  \square
> $$

## ODE的系数

**反传ODE的系数为**

$$
\begin{align}
f(t)&=\frac{\dd}{\dd t}\ln a_t\\
G(x_t,t)&=-b_t\frac{\dd \lambda_t}{\dd t} \epsilon_\theta(x_t,t)
\end{align}
$$

**证明：**

**DDIM的正传（加噪）公式为**

$$
x_t= a_t x_0+b_t z_t, z_t\sim \mathcal{N}(0,I)\label{forward}\\
$$

其中

* **信号强度**$=a^2_t=\bar\alpha_t$
* **噪声强度**$=b^2_t=1-\bar\alpha_t$
* **信噪比(signal-to-noise-ratio)**  $SNR:=\dfrac{ a_t^2}{b_t^2}=\dfrac{\bar\alpha_t}{1-\bar\alpha_t}$
* **半对数信噪比**  $\lambda_t:=\ln\dfrac{a_t}{b_t}=\dfrac{1}{2}\ln SNR=\dfrac{1}{2}\ln\dfrac{\bar\alpha_t}{1-\bar\alpha_t}$

> 将式$\eqref{forward}$其带入式$\eqref{ode}$，得到
>
> $$
> frac{\dd}{\dd t}(  a_t x_0+b_t z_t) = f(t)(  a_t x_0+b_t z_t)+G(x_t,t)
> $$
>
> 即
>
> $$
> frac{\dd{ a_t}}{\dd t}  x_0+ \frac{\dd{b_t}}{\dd t}  z_t = f(t) a_t x_0+(f(t)b_t z_t+G(x_t,t))
> $$
>
> 故
>
> $$
> begin{align}
> \frac{\dd{ a_t}}{\dd t}&=f(t) a_t \\
> \frac{\dd{b_t}}{\dd t}  z_t&=f(t)b_t z_t+G(x_t,t)
> \end{align}
> $$
>
> 故
>
> $$
> begin{align}
> f(t)&=\frac{\dd}{\dd t}\ln a_t\\
> G(x_t,t)&=(\frac{\dd}{\dd t} b_t-f(t)b_t)z_t=(\frac{\dd b_t}{\dd t} -b_t\frac{\dd}{\dd t}\ln a_t)z_t=-b_t\frac{\dd}{\dd t}\ln\frac{ a_t}{b_t} z_t=-b_t\frac{\dd \lambda_t}{\dd t} z_t\label{G}
> \end{align}
> $$
>
> 由于$\epsilon_\theta(x_t,t)$是对$z_t$的估计，故可带入式$\eqref{G}$，得到反传ODE的系数为
>
> $$
> begin{align}
> f(t)&=\frac{\dd}{\dd t}\ln a_t\\
> G(x_t,t)&=-b_t\frac{\dd \lambda_t}{\dd t} \epsilon_\theta(x_t,t)\ \ \ \ \square
> \end{align}
> $$

**使用此性质，则ODE的精确积分形式的解（式$\eqref{int}$化）为**

$$
x_t=\frac{ a_t}{ a_s}x_s- a_t\int^{\lambda_t}_{\lambda_s}  e^{-\lambda}\epsilon_\theta(x_\lambda,\lambda) \dd \lambda \label{solve-lambda}
$$

证明：

> $$
> |^t_s:=\int^t_s f(\tau)\dd \tau=\int^t_s \frac{\dd \ln a_\tau}{\dd \tau}\dd\tau=\ln\frac{ a_t}{ a_s}
> $$
>
> 故由式$\eqref{int}$得
>
> $$
> begin{align}
> x_t&=e^{F|^\tau_s}x_s+\int_s^t e^{F|^t_\tau} G(x_\tau,\tau) \dd \tau\\
> &=\frac{ a_t}{ a_s}x_s+\int^t_s \frac{ a_t}{ a_\tau}\cdot(-b_\tau\frac{\dd\lambda_\tau}{\dd\tau}\epsilon_\theta(x_\tau,\tau))\dd \tau\\
> &=\frac{ a_t}{ a_s}x_s- a_t \int^{\lambda_t}_{\lambda_s} \frac{b_\tau}{ a_\tau} \hat\epsilon_\theta(x_\lambda,\lambda)) \dd\lambda, 由于信噪比随t单调递增，故可t换元为\lambda, 换元后\epsilon记为\hat\epsilon\\
> &=\frac{ a_t}{ a_s}x_s- a_t \int^{\lambda_t}_{\lambda_s}  e^{-\lambda}\epsilon_\theta(x_\lambda,\lambda)) \dd\lambda \ \ \ \ \square
> \end{align}
> $$

## 对噪声的近似展开

在反向传播（降噪、采样）时，采样时间取为$T=t_0>t_1>t_2>...>t_{final}=0$（**时间递减**），相应的半对数信噪比$\lambda_0<\lambda_1<\lambda_2...$ （**噪声递减，信噪比递增**）。

设$t:=t_{i}, s:=t_{i-1}$，则反传（采样）迭代公式推导如下

知道$x_s$，用式$\eqref{solve-lambda}$去精确计算$x_{t}$，

$$
x_t=\frac{ a_t}{ a_s} x_s- a_t\int^{\lambda_{t}}_{\lambda_s}  e^{-\lambda}\hat\epsilon_\theta(x_\lambda,\lambda) \dd \lambda
$$

对$\hat\epsilon_\theta(x_\lambda,\lambda)$使用泰勒展开，其中$\hat\epsilon^{(n)}_\theta(x_{\lambda_{s}},\lambda_s)=\dfrac{\dd{}^n\hat\epsilon(x_\lambda,\lambda)}{\dd \lambda^n}\bigg|_{\lambda=\lambda_{s}}$

$$
\hat\epsilon_\theta(x_\lambda,\lambda)=\sum_{n=0}^{k-1}\frac{(\lambda-\lambda_s)^n}{n!}\hat\epsilon^{(n)}_\theta(x_{\lambda_s},\lambda_{s})+O((\lambda-\lambda_s)^{k})
$$

带入上式求积分，可得DPM-Solver的**k阶迭代公式**，$k$阶精度的算法，使用$k-1$阶导，误差为$k+1$阶：

$$
x_t=\frac{ a_t}{ a_s}x_s
- a_t

\sum_{n=0}^{k-1} \hat\epsilon^{(n)}_\theta(x_{\lambda_s},\lambda_s)
\int^{\lambda_t}_{\lambda_s}   e^{-\lambda} \frac{(\lambda-\lambda_{t_s})^n}{n!}  \dd \lambda
 +O(h^{k+1})
$$

其中$h:=\lambda_t-\lambda_s>0$。上式仅在噪声估计网络$\epsilon$处使用了$k$阶近似，其他项均精确计算。

设$\delta=\dfrac{\lambda-\lambda_s}{h}$，则上式变为，

$$
\begin{align}
x_t&=\frac{ a_t}{ a_s}x_s
- a_t
\sum_{n=0}^{k-1} \hat\epsilon^{(n)}_\theta(x_{\lambda_s},\lambda_s)
\int^1_0  e^{-(\lambda_t-h(1-\delta))} \frac{(h\delta)^n}{n!}  h \dd \delta
 +O(h^{k+1})\\
 &=\frac{ a_t}{ a_s}x_s
- a_t
\sum_{n=0}^{k-1} \hat\epsilon^{(n)}_\theta(x_{\lambda_s},\lambda_s)
h^{n+1}
\int^1_0 e^{-\lambda_t}  e^{h(1-\delta))} \frac{\delta^n}{n!} \dd \delta
 +O(h^{k+1})\\
 &=\frac{ a_t}{ a_s}x_s
- b_t
\sum_{n=0}^{k-1} \hat\epsilon^{(n)}_\theta(x_{\lambda_s},\lambda_s)
h^{n+1}
\int^1_0  e^{h(1-\delta))} \frac{\delta^n}{n!} \dd \delta
 +O(h^{k+1})\\
  &=\frac{ a_t}{ a_s}x_s
- b_t
\sum_{n=0}^{k-1} \hat\epsilon^{(n)}_\theta(x_{\lambda_s},\lambda_s)
h^{n+1} \varphi_{n+1}(h)
 +O(h^{k+1})\label{k-iter}
\end{align}
$$

其中，

$$
\varphi_{n+1}(h):=\int^1_0  e^{h(1-\delta))} \frac{\delta^n}{n!} \dd \delta ,\ \ \ \ n\geq 0 \\
\varphi_0(h):=e^h
$$

注意到 $\varphi_n(0)=\frac{1}{n!}$，用分部积分可证，$\varphi_n(h)$有如下递归关系

$$
\varphi_{n+1}(h)=\frac{\varphi_n(h)-\varphi_{n}(0)}{h}
$$

故常用的前几阶 $\varphi_n(h)$ 是

$$
\begin{align}
\varphi_0(h)&=e^h=1+h+\frac{1}{2}h^2+\frac{1}{6}h^3+\frac{1}{24}h^4+\cdots\\
\varphi_1(h)&=\frac{e^h-1}{h}=1+\frac{1}{2}h+\frac{1}{6}h^2+\frac{1}{24}h^3+\cdots\\
\varphi_2(h)&=\frac{e^h-1-h}{h^2}=\frac{1}{2}\ \ +\frac{1}{6}h\ \ +\frac{1}{24}h^2+\cdots\\
\varphi_3(h)&=\frac{e^h-1-h-\frac{1}{2}h^2}{h^3}=\frac{1}{6}\ \ \ +\frac{1}{24}h+\cdots\\
&\cdots
\end{align}
$$

**更简洁的记法是**：

$$
x_t=\frac{a_t}{b_s}x_s-b_t\sum^{k-1}_{n=0} \hat\epsilon_\theta^{(n)}(x_{\lambda_s},\lambda_s)\Phi_{n+1}(h)+O(h^{k+1})\\
\Phi_{n+1}(h):=h^{n+1}\varphi(h)=h^{n+1}\int^1_0  e^{h(1-\delta))} \frac{\delta^n}{n!} \dd \delta ,\ \ \ \ n\geq 0 \\
\Phi_0(h):=e^h
$$

递推公式为

$$
\Phi_{n+1}(h)=\Phi_{n}(h)-\Phi_{n}(0)\\
\Phi_{n}(0)=\frac{h^n}{n!}
$$

常用的前几阶 $\varphi_n(h)$ 是

$$
\begin{align}
\Phi_0(h)&=e^h=1+h+\frac{1}{2}h^2+\frac{1}{6}h^3+\frac{1}{24}h^4+\cdots\\
\Phi_1(h)&=e^h-1=h+\frac{1}{2}h^2+\frac{1}{6}h^3+\frac{1}{24}h^4+\cdots\\
\Phi_2(h)&=e^h-1-h=\frac{1}{2}h^2+\frac{1}{6}h^3+\frac{1}{24}h^4+\cdots\\
\Phi_3(h)&=e^h-1-h-\frac{1}{2}h^2=\frac{1}{6}h^3+\frac{1}{24}h^4+\cdots\\
\cdots&\\
\Phi_k(h)&=e^h-\sum_{i=1}^{n-1}\frac{h^i}{i!}=\sum_{i=n}^{\infty}\frac{h^i}{i!}
\end{align}
$$

故展开后，是

$$
\begin{align}
x_t=\frac{a_t}{b_s}x_s-b_t \bigg( & \hat\epsilon_\theta(x_{\lambda_s},\lambda_s)       e^h\\
+&\hat\epsilon_\theta^{(1)}(x_{\lambda_s},\lambda_s) (e^h-1)\\
+&\hat\epsilon_\theta^{(2)}(x_{\lambda_s},\lambda_s) (e^h-1-h)\\
+&\hat\epsilon_\theta^{(3)}(x_{\lambda_s},\lambda_s) (e^h-1-h-\frac{1}{2}h^2)\\
&\cdots\\
+&\hat\epsilon_\theta^{(k)}(x_{\lambda_s},\lambda_s) (e^h-1-h-\frac{1}{2}h^2-\cdots-\frac{1}{k!}h^{k})\bigg)
+O(h^{k+1})
\end{align}
$$

### 1阶DPM-Solver即**DDIM**

DPM-Solver-1阶即**DDIM**，反向传播（采样）的公式是

$$
x_{t}=\frac{ a_{t}}{ a_{s}}x_{s}
-b_{t} {\epsilon_\theta(x_{s},s)} (e^{h}-1)
$$

和DDIM的式$\eqref{ddim}$等价。

证明：

> $$
> begin{align}
> x_{t}&=\frac{ a_{t}}{ a_{s}}x_{s}
> - a_{t}
> {\epsilon_\theta(x_{\lambda_{s}},\lambda_{s})}
> \int^{\lambda_{t}}_{\lambda_{s}}   e^{-\lambda}  \dd \lambda
>  +O(h^{k+1})\\
>  &=\frac{ a_{t}}{ a_{s}}x_{s}
> - a_{t} {\epsilon_\theta(x_{s},s)}(-e^{-\lambda_{t}}+e^{-\lambda_{s}})\\
>  &=\frac{ a_{t}}{ a_{s}}x_{s}
> - a_{t} {\epsilon_\theta(x_{s},s)}e^{-\lambda_{t}}(e^{h}-1)\\
>  &=\frac{ a_{t}}{ a_{s}}x_{s}
> - a_{t} {\epsilon_\theta(x_{s},s)} \frac{b_{t}}{ a_i} (e^{h}-1)\\
>  &=\frac{ a_{t}}{ a_{s}}x_{s}
> -b_{t} {\epsilon_\theta(x_{s},s)} (e^{h}-1) \label{ddim-pre}
> \end{align}
> $$
>
> 向式$\eqref{ddim-pre}$中的各项可做如下赋值，
>
> $$
> :=t,\ t:=t-\Delta t,\ s-t:=\Delta t>0\\
> a_{t}:=\sqrt{\bar{\alpha}_{t-\Delta t}},a_{s}:=\sqrt{\bar{\alpha}_{t}}\\
> b_{t}:=\sqrt{\alpha_{t-\Delta t}}\\
> e^{h}:=\exp(\lambda_{t}-\lambda_{s})=\exp(\ln\frac{a_{t}}{b_{t}}  -\ln\frac{a_{s}}{b_{s}}  )=\frac{a_{t}}{b_{t}} \frac{b_{s}}{a_{s}} =\sqrt{\frac{\bar{\alpha}_{t-\Delta t}}{1-\bar{\alpha}_{t-\Delta t}} \cdot \frac{1-\bar{\alpha}_{t}}{\bar{\alpha}_{t}}}
> $$
>
> 于是，式$\eqref{ddim-pre}$变成，
>
> $$
> begin{align}
> x_{t-1}&=\frac{\sqrt{\bar{\alpha}_{t-\Delta t}}}{\sqrt{\bar{\alpha}_{\mathrm{t}}}}x_t
>
> -\sqrt{1-\bar\alpha_{t-\Delta t}}
>
> \left( \sqrt{\frac{\bar{\alpha}_{t-\Delta t}}{1-\bar{\alpha}_{t-\Delta t}} \cdot \frac{1-\bar{\alpha}_{t}}{\bar{\alpha}_{t}}}-1 \right)
>
> \epsilon_\theta(x_t,t)
> \\
> &=\frac{\sqrt{\bar{\alpha}_{t-\Delta t}}}{\sqrt{\bar{\alpha}_{\mathrm{t}}}}\left(x_t-\sqrt{1-\bar{\alpha}_t} \epsilon_\theta\left(x_t, t\right)\right)+\sqrt{1-\bar{\alpha}_{t-\Delta t}} \epsilon_\theta\left(x_t, t\right)
> \ \ \ \ 即式\eqref{ddim}  \ \ \ \ \square
> \end{align}
> $$

## 导数的数值计算

**高阶导**$\hat\epsilon^{(n)}(x_\lambda,\lambda)$可以用**传统的数值方法**近似求得，这和数值求解ODE类似，除了所在点但函数值，还需要用中间点（单步法）或先前点（多步法）但函数值去计算。其解法已在下列文献中研究过：

* M. Hochbruck and A. Ostermann, “Explicit exponential Runge-Kutta methods for semilinear parabolic problems,” SIAM Journal on Numerical Analysis, vol. 43, no. 3, pp. 1069–1090, 2005.
* V. T. Luan, “Efﬁcient exponential Runge-Kutta methods of high order: Construction and implementation,” BIT Numerical Mathematics, vol. 61, no. 2, pp. 535–560, 2021.

比如，$s$处的一阶导，可以用$t$处的$\hat\epsilon$函数值，与**中间点**$\varsigma\in(t,s)$ 或 **先前点**（$\varsigma>s$）处的$\hat\epsilon$函数值去计算：

$$
\hat{{\epsilon}}_\theta^{(1)}\left(\hat{{x}}_{\lambda_s}, \lambda_s\right) \approx \frac{\hat{{\epsilon}}_\theta\left(\hat{{x}}_\varsigma, \varsigma\right)-\hat{{\epsilon}}_\theta\left(\hat{{x}}_{\lambda_s}, \lambda_s\right)}{\lambda_{\varsigma}-\lambda_s}
$$

在DPM-Solver的论文中，有以下几种具体的做法，能够避免数值求>=2阶导：

* **DPM-Solver-1**: 使用0阶导

  $$
  x_t=\frac{ a_t}{ a_s}x_s
  - b_t (e^h-1) \hat\epsilon_\theta(x_{\lambda_s},\lambda_s)
  $$
* **DPM-Solver-2**: 使用0、1阶导

  $$
  \begin{align}
  & 引入中间点\varsigma,\ s>\varsigma>t, \\
  & s.t. \lambda_\varsigma=\lambda_s+r h, r\in(0,1)\\
  & \forall r \in (0,1)下列算法都成立，通常取r=\frac{1}{2}\\
  &赋值公式 &误差\\
  x_\varsigma&=\frac{ a_\varsigma}{ a_s}x_s- b_t (e^{r h}-1) \epsilon_\theta(x_x,x)&O(h^2)\\
  D &=\epsilon_\theta(x_\varsigma,\varsigma)-\epsilon_\theta(x_s,s) &O(h^2)\\
  x_t&=\frac{ a_t}{ a_s}x_s- b_t (e^h-1) \epsilon_\theta(x_\varsigma,\varsigma) &O(h^3)
  \end{align}
  $$

  证明:

  > $$
  > begin{align}
  > x_t&=\frac{ a_t}{ a_s}x_s
  > - b_t (e^h-1) \epsilon_\theta(x_s,s)-b_t(e^h-1-h)\frac{D}{r h} +O(h^3)\\
  > &=\frac{ a_t}{ a_s}x_s
  > - b_t (e^h-1) \epsilon_\theta(x_s,s)-\frac{b_t}{2 r}(e^h-1-O(h^2)) D + O(h^3)\\
  > &\xlongequal{因D=O(h)}\frac{ a_t}{ a_s}x_s
  > - b_t (e^h-1) \epsilon_\theta(x_s,s)-\frac{b_t}{2 r}(e^h-1) D + O(h^3)\\
  > &\xlongequal{当r=\frac{1}{2}}\frac{ a_t}{ a_s}x_s- b_t (e^h-1) \epsilon_\theta(x_\varsigma,\varsigma) +O(h^3)
  > \end{align}
  > $$
  >
  > 其中 $D=O(h)$证明如下，
  >
  > $$
  > D=\epsilon_\theta(x_\varsigma,\varsigma)-\epsilon_\theta(x_s,s) \leq \sup_{\lambda}|\epsilon^{(1)}_\theta(x_\lambda,\lambda)|rh=O(h)
  > $$
  >
* **DPM-Solver-3**: 使用0、1、2阶导

  $$
  \begin{align}
  & 引入中间点\varsigma_1,\varsigma_2,\ s>\varsigma_1>\varsigma_2>t, \\
  & s.t. \lambda_{\varsigma_i}=\lambda_s+r_{i} h, r_{i}\in(0,1)\\
  & \forall r_1\in(0,r_2)都成立，下列算法通常取r_1=\frac{1}{3}\\
  &仅对r_2=\frac{2}{3}下列算法才成立\\
  &赋值公式 &误差\\
  x_{\varsigma_1}&=\frac{ a_{\varsigma_1}}{ a_s}x_s- b_t (e^{r_1 h}-1) \epsilon_\theta(x_x,x)&O(h^2)\\
  D_1&=\epsilon_\theta(x_{\varsigma_1},\varsigma_1)-\epsilon_\theta(x_s,s)&O(h^2)\\
  x_{\varsigma_2}&=\frac{ a_{\varsigma_2}}{ a_s}x_s
  - b_t (e^{r_2 h}-1) \epsilon_\theta(x_s,s)-b_{\varsigma_2}(e^{r_2 h}-1-r_2 h) \frac{D_1}{r_1 h}&O(h^3) \\
  D_2&=\epsilon_\theta(x_{\varsigma_2},\varsigma_2)-\epsilon_\theta(x_s,s)&O(h^3)\\
  x_t&=\frac{ a_t}{ a_s}x_s
  - b_t (e^h-1) \epsilon_\theta(x_s,s)-b_t(e^h-1-h) \frac{D_2}{r_2 h}&O(h^4)
  \end{align}
  $$

  证明：只需要2个中间点，并令$r_2=\frac{2}{3}$，就能免去数值计算$\hat\epsilon_\theta^{(2)}(x_s,s)$，

  > $$
  > begin{align}
  > x_t&=\frac{ a_t}{ a_s}x_s- b_t (e^h-1) \epsilon_\theta(x_s,s)\\
  > &\quad -b_t (e^h-1-h) \hat\epsilon_\theta^{(1)}(x_s,s)\\
  > &\quad -b_t (e^h-1-h-\frac{1}{2}h^2)\hat\epsilon_\theta^{(2)}(x_s,s)+O(h^4)\\
  >
  > &=\frac{ a_t}{ a_s}x_s- b_t (e^h-1) \epsilon_\theta(x_s,s)\\
  > &\quad-b_t \frac{e^h-1-h}{r_2h}[\hat\epsilon_\theta(x_s,s)+\hat\epsilon_\theta^{(1)}(x_s,s)r_2h+\frac{1}{2}\hat\epsilon_\theta^{(2)}(x_s,s)(r_2h)^2 -\hat\epsilon_\theta(x_s,s) - \frac{1}{2}\hat\epsilon_\theta^{(2)}(x_s,s)(r_2h)^2 ]\\
  > &\quad-b_t (e^h-1-h-\frac{1}{2}h^2)\hat\epsilon_\theta^{(2)}(x_s,s)+O(h^4)\\
  >
  > &=\frac{ a_t}{ a_s}x_s- b_t (e^h-1) \epsilon_\theta(x_s,s)\\
  > &\quad-b_t \frac{e^h-1-h}{r_2h}[\hat\epsilon_\theta(x_{\varsigma_2},\varsigma_2) -O((r_2h)^3)-\hat\epsilon_\theta(x_s,s) - \frac{1}{2}\hat\epsilon_\theta^{(2)}(x_s,s)(r_2h)^2 ] \\
  > &\quad-b_t (e^h-1-h-\frac{1}{2}h^2)\hat\epsilon_\theta^{(2)}(x_s,s)+O(h^4)\\
  >
  > &\xlongequal{因\frac{e^h-1-h}{r_2h}=O(h) }\frac{ a_t}{ a_s}x_s- b_t (e^h-1) \epsilon_\theta(x_s,s)-b_t (e^h-1-h)\frac{D_2}{r_2h}\\
  > &\quad-b_t \hat\epsilon_\theta^{(2)}(x_s,s) [-\frac{r_2}{2}h(e^h-1-h)  + (e^h-1-h-\frac{1}{2}h^2)]+O(h^4)\\
  >
  > &\xlongequal{当r_2=\frac{2}{3}}\frac{ a_t}{ a_s}x_s
  > - b_t (e^h-1) \epsilon_\theta(x_s,s)-b_t(e^h-1-h) \frac{D_2}{r_2 h}-b_t\hat\epsilon_\theta^{(2)}(x_s,s) O(h^4) +O(h^4)\\
  > &=\frac{ a_t}{ a_s}x_s- b_t (e^h-1) \epsilon_\theta(x_s,s)-b_t(e^h-1-h) \frac{D_2}{r_2 h} +O(h^4)
  > \end{align}
  > $$
  >
* DPM-Solver-12：启动时采用预设的大步长，之后每步都同时使用DPM-Solver-1和DPM-Solver-2，**二者输出的差值为依据**，**去自动减小步长**。若这个差值小于阈值，才以DPM-Solver-2的输出为下一步的输入，下一步使用缩小的步长；否则，以缩小的步长重做本步。
* DPM-Solver-23：和上面一样，但换成DPM-Solver-2和DPM-Solver-3。

# Analytic-DPM

论文：

* Analytic-DDIM、Analytic-DDPM、Analytic-DPM：[Analytic-DPM: an Analytic Estimate of the Optimal Reverse Variance in Diffusion Probabilistic Models](https://arxiv.org/abs/2201.06503)
* Extended-Analytic-DPM：[Estimating the Optimal Covariance with Imperfect Mean in Diffusion Probabilistic Models](https://arxiv.org/abs/2206.07309v1)

简介：

* Analytic-DPM：[生成扩散模型漫谈（七）：最优扩散方差估计（上）](https://kexue.fm/archives/9245)
* Extended-Analytic-DPM：[生成扩散模型漫谈（八）：最优扩散方差估计（下）](https://kexue.fm/archives/9246)

## Analytic-DPM简介

### 推导修正方差

在上文的推导中，使用$\mu_t(x_t,z_0)$单点分布去替代$x_0$，不准确。实际上，从$x_t$估计$x_0$无法准确估计，只能估计一个分布。又因为精确的$q(x_0|x_t)=\frac{q(x_t|x_0)q(x_0)}{\int q(x_t|x_0)q(x_0)\dd x_)}$无法计算，故不妨用高斯分布估计$q(x_0|x_t)$，即

$$
q(x_0|x_t)\approx N(x_0|\mu_{0|t}(x_t),\sigma_{0|t}^2I)
$$

即

$$
\boldsymbol x_0=\boldsymbol \mu_{0|t}(x_t)+\sigma_{0|t}\boldsymbol  z_{0|t},\boldsymbol  z_{0|t}\sim N(0,I)\label{q0t}
$$

要求$q(x_\tau|x_t)=\int q(x_\tau |x_t,x_0)q(x_0|x_t)\dd x_0$，可以通过重参数化方法，即将$q(x_0|x_t)$重参数化表示($\eqref{q0t}$)带入$q(x_\tau |x_t,x_0)$的重参数化表示($\eqref{ddim-repara}$)。故$q(x_\tau|x_t)$近似为如下结果

$$
\begin{align}
x_\tau &=\kappa_t x_t+(a_\tau-a_t \kappa_t)x_0+\sigma_t z, z\sim N(0,I),\kappa_t=\frac{\sqrt{b^2_{\tau}-\sigma_t^2}}{b_t}\\
&=\kappa_t x_t+(a_\tau-a_t \kappa_t)(\mu_{0|t}(x_t)+\sigma_{0|t}z_{0|t})+\sigma_t z, z_{0|t}\sim N(0,I)\\
&=\kappa_t x_t+(a_\tau-a_t \kappa_t)\mu_{0|t}(x_t)+\tilde\sigma_t \tilde z,\tilde z\sim N(0,I)
\end{align}
$$

这个答案和DDIM的普遍解$\eqref{ddim-general}$相比，除了噪声方差，其他都相同。其中，经过Analytic-DPM修正之后的噪声方差为

$$
\tilde\sigma_t^2=(a_\tau-a_t\kappa_t)^2\sigma_{0|t}^2+\sigma_t^2
$$

多出了$(a_\tau-a_t\kappa_t)^2\sigma_{0|t}^2$这项。因此，即使像DDIM取$\sigma_t=0$，$q(x_\tau |x_t)$也有噪声项。

### 估计均值

下面证明，当用$ N(x_0|\mu_\theta(x_t,t),\sigma_{0|t}^2I)$估计真实$q(x_0|x_t)$时，$\mu_{0|t}(x_t)$正好等于DDPM、DDIM中的$\mu_\theta(x_t,t)$。

当用最小二乘法拟合$\mu_t(x_t)$时，使用的损失函数为

$$
\arg\min_\mu \mathbb{E}_{x_0,x_t\sim q(x_0,x_t)}\Vert x_0-\mu_t(x_t) \Vert^2\\
=\arg\min_\mu\mathbb{E}_{x_t\sim q(x_t)} \mathbb{E}_{x_0\sim q(x_0|x_t)}\Vert x_0-\mu_t(x_t) \Vert^2\\
=\arg\min_\mu\mathbb{E}_{x_0\sim q(x_0)} \mathbb{E}_{x_t\sim q(x_t|x_0)}\Vert x_0-\mu_t(x_t) \Vert^2 (损失函数)
$$

其第二行的解为

$$
\mu_t(x_t)=\mathbb{E}_{x_0\sim q(x_0|x_t)} x_0
$$

若像之前那样引入参数化，$\mu_t(x_t)=\frac{1}{a_t}(x_t-b_t \epsilon_\theta(x_t,t))$，则优化目标变为

$$
\mathbb{E}_{x_0\sim q(x_0),z_t\sim N(0,I)}\Vert z_t-\epsilon_\theta(x_t,t) \Vert^2
$$

其解为，

$$
\epsilon_\theta(x_t,t)=\mathbb{E}_{x_0\sim q(x_0|x_t)} z_t(x_t,x_0)\\
其中z_t是关于x_0、x_t的函数，z_t=\frac{1}{b_t}(x_t-a_t x_0)
$$

这和DDPM、DDIM的噪声估计方程完全一样。

因此，上面的$\mu_t(x_t)$和DDPM、DDIM的均值$\mu_\theta(x_t,t)$完全一样。

### 估计方差

下面估计$\sigma_{0|t}^2$。

思路：

* 求真实的条件协方差矩阵的对角线$\Sigma(x_t)=\mathbb{E}_{x_0\sim q(x_0|x_t)} [(x_0-\mu_t(x_t))(x_0-\mu_t(x_t))^\top] $,

* 为避免训练从$x_t$预测方差矩阵的网络（会因为方差矩阵维度太高而学不好，拉低diffusion表现），需要使方差和$x_t$无关，故求真实协方差矩阵$\Sigma_t=\mathbb{E}_{x_t\sim q(x_t)} \Sigma(x_t)$，

* 为降低维度，只考虑该矩阵的对角线元素，取$\sigma_{0|t}^2=\dfrac{\tr(\Sigma)}{d}, d=\dim(x)$

若以$x_t$为条件，计算真实的条件协方差矩阵，则

$$
\begin{align}
\Sigma(x_t):&=\mathbb{E}_{x_0\sim q(x_0|x_t)}[(x_0-\mu_t(x_t))(x_0-\mu_t(x_t))^\top]\\
//其中x_t&=a_t x_0+b_t z_t, x_t=a_t \mu_t(x_t)+b_t \epsilon_\theta(x_t,t))\\
//故x_0-\mu_t(x_t)&=\frac{1}{a_t}(x_t-b_t z_t)-\frac{1}{a_t}(\mu_t(x_t)-b_t  \epsilon_\theta(x_t,t))=\frac{b_t}{a_t}(\epsilon_\theta(x_t,t)-z_t)\\
&=\frac{b_t^2}{a_t^2}\mathbb{E}_{x_0\sim q(x_0|x_t)}[(\epsilon_\theta(x_t,t)-z_t)(\epsilon_\theta(x_t,t)-z_t)^\top]\\
&=\frac{b_t^2}{a_t^2}\mathbb{E}_{x_0\sim q(x_0|x_t)}[\epsilon_\theta(x_t,t)\epsilon_\theta(x_t,t)^\top
- z_t \epsilon_\theta(x_t,t)^\top - \epsilon_\theta(x_t,t) z_t^\top + z_t z_t^\top]\\
//因为，\epsilon_\theta(x_t,t)&=\mathbb{E}_{x_0\sim q(x_0|x_t)} z_t\\
&=\frac{b_t^2}{a_t^2}\mathbb{E}_{x_0\sim q(x_0|x_t)}[z_tz_t^\top-\epsilon_\theta(x_t,t)\epsilon_\theta(x_t,t)^\top]\\
//因为，\Sigma(x_t)&是关于x_t的函数，故需要把z_t表示成x_t的函数\\
&=\frac{b_t^2}{a_t^2}\mathbb{E}_{x_0\sim q(x_0|x_t)}[\frac{1}{b^2_t}(x_t-a_t x_0)(x_t-a_t x_0)^\top-\epsilon_\theta(x_t,t)\epsilon_\theta(x_t,t)^\top]
\end{align}
$$

故真实的协方差矩阵为

$$
\begin{align}
\Sigma_t&=\mathbb{E}_{x_t\sim q(x_t)} \Sigma(x_t)\\
&=\frac{b_t^2}{a_t^2}\mathbb{E}_{x_t\sim q(x_t)}\mathbb{E}_{x_0\sim q(x_0|x_t)}[\frac{1}{b^2_t}(x_t-a_t x_0)(x_t-a_t x_0)^\top-\epsilon_\theta(x_t,t)\epsilon_\theta(x_t,t)^\top]\\
&=\frac{b_t^2}{a_t^2}\mathbb{E}_{x_0\sim q(x_0)}\mathbb{E}_{x_t\sim q(x_t|x_0)}[\frac{1}{b^2_t}(x_t-a_t x_0)(x_t-a_t x_0)^\top-\epsilon_\theta(x_t,t)\epsilon_\theta(x_t,t)^\top]\\
&=\frac{b_t^2}{a_t^2}\mathbb{E}_{x_0\sim q(x_0)}\mathbb{E}_{z_t\sim N(0,I)}[z_t z_t^\top-\epsilon_\theta(x_t,t)\epsilon_\theta(x_t,t)^\top]\\
&=\frac{b_t^2}{a_t^2}[I-\mathbb{E}_{x_0\sim q(x_0),z_t\sim N(0,I)}\big(\epsilon_\theta(x_t,t)\epsilon_\theta(x_t,t)^\top\big)]\\
&=\frac{b_t^2}{a_t^2}[I-\mathbb{E}_{x_t\sim q(x_t)}\big(\epsilon_\theta(x_t,t)\epsilon_\theta(x_t,t)^\top\big)]\\
\end{align}
$$

故方差为

$$
\begin{align}
\sigma_{0|t}^2&=\frac{1}{d}\tr(\Sigma_t)\\
&=\frac{b_t^2}{a_t^2}[1-\frac{1}{d}\mathbb{E}_{x_t\sim q(x_t)}\tr\big(\epsilon_\theta(x_t,t)\epsilon_\theta(x_t,t)^\top\big)]\\
//因为\tr(\boldsymbol x\boldsymbol x^\top)&=\=(\boldsymbol x\boldsymbol x^\top)_{ii}=x_i x_i=\Vert x\Vert^2\\
&=\frac{b_t^2}{a_t^2}\big( I-\frac{1}{d} \mathbb{E}_{x_t\sim q(x_t)}\Vert \epsilon_\theta(x_t,t)\Vert ^2 \big) \\
//因为\epsilon_\theta(x_t,t)估计的是z_t, 而z_t\sim N(0,I), 故\mathbb{E}_{x_t\sim q(x_t)}\Vert z_t\Vert^2 =\mathbb{E}_{x_0\sim q(x_0),z_t\sim N(0,I)}\Vert z_t\Vert^2 =\mathbb{E}_{} \\
\end{align}
$$