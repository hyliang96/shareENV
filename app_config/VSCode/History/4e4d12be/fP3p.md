# 记号约定

下面的推导将会使用到如下的记号约定。

参考：[关于三维矢量和三维二阶张量的一些运算](https://0382.github.io/2019/10/16/einstein-notation-simple/)

### 凡例

下列最右侧是爱因斯坦求和记号，默认张量标量顺序是$ijkl\cdots$
$$
\phi\in\R\\
\boldsymbol b:=[b_i]_{m\times 1}=b_i\\
\nabla :=[\frac{\partial}{\partial x_i}]_{m\times 1}=\partial_i\\
\phi的Jacobian矩阵：J_\phi:=\nabla\phi=\partial_i\phi \\
\boldsymbol A:=[a_{ij}]_{m\times n}=a_{ij}\\
$$

### 并矢

$$
\boldsymbol a\boldsymbol b:=\boldsymbol a\boldsymbol b^\top=a_i b_j\\
\nabla\boldsymbol b:=[\nabla b_1,\nabla b_2,\cdots,\nabla b_n]=\partial_i b_j\\
\phi的Hessian矩阵：H_\phi:=\mathop{\nabla}_i\mathop{\nabla}_j\phi :=\mathop{\nabla}_i\mathop{\nabla}_j{}^\top\phi=\partial_i\partial_j\phi
$$


### 向量点乘/向量内积

$$
\langle\boldsymbol a, \boldsymbol b\rangle:=\boldsymbol a\cdot \boldsymbol b:= a_i b_i\\
\nabla\cdot \boldsymbol b:=\partial_i b_i\\
\boldsymbol a\cdot\nabla:=a_i\partial_i\\
Laplace算子：\Delta\phi:=\nabla^2\phi:=\nabla\cdot \nabla\phi=\partial_i^2\phi
$$

性质：

* 分配律

$$
\nabla\cdot(\phi\boldsymbol a)=(\nabla\phi)\cdot\boldsymbol a +\phi(\nabla\cdot\boldsymbol a)
$$

>   证：

>   $$
>   \nabla\cdot(\phi\boldsymbol a)=\partial_i (\phi a_{i})=(\partial_i\phi)a_{i}+\phi(\partial_i a_{i})=(\nabla\phi)\cdot\boldsymbol a +\phi(\nabla\cdot\boldsymbol a)
>   $$

*   Laplace算子是Hessian的迹
    $$
    \nabla^2\phi=\partial_i^2\phi=\tr(\partial_i\partial_j\phi)=\tr(\mathop{\nabla}_i\mathop{\nabla}_j\phi)
    $$

### 矩阵点乘向量

$$
\begin{align}
\boldsymbol A\cdot\boldsymbol b =\boldsymbol A\boldsymbol b :&=\left[\begin{aligned}\boldsymbol a_{\cdot 1}\cdot\boldsymbol b \\\boldsymbol a_{\cdot 2}\cdot\boldsymbol b \\ \vdots\\ \boldsymbol a_{\cdot m}\cdot\boldsymbol b \end{aligned}\right]= a_{ij} b_j\\
\boldsymbol A \cdot\nabla=\boldsymbol A \nabla :&=\left[\begin{aligned}\boldsymbol a_{\cdot 1}\cdot \nabla\\ \boldsymbol a_{\cdot 2}\cdot \nabla\\ \vdots\\  \boldsymbol a_{\cdot m}\cdot \nabla\end{aligned}\right]= a_{ij}\partial_j \\
\end{align}
$$



### 向量点乘矩阵

$$
\begin{align}
\boldsymbol A&=\left[\boldsymbol a_{1\cdot}, \boldsymbol a_{2\cdot}, \cdots, \boldsymbol a_{m\cdot }\right]\\
\boldsymbol y\cdot\boldsymbol A=\boldsymbol y^\top\boldsymbol A:&=\left[ \boldsymbol y\cdot\boldsymbol a_{1\cdot},\boldsymbol y\cdot\boldsymbol a_{2\cdot},\cdots, \boldsymbol y\cdot\boldsymbol a_{n\cdot }\right]= x_i a_{ij}\\

\mathop{\nabla}\limits_i{}\cdot\boldsymbol A=\mathop{\nabla}\limits_i{}^\top\boldsymbol A:&=\left[\nabla\cdot\boldsymbol a_{1\cdot}, \nabla\cdot\boldsymbol a_{2\cdot}, \cdots, \nabla\cdot\boldsymbol a_{n\cdot}\right]=\partial_i a_{ij}
\end{align}
$$

性质：

*   分配律

$$
\nabla\cdot(\phi\boldsymbol A)=(\nabla\phi)\cdot\boldsymbol A +\phi(\nabla\cdot\boldsymbol A)
$$

>   证：

>   $$
>   \nabla\cdot(\phi\boldsymbol A)=\partial_i (\phi a_{ij})=(\partial_i\phi)a_{ij}+\phi(\partial_i a_{ij})=(\nabla\phi)\cdot\boldsymbol A +\phi(\nabla\cdot\boldsymbol A)
>   $$

*   点乘并矢

$$
\nabla\cdot(\boldsymbol a\boldsymbol b)=(\nabla\cdot\boldsymbol a)\boldsymbol b+\boldsymbol a\cdot(\nabla\boldsymbol b)
$$

>   证：

>   $$
>   \nabla\cdot(\boldsymbol a\boldsymbol b)=\partial_i(a_i b_j) =(\partial_i a_i) b_j+a_i(\partial_i b_j)=(\nabla\cdot\boldsymbol a)\boldsymbol b+\boldsymbol a\cdot(\nabla\boldsymbol b)
>   $$

### 矩阵点乘矩阵

$\boldsymbol{A}\in\R^{{m\times n}}, \boldsymbol{B}\in\R^{n\times r}$
$$
\boldsymbol{A}\cdot \boldsymbol{B}:=\boldsymbol{A} \boldsymbol{B}=a_{ij}b_{jk}
$$

### 双点乘/矩阵内积

两个矩阵双点乘，即两个矩阵逐点相乘再求和

$$
\begin{align}
\boldsymbol A,\boldsymbol B &\in\R^{m\times n}\\
\langle\boldsymbol A ,\boldsymbol B\rangle:=\boldsymbol A : \boldsymbol B&=a_{ij}b_{ij}=\tr(\boldsymbol A\boldsymbol B^\top)=\tr(\boldsymbol A^\top\boldsymbol B)\\
\boldsymbol A:\boldsymbol I& = \tr(\boldsymbol A)\\
(\mathop{\nabla}\limits_i\mathop{\nabla}\limits_j):\boldsymbol B&=\partial_i\partial_j b_{ij}=\mathop{\nabla}\limits_j\cdot\mathop{\nabla}\limits_i\cdot \boldsymbol B=\mathop{\nabla}\limits_j{}^\top( \mathop{\nabla}\limits_i{}^\top\boldsymbol B)^\top
\end{align}
$$



# 扩散过程通用框架

伊藤(Itô)过程/即扩散过程的通用框架如下，称为DPM（Diffusion Probabilistic Model, 扩散概率模型）：

**正向扩散SDE**为
$$
\dd{\boldsymbol{x}_t}=\boldsymbol{f}(\boldsymbol{x}_t,t)\dd t+\boldsymbol{G}(\boldsymbol{x}_t,t)\dd{\boldsymbol{w}_t}\label{sde}
$$

$\boldsymbol{f}(\boldsymbol{x}_t,t)\dd t$称漂移项（shift term），$\boldsymbol{G}(\boldsymbol{x}_t,t)\dd {\boldsymbol{w}_t}$称扩散项（diffusion term）。

$\boldsymbol x_t,\boldsymbol{f}(\boldsymbol{x}_t,t)\in \R^m, \boldsymbol{w}_t\in\R^n, \boldsymbol{G}(\boldsymbol{x}_t,t)\in\R^{m\times n}$。$\boldsymbol w_t$ 是一个标准Wiener过程（又名标准布朗运动），满足性质
$$
\boldsymbol{w}_{t+\Delta t}-\boldsymbol{w}_t\sim N(\boldsymbol 0,\Delta t\boldsymbol{I}), \forall \Delta t >0
$$
它等价于重参数化的表示$\boldsymbol{w}_{t+\Delta t}-\boldsymbol{w}_t=\sqrt{\Delta t}z, z\sim N(\boldsymbol 0,\boldsymbol{I})$。

其微分形式为 $\dd{\boldsymbol{w}_t}:=\sqrt{\dd t}\boldsymbol{z},\boldsymbol{z}\sim N(\boldsymbol 0,\boldsymbol{I})$。

**正向逆向都适用的概率流ODE**为
$$
\begin{align}
\dd{ \boldsymbol x_t }&=\tilde{\boldsymbol f}(\boldsymbol x_t,t)\dd t\label{ode-0}\\
\tilde{\boldsymbol f}(\boldsymbol x_t,t):&=
\boldsymbol f(\boldsymbol x,t)-\frac{1}{2 q_t(\boldsymbol x_t)}\nabla\cdot\big(q_t(\boldsymbol x) \boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t) \big)\\
&=\boldsymbol{f}(\boldsymbol x_t,t)
-\frac{1}{2} \nabla \log q_t(\boldsymbol x_t) \cdot \boldsymbol G(\boldsymbol x_t,t)\boldsymbol G^\top(\boldsymbol x_t,t)
-\frac{1}{2}\nabla\cdot\big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G^\top(\boldsymbol x_t,t)\big)
\label{ode}
\end{align}
$$
**逆向扩散SDE**为
$$
\begin{align}
\dd{ \boldsymbol x_t }&=\bar{\boldsymbol f}(\boldsymbol x_t,t)\dd t+\boldsymbol G(\boldsymbol x_t,t)\dd{\bar{\boldsymbol w}_t}\\
\bar{\boldsymbol f}(\boldsymbol x_t,t)
:&=\boldsymbol f(\boldsymbol x,t)-\frac{1}{ q_t(\boldsymbol x_t)}\nabla\cdot\big(q_t(\boldsymbol x) \boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t) \big)\\
&=\boldsymbol{f}(\boldsymbol x_t,t)
-\nabla \log q_t(\boldsymbol x_t) \cdot \boldsymbol G(\boldsymbol x_t,t)\boldsymbol G^\top(\boldsymbol x_t,t)
-\nabla\cdot\big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G^\top(\boldsymbol x_t,t)\big)
\label{rev-sde}
\end{align}
$$
注意：ODE的$\nabla$前面的系数为$-\dfrac{1}{2}$，逆向SDE的为$-1$。

**逆向布朗运动**

