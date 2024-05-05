# DDIM

加速Diffusion采样和方差的选择(DDIM) https://zhuanlan.zhihu.com/p/525106459

扩散模型之DDIM https://zhuanlan.zhihu.com/p/565698027

DDIM的改进：

- 加速：DDIM和DDPM有相同的训练目标，但是它不再限制扩散过程必须是一个马尔卡夫链，这使得DDIM可以采用更小的采样步数来加速生成过程
- 确定：DDIM的另外是一个特点是从一个随机噪音生成样本的过程是一个确定的过程，中间没有加入随机噪音

详见：扩散模型之DDIM https://zhuanlan.zhihu.com/p/565698027

# 扩散模型与微分方程

## 为什么DDIM能比DDPM节省采样步数？

为什么DDIM能比DDPM苏省采样步数？
DDPM反向扩散每步都有噪声，可以转化成SDE（随机微分方程 )，只能用小步长从 $x_{\mathrm{T}}$ 去数值计算 $\mathrm{x}_0$ ，不然求得的 $\mathrm{x}_0$ 误差很大，即生成的图像 $\left(\mathrm{x}_0\right)$ 效果很差。
DDIM反向扩散每步都是确定的，可以转化成ODE ( 常微分方程 ) ，可以用较大的步长从 $\mathrm{x}_{\mathrm{T}}$ 去数值计算 $\mathrm{x}_0$ ，仍得到较准确的 $\mathrm{x}_0$ ，即生成的图像 $\left(\mathrm{x}_0\right)$ 效果还好。

## DDPM的前向传播 ( 加噪 )

$$
\begin{array}{l}
x_t=\sqrt{1-\beta_t} x_{t-1}+\sqrt{\beta_t} z, \quad z \sim N(\mathbf{0}, \mathbf{I}) \\
=\sqrt{1-\beta_t \Delta \mathrm{t}} x_{t-\Delta \mathrm{t}}+\sqrt{\beta_t \Delta \mathrm{t}} z, \Delta t=1 \\
\approx\left(1-\frac{1}{2} \beta_t \Delta t\right) x_{t-\Delta \mathrm{t}}+\sqrt{\beta_t \Delta \mathrm{t}} z, \Delta t \rightarrow 0 \\
\Rightarrow \mathrm{d} x_t=-\frac{1}{2} \beta_t x_t \mathrm{~d} t+\sqrt{\beta_t \mathrm{~d} t} z ， \quad \sqrt{\mathrm{d} t} z \text { 是一个布朗运动 } \\
\Leftrightarrow d x_t \left\lvert\, x_t \sim N\left(-\frac{1}{2} \beta_t x_t \mathrm{~d} t, \beta_t \mathrm{~d} t \mathbf{I}\right)\right.
\end{array}
$$

这是一个随机微分方程 (SDE) ）, 是马尔可夫过程，称作伊藤(Itô)过程或扩散过程。

详见：

【理论推导】随机微分方程(SDE)视角下的Diffusion Model与Score-based Model https://blog.csdn.net/fnoi2014xtx/article/details/129871986

## DDIM的反向传播（去噪）

$$
\begin{array}{l}
x_{t-1}=\frac{\sqrt{\bar{\alpha}_{t-1}}}{\sqrt{\bar{\alpha}_{\mathrm{t}}}}\left(x_t-\sqrt{1-\bar{\alpha}_t} \epsilon_\theta\left(x_t, t\right)\right)+\sqrt{1-\bar{\alpha}_{t-1}} \epsilon_\theta\left(x_t, t\right) \\
\Leftrightarrow \frac{x_{t-1}}{\sqrt{\bar{\alpha}_{t-1}}}=\frac{x_t}{\sqrt{\bar{\alpha}_t}}+\left(\sqrt{\frac{1-\bar{\alpha}_{t-1}}{\bar{\alpha}_{t-1}}}-\sqrt{\frac{1-\bar{\alpha}_t}{\bar{\alpha}_t}}\right) \epsilon_\theta\left(x_t, t\right) \\
\Leftrightarrow \frac{x_{t-\Delta \mathrm{t}}}{\sqrt{\bar{\alpha}_{t-\Delta \mathrm{t}}}}=\frac{x_t}{\sqrt{\bar{\alpha}_t}}+\left(\sqrt{\frac{1-\bar{\alpha}_{t-\Delta \mathrm{t}}}{\bar{\alpha}_{t-\Delta \mathrm{t}}}}-\sqrt{\frac{1-\bar{\alpha}_t}{\bar{\alpha}_t}}\right) \epsilon_\theta\left(x_t, t\right), \Delta t=1 \\
\Leftrightarrow \mathrm{d} \bar{x}(t)=\epsilon_\theta\left(\frac{\bar{x}_t}{\sqrt{\sigma^2(t)+1}}, t\right) \mathrm{d} \sigma(t) \text { ，令 } \sigma(t)=\sqrt{\frac{1-\bar{\alpha}_t}{\bar{\alpha}_t}}, \bar{x}(t)=\frac{x_t}{\bar{\alpha}_t}
\end{array}
$$

这是一个常微分方程 (ODE) ，其正向过程 ( 加噪 ) $\left(x_{\tau_i} \mid x_0 \sim N\left(\sqrt{\bar{\alpha}_{\tau_i}} x_0 ，\left(1-\bar{\alpha}_{\tau_i}\right) \mathbf{I}\right)\right)$ 不是马尔可夫过程。

详见：扩散模型之DDIM https://zhuanlan.zhihu.com/p/565698027

## 扩展阅读

[扩散模型与能量模型，Score-Matching和SDE，ODE的关系](https://zhuanlan.zhihu.com/p/576779879)

先修知识 Score-Based Generative Modeling through Stochastic Differential Equations  https://arxiv.org/abs/2011.13456

路橙：DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps https://arxiv.org/abs/2206.00927
