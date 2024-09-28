# NCSN简介

[图像生成别只知道扩散模型(Diffusion Models)，还有基于梯度去噪的分数模型：NCSN(Noise Conditional Score Networks)](https://zhuanlan.zhihu.com/p/597490389)

问题：朗之万动力学模拟退火，为什么理论上，在一定约束条件下，并且当$\epsilon\rightarrow 0, T\rightarrow\infty$, 最终生成的样本$x_T$将会服从原数据分布$p_{data}(x)$。

# NCSN和DDPM的关系

## 证明NCSN和DDPM等价

论文：[Understanding Diffusion Models: A Unified Perspective](https://arxiv.org/abs/2208.11970)

[需要使用此结论去证明二者loss等价](https://www.tandfonline.com/doi/abs/10.1198/jasa.2011.tm11181)

## 在SDE框架下比较NCSN和DDPM并证明其等价

### 反向扩散的比较

论文：[Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/abs/2011.13456)

[【理论推导】随机微分方程(SDE)视角下的Diffusion Model与Score-based Model ](https://blog.csdn.net/fnoi2014xtx/article/details/129871986)


![1708935913520](assets/1708935913520.png)

### 正向扩散的比较

[SDE in diffusion models](https://blog.csdn.net/weixin_44966641/article/details/135541595)

在文章中，NCSN 和 DDPM 分别对应于 VE-SDE（Variance Exploding） 和 VP-SDE（Variance Preseving），其意义分别为 Variance Exploding 和 Variance Preseving。这里我们先写出两类模型的扩散公式：


![1708935953701](assets/1708935953701.png)

这两个名字是从何得来呢? 我们知道, 在扩散模型中, 加到最大的噪声强度时, 噪声图 $x_T$ 需要几乎完全是一个高斯分布。

* 在 NCSN 中, $x_T=x_0+\sigma_T \epsilon$ 要是一个完全的噪声, 其中方差 $\sigma_T$ 就要非常大, 故称为 Variance Exploding, 方差爆炸;
* 在 DDPM 中, $x_T=\sqrt{\bar{\alpha}_T} x_0+\sqrt{1-\bar{\alpha}_T} \epsilon$ 要是一个完全的噪声, 其中 $\bar{\alpha}_T$ 就要非常小, 所以噪声 $\sqrt{1-\bar{\alpha}_t}$ 最大也只有 1 , 故称为 Variance Preserving, 方差收紧。

### Score的比较

[SDE in diffusion models](https://blog.csdn.net/weixin_44966641/article/details/135541595)

|                | NCSN                                           | DDPM |
| -------------- | ---------------------------------------------- | ---- |
| 估计噪声的定义 | $s_\theta(x_t,t):=\nabla_{x_t}\log P(x_t)$  |      |
|                |                                                |      |