$\bar{\boldsymbol w}_t\in\R^n$​​, 是一个标准Wiener过程（又名标准布朗运动）。
$$
\dd {\bar{\boldsymbol w}_t}=\dd{\boldsymbol w_t}+\frac{1}{q_t(\boldsymbol x_t)}\nabla\cdot(q_t(\boldsymbol x_t) \boldsymbol G^\top(\boldsymbol x_t,t))\dd t\label{rev-w}
$$

满足 $\bar{\boldsymbol{w}_0}=\boldsymbol 0$​​

>   式$\eqref{rev-w}$来自Anderson, B.D.O. (1982) ‘Reverse-time diffusion equation models’, *Stochastic Processes and their Applications*, 12(3), pp. 313–326. 式(3.10)，但改论文没有证明。**如何证明**？需要使用Girsanov定理，但具体如何证明，我还没推出来。



**ODE和逆向SDE**的**证明过程见下：**

## FPK方程

前向SDE（式$\eqref{sde}$）的解的概率$q_t(\boldsymbol x)$，满足下列方程偏微分方程（PDE），称前向FPK（Fokker–Planck–Kolmogorov）方程。在物理学中称Fokker–Planck方程，在随机分析中称前向Kolmogorov方程，故名**前向FPK方程。**
$$
\frac{\partial q_t(\boldsymbol x)}{\partial t}=-\nabla\cdot(q_t(\boldsymbol x)\boldsymbol f(\boldsymbol x,t))
+\frac{1}{2}\nabla\cdot\nabla\cdot\big(q_t(\boldsymbol x)\boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t)\big)\label{fpk}
$$
### 证明方法一

参考：

*   Särkkä, S. and Solin, A. (2019) Applied Stochastic Differential Equations. 第一版. 61页, 5.2章, Theorem 5.4

>   证明：
>
>   物理含义：$p_t(\boldsymbol x)$是$t$时刻粒子的分布，SDE（式$\eqref{sde}$）是单个粒子的运动方程，$\phi(\boldsymbol x)$是势能场。
>
>   $t$时刻所有粒子的总势能为

>   $$
>   U_t=\mathbb{E}_{\boldsymbol x\sim q_t(\boldsymbol x)} \phi(\boldsymbol x)
>   $$
>   有两种等效的计算$\dfrac{\dd U_t}{\dd t}$的方式：
>
>   *   法一：跟踪每个位置的粒子分布的变化率，乘上该处的势能，然后求和：$\dfrac{\dd U_t}{\dd t}=\int \dfrac{\partial q_t(\boldsymbol x)}{\partial t}\phi(\boldsymbol x)\dd {\boldsymbol x}$
>   *   法二：跟踪每个粒子的势能的变化率，乘粒子在当前位置的概率，然后求和：$\dfrac{\dd U_t}{\dd t}=\int q_t(\boldsymbol x) \dot\phi(\boldsymbol x)\dd x$
>
>   取势能场为任意二阶可微函数$\phi(\boldsymbol x):\R^3\mapsto\R$，取二阶微分

>   $$
>   \dd\phi(\boldsymbol x)=\nabla\phi(\boldsymbol x)\cdot \dd {\boldsymbol x}+\frac{1}{2}(\nabla\nabla\phi(\boldsymbol x)):(\dd{\boldsymbol x}\dd{\boldsymbol x}^\top)
>   $$
>
>   带入SDE（式$\eqref{sde}$），则

>   $$
>   \dd\phi(\boldsymbol x)=\nabla\phi(\boldsymbol x)\cdot\big(\boldsymbol f(\boldsymbol x,t)\dd t+\boldsymbol G(\boldsymbol x_t,t)\dd {\boldsymbol w_t}\big)+\\
>   \frac{1}{2}\big(\nabla\nabla^\top\phi(\boldsymbol x)\big):\big[\big(\boldsymbol f(\boldsymbol x,t)\dd t+\boldsymbol G(\boldsymbol x_t,t)\dd {\boldsymbol w_t}\big)\big(\boldsymbol f(\boldsymbol x,t)\dd t+\boldsymbol G(\boldsymbol x_t,t)\dd {\boldsymbol w_t}\big)^\top \big]
>   $$
>   带入$\dd{\boldsymbol w_t}=\sqrt{\dd t}\boldsymbol z,\boldsymbol z\sim N(\boldsymbol 0,\boldsymbol I)$，并舍去$\dd t$的$>1$阶项，

>   $$
>   \dd\phi(\boldsymbol x)=\nabla\phi(\boldsymbol x)\cdot\big(\boldsymbol f(\boldsymbol x,t)\dd t+\boldsymbol G(\boldsymbol x_t,t)\sqrt{\dd t}\boldsymbol z\big)+ \frac{1}{2}\big(\nabla\nabla^\top\phi(\boldsymbol x)\big):\big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol z\boldsymbol z^\top\boldsymbol G(\boldsymbol x_t,t)^\top \big)\dd t
>   $$
>   对$\boldsymbol z$取期望，由于$\mathbb{E}_{\boldsymbol z} \boldsymbol z=\boldsymbol 0,\mathbb{E}_{\boldsymbol z} \boldsymbol z\boldsymbol z^\top=\boldsymbol I$，

>   $$
>   \mathbb{E}_{\boldsymbol z}\dd{\phi(\boldsymbol x)}=\nabla\phi(\boldsymbol x)\cdot\boldsymbol f(\boldsymbol x,t)\dd t+\frac{1}{2}\big(\nabla\nabla^\top\phi(\boldsymbol x)\big):\big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top \big)\dd t
>   $$
>   故单个粒子在运动中，其势能随时间变化的导数为

>   $$
>   \dot\phi(\boldsymbol x):=\frac{\mathbb{E}_{\boldsymbol z}\dd{\phi(\boldsymbol x)}}{\dd t}=\nabla\phi(\boldsymbol x)\cdot\boldsymbol f(\boldsymbol x,t)+\frac{1}{2}\big(\nabla\nabla^\top\phi(\boldsymbol x)\big):\big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top \big)
>   $$
>   故

>   $$
>   \dfrac{\dd U_t}{\dd t}=\int q_t(\boldsymbol x) \dot\phi(\boldsymbol x)\dd {\boldsymbol x}\\
>   =\int \nabla\phi(\boldsymbol x)\cdot\boldsymbol f(\boldsymbol x,t)q_t(\boldsymbol x) \dd {\boldsymbol x}+
>   \frac{1}{2}\int \big(\nabla\nabla^\top\phi(\boldsymbol x)\big):\big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top \big) \dd {\boldsymbol x}
>   $$
>   由分部积分可得

>   $$
>   \begin{align}
>   &\int_\Omega \nabla\phi(\boldsymbol x)\cdot\boldsymbol f(\boldsymbol x,t)q_t(\boldsymbol x)\dd {\boldsymbol x}\\
>   &=\oint_{\partial\Omega} \phi(\boldsymbol x)q_t(\boldsymbol x)\boldsymbol f(\boldsymbol x,t)\cdot\boldsymbol n\dd{ S}-\int_\Omega \phi(\boldsymbol x)\nabla\cdot\big(q_t(\boldsymbol x)\boldsymbol f(\boldsymbol x,t)\big)\dd{\boldsymbol x}\\
>   &\xlongequal{\Omega=\R^3}-\int_\Omega \phi(\boldsymbol x)\nabla\cdot\big(q_t(\boldsymbol x)\boldsymbol f(\boldsymbol x,t)\big)\dd{\boldsymbol x}
>   \end{align}
>   $$
>
>   以及，

>   $$
>   \begin{align}
>   &\int_\Omega \big(\nabla\nabla^\top\phi(\boldsymbol x)\big):\big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top \big)q_t(\boldsymbol x) \dd {\boldsymbol x}\\
>   &=\int_\Omega \sum_{i,j}\frac{\partial}{\partial x_i}\frac{\partial}{\partial x_j}\phi(\boldsymbol x)\big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top\big)_{ij} q_t(\boldsymbol x) \dd {\boldsymbol x}\\
>   &= \sum_{i,j}\oint_{\partial\Omega}\frac{\partial}{\partial x_j}\phi(\boldsymbol x)q_t(\boldsymbol x)\big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top\big)_{ij}  n_i\dd { S}\\
>   &\quad\ -\sum_{i,j}\int_\Omega \frac{\partial}{\partial x_j}\phi(\boldsymbol x) \frac{\partial}{\partial x_j}[q_t(\boldsymbol x) \big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top\big)_{ij}  ]\dd{\boldsymbol x}\\
>   &\xlongequal{\Omega=\R^3}-\sum_{i,j}\int_\Omega \frac{\partial}{\partial x_j}\phi(\boldsymbol x) \frac{\partial}{\partial x_j}[q_t(\boldsymbol x) \big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top\big)_{ij}  ]\dd{\boldsymbol x}\\
>   &\xlongequal{同理}\sum_{i,j}\int_\Omega \phi(\boldsymbol x) \frac{\partial}{\partial x_j}\frac{\partial}{\partial x_j}[q_t(\boldsymbol x) \big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top\big)_{ij}  ]\dd{\boldsymbol x}\\
>   &\xlongequal{同理}\sum_{i,j}\int_\Omega \phi(\boldsymbol x) \frac{\partial}{\partial x_j}\frac{\partial}{\partial x_j}[q_t(\boldsymbol x) \big(\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top\big)  ]_{ij}\dd{\boldsymbol x}\\
>   &=\int_\Omega \phi(\boldsymbol x) \nabla\cdot\nabla\cdot[q_t(\boldsymbol x) \boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top ]\dd{\boldsymbol x}
>   \end{align}
>   $$
>   故联合法一、法二可得

>   $$
>   \begin{aligned}
>   \frac{\dd U_t}{\dd t}&=\int \frac{\partial q_t(\boldsymbol x)}{\partial t}\phi(\boldsymbol x)\dd {\boldsymbol x}\\&=-\int \phi(\boldsymbol x)\nabla\cdot\big(q_t(\boldsymbol x)\boldsymbol f(\boldsymbol x,t)\big)\dd{\boldsymbol x}+
>   \frac{1}{2}\int \phi(\boldsymbol x) \nabla\cdot\nabla\cdot[q_t(\boldsymbol x)\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top  ]\dd{\boldsymbol x}
>   \end{aligned}
>   $$
>   即

>   $$
>   \int\phi(\boldsymbol x)\bigg[ \frac{\partial q_t(\boldsymbol x)}{\partial t}+
>   \nabla\cdot(q_t(\boldsymbol x)\boldsymbol f(\boldsymbol x,t))\dd{\boldsymbol x}-\frac{1}{2}\nabla\cdot\nabla\cdot[q_t(\boldsymbol x)\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top  ]\bigg]\dd{\boldsymbol x}=0
>   $$
>   由于该式任意二阶可微$\phi$​都成立，故

