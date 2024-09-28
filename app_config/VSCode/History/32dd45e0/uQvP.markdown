# [IS、FID、PPL评估指标](https://zhuanlan.zhihu.com/p/432965561)

## IS（Inception Score）

参考资料： [全面解析Inception Score原理及其局限性](https://www.jiqizhixin.com/articles/2019-01-10-18)



含义：IS是对生成图片清晰度和多样性的衡量，IS值越大越好。

思想：使用图片类别分类器来评估生成图片的质量。

使用模型：使用图像分类器Inception Net-V3，1000分类



公式：

$I S(G):=\exp H(X, Y) \quad \exp$ 上 生成图像和预测类别之间的互信息
$$
H(X, Y)=\sum_{x, y} p(x, y) \ln \frac{p(x, y)}{p(x) p(y)}=E_{x \sim p_G} \sum_y p(y \mid x) \ln \frac{p(y \mid x)}{p(y)}=E_{x \sim p_G} K L(p(y \mid x) \| p(y)
$$

其中:
- 大量图像 $x$ 由生成器 $G$ 生成，计作 $x \sim p_G$ ，简写为 $p(x)$
- 分类器预测 $x$ 属于各类别 $\mathrm{y}$ 的概率为 $p(y \mid x)$
- $p(y)=\sum_{x \sim p_G} p(y \mid x)$
- $p(x, y)=p(x) p(y / x)$



局限性：

-   Inception     Score得分过于依赖分类器，是一种间接的对图片质量评估的方法，没有考虑真实数据与生成数据的具体差异。
-   Inception     Score是基于ImageNet得到的，在IS看来，凡是不像ImageNet的数据，都是不真实的。
-   IS小不一定图像不真实，IS大不一定图像真实，刷分会导致图片质量变差
-   不能反映过拟合
-   当生成模型生成各类别图像的概率相等，IS无法反映出这个问题

建议：IS 是一个浑身硬伤的评价指标，尽量别用。

## FID（Fréchet Inception Distance）

含义：FID是反应生成图片和真实图片的距离，数据越小越好。

思想：生成数据和真实数据在feature层次的距离。

使用模型：使用Inception Net-V3全连接前的2048维向量作为图片的feature。



公式：

用多元正态分布去分别拟合真实、生成数据的feature，计算这两个正态分布的的Frechet距离（又称 Wasserstein-2 距离）。

   参考：

-   [两个多元正态分布的KL散度、巴氏距离、Hellinger距离、W距离、Frechet距离](https://kexue.fm/archives/8512)
-   [从Wasserstein距离、对偶理论到WGAN](https://kexue.fm/archives/6280)

$$
F I D=\left\|\mu_r-\mu_g\right\|^2+\operatorname{Tr}\left(\Sigma_r+\Sigma_g-2\left(\Sigma_r \Sigma_g\right)^{\frac{1}{2}}\right)
$$

其中 :
- $\mu_r$ : 真实图片的特征均值
- $\mu_g$ : 生成图片的特征均值
- $\Sigma_r$ : 真实图片的协方差矩阵
- $\Sigma_g$ : 生成图片的协方差矩阵
- $\operatorname{Tr}$ : 迹

优点

-   生成模型的训练集可以和Inception     Net-V3不同
-   刷分不会导致生成图片质量变差

缺点

-   FID是衡量多元正态分布直接按的距离，但提取的图片特征不一定是符合多元正态分布的
-   无法解决过拟合问题，如果生成模型只能生成和训练集一模一样的数据无法检测

## PPL（Perceptual Path Length）

PPL评估利用生成器从一个图片变到另一个图片的距离，越小越好。

原始论文： https://arxiv.org/pdf/1812.04948.pdf

使用VGG16

## KID (Kernel Inception Distance)

原始论文： https://arxiv.org/pdf/1801.01401.pdf

# 图像相似度指标

来自： https://zhuanlan.zhihu.com/p/309892873

## 结构相似性指数（structural similarity index，SSIM）

## 峰值信噪比(Peak Signal to Noise Ratio, PSNR)

## 学习感知图像块相似度(Learned Perceptual Image Patch Similarity, LPIPS)

Perceptual distance (LPIPS): https://arxiv.org/pdf/1801.03924.pdf



也称为“感知损失”(perceptual loss)

LPIPS的值越低表示两张图像越相似



公式:
$$
d\left(x, x_0\right)=\sum_l \frac{1}{H_l W_l} \sum_{h, w}\left\|\boldsymbol{w}_l \odot\left(\widehat{\boldsymbol{y}}_{h w}^l-\widehat{\boldsymbol{y}}_{0 h w}^l\right)\right\|^2
$$

图像 $x, x_0$ ，送入图像识别网络 (通常是VGG ) ，将第 1 层的特征，逐层沿通道维度归一化为 $\widehat{\boldsymbol{y}}_{h w}^l=\frac{y_{h w}^l}{\left\|y_{h w}^l\right\|}, \widehat{y}_{0 h w}^l=\frac{y_{0 h w}^l}{\left\|y_{0 h w}^l\right\|} \in$ $\mathbb{R}^{c_l}$ ，再用可学习的向量 $\boldsymbol{w}_l \in \mathbb{R}^{c_l}$ 来激活各通道的特征，最终计算 $\mathrm{L} 2$ 距离 ; 然后在空间上求平均，在通道上求和。第 $l$ 层特征 $\in \mathbb{R}^{H_l \times W_l \times C_l}$ ，其中 $H_l \times W_l \times C_l$ 为第 $l$ 层的高度、宽度、通道数。

论文中提到，如果 $\boldsymbol{w}_l=\mathbf{1}(\forall l)$ 时，那么 $\left\|\boldsymbol{w}_l \odot\left(\widehat{\boldsymbol{y}}_{h w}^l-\widehat{\boldsymbol{y}}_{O h w}^l\right)\right\|^2$ 和计算 $\widehat{\boldsymbol{y}}_{h w}^l$ 和 $\widehat{\boldsymbol{y}}_{O h w}^l$ 欧氏距离是等价的。

训练 $w_l$ 的方法:

![image-20240127111355621](assets/image-20240127111355621-6325239.png)
$$
L\left(x, x_0, x_1, h\right)=-h \log G\left(d\left(x, x_0\right), d\left(x, x_1\right)\right)-(1-h) \log \left(1-G\left(d\left(x, x_0\right), d\left(x, x_1\right)\right)\right)
$$

其中 $\mathrm{h} \in\{0,1\}$ 分别表示，在人类标注下，扭曲后的图片 $x_0, x_1$ 谁离扭曲前的原图 $x$ 更近。 $\mathrm{G}$ 是用 $d\left(x, x_0\right), d\left(x, x_1\right)$ 来预测 $h$ 的小网络。

![image-20240127111411981](assets/image-20240127111411981.png)