# 参考文献

[扩散薛定谔桥和最优传输](https://zhuanlan.zhihu.com/p/690392523)

[^liaison]: Chen, Y., Georgiou, T.T., Pavon, M., 2020. Stochastic control liaisons: Richard Sinkhorn meets Gaspard Monge on a Schroedinger bridge., https://doi.org/10.48550/arXiv.2005.10963

# Diffusion和薛定谔桥的对比

## Diffusion的缺点

基于Score的生成模型（Score-based Generative Model，SGM，在下文中也叫做Diffusion）已经是目前CV领域中最火的话题之一。其可以简单总结成两个过程：一个加噪（前向）过程，根据手工定义的规则在数据上反复加高斯噪声，最后得到一个近似高斯的分布；一个去噪（反向）过程，模拟我们定义好的加噪过程的反向，一般用一个神经网络来学习。但是Diffusion也有一些缺点，比如

- 生成速度慢：Diffusion的训练过程需要分很多timestep（时间步），对连接两个分布的轨迹进行分段离散化，进而导致生成一张图片需要迭代成百上千次；

- 加噪过程需要手工定义：在加噪过程中，每个timestep加多大的高斯噪声都是手工定义的（schedule），具体什么样的schedule效果好只能通过实验尝试；

- 拟合能力有限：对于更高维度空间中的低维流形，如视频生成，diffusion模型的能力可能仍然不够强。

- 只能单向生成：现有的Diffusion基本都只能从高斯分布生成复杂分布（比如图像），无法在两个复杂分布之间建立映射。

近来，基于薛定谔桥（Schrödinger Bridge，SB）问题的生成模型开始引起关注，而扩散薛定谔桥（Diffusion Schrödinger Bridge，DSB）是其中的一项重要工作，显示出了一定程度上缓解和解决这些问题的潜力。

## SB的优点

相比于Diffusion, DSB主要有以下两个优点：

- DSB计算的是两个分布之间的最优传输（Optimal Transport，OT）；

- DSB可以计算任意两个可采样分布之间的OT，而相比之下Diffusion只能从已知分布（如高斯噪声）开始生成数据。

# 薛定谔桥的物理背景

1931-1932年，薛定谔提出一个思想实验，

# 数学概念

## 轨迹的概率

## 某时的分布

# 静态薛定谔桥

# 最优传输

# 因式分解

# 随机控制

# 流体力学

# 普遍先验