>   $$
>   \frac{\partial q_t(\boldsymbol x)}{\partial t}+
>   \nabla\cdot\big( q_t(\boldsymbol x)\boldsymbol f(\boldsymbol x,t)\big)\dd{\boldsymbol x}-
>   \frac{1}{2}\nabla\cdot\nabla\cdot[ q_t(\boldsymbol x)\boldsymbol G(\boldsymbol x_t,t)\boldsymbol G(\boldsymbol x_t,t)^\top]=0
>   $$
>   此即FPK方程。

### 证明方式二

参考：[随机动力学（2）---Fokker Planck Kolmogorov 方程](https://zhuanlan.zhihu.com/p/344968725)

>   设随机变量$X=x_{t+\Delta t}-y$，则下列条件概率的密度函数可以用其特征函数变换得到

>   $$
>   q(x,t+\Delta t|y, t)=\frac{1}{2\pi}\int_{-\infty}^{+\infty}e^{-iu(x-y)}\varphi_X(u)\dd x
>   $$
>   其中，特征函数为

>   $$
>   \varphi_X(u)=\int_{-\infty}^{+\infty}e^{iu(x-y)}q(x,t+\Delta t |y,t)\dd x\\
>   =\sum_{n=0}^{+\infty}\frac{(iu)^n}{n!}\mathbb{E}(X_{t+\Delta t}-y)^n\\
>   =\sum_{n=0}^{+\infty}\frac{(iu)^n}{n!}J_n(y,t),\\
>   n阶矩J_n(y,t):=\mathbb{E}(X_{t+\Delta t}-y)^n
>   $$
>   故

>   $$
>   q(x,t+\Delta t|y, t)=\frac{1}{2\pi}\int_{-\infty}^{+\infty}e^{-iu(x-y)}\sum_{n=0}^{+\infty}\frac{(iu)^n}{n!}J_n(y,t)\dd x\\
>   =\sum_{n=0}^{+\infty}\frac{(-1)^n}{n!}J_n(y,t)\frac{1}{2\pi}\int_{-\infty}^{+\infty}e^{-iu(x-y)}(-iu)^n\dd x
>   $$
>   由于

>   $$
>   \delta(x)=\frac{1}{2\pi}\int_{-\infty}^{+\infty}e^{-iux}\dd u\\
>   \delta^{(n)}(x)=\frac{1}{2\pi}\int_{-\infty}^{+\infty}e^{-iux}(-iu)^n\dd u
>   $$
>   故

>   $$
>   q(x,t+\Delta t|y, t)
>   =\sum_{n=0}^{+\infty}\frac{(-1)^n}{n!}J_n(y,t)\delta^{(n)}(x-y)
>   $$
>   由贝叶斯公式可得

>   $$
>   q(x,t+\Delta t)=\int_{-\infty}^{+\infty}q(x,t+\Delta t|y, t)q(y,t)\dd y\\
>   =\int_{-\infty}^{+\infty} \sum_{n=0}^{+\infty}\frac{(-1)^n}{n!}J_n(y,t)\delta^{(n)}(x-y)q(y,t)\dd y\\
>   =\sum_{n=0}^{+\infty}\frac{(-1)^n}{n!}\int_{-\infty}^{+\infty}J_n(y,t)q(y,t)\delta^{(n)}(x-y)\dd y
>   $$
>   由分部积分可知

>   $$
>   \int_{-\infty}^{+\infty}f(y)\delta^{(n)}(x-y)\dd y=\int_{-\infty}^{+\infty}f^{(n)}(y)\delta(x-y)\dd x=f^{(n)}(x)
>   $$
>   故

>   $$
>   q(x,t+\Delta t)=\int_{-\infty}^{+\infty}q(x,t+\Delta t|y, t)q(y,t)\dd y\\
>   =\int_{-\infty}^{+\infty} \sum_{n=0}^{+\infty}\frac{(-1)^n}{n!}J_n(y,t)\delta^{(n)}(x-y)q(y,t)\dd y\\
>   =\sum_{n=0}^{+\infty}\frac{(-1)^n}{n!} \frac{\partial^n}{\partial x^n}\big(J_n(x,t)q(x,t)\big)
>   $$
>   故

>   $$
>   q(x,t+\Delta t)-q(x,t)=\sum_{n=1}^{+\infty}\frac{(-1)^n}{n!} \frac{\partial^n}{\partial x^n}\big(J_n(x,t)q(x,t)\big)
>   $$
>   故

>   $$
>   \frac{\partial q_t(x)}{\partial t}=\lim_{\Delta \rightarrow 0+}\frac{q(x,t+\Delta t)-q(x,t)}{\Delta t}=\sum_{n=1}^{+\infty}\frac{(-1)^n}{n!} \frac{\partial^n}{\partial x^n}\big(a_n(x,t)q(x,t)\big)
>   $$
>   其中，“n阶矩导”（自己起的名字）为

>   $$
>   a_n(x,t):=\lim_{\Delta t \rightarrow 0+}\frac{J_n(x,t)}{\Delta t}=\lim_{\Delta t \rightarrow 0+}\frac{\mathbb{E}[(X_{t+\Delta t}-X_{t})^n|X_t=x]}{\Delta t}\\
>   =\frac{\mathbb{E}\dd x_t^n}{\dd t}|_{x_t=x}
>   $$
>   当$\boldsymbol x_t\in\R^m$时，将m元n阶矩（n阶张量） 和m元n阶导数（n阶张量）逐点相乘再求和（如下式），就是m元泰勒展开式的第n次项

>   $$
>   \boldsymbol a_1(x,t)=\frac{\mathbb{E}\dd {\boldsymbol x}_t^n}{\dd t}\bigg\vert_{\boldsymbol x_t=x}\in\R^{m}\\
>   \boldsymbol A_2(x,t)=\frac{\mathbb{E}\dd {\boldsymbol x}_t \dd {\boldsymbol x}_t^\top}{\dd t}\bigg\vert_{\boldsymbol x_t=x}\in\R^{m\times m}\\
>   \boldsymbol A^{ijk}_3(x,t)=\frac{\mathbb{E}\dd { x}_t^i \dd { x}_t^j\dd { x}_t^k}{\dd t}\bigg\vert_{\boldsymbol x_t=x}\in\R^{m\times m\times m}\\
>   \cdots\\
>   \frac{\partial q_t(x)}{\partial t}=-\sum_i\frac{\partial}{\partial x_i}[a_1^i(\boldsymbol x ,t)q_t(\boldsymbol x)]\\
>   +\frac{1}{2}\sum_{i,j}\frac{\partial^2}{\partial x_i\partial x_j}[a_2^{ij}(\boldsymbol x ,t)q_t(\boldsymbol x)]\\
>   -\frac{1}{3!}\sum_{i,j,k}\frac{\partial^3}{\partial x_i\partial x_j\partial x_k}[a_3^{ijk}(\boldsymbol x ,t)q_t(\boldsymbol x)]+\cdots
>   $$
>   特别地，当$q_t(\boldsymbol x)$是SDE（式$\eqref{sde}$）的解时，

>   $$
>   \begin{align}
>   \boldsymbol a_1&=\frac{\mathbb{E}_{\boldsymbol z}\dd {\boldsymbol x}}{\dd t}=\frac{\mathbb{E}_{\boldsymbol z}[\boldsymbol f\dd t+\boldsymbol G\sqrt{\dd t}\boldsymbol z]}{\dd t}=\boldsymbol f\\
>   \boldsymbol A_2&=\frac{\mathbb{E}_{\boldsymbol z}\dd {\boldsymbol x}\dd{\boldsymbol x}^\top}{\dd t}=\frac{\mathbb{E}_{\boldsymbol z}[(\boldsymbol f\dd t+\boldsymbol G\sqrt{\dd t}\boldsymbol z)(\boldsymbol f\dd t+\boldsymbol G\sqrt{\dd t}\boldsymbol z)^\top]}{\dd t}=\boldsymbol G\boldsymbol G^\top\\
>    \boldsymbol A_n&=\boldsymbol 0\ （\forall n\geq3）, 因为\mathbb{E}_{\boldsymbol z}\dd {\boldsymbol x}^n=O((\dd t)^\frac{n}{2})=o(\dd t) \\
>   \frac{\partial q_t(x)}{\partial t}&=-\sum_i\frac{\partial}{\partial x_i}[a_1^i(\boldsymbol x ,t)q_t(\boldsymbol x)]+\frac{1}{2}\sum_{i,j}\frac{\partial^2}{\partial x_i\partial x_j}[a_2^{ij}(\boldsymbol x ,t)q_t(\boldsymbol x)]\\
>   &=-\nabla\cdot(q_t(\boldsymbol x)\boldsymbol f(\boldsymbol x,t))+\frac{1}{2}\nabla\cdot\nabla\cdot(q_t(\boldsymbol x)\boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t))
>   \end{align}
>   $$
>

### SDE/ODE/FPK方程的解的唯一性

*   若给定初值$q_0(\boldsymbol x)$，FPK方程有唯一解$q_t(\boldsymbol x)$
*   满足同一个FPK方程（或具有同样的$q_t(\boldsymbol x)$）的正向扩散/反向扩散SDE有无穷个

>   比如FPK方程可以做如下变形，任意$\lambda\in\R$：

>   $$
>   \begin{align}
>   \frac{\partial q_t(\boldsymbol x)}{\partial t}
>   &=-\nabla\cdot(q_t(\boldsymbol x)\boldsymbol f(\boldsymbol x,t))+\frac{1}{2}\nabla\cdot\nabla\cdot(q_t(\boldsymbol x)\boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t))\\
>   &=-\nabla\cdot\big[q_t(\boldsymbol x)\boldsymbol f(\boldsymbol x,t)-\frac{\lambda}{2}\nabla\cdot\big(q_t(\boldsymbol x)\boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t)\big)\big]+\frac{1-\lambda}{2}\nabla\cdot\nabla\cdot(q_t(\boldsymbol x)\boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t))\\
>   &=-\nabla\cdot[q_t(\boldsymbol x) \boldsymbol f_\lambda(\boldsymbol x,t) ]+\frac{1}{2}\nabla\cdot\nabla\cdot(q_t(\boldsymbol x)\boldsymbol G_\lambda(\boldsymbol x,t)\boldsymbol G_\lambda^\top(\boldsymbol x,t))
>   \end{align}
>   $$
>   其中，

