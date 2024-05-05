[图像生成别只知道扩散模型(Diffusion Models)，还有基于梯度去噪的分数模型：NCSN(Noise Conditional Score Networks)](https://zhuanlan.zhihu.com/p/597490389)

问题：朗之万动力学模拟退火，为什么理论上，在一定约束条件下，并且当$\epsilon\rightarrow 0, T\rightarrow\infty$, 最终生成的样本$x_T$将会服从原数据分布$p_{data}(x)$。

[证明NCSN和DDPM等价](https://arxiv.org/abs/2208.11970)

[需要使用此结论去证明二者loss等价](https://www.tandfonline.com/doi/abs/10.1198/jasa.2011.tm11181)



[【理论推导】随机微分方程(SDE)视角下的Diffusion Model与Score-based Model ](https://blog.csdn.net/fnoi2014xtx/article/details/129871986)

![1708935913520](assets/1708935913520.png)


[SDE in diffusion models](https://blog.csdn.net/weixin_44966641/article/details/135541595)

在文章中，NCSN 和 DDPM 分别对应于 VE-SDE 和 VP-SDE，其意义分别为 Variance Exploding 和 Variance Preseving。这里我们先写出两类模型的扩散公式：

![1708935953701](assets/1708935953701.png)