>   $$
>   \begin{align}
>   \boldsymbol f_\lambda(\boldsymbol x,t)&=\boldsymbol f(\boldsymbol x,t)-\frac{\lambda}{2q^*_t(\boldsymbol x)}\nabla\cdot\big(q^*_t(\boldsymbol x)\boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t)\big)\\
>   \boldsymbol G_\lambda(\boldsymbol x,t)&=\sqrt{1-\lambda}\boldsymbol G(\boldsymbol x,t)
>   \end{align}
>   $$
>   上式中的$q_t^*(\boldsymbol x)$表示变形前的方程的解，于是$\boldsymbol f_\lambda(\boldsymbol x,t)$中不包含待解的函数$q_t(\boldsymbol x)$。
>
>   变形后的FPK方程（虽仍是原来同一个FPK方程，但整理成不同的形式）说明，如下的正向扩散SDE的解也满足上述FPK方程：

>   $$
>   \dd{\boldsymbol{x}_t}=\boldsymbol{f}_\lambda(\boldsymbol{x}_t,t)\dd t+\boldsymbol{G}_\lambda(\boldsymbol{x}_t,t)\dd{\boldsymbol{w}_t}
>   $$
>   同理可证，有无穷个反向扩散SDE满足上述FPK方程同理可证。

*   满足同一个FPK方程（或具有同样的$q_t(\boldsymbol x)$​）的ODE不唯一（怎么给更普遍的证明？）

>   举个例子，若$\boldsymbol \in \R^2, \forall t\in [0,T], q_t(\boldsymbol x)=\mathcal N(\boldsymbol x|\boldsymbol 0,\boldsymbol I)$，也即初值FPK问题$q_0(\boldsymbol x)=\mathcal N(\boldsymbol x|\boldsymbol 0,\boldsymbol  I), \frac{\partial q_t(\boldsymbol x) }{\partial t}=0$。
>
>   此时，ODE可以为

>   $$
>   \dd{ \boldsymbol x}=\left[\begin{gathered}\cos \omega\dd t & -\sin \omega\dd t \\ \sin \omega\dd t & \cos \omega\dd t  \end{gathered}\right] \boldsymbol x- \boldsymbol x\\
>   =\left[\begin{gathered}\cos \omega\dd t -1 & -\sin \omega\dd t \\ \sin \omega\dd t & \cos \omega\dd t-1  \end{gathered}\right] \boldsymbol x\\
>   =\left[\begin{gathered} - \omega^2\dd t^2/2 & - \omega\dd t \\  \omega\dd t & - \omega^2\dd t^2/2 \end{gathered}\right] \boldsymbol x+O(\dd t^3)\\
>   =\left[\begin{gathered} 0 & - \omega \\  \omega &0 \end{gathered}\right] \boldsymbol x \dd t
>   $$
>   满足概率流方程的格式$\eqref{ode-0}$。这个ODE表示粒子（坐标为$\boldsymbol x$）以角速度$\omega$随时间逆时针旋转。因为角速度可以取任意实数，故有无穷种ODE。

## 从正向SDE推ODE

参考：

*   知乎：[扩散模型中的Reverse Time SDE是怎么推导得到的呢](https://www.zhihu.com/question/629085800)

此ODE又叫概率流ODE，适用于同时正反向扩散。名字来源于，它用$x_t$随时间确定性变化的方程，刻画了$q(x_t|x_0)$以及$q_t(x_t)=\int q(x_t|x_0)q_0(x_0)\dd x_0$​随时间的演化。

正向SDE式$\eqref{sde}$的解，满足FPK方程$\eqref{fpk}$，
$$
\begin{align}
\frac{\partial q_t(\boldsymbol x)}{\partial t}
&=-\nabla\cdot(q_t(\boldsymbol x)\boldsymbol f(\boldsymbol x,t))+\frac{1}{2}\nabla\cdot\nabla\cdot(q_t(\boldsymbol x)\boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t))\\
&=-\nabla\cdot\big[q_t(\boldsymbol x)\boldsymbol f(\boldsymbol x,t)-\frac{1}{2}\nabla\cdot\big(q_t(\boldsymbol x)\boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t)\big)\big]\\
&=-\nabla\cdot[q_t(\boldsymbol x) \tilde{\boldsymbol f}(\boldsymbol x,t) ]\label{ode-1}
\end{align}
$$
其中，
$$
\begin{align}
\tilde{\boldsymbol f}(\boldsymbol x,t)
:&=\boldsymbol f(\boldsymbol x,t)-\frac{1}{2q_t(\boldsymbol x_t)}\nabla\cdot\big(q_t(\boldsymbol x) \boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t) \big)\\
&=\boldsymbol f(\boldsymbol x,t)
-\frac{1}{2}  \nabla \log q_t(\boldsymbol x) \cdot \big(\boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t) \big)
-\frac{1}{2} \nabla\cdot\big(\boldsymbol G(\boldsymbol x,t)\boldsymbol G^\top(\boldsymbol x,t)\big)
\end{align}
$$

由于$\eqref{ode-1}$也是一个FPK方程（实际上和原先的PFK是同一个方程，但整理成新形式），也有对应的正向SDE
$$
\dd{ \boldsymbol x_t}=\tilde{\boldsymbol f}(\boldsymbol x,t)\dd t+\boldsymbol 0\dd {\tilde w_t}
$$
这实际上ODE，没有随即项（布朗运动），能给出确定轨迹，因而正向、反向成立。

## 从ODE推逆向 SDE

通用框架下的逆向SDE，最早提出和证明见：

*   Anderson, B.D.O. (1982) ‘Reverse-time diffusion equation models’, *Stochastic Processes and their Applications*, 12(3), pp. 313–326.

下文的推导参考了：[知乎｜扩散模型中的Reverse Time SDE是怎么推导得到的呢](https://www.zhihu.com/question/629085800)

将上述ODE的时间颠倒，令$\bar t=-t$，ODE即变成
$$
\dd{ \boldsymbol x}=\tilde{\boldsymbol f}\dd{t}=-\tilde{\boldsymbol f}\dd {\bar t}
$$
记$\bar{\tilde{\boldsymbol f}}=-\tilde{\boldsymbol f}=-\boldsymbol f+\dfrac{1}{2 q}\nabla\cdot(q \boldsymbol G\boldsymbol G^\top )$，则对于逆向过程（$\dd t<0$，即$\dd{\bar t}>0$），有时间颠倒的ODE
$$
\dd{ x} = \bar{\tilde {\boldsymbol f}}\dd t
$$

时间颠倒的ODE所对应的FPK方程为
$$
\begin{align}
\frac{\partial}{\partial \bar t}q
&=-\nabla\cdot(q\bar{\tilde {\boldsymbol f}})\\
&=-\nabla\cdot\big[q\big(-\boldsymbol f+\frac{1}{2 q}\nabla\cdot(q \boldsymbol G\boldsymbol G^\top )\big)\big]\\
&=-\nabla\cdot\big[q\big(-\boldsymbol f+\frac{1}{ q}\nabla\cdot(q \boldsymbol G\boldsymbol G^\top )\big)-\nabla\cdot(q \boldsymbol G\boldsymbol G^\top )\big)\big]\\
&=-\nabla\cdot\big[q\big(-\boldsymbol f+\frac{1}{ q}\nabla\cdot(q \boldsymbol G\boldsymbol G^\top )\big)\big]
+\frac{1}{2}\nabla\cdot\nabla\cdot(q\boldsymbol G\boldsymbol G^\top )\\
&=-\nabla\cdot\big(q(-\bar{\boldsymbol f})\big)
+\frac{1}{2}\nabla\cdot\nabla\cdot(q\boldsymbol G\boldsymbol G^\top ),\\
&\quad 其中\bar {\boldsymbol f}:= \boldsymbol f-\frac{1}{ q}\nabla\cdot(q \boldsymbol G\boldsymbol G^\top )
\end{align}
$$
变形后，仍符合FPK方程，有对应的SDE，
$$
\dd x=-\bar {\boldsymbol f}\dd{\bar t}+\boldsymbol G\dd w,\\
$$
再将时间颠倒回来，$\dd{t}=-\dd {\bar t}<0$，则
$$
\dd x=\bar {\boldsymbol f}\dd t+\boldsymbol G\dd w,\\
\bar {\boldsymbol f}:= \boldsymbol f-\frac{1}{ q}\nabla\cdot(q \boldsymbol G\boldsymbol G^\top )
$$

此即逆向SDE。


## 从正向SDE推导直达概率:  $a_t,b_t\Leftarrow f(t),g(t)$

在DDPM的前传过程中，前传SDE为：

$$
\dd {\boldsymbol x_t} =f(t)\boldsymbol x_t\dd t+g(t)\dd {\boldsymbol w_t}, {\boldsymbol w_t}是标准布朗运动
$$

式中$\boldsymbol x_t, {\boldsymbol w_t}\in\R^n, f,g:\R\mapsto \R$。

其通解为

$$
\boldsymbol x_t = a_t \boldsymbol x_0 +  b_t \boldsymbol z, \boldsymbol z\sim N(0,I),
$$
或表示成直达概率
$$
p(\boldsymbol x_t|\boldsymbol x_0)=\mathcal N(\boldsymbol x_t|a_t \boldsymbol x_0, b_t I),
$$
其中$a_t,b_t,c_t:\R\mapsto \R$
$$
a_t:= \exp \int_0^t f(\tau)\dd \tau\\
  c_t^2:=\int_0^t \frac{g^2(\tau)}{a_{\tau}^2}\dd \tau\\
  b_t:=a_t c_t \label{eq:pt0}
$$

若已知$a_t,b_t$，想反向求$f(t),g(t)$：
$$
f(t)=\frac{\dd{}}{\dd t}\ln a_t
g^2(t)=a^2_t\frac{\dd{} }{\dd t}\frac{b_t^2}{a_t^2}=-2b_t^2\frac{\dd{\lambda_t}}{\dd t}
$$
其中半对数SNR（信噪比）:
$$
\lambda_t:=\ln\frac{a_t}{b_t}
$$

**注：**
上述所有结论，可由从$x_0$求$x_t$，**推广至从$x_s$求$x_t$，只需将$a_t,c_t$的积分下界由$0$变为$s$ 即可**，如此就能得到$a_{t|s},c_{t|s},b_{t|s}$。

**证明：**

* 当$g(t)\equiv 0$，方程变为
  $$
  \dd {\boldsymbol x_t} =f(t)\boldsymbol x_t\dd t
  $$
  化简为
  $$
  \dd \ln \boldsymbol x_t = f(t)\dd t
  $$
  通解为
  $$
  \boldsymbol x_t = a_t \boldsymbol x_0,\\
  a_t := \exp \int_0^t f(\tau)\dd \tau
  $$
  有性质
  $$
  a_{0}=1\\
  \dd a_t=a_t f(t)\dd t\\
  \frac{\boldsymbol x_t}{a_t}=\frac{\boldsymbol x_0}{a_0}=\text{const.}
  $$
  由这些性质可以推导回ODE：
  $$
  \frac{\boldsymbol x_t}{a_t}=\frac{\boldsymbol x_0}{a_0}=\text{const.}\Rightarrow \dd{} \frac{\boldsymbol x_t}{a_t}=0\Rightarrow a_t\dd {\boldsymbol x_t}-\boldsymbol x_t \dd a_t=0\Rightarrow \dd {\boldsymbol x_t}=f(t)\boldsymbol x_t\dd t
  $$

* 当$g(t)\not\equiv 0$，$\dfrac{\boldsymbol x_t}{a_t}$将不再是常数，设其为辅助变量$\boldsymbol y_t:=\dfrac{\boldsymbol x_t}{a_t}$，将关于$\boldsymbol x_t$的正向SDE转化为关于$\boldsymbol y_t$的SDE，即可直观引入$\dd{\boldsymbol w_t}$造成了什么变化。

    使用上述性质，原前向SDE变为
    $$
    \begin{align}
    \dd ({a_t \boldsymbol y_t} )&= \boldsymbol y_t a_t f(t)\dd t+g(t)\dd {\boldsymbol w_t}\\
            &= \boldsymbol y_t \dd a_t +g(t)\dd {\boldsymbol w_t}\\
           a_t \dd{ \boldsymbol y_t} &=g(t)\dd {\boldsymbol w_t}\\
    \dd {\boldsymbol y_t} &=\frac{g(t)}{a_t}\dd {\boldsymbol w_t}\\
    \dd {\frac{\boldsymbol x_t}{a_t}} &=\frac{g(t)}{a_t}\dd {\boldsymbol w_t}\\
    \end{align}
    $$
    故通解为
    $$
    \frac{\boldsymbol x_t}{a_t}-\frac{\boldsymbol x_0}{a_{0}}=c_t \boldsymbol z, \boldsymbol z\sim N(0,I),\\
    c_t^2:=\int_0^t \frac{g^2(\tau)}{a_{\tau}^2}\dd \tau, c_t>0
    $$
    利用性质$a_{0}=1$，化简即得通解为
    $$
    \boldsymbol x_t=a_t \boldsymbol x_0+a_tc_t\boldsymbol z , \boldsymbol z\sim N(0,I)
    $$
    记$b_t:=a_t c_t$，则通解得证。

* 若已知$a_t,b_t$，想反向求$f(t),g(t)$：

    由上面的关系式，显然有
    $$
    f(t)=\frac{\dd{}}{\dd t}\ln a_t\\
    g^2(t)=a^2_t\frac{\dd{} }{\dd t}\frac{b_t^2}{a_t^2}
    $$
    只需再证明
    $$
    a^2_t\frac{\dd{} }{\dd t}\frac{b_t^2}{a_t^2}=-2b_t^2\frac{\dd{\lambda_t}}{\dd t}
    $$
    证：
    $$
    \log \frac{a_t}{b_t}=:\lambda_t\\
    \frac{b_t^2}{a_t^2}=e^{-2\lambda_t}\\
    \frac{\dd{}}{\dd t}\frac{b_t^2}{a_t^2}=\frac{\dd{}}{\dd t}e^{-2\lambda_t}=-2 \frac{\dd \lambda_t}{\dd t} e^{-2\lambda_t}=-2 \frac{\dd \lambda_t}{\dd t} \frac{b_t^2}{a_t^2}\\
    g_t^2=a_t^2 \frac{\dd{}}{\dd t}\frac{b_t^2}{a_t^2}=-2b_t^2\frac{\dd \lambda_t}{\dd t}
    $$


# 特例

本章将讲在DDPM正传设定（见下）下，不借助上一章的理论推导，直接“推出”正向SDE、反向SDE和ODE在该设定下的特殊形式。请注意，这种“推出”颠倒了条件和结论的关系，在逻辑上其实不成立，仅为这些SDE/ODE提供启发式的理解。严格推导这些SDE/ODE还是得按照上一章。

## DPM的设定

**DPM正向扩散的正向SDE**为，$\forall 0 \leq t\leq T$，
$$
\dd{\boldsymbol{x}_t}=f(t)\boldsymbol{x}_t\dd t+g(t) \dd {\boldsymbol{w}_t},\label{eq:dxfg}
$$
漂移系数(shift coefficient)$ af(t)\in \R$，扩散系数(diffusion coefficient)$ g(t)\in \R$。

**DPM正向扩散的条件概率分布**为，$\forall 0\leq s<t\leq T$，
$$
q(\boldsymbol{x}_t|\boldsymbol{x}_s)=N(\boldsymbol{x}_t|a_{st}\boldsymbol{x}_s,b_{st}^2\boldsymbol{I}),\label{eq:pxtxs}
$$
其中，$\boldsymbol{x}_t\in\R^m, t\in[0,T]$。

**无条件概率**
$$
训练集来自q_0(\boldsymbol x_0)\\
q_t(\boldsymbol x_t)=\int q(\boldsymbol x_t|\boldsymbol x_s)q_0(\boldsymbol x_0)\dd {\boldsymbol x_0}\\
q_T(\boldsymbol x_T)\approx N(\boldsymbol x_T|\boldsymbol0,\boldsymbol b_T^2 I)
$$

## DDPM使用的设定: VP/MR-VP

* VP：向上文的DPM$\eqref{eq:pxtxs}$通用设定，引入以下假设，就是VP (Variance Preserving)问题：
  $$
  a_{st}^2+b_{st}^2=1, \forall 0\leq s<t\leq T, \label{eq:ast2bst2}
  $$
  即
  $$
  q(\boldsymbol{x}_t|\boldsymbol{x}_s)=N(\boldsymbol{x}_t|a_{st}\boldsymbol{x}_s,(1-a_{st}^2)\boldsymbol{I})
  $$
  DDPM等论文用此设定，记号为$a_{0t}^2=\bar\alpha_t,b_{0t}^2=\bar\beta_t$。
* MR-VP：向正向SDE$\eqref{eq:dxfg}$，引入以下假设，就是MR-VP (Mean Reverting Variance Preserving)问题：
  $$
  f(t)=-\frac 1 2 g^2(t)
  $$
  即
  $$
  \dd{\boldsymbol{x}_t}=-\frac 1 2 g^2(t)\boldsymbol{x}_t\dd t+g(t) \dd {\boldsymbol{w}_t},
  $$
  DDDM-VC等论文用此设定，记号为$f(t)=-\frac{1}{2}\beta_t, g^2(t)=\beta_t$。

* VP等价于MR-VP。证明如下：

  VP=>MR-VP: 由式$\eqref{eq:ab-fg}$有，
  $$
  g^2(t)=a^2_{t}\frac{\dd{}}{\dd t}\frac{b^2_{t}}{a^2_{t}}\\
  =a^2_{t}\frac{\dd{}}{\dd t}\frac{1-a^2_{t}}{a^2_{t}}\quad  //代入\eqref{eq:ast2bst2}\\
  =a^2_{t}\frac{\dd{}}{\dd t}\frac{1}{a^2_{t}}=-\frac 2 {a_{t}}\frac{\dd a_{t}}{\dd t}=-2\frac{\dd{}}{\dd t}\log a_{t}=-2f(t)
  $$
  故
  $$
  f(t)=-\frac 1 2 g^2(t)
  $$


### MR-VP方程

正向SDE：
$$
\dd x_t=-\frac{1}{2}\beta_t x_t \dd t+\sqrt{\beta_t}\dd w_t
$$
直达概率：
$$
x_t\sim N\big(a_{t|s} x_s, (1-a^2_{t|s})I\big )\\
a_{t|s}=e^{-\frac 1 2\int_s^t \beta_\tau\dd \tau}
$$

>   证明：向直达概率通式 即式$\eqref{eq:pt0}$带入上述设定，并不妨令$s=0$，则有

>   $$
>   x_t=a_t x_0+b_t z, z\sim N(0,I),其中\\
>   a_t=e^{-\frac{1}{2}\int_0^t\beta_\tau\dd\tau}\\
>   c^2_t=\int_0^t \frac{g^2(s)}{a_s^2}\dd s= \int_0^t e^{\int_0^s\beta_\tau\dd\tau}\beta_s \dd s = \int_0^t \dd (e^{\int_0^s\beta_\tau\dd\tau})=e^{\int_0^s\beta_\tau\dd\tau}\big|_0^t=e^{\int_0^t\beta_\tau\dd\tau}-1\\
>   b^2_t=a^2_tc^2_t=e^{-\int_0^t\beta_\tau\dd\tau}(e^{\int_0^t\beta_\tau\dd\tau}-1)=1-e^{-\int_0^t\beta_\tau\dd\tau}=1-a_t^2\\
>  故a_t^2+b^2_t=1
>   $$

ODE：
$$
\dd x_t=-\frac{1}{2}\beta_t[x_t+\nabla\log q(x_t)]\dd t
$$

>   证明：ODE通式为

>   $$
>   \dd x_t=[f(t)x_t-\frac 1 2 g^2(t)\nabla \log q(x_t)]\dd t
>   $$
>   代入上面系数，得到

>   $$
>   \dd x_t=[-\frac{1}{2}\beta_t x_t-\frac 1 2\beta_t \nabla\log q(x_t)]\dd t+\sqrt{\beta_t}\dd {\bar{w}_t}\\
>   =-\frac{1}{2}\beta_t[x_t+\nabla\log q(x_t)]\dd t+\sqrt{\beta_t}\dd {\bar w_t}
>   $$

逆向SDE：
$$
\dd x_t=-\beta_t[\frac{1}{2}x_t+\nabla\log q(x_t)]\dd t+\sqrt{\beta_t}\dd {\bar w_t}
$$

>   证明：逆向SDE通式为

>   $$
>   \dd x_t=[f(t)x_t-g^2(t)\nabla \log q(x_t)]\dd t+g(t)\dd {\bar{w}_t}
>   $$
>   代入上面系数，得到

>   $$
>   \dd x_t=[-\frac{1}{2}\beta_t x_t-\beta_t \nabla\log q(x_t)]\dd t+\sqrt{\beta_t}\dd {\bar{w}_t}\\
>   =-\beta_t[\frac{1}{2}x_t+\nabla\log q(x_t)]\dd t+\sqrt{\beta_t}\dd {\bar w_t}
>   $$


### DDPM正传是正SDE在离散时间上的精确变形

从DDPM正传的迭代公式，相当于在精确的正向SDE（式$\eqref{ddpm-sde}$）中用$\Delta t=1$代替$\dd t$。从从DDPM正传的迭代公式（下式）出发，把$\Delta t$换成$\dd t$也可以推导出一个SDE，但那是近似的正向SDE，而非精确的。
$$
x_t=\sqrt{\alpha_t} x_{t-1}+\sqrt{\beta_t} z, \quad z \sim N(\mathbf{0}, \mathbf{I})
$$
由于在DDPM的原论文中，$\beta_t$的取值设定是，将$\beta_1= 10^{−4}$ 到$\beta_T = 0.02$线性等分。因此，当$T\rightarrow +\infty$时，有$ \forall t\geq 0, \beta_t\ll 1$。故上式近似为
$$
\begin{align}
x_t&=\sqrt{1-\beta_t} x_{t-1}+\sqrt{\beta_t} z\\
x_t&\approx\left(1-\frac{1}{2} \beta_t \right) x_{t-1}+\sqrt{\beta_t } z，若T\rightarrow +\infty\\
&=(1-\beta_t \Delta \mathrm{t}) x_{t-\Delta \mathrm{t}}+\sqrt{\beta_t \Delta \mathrm{t}} z, \Delta t=1 \\
\xLeftarrow[时间离散化]{一阶近似}  \mathrm{d} x_t&=-\frac{1}{2} \beta_t x_t \mathrm{~d} t+\sqrt{\beta_t \mathrm{~d} t} z\\
\Leftrightarrow \dd x_t&=-\frac{1}{2} \beta_t x_t \mathrm{~d} t+\sqrt{\beta_t}\dd \omega_t,\label{ddpm-sde2}\\
&\quad \quad \dd\omega_t:=\sqrt{\mathrm{d} t}z, \omega_t 是一个标准布朗运动（又名标准Wiener过程） \\
\Leftrightarrow d x_t \vert x_t &\sim N\left(-\frac{1}{2} \beta_t x_t \mathrm{~d} t, \beta_t \mathrm{~d} t \mathbf{I}\right)
\end{align}
$$

这是一个随机微分方程 (SDE) ）, 是马尔可夫过程，称作伊藤(Itô)过程或扩散过程。

**上式$\eqref{ddpm-sde2}$ 是 精确的正向SDE（式$\eqref{ddpm-sde}$）的近似形式**，证明如下。

>   证明：
>
>   只需证

>   $$
>   -\frac{1}{2}\beta_t\approx f_t,\beta_t\approx g_t^2 \label{approx-sde}
>   $$
>
>   1. 证明$-\frac{1}{2}\beta_t\approx f_t$​：
>
>   仿照式$\eqref{coef}$的推导方式，有

>   $$
>   \beta_t=\bar{\beta_t}-\alpha_t\bar\beta_{t-1}=\bar{\beta_t}-\frac{\bar\alpha_t}{\bar\alpha_{t-1}}\bar\beta_{t-1}
>   $$
>   由于DDPM有特定的约束条件，$\bar\alpha_t+\bar\beta_t=1$，故上式继续化简为

>   $$
>   \beta_t=\bar{\beta_t}-\alpha_t\bar\beta_{t-1}=(1-\bar\alpha_t)-\frac{\bar\alpha_t}{\bar\alpha_{t-1}}(1-\bar\alpha_{t-1})\\
>   =\frac{\bar\alpha_{t-1}-\bar\alpha_{t}}{\bar\alpha_{t-1}}\\
>   \xlongequal{若\Delta t=1}\frac{\bar\alpha_{t-\Delta t}-\bar\alpha_{t}}{\bar\alpha_{t-\Delta t}\Delta t}\Delta t\\
>   \xlongequal{若\Delta t =\dd t}-\frac{\dd \log \bar \alpha_t}{\dd t}\dd t\\
>   =-\frac{\dd \log a^2_t}{\dd t}\dd t=-2\frac{\dd \log a_t}{\dd t}\dd t=-2 f_t\dd t
>   $$
>   故

>   $$
>   -\frac{1}{2}\beta_t\approx f_t\Delta t\vert_{\Delta t=1}=f_t
>   $$
>
>   2. 证明$\beta_t\approx g_t^2$​：
>
>   由于

>   $$
>   \bar\beta_t=b_t^2\\
>   \bar\alpha_t=a_t^2
>   $$
>   故

>   $$
>   \beta_t=\bar{\beta_t}-\alpha_t\bar\beta_{t-1}=b_t^2-\frac{a_t^2}{a_{t-1}^2}b_{t-1}^2\\
>   =\frac{a_{t-1}^2b_t^2-a_t^2b_{t-1}^2}{a_{t-1}^2}\\
>   \xlongequal{若\Delta t=1}\frac{a_{t-\Delta t}^2b_t^2-a_t^2b_{t-\Delta t}^2}{a_{t-\Delta t}^2\Delta t}\Delta t\\
>   \xlongequal[推导同\eqref{coef-g}]{若\Delta t=\dd t}-2b_t^2\frac{\dd\lambda_t}{\dd t}\dd t
>   =g_t^2\dd t
>   $$
>   故

>   $$
>   \beta_t\approx g_t^2 \Delta t\vert_{\Delta t=1}=g_t^2
>   $$


### DDPM反传是逆向SDE的一阶近似

DDPM反传的迭代公式为
$$
\boldsymbol{x}_{t-1}=\frac{1}{\sqrt{\alpha_t}}\left(\boldsymbol{x}_t-\frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}\boldsymbol{\epsilon}_\theta(\boldsymbol x_t,t)\right)+\sigma_t\boldsymbol{z},\boldsymbol{z}\sim\mathcal{N}(\boldsymbol{0},\boldsymbol{I})\\

\sigma_t=\frac{1-\bar{\alpha}_{t-1}}{1-\bar{\alpha}_t}\beta_t\approx \beta_t
$$
故
$$
\boldsymbol{x}_{t-1}-\boldsymbol{x}_{t}=(\frac{1}{\sqrt{\alpha_t}}-1)\boldsymbol{x}_t-\frac{1}{\sqrt{\alpha_t}}\frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}\boldsymbol{\epsilon}_\theta(\boldsymbol x_t,t)+\sigma_t\boldsymbol{z}
$$
记$\Delta t=-1<0,\Delta \boldsymbol x_t=\boldsymbol x_{t-\Delta t}-\boldsymbol x_t$
$$
\Delta x_t=(\frac{1}{\sqrt{1-\beta_t}}-1)\boldsymbol x_t-\frac{1}{\sqrt{1-\beta_1}}\frac{\beta_t}{b_t}\boldsymbol \epsilon_\theta(\boldsymbol x_t,t)+\sigma_t\boldsymbol z\\
\approx -\frac{\beta_t}{2}\boldsymbol x_t\Delta t+(1-\frac{\beta_t}{2})\frac{\beta_t}{b_t}\boldsymbol \epsilon_\theta(\boldsymbol x_t,t)\Delta t+\sqrt{\beta_t}\sqrt{\Delta t}\boldsymbol z,舍去O(\beta_t^2)\\
\approx (-\frac{\beta_t}{2}\boldsymbol x_t+\frac{\beta_t}{b_t}\epsilon_\theta(\boldsymbol x_t,t))\Delta t+\sqrt{\beta_t}\sqrt{\Delta t}\boldsymbol z， 舍去O(\beta_t^2)
$$
将$\Delta t$ 替换为$\dd t$​，即近似逆向SDE，是上式的一阶近似
$$
\dd{ \boldsymbol x_t}=(-\frac{\beta_t}{2}\boldsymbol x_t+\frac{\beta_t}{b_t}\boldsymbol\epsilon_\theta(\boldsymbol x_t,t))\dd t++\sqrt{\beta_t}\dd{\boldsymbol w_t}
$$
近似正向SDE($\eqref{ddpm-sde2}$)带入 逆向SDE的公式$\eqref{diffusion-rev-sde}$，恰好就得到上式。

其中，$-\frac{\beta_t}{2}\approx f_t, \beta_t\approx g_t^2$的证明详见$\eqref{approx-sde}$的证明过程。




## 推导正向SDE

### 非条件系数和条件系数的关系

用重参数化的方式可以推出，$\forall 0\leq s<t\leq T$，
$$
q(\boldsymbol{x}_t|\boldsymbol{x}_0)=N(\boldsymbol{x}_t|a_t \boldsymbol x_0, b_t^2 \boldsymbol I)
$$

$$
a_t:=a_{0t},b_t:=b_{0t}
$$

定义，
$$
信号强度:=a_t^2\\
噪声强度:=b_t^2\\
信噪比SNI:=\frac{a_t^2}{b_t^2}\\
半对数信噪比\lambda_t=\frac{1}{2}\log SNI=\log \frac{a_t}{b_t}
$$
非条件系数和条件系数有如下关系
$$
a_{t}=a_s a_{st}, b_{t}^2=a_{st}^2b_s^2+b_{st}^2\label{coef}
$$

>   证明：
>
>   将 $q(\boldsymbol x_t|\boldsymbol x_s)$和 $q(\boldsymbol x_s|\boldsymbol x_0)$和 重参数化

>   $$
>   \boldsymbol x_{t}=a_{st}\boldsymbol x_s+b_{st}\boldsymbol z_{st}, \boldsymbol z_{st}\sim N(\boldsymbol 0,\boldsymbol I)\\
>
>   \boldsymbol x_{s}=a_{s}\boldsymbol x_0+b_{s}\boldsymbol z_{st}, \boldsymbol z_{s}\sim N(\boldsymbol 0,\boldsymbol I)\\
>   $$
>   下式带入上式，得

>   $$
>   \boldsymbol x_t=a_s a_{st} \boldsymbol x_0+a_{st}b_s \boldsymbol  z_s+b_s \boldsymbol z_{st}
>   $$
>   由于 $\boldsymbol z_{st}$和$\boldsymbol z_{s}$ 独立，故

>   $$
>   \boldsymbol x_t=a_s a_{st} \boldsymbol x_0+ \sqrt{a_{st}^2b_s^2+b_{st}^2} \boldsymbol z, \boldsymbol z\sim N(\boldsymbol 0,\boldsymbol I)
>   $$
>   和$q(\boldsymbol{x}_t|\boldsymbol{x}_0)=N(\boldsymbol{x}_t|a_t \boldsymbol x_0, b_t^2 \boldsymbol I)$对比，即得

>   $$
>   a_{t}=a_s a_{st}, b_{t}^2=a_{st}^2b_s^2+b_{st}^2
>   $$

### 从直达概率推正向SDE系数: $a_t,b_t\Rightarrow f(t),g(t)$

正向SDE为
$$
\dd {\boldsymbol x_t}=f_t\boldsymbol x_t\dd t+g_t\dd{\boldsymbol w_t}\label{ddpm-sde}
$$
概率分布系数和正向ODE系数的关系为
$$
f_t=\frac{\dd{\log a_t}}{\dd t}\\
g_t^2=-2b_t^2\frac{\dd{\lambda_t}}{\dd t}=b_t^2 \frac{\dd{} }{\dd t}\log\frac{b_t^2}{a_t^2}=a_t^2 \frac{\dd {}}{\dd t} \frac{b_t^2}{a_t^2} \label{eq:ab-fg}
$$

即正向SDE为
$$
\dd {\boldsymbol x_t}=\frac{\dd{\log a_t}}{\dd t}\boldsymbol x_t\dd t-2b_t^2\frac{\dd{\lambda_t}}{\dd t}\dd{\boldsymbol w_t}
$$

说明：上述关系，等价于 从正向SDE推导直达概率: $a_t,b_t\Leftarrow f(t),g(t)$ 的 式$\eqref{eq:pt0}$。

>   证明：

>   $$
>   \boldsymbol x_t=a_{st}\boldsymbol x_s+b_{st}\boldsymbol z_{st}, \boldsymbol z_{st}\sim N(\boldsymbol 0,\boldsymbol I)
>   $$
>
>   带入$\eqref{coef}$，即得

>   $$
>   \boldsymbol x_t-\boldsymbol x_s=(a_{st}-1)\boldsymbol x_s+b_{st}\boldsymbol z_{st}\\
>   =(\frac{a_t}{a_s}-1)\boldsymbol x_s+\sqrt{ b_{t}^2-a_{st}^2b_s^2}\boldsymbol z_{st}\\
>   =\frac{a_t-a_s}{a_s}\boldsymbol x_s+\sqrt{ b_{t}^2-\frac{a_{t}^2}{a_s^2}b_s^2}\boldsymbol z_{st}\\
>   =\frac{a_t-a_s}{a_s}\boldsymbol x_s+\sqrt{\frac{a_s^2 b_{t}^2 - a_t^2b_s^2}{a_s^2}}\boldsymbol z_{st}
>   $$
>   取$t$为$t+\Delta t$, 取$s$ 为$t$​​，则有

>   $$
>   \boldsymbol x_{t+\Delta t}-\boldsymbol x_t=
>   \frac{a_{t+\Delta t}-a_t}{a_t }\boldsymbol x_t +
>   \sqrt{\frac{a_t^2 b_{t+\Delta t}^2 - a_{t+\Delta t}^2b_t^2}{a_t^2}}\boldsymbol z_{st}
>   $$
>   上式中各项分别取极限：

>   $$
>   \begin{align}
>   \boldsymbol x_{t+\Delta t}-\boldsymbol x_t&= \frac{\dd {\boldsymbol x_t}}{\dd t}\Delta t+O(\Delta^2)\\
>   \frac{a_{t+\Delta t}-a_t}{a_t }&=\frac{\dd{\log a_t}}{\dd{t} }\Delta t+O(\Delta^2) \\
>
>
>   \frac{a_t^2 b_{t+\Delta t}^2 - a_{t+\Delta t}^2b_t^2}{a_t^2}&=\frac{a_t^2 b_{t+\Delta t}^2 -a_t^2b_t^2+a_t^2b_t^2 - a_{t+\Delta t}^2b_t^2}{a_t^2}\\
>   &=\frac{a_t^2 (b_{t+\Delta t}^2 -b_t^2)-(a_t^2-a_{t+\Delta t}^2)b_t^2}{a_t^2}\\
>   &= (2 b_t \frac{\dd{b_t}}{\dd{t}} - 2\frac{b_t^2\dd{a_t}}{a_t\dd{t}})\Delta t +O(\Delta t^2)\\
>   &=2b_t^2(\frac{\dd{\log b_t}}{\dd{t}} -\frac{\dd{\log a_t}}{\dd{t}})\Delta t +O(\Delta t^2)\\
>   &=-2b_t^2 \frac{\dd{} }{\dd t}\log \frac{a_t}{b_t}\Delta t +O(\Delta t^2)\\
>   &=-2b_t^2 \frac{\dd{} }{\dd t}\lambda_t\Delta t +O(\Delta t^2)\label{coef-g}\\
>   &=-2b_t^2 \frac{\dd{} }{\dd t}\lambda_t(\Delta t +O(\Delta t^2))
>   \end{align}
>   $$
>   带入上式可得

>   $$
>   \begin{align}
>   \frac{\dd{\boldsymbol x_t}}{\dd t}\Delta t&=
>   \frac{\dd{\log a_t}}{\dd t}\Delta t+O(\Delta t^2)+\sqrt{-2b_t^2\frac{\dd\lambda_t}{\dd t}(\Delta t+O(\Delta t^2))}\boldsymbol z_{st}\\
>   &=\frac{\dd{\log a_t}}{\dd t}\Delta t+O(\Delta t^2)+\sqrt{-2b_t^2\frac{\dd\lambda_t}{\dd t}}\sqrt{1+O(\Delta t)}\sqrt{\Delta t}\boldsymbol z_{st}\\
>   &=\frac{\dd{\log a_t}}{\dd t}\Delta t+O(\Delta t^2)+\sqrt{-2b_t^2\frac{\dd\lambda_t}{\dd t}}(1+O(\Delta t))\sqrt{\Delta t}\boldsymbol z_{st}\\
>   &=\frac{\dd{\log a_t}}{\dd t}\Delta t+O(\Delta t^2)+\sqrt{-2b_t^2\frac{\dd\lambda_t}{\dd t}}\sqrt{\Delta t}\boldsymbol z_{st}+O(\Delta t^\frac{3}{2})\\
>   &=\frac{\dd{\log a_t}}{\dd t}\Delta t+\sqrt{-2b_t^2\frac{\dd\lambda_t}{\dd t}}\Delta \boldsymbol w_t+o(\Delta t),\\
>   &\quad \quad 其中\Delta \boldsymbol w_t:=\boldsymbol w_{t+\Delta t}-\boldsymbol w_t\sim N(\boldsymbol 0,\Delta t\boldsymbol I)
>   \end{align}
>   $$
>   因此，当 $\Delta t$取微分$\dd t$时，上式只保留$\Delta t$​的**一阶或更低阶项**，因而化为如下微分方程

>   $$
>   \dd {\boldsymbol x_t}=\frac{\dd \log a_t}{\dd t}\boldsymbol x_t\dd t+\sqrt{-2b_t^2\frac{\dd \lambda_t}{\dd t}}\dd{\boldsymbol w_t}
>   $$
>   即

>   $$
>   \dd {\boldsymbol x_t}=f_t\boldsymbol x_t\dd t+g_t\dd{\boldsymbol w_t}\\
>   f_t=\frac{\dd{\log a_t}}{\dd t}\\
>   g_t^2=-2b_t^2\frac{\dd{ \lambda_t}}{\dd{t}}
>   $$
> 故对$g_t^2$变形得，

> $$
> g_t^2=-2b_t^2\frac{\dd{\lambda_t}}{\dd t}=b_t^2 \frac{\dd{} }{\dd t}\log\frac{b_t^2}{a_t^2}=a_t^2 \frac{\dd {}}{\dd t} \frac{b_t^2}{a_t^2}
> $$

## 推导ODE

由上文通用框架中的ODE$\eqref{ode}$，取$\boldsymbol f(\boldsymbol x_t,t)=f_t\boldsymbol x_t, \boldsymbol G(\boldsymbol x_t,t)=g_t\boldsymbol I$，并代入$\nabla_{\boldsymbol x_t}\log q_t(\boldsymbol x_t)\approx -\dfrac{\epsilon_\theta(\boldsymbol x_t,t)}{b_t}$，即得diffusion模型的ODE为
$$
\begin{align}
概率流ODE：\frac{\dd{\boldsymbol x}_t}{\dd t}&=f_t\boldsymbol x_t-\frac{1}{2}g^2_t\nabla_{\boldsymbol x_t}\log q_t(\boldsymbol x_t)\label{diffusion-ode}, \boldsymbol x_t是概率建模的对象\\
\Rightarrow DDIM采样过程ODE：\frac{\dd{\hat{\boldsymbol x}}_t}{\dd t} & = f_t \hat{\boldsymbol x}_t+\frac{g^2_t}{2b_t}\epsilon_\theta(\hat{\boldsymbol x}_t,t),\hat{\boldsymbol x}_t是采样得到的\\
f_t&=\frac{\dd{\log a_t}}{\dd t}\\
g_t^2&=-2b_t^2\frac{\dd{ \lambda_t}}{\dd{t}}\\
即\frac{\dd{\hat{\boldsymbol x}}_t}{\dd t} & = \frac{\dd{\log a_t}}{\dd t} \hat{\boldsymbol x}_t-b_t\frac{\dd{ \lambda_t}}{\dd{t}}\epsilon_\theta(\hat{\boldsymbol x}_t,t)
\end{align}
$$

从此ODE可以推导出DDIM使用的反传迭代公式。

DDIM正向过程 ( 加噪 ) $q(x_t \mid x_0) =\mathcal{N}\left(x_t\mid \sqrt{\bar{\alpha}_t} x_0 ，\left(1-\bar{\alpha}_t\right) \mathbf{I}\right)$ 不是马尔可夫过程，和DDPM不同。

不论DDPM还是DDIM，它们正向过程的条件概率$q(x_t \mid x_0)$是一样的，都能用概率流ODE（式$\eqref{diffusion-ode}$）去刻画$q(x_t \mid x_0)$随时间的演化。

### DDIM反是ODE的一阶近似

DDIM采样会跳步数，即通常步长$\Delta t>1$

$$
\begin{align}
x_{\tau}&=\frac{a_\tau}{a_t}x_t-(\frac{a_\tau}{a_t}b_t-b_\tau)\epsilon_\theta(x_t,t),\tau=t-\Delta t \\
\Leftrightarrow \frac{x_{\tau}}{a_{\tau}}&=\frac{x_t}{a_t}+\left( \frac{b_{\tau}}{a_{\tau}}- \frac{b_t}{a_t}\right) \epsilon_\theta\left(x_t, t\right),\tau=t-\Delta t \\
\xLeftarrow[时间离散化]{一阶近似} \frac{\dd{} }{\dd t}(\frac{x_t}{a_t})&=\epsilon_\theta(x_t,t)\frac{\dd{}  }{\dd t}(\frac{b_t}{a_t})\label{diffusion-ode2}
\end{align}
$$

详见：扩散模型之DDIM https://zhuanlan.zhihu.com/p/565698027

**该方程和ODE的式$\eqref{diffusion-ode}$等价**

>   证明：
>
>   式$\eqref{diffusion-ode2}$等价于

>   $$
>   \frac{\dd{}}{\dd t}{\frac{\boldsymbol x_t}{a_t}}=\epsilon_\theta(\boldsymbol x_t,t)\dd e^{-\lambda_t}
>   $$
>   即

>   $$
>   \frac{\dd {\boldsymbol x_t}}{a_t\dd t}-\boldsymbol x_t \frac{\dd a_t}{a_t^2\dd t}
>   =-\epsilon_\theta(\boldsymbol x_t ,t )e^{-\lambda_t}\frac{\dd \lambda_t}{\dd t}
>   $$
>   即

>   $$
>   \frac{\dd {\boldsymbol x_t}}{\dd t}=\boldsymbol x_t \frac{\dd a_t}{a_t\dd t}
>   -\epsilon_\theta(\boldsymbol x_t ,t )b_t\frac{\dd \lambda_t}{\dd t}
>   $$
>   即

>   $$
>   \frac{\dd {\boldsymbol x_t}}{\dd t}= \frac{\dd \log a_t}{\dd t}\boldsymbol x_t
>   -b_t\frac{\dd \lambda_t}{\dd t}\epsilon_\theta(\boldsymbol x_t ,t )\
>   $$
>   此即式$\eqref{diffusion-ode}$。
>

## 推导逆向SDE

由通用的逆向SDE（式$\eqref{rev-sde}$），取$\boldsymbol f(\boldsymbol x_t,t)=f_t\boldsymbol x_t, \boldsymbol G(\boldsymbol x_t,t)=g_t\boldsymbol I$，并代入$\nabla_{\boldsymbol x_t}\log q_t(\boldsymbol x_t)\approx -\dfrac{\epsilon_\theta(\boldsymbol x_t,t)}{b_t}$，即得diffusion模型的ODE为，即得到

DDPM的设定下的逆向SDE：
$$
\begin{align}
DDPM的逆向SDE：\dd {\boldsymbol x_t}&=[f_t\boldsymbol x_t-g_t^2\nabla_{\boldsymbol  x_t} \log q_t(\boldsymbol x_t)]\dd t+g_t\dd {\boldsymbol w_t},\boldsymbol x_t是概率建模的对象\\
\Rightarrow DDPM采样过程：\dd {\hat{\boldsymbol x}_t}&=[f_t\hat{\boldsymbol x}_t+\frac{g^2_t}{b_t}\epsilon_\theta(\hat{\boldsymbol x}_t,t)]\dd t+g_t\dd {\boldsymbol w_t},\hat{\boldsymbol x}_t是采样得到的 \label{diffusion-rev-sde}\\
f_t&=\frac{\dd{\log a_t}}{\dd t}\\
g_t^2&=-2b_t^2\frac{\dd{ \lambda_t}}{\dd{t}}\\
即 \dd {\hat{\boldsymbol x}_t}&=[\frac{\dd{\log a_t}}{\dd t}\hat{\boldsymbol x}_t-2b_t^2\frac{\dd{ \lambda_t}}{\dd{t}}\epsilon_\theta(\hat{\boldsymbol x}_t,t)]\dd t+\sqrt{-2b_t^2\frac{\dd{ \lambda_t}}{\dd{t}}}\dd {\boldsymbol w_t}
\end{align}
$$

### 直接从正向SDE推逆向SDE

*   下面的推导参考：苏剑林：[生成扩散模型漫谈（五）：一般框架之SDE篇/逆向方程](https://kexue.fm/archives/9209#逆向方程)

正向条件概率为
$$
\begin{aligned}
q\left(\boldsymbol{x}_{t+\Delta t} \mid \boldsymbol{x}_t\right) & =\mathcal{N}\left(\boldsymbol{x}_{t+\Delta t} ; \boldsymbol{x}_t+\boldsymbol{f}_t\left(\boldsymbol{x}_t\right) \Delta t, g_t^2 \Delta t \boldsymbol{I}\right) \\
& \propto \exp \left(-\frac{\left\|\boldsymbol{x}_{t+\Delta t}-\boldsymbol{x}_t-\boldsymbol{f}_t\left(\boldsymbol{x}_t\right) \Delta t\right\|^2}{2 g_t^2 \Delta t}\right)
\end{aligned}
$$

因此，由贝叶斯定理，逆向条件概率为
$$
\begin{aligned}
q\left(\boldsymbol{x}_t \mid \boldsymbol{x}_{t+\Delta t}\right) & =\frac{q\left(\boldsymbol{x}_{t+\Delta t} \mid \boldsymbol{x}_t\right) q\left(\boldsymbol{x}_t\right)}{q\left(\boldsymbol{x}_{t+\Delta t}\right)}=q\left(\boldsymbol{x}_{t+\Delta t} \mid \boldsymbol{x}_t\right) \exp \left(\log q_t\left(\boldsymbol{x}_t\right)-\log q_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)\right) \\
& \propto \exp \left(-\frac{\left\|\boldsymbol{x}_{t+\Delta t}-\boldsymbol{x}_t-\boldsymbol{f}_t\left(\boldsymbol{x}_t\right) \Delta t\right\|^2}{2 g_t^2 \Delta t}+\log q_t\left(\boldsymbol{x}_t\right)-\log q_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)\right)
\end{aligned}
$$

不难发现, 当 $\Delta t$ 足够小时, 只有当 $\boldsymbol{x}_{t+\Delta t}$ 与 $\boldsymbol{x}_t$ 足够接近时, $q\left(\boldsymbol{x}_{t+\Delta t} \mid \boldsymbol{x}_t\right)$ 才会明显不等于 0 , 反过来也只有这种情况下 $q\left(x_t \mid x_{t+\Delta t}\right)$ 才会明显不等于 0 。因此, 我们只需要对 $\boldsymbol x_{t+\Delta t}$ 与 $\boldsymbol{x}_t$ 足够接近时的情形做近似分析, 为此, 我们可以用泰勒展开:
$$
\log q_t\left(\boldsymbol{x}_t\right) \approx \log q_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)+\left(\boldsymbol{x}_t-\boldsymbol{x}_{t+\Delta t}\right) \cdot \nabla\log q_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right) -\Delta t \frac{\partial}{\partial t} \log q_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)
$$

代入到前式，配方得到
$$
q\left(\boldsymbol{x}_t \mid \boldsymbol{x}_{t+\Delta t}\right) \propto \exp \left(-\frac{\left\|\boldsymbol{x}_{t+\Delta t}-\boldsymbol{x}_t-\left[\boldsymbol{f}_t\left(\boldsymbol{x}_t\right)-g_t^2 \nabla \log q_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)\right] \Delta t\right\|^2}{2 g_t^2 \Delta t}+\mathcal{O}(\Delta t)\right)
$$

当 $\Delta t \rightarrow 0$ 时, $\mathcal{O}(\Delta t) \rightarrow 0$ ，在上述概率式子中不起作用, 因此
$$
\begin{aligned}
q\left(\boldsymbol{x}_t \mid \boldsymbol{x}_{t+\Delta t}\right) & \propto \exp \left(-\frac{\left\|\boldsymbol{x}_{t+\Delta t}-\boldsymbol{x}_t-\left[\boldsymbol{f}_t\left(\boldsymbol{x}_t\right)-g_t^2 \nabla\log q_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)\right] \Delta t\right\|^2}{2 g_t^2 \Delta t}\right) \\
& \approx \exp \left(-\frac{\left\|\boldsymbol{x}_t-\boldsymbol{x}_{t+\Delta t}+\left[\boldsymbol{f}_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)-g_{t+\Delta t}^2 \nabla \log q_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)\right] \Delta t\right\|^2}{2 g_{t+\Delta t}^2 \Delta t}\right)
\end{aligned}
$$

即
$$
\begin{align}
\boldsymbol{x}_{t}&=\boldsymbol{x}_{t+\Delta t}-\left[\boldsymbol{f}_{t}\left(\boldsymbol{x}_{t}\right)-g_{t}^2 \nabla \log q_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)\right] \Delta t+g_{t}\sqrt{\Delta t}\boldsymbol z, \boldsymbol z\sim N(\boldsymbol 0,\boldsymbol I)\\
&=\boldsymbol{x}_{t+\Delta t}-\left[\boldsymbol{f}_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)-\frac{\partial \boldsymbol{f}_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)}{\partial t}\Delta t-(\boldsymbol x_{t}-\boldsymbol x_{t+\Delta t})\cdot\nabla \boldsymbol{f}_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right) \right]\Delta t\\
&\quad -\left[(g_{t+\Delta t}^2-2g_{t+\Delta t}\frac{\partial g_{t+\Delta t}}{\partial t}\Delta t) \nabla \log q_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)\right] \Delta t\\
&\quad + (g_{t+\Delta t} -\frac{\partial g_{t+\Delta t}}{\partial t}\Delta t) \sqrt{\Delta t}\boldsymbol z\\

&=\boldsymbol{x}_{t+\Delta t}-\boldsymbol{f}_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)\Delta t
+O(\Delta t^2)
+O(\Delta t^2), 因为\boldsymbol{x}_{t}-\boldsymbol{x}_{t+\Delta t}=O(\Delta t)\\
&\quad -g_{t+\Delta t}^2q_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)\Delta t+O(\Delta t^2)\\
&\quad + g_{t+\Delta t}\sqrt{\Delta t}\boldsymbol z +O(\Delta t^{\frac{3}{2})}\\

&=\boldsymbol{x}_{t+\Delta t}-[\boldsymbol{f}_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)
-g_{t+\Delta t}^2q_{t+\Delta t}\left(\boldsymbol{x}_{t+\Delta t}\right)]\Delta t+ g_{t+\Delta t}\sqrt{\Delta t}\boldsymbol z +O(\Delta t^{\frac{3}{2})}
\end{align}
$$
 故当$\Delta t=-\dd t, \dd t<0$时，舍去$O(\Delta t^{\frac{3}{2}})$，有逆向SDE
$$
d \boldsymbol{x}=\left[\boldsymbol{f}_t(\boldsymbol{x})-g_t^2 \nabla_{\boldsymbol{x}} \log q_t(\boldsymbol{x})\right] d t+g_t d \boldsymbol{w}
$$

这就是反向过程对应的SDE, 最早出现在《Reverse-Time Diffusion Equation Models»中。
