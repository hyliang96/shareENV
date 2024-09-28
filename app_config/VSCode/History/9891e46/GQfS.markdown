# 参考文献


[^应用随机过程]: [北大数学系在线教案，应用随机过程](https://www.math.pku.edu.cn/teachers/lidf/course/stochproc/stochprocnotes/html/_book/index.html)
[^香蕉空间]: [香蕉空间：一个正在成长的中文数学社区](https://www.bananaspace.org/wiki/首页)
[^中文数学wiki]: [中文数学wiki](https://math.fandom.com/zh/wiki/中文数学_Wiki:主页)



# 测度

## 代数

定义｜**$\sigma$-代数**：集合$\Omega$，集合$\Sigma\sube 2^\Omega$，$\Sigma$是$\sigma$代数，当$\Sigma$满足:

*   对**并**封闭：若$A,B\in\Sigma$，则$A\cup B\in\Sigma$
*   对**补**封闭：若$A\in\Sigma$，则$\bar A\in\Sigma$​​​

性质：

*   对**交**封闭：若$A,B\in\Sigma$，则$A\cap B\in\Sigma$（使用德摩根律），可以定义具有有限可加性的函数$f:\Omega\mapsto \R_{\geq 0}$（希望定义为测度）。但无法处理极限问题（即$\Sigma$对可数次并不一定封闭，$f$没法具有可数可加性）。因而需要在增强一下，变成σ-代数，增加两项：
    *   包含空集，以便在定义测度时，测度能具有规范性。
    *   对可数次并封闭，以便在定义测度时，测度能具有可数可加性。

## $\sigma$-代数

下文摘自：[$\sigma$-代数的定义](https://math.fandom.com/zh/wiki/Σ-代数)

定义｜**σ-代数/σ-域**：集合$\Omega$，集合$\Sigma\sube 2^\Omega$，$\Sigma$是$\sigma$-代数/σ-域，当$\Sigma$满足:

*   包含**空集**: $\varnothing\in\Sigma$
*   对**可数次并**封闭：若$A_i\in\Sigma$，$i=1,2,3$，则$\bigcup_{i=1}^\infty A_i\in\Sigma$
*   对**补**封闭：若$A\in\Sigma$，则$\bar A\in\Sigma$​​

推论：

*   $\sigma$-代数对**可数次交**也封闭：若$A_i\in\Sigma$，$i=1,2,3$，则$\bigcap_{i=1}^\infty A_i\in\Sigma$.

>   证明：由无穷个集合的德摩根律得，$\bigcap_{i=1}^\infty A_i=\overline{\bigcup_{i=1}^\infty \bar A_i}\in\Sigma$
>
>   >   证明无穷个集合的德摩根律：对于指标集合$I$（不必有限、不必可数），有$\bigcap_{i\in I}A_i=\overline{\bigcup_{i\in I} \bar A_i}$：
>   >
>   >   $x\in\bigcap_{i\in I}A_i\leftrightarrow \forall i \in I, x\in A_i\leftrightarrow \neg(\exists i\in I, x\notin A_i) \leftrightarrow \neg(\exists i\in I, x\in \bar A_i)\leftrightarrow \neg(x\in\bigcup_{i\in I} \bar A_i)\leftrightarrow x\in\overline{\bigcup_{i\in I} \bar A_i}$

定义｜**生成的$\sigma$-代数**：$\Gamma\sube 2^\Omega$，由$\Gamma$生成的$\sigma$-代数 $\sigma(\Gamma):=\{\Sigma|\Sigma是\sigma\text{-}代数 \and \Gamma\sube \Sigma\}$。

解释：对于$\Gamma\sube 2^\Omega$，包含$\Gamma$的最小的$\sigma$代数称由$\Gamma$生成的$\sigma$-代数，称**由$\Gamma$生成的$\sigma$-代数**，记作$\sigma(\Gamma)$。所谓“最小”指，$\Omega$上的任意$\sigma$-代数$\Sigma$，都满足$\sigma(\Gamma)\sube\Sigma$​。

## 拓扑

定义｜**拓扑空间**及其上的**开集**：集合$\Omega$，若集族$\tau\sube 2^\Omega$，满足如下开集公理，则称$\tau$是$\Omega$的开集系或拓扑，称$\tau$中元素为开集：

*   全集、空集都是开集：$\Omega,\varnothing\in\tau$
*   **有限**个开集的**交**是开集：$A_1,A_2\in\tau\Rightarrow A_1\cap A_2\in \tau$
*   **任意**个开集的**并**是开集：$A_i\in\tau, i\in I\Rightarrow \bigcup_{i\in I} A_i\in \tau$（$I$不必有限、不必可数）

定义｜**欧式空间上的开集**：若$O\sube\R^n$，$\forall p\in O，\exists r>0$，使得$B(p,r):=\{a\in \R^n\big| \Vert a-p\Vert_2<r\}\sube O$，则称$O$是欧氏空间$(\R^n,d_2)$​上的开集。

## Borel $\sigma$-代数

下文摘自：[Borel集合的定义](https://math.fandom.com/zh/wiki/Borel_集)

定义｜**Borel $\sigma$-代数**：对于拓扑空间$(\Omega,\tau)$，由开集系$\tau$所生成的$\sigma$-代数，称$\Omega$的Borel $\sigma$-代数，记作$\mathscr B((\Omega,\tau)):=\sigma(\tau)$​，其中所含元素称**Borel集**。

推论：

*   Borel集即能通过开集进行有限或可数次「（交、）并、补」所得到的集合；Borel σ-代数即所有这样的集合构成的集族。
*   闭集都是Borel集。因为σ-代数对补封闭，而闭集的补集是开集。

欧式空间上的特例：

*   $\R^n$的Borel σ-代数记作$\mathscr B(\R^n)$​

*   $[0,\infty)$的Borel σ-代数记作$\mathscr B([0,\infty))$，其他任何区间的的Borel σ-代数的记法同理。

*   $\R$上所有半开半闭区间$[a,b),(a,b],[a,\infty),(-\infty,b]\in\mathscr B(\R)$​。

## 测度和概率测度

下文摘自： [可测空间](https://www.bananaspace.org/wiki/可测空间)  [测度空间](https://www.bananaspace.org/wiki/测度空间) [测度](https://www.bananaspace.org/wiki/测度)

定义｜**可测空间**：即配备了σ-代数的空间。若$\Sigma$是σ-代数，则$(\Omega,\Sigma)$称可测空间，$\Sigma$中的元素称可测集。

定义｜**测度空间**：即配备了测度的可测空间。$(\Omega,\Sigma)$是可测空间，若映射$\mu:\Omega\mapsto\R\cup\{\infty\}$，若满足

*   非负性：$\forall A\in \Omega$，有$\mu(A)\geq 0$；
*   规范性：$\mu(\varnothing)=0$；
*   可数可加性：若$A_i\cap A_j=\varnothing (\forall i\neq j)$，则$\mu(\bigcup_{i=1}^\infty A_i)=\sum_{i=1}^\infty\mu(A_i)$

则称$\mu$为$(\Omega,\Sigma)$上的测度，称$(\Omega,\Sigma,\mu)$为测度空间。

*   σ-有限测度：$\exists \{A_n\in \Sigma\}_{i\in\N^+},\mu(A_i)<\infty,\Omega=\bigcup_{i=1}^{\infty}A_i$​
*   有限测度：$\mu(\Omega)<\infty$，等价于$\forall A\in\Sigma, \mu(A)<\infty$​
    *   比如，Lebesgue测度在$\R$上不有限，但σ-有限。因为$[-n,n]$的Lebesgue测度为$n$，有限，且$\bigcup_{n=1}^\infty [-n,n]=\R$

*   **概率测度**：$\mu(\Omega)=1$，通常将$\mu$记作$P$，称$(\Omega,\Sigma,P)$​为概率测度空间/概率空间。
    *   定义｜**样本点、事件、基本事件、复合事件**：$(\Omega,\Sigma,P)$是概率空间，则$\forall A\in \Sigma$称事件，$\forall x\in \Omega$称样本点，$\{x\}$称基本事件，若$A$包含不止一个元素则称复合事件。

*   亚概率测度：$\mu(\Omega)\leq1$​

## 乘积空间和张量积

下文摘自：[ *σ*-代数, 可测空间与可测函数](https://www.bananaspace.org/wiki/讲义:数学分析/sigma-代数,_可测空间与可测函数)

定义｜**乘积空间**：集合$\Omega_1,\Omega_2$，二者的乘积空间定义为$\Omega_1\times \Omega_2:=\{(x_1,x_2)|x_1\in \Omega_1,x_2\in \Omega_2\}$。

定义｜**张量积**：可测空间$(\Omega_1,\Sigma_1),(\Omega_2,\Sigma_2)$，则$\Sigma_1$与$\Sigma_2$的张量积定义为$\Sigma_1\otimes\Sigma_2:=\sigma(\{A_1\times A_2|A_1\in \Sigma_1, A_2\in \Sigma_2\})$​。

推论：

*   可测空间$(\Omega_1,\Sigma_1),(\Omega_2,\Sigma_2)$，则$(\Omega_1\times\Omega_2,\Sigma_1\otimes\Sigma_2)$是可测空间。
*

$$
\mathscr{B}(\R^n)=\underbrace{\mathscr B(\R)\otimes\mathscr B(\R)\otimes\cdots\otimes \mathscr B(\R)}_{n}:=\sigma(\{A_1\times A_2\times \cdots\times A_n|A_i\in\mathscr B(\R)\})\\
=\sigma\big(\{(a_1,b_1)\times(a_2,b_2)\times\cdots\times(a_n,b_n)|a_i,b_i\in\R\}\big)\\
=\sigma\big(\{(-\infty,b_1]\times(-\infty,b_2]\times\cdots\times(-\infty,b_n]|b_i\in\R\}\big)
$$



# 随机过程

参考：[随机微积分(3) 随机过程Stochastic Process、滤流Filtration](https://zhuanlan.zhihu.com/p/345656686)

## 可测函数

定义｜**可测函数**：

$(X,\Sigma_X),(Y,\Sigma_Y)$为可测空间，函数$f:X\mapsto Y$，对$\forall B\in \Sigma_Y$，有$f^{-1}(B)\in\Sigma_X$，则称$f$为$\Sigma_X$-$\Sigma_Y$可测函数。

说明：$f^{-1}(B):=\{x\in X|f(x)\in B\}$

通俗解释：

*   可测函数是(其逆函数)保持测度空间结构的函数。
*   我自己约定记号$f^{-1}(\Sigma_Y):=\sigma(\{f^{-1}(B)|B\in \Sigma_Y\})$，表示由$\Sigma_Y$中全体元素的原像生成的σ-代数。
*   若存在$\Sigma_X$-$\Sigma_Y$可测函数$f$，则$f^{-1}(\Sigma_Y)\sube \Sigma_X$，说明$(X,\Sigma_X)$对事件的描述不会比$(Y,\Sigma_Y)$更粗糙
*   由$(X,\Sigma_X)$上的（概率）测度$\mu$，可以诱导/决定出$(Y,\Sigma_Y)$上的（概率）测度$\tilde \mu$，$\tilde \mu(B):=\mu(f^{-1}(B))$，可以简记为$\mu(f(x)\in B)$，即在记号上把$\tilde \mu$也记作$\mu$。这说明，可测函数可以让一个可测空间上的（概率）测度，到另一个可测空间上也能用。

## 随机变量

[随机变量](https://math.fandom.com/zh/wiki/随机变量)

定义｜（多元）**随机变量**：概率空间$(\Omega,\Sigma,P)$ ，可测空间$(S,\mathscr S)$，当且仅当$X:\Omega\mapsto \R^n$是$\Sigma$-$\mathscr S$**可测函数**时，称$X$是**随机变量**，称$(\Omega,\Sigma,P)$为样本空间，称$(S,\mathscr S)$为状态空间。

说明：

*   $(\Omega,\Sigma,P)$样本空间，也即随机种子空间。不同的随机变量可以共用同一个随机种子空间，共用随机种子空间 是 随机变量之间获得相关性 的必要不充分条件。也有共用随机种子空间的两个随机变量不具有相关性的。
*   随机变量是函数，将随机种子空间中的基本事件，映射为$\R,\R^n$​中的一个点，这是将事件数量/向量化。
*   $X$不必是双射，可以多对一。
*   可测空间$(\Omega,\Sigma)$上的概率$P$，经可测函数$X$的映射，导出了$ (\R^n,\mathscr B(\R^n))$上的概率测度$\mu$，其定义为：$\forall B\in\mathscr S,\mu(B):=P(X^{-1}(B))$。
    *   为记号方便，会把**概率**$\mu(B)$或$P(X^{-1}(B))$简记成$P(X\in B)$，把**事件**$X^{-1}(B)$简记作$\{X\in B\}$。比如写作$P(X<0\or X>1)$，事件$\{X<0\or X>1\}$。
    *   请注意区分$\mu:\mathscr S\mapsto \R_{\geq0}$和$P:\Sigma\mapsto \R_{\geq0}$是定义在两个不同的可测空间上的测度，但$\mu$是由$P$​决定的。

*   通常研究状态空间为$(\R^n,\mathscr B(\R^n))$的随机变量。

定义｜ **分布函数**：一元随机变量 $X:\Omega\mapsto \R$，可以定义**分布函数**$F(x):=P(\{X\leq x\})$。能定义它的原因是，$(-\infty,x]\in \mathscr B(\R^n)$，故$X^{-1}((-\infty,x]):=\{\omega\in\Omega|X(\omega)\leq x\}\in \Sigma$，故$P\big( X^{-1}((-\infty,x])\big)$有定义，简单记作$P\{X\leq x\}$。

## 随机过程

以下两种定义等价（有待证明）

定义1｜**随机过程（时间,种子→状态）**：概率空间$(\Omega,\Sigma,P)$ ，可测空间$(S,\mathscr S)$，全序集合$T\sube \R$为时间指标集，$X:T\times\Omega\mapsto S$为**可测函数**，则称$X$为在$(\Omega,\Sigma,P)$上时间段$T$​​​取值的随机过程。

说明：

*   **上述$X$可测** 的定义：，$\forall B\in\mathscr S, X^{-1}(B)\in \mathscr B(T)\otimes \Sigma$​​​。

*   固定时间$t\in T$，则$X(t,\omega)$​变成一个随机变量。
*   固定种子$\omega\in \Omega$，$X(t,\omega)$变成一个确定轨迹$f(t)\in S^T$。
    *   种子到轨道可以多对一。
    *   一个种子决定了每个时刻下随机变量的取值，这些取值可以各不相同。比如，扔无穷次硬币的随机过程，可以取$\omega=(正，反，正，正,\cdots)$。
    *   $(\Omega,\Sigma)$不能比$(S^{\#(T)},\mathscr S^{\#(T)})$更粗糙。

例子：

*   当$T=\{t\}$，$X(t,\omega)$退化一个随机变量。
*   当$T=\{t_1,t_2,\cdots,t_n\}$，$S=\R$，$X$退化为n维随机变量。
*   当$T=\N$，$X$称离散（时间/参数）随机过程
*   当$T=\R$，$X$​​称连续（时间/参数）随机过程
*   当$S$可数，$X_t$是离散取值的随机变量
*   当$S=\R^n$​，$X_t$​是连续取值的随机变量
*   当$T=\R,S=\R^n$，$\forall \omega\in \Omega, X(\cdot,\omega)\in C(T;\R^n) $，则称$X$轨道连续
*   当$T=\R,S=\R^n$，$\forall t\in T, \lim _{\Delta t \rightarrow 0}\mathbb E[(X_{t+\Delta t}-X_t)^2]=0$，则称$X$在均方意义下连续，简称均方连续

定义2｜**随机过程（种子→状态关于时间的函数）**：概率空间$(\Omega,\Sigma,P)$ ，可测空间$(S,\mathscr S)$，集合$T\sube \R$为时间指标集，$X:\Omega\mapsto S^{T}$为**可测函数**，则称$X$为在$(\Omega,\Sigma,P)$上时间段$T$取值的随机过程。

说明：

*   $S^T$表示全体$T\mapsto S$的映射构成的集合。当$S=\R$时，也会记作$\R^{\#(T)}$，其中$\#(T)$表示$T$的势/基数（cardinality），也记作$\text{card}(T),n(T),\overline{\overline{T}},|T|$，但在随机过程的资料中通常记作$\#(T)$。特别地，当$T$是有限集合时 $\#(T)$ 即$T$中元素的个数。
*   **上述$X$可测 的定义**：若$S^T$有σ-代数$\mathcal F$，使$\forall A\in \mathcal F, X^{-1}(A)\in \Sigma$。
*   $\mathcal F$和$T,\mathscr S$的关系：
    *   若$T$是有限集合，则$\mathcal F:=\sigma(\{ \hat A|A\in \mathscr S^{\#(T)}\})$是$S^T$上的σ-代数。
        *   集合序列 $A:=(A_i)_{i=1,2,\cdots,\#(T)}$
        *   $\mathscr S^{\#(T)}:=\underbrace{\mathscr S\otimes\mathscr S\otimes\cdots\otimes\mathscr S}_{\#(T)}$​
        *   $\hat A:=\{f\in S^T |f(\tau_i)\in A_i,i=1,2,\cdots,\#(T) \} $
    *   若$T$是可数无限集合，即存在双射$\tau: \N\mapsto T$，则$\mathcal F:=\sigma(\{ \hat A| A \in \mathscr S^\N \})$是$S^T$上的σ-代数。
        *   集合序列 $A:=(A_i)_{i\in\N}$
        *   $\mathscr S^\N:=\sigma(\{A=(A_i)_{i\in\N}|A_i\in\mathscr S\})$
        *   $\hat A:=\{f\in S^T |f(\tau_i)\in A_i,i\in \N \} $
    *   若$T$是不可数无限集合：
        *   若区间$T\sub \R$， $S=\R^n,\mathscr S=\mathscr B(R^n)$，$\forall \omega\in \Omega, X(\omega)$连续（ **即**$X:\Omega\mapsto C(T;\R^n)$ ），则$C(T;\R^n)$上的σ-代数$\mathcal F$​​可以用柱集/紧收敛拓扑/贯通开区域去定义，详见[轨迹空间的σ-代数](#轨迹空间的sigma代数)。
*   每个种子$\omega\in \Omega$对应一个轨迹$f\in S^T$。种子到轨道可以多对一。

## 域流(filtration)

定义｜**域流/滤流/滤子**：：域流是一族有序的、不缩小的σ-代数。

数学表示：概率测度$(\Omega,\Sigma,P)$，$I$为指标集、有全序（通常取$\N,\R^+,\R^+$的子集）。$\forall i \in I$，有子σ-代数$\mathcal F_i\sube\Sigma$。记$F:=(\mathcal F_i)_{i\in I}$。$\mathcal F_k\sube \mathcal F_l, \forall k\leq l$（单调递增），则称$F$为域流/滤流/滤子（filtration)，称$(\Omega,\Sigma,F,P)$为域流/滤子/滤波概率空间**（filtered probabilistic space）**。

理解：

*   $I$ 是时间，$ \mathcal F_t$是时刻$t$​时描述随机事件的空间，这个空间只会随着时间增长而变得更精细，而不会变得更粗糙，数学上即可测性不断改善。
*   在域流概率空间$(\Omega,\Sigma,F,P)$上定义随机过程$X_t$。尽管不知道底层的随机种子$\omega$，但可以观测到已经发生的事件（记作$\mathcal F_t(\omega)=E\in \mathcal F_t$  ），并用此去估计$X_s(s\geq t)$的期望：$\mathbb E (X_s\big|_{\mathcal F_t})=\mathbb E[X_s|E]$。

**注意:**
严格来讲, 滤流 $F$ 并非单个信息本身("磁带并不是信息本身"), 而是对$t$时刻所有可观察事件信息的汇总。之后再使用条件期望对未来时刻随机变量不断细化加工。正因为此, 称加工为"滤", 细化为"流"。滤流是信息的载体, 不同的滤流编码了不同信息。

## 适应过程

定义｜**适应过程**：概率测度$(\Omega,\Sigma,P)$，全序指标集$T$， $F=(\mathcal F_t)_{t\in T}$是域流，$X$是随机过程，若$\forall t\in T, X_t$均是$\mathcal F_t$可测的，则称随机过程$X$适应于域流$F$，或者说$X$是$F$上的适应过程。

理解:
从信息角度讲， $X$ 适应于域流 $\left\{\mathcal{F}_t\right\}_{t \in T}$ 即指在任意时间 $t, X_t$ 都可以通过观测 $\mathcal{F}_t$ 中包含的事件信息后成为 predetermined/known value，不再具有随机性，即**以 $\mathcal{F}_t$ 对 $\Omega$ 的分类方式， $t$时刻之前的所有可行轨道必须全部能被逐个区分.**

## 自然域流

定义｜**自然域流(natural filtration)**：考察定义在 $(\Omega, \Sigma, \mathbb{P})$ ， $T\sube R$ 上的随机过程 $X:\Omega\mapsto (\R^n)^{\#(T)}$.
则 $\forall t<\tau$ ，记
$$
B((\R^n)^{\#([0,t])}):=\sigma(\{f\in(\R^n)^{\#(T)} |f(s)\in B, \forall s\in[0,t],\forall B\in \mathscr B(\R^n) \})\\
\mathcal{F}_t^X:=X^{-1}( \mathscr B((\R^n)^{\#([0,t])}) )\\

=\sigma\left(\left\{X_s^{-1}(B) \mid \forall s\in[0,t], \forall B \in \mathscr{B}(\R^n)\right\}\right)
=:\sigma\left(\left\{X_s\right\}_{s \in[0, t]}\right)
$$

则显然 $F^X=\left\{\mathcal{F}_t^X\right\}_{t \in T}$ 为概率空间 $(\Omega, \mathcal{F}, \mathbb{P})$ 上的域流, 称为 $X$ 生成自然域流。

理解:
$\mathcal{F}_t^X$ 即按照随机过程 $X$ 从 0 到 $t$ 时段所有可能实现的轨道片段 $\left\{X_t(\omega)\right\}_0^t$ 对原轨道空间 $\Omega$进行划分. 则用 $\mathcal{F}_t^X$ 来编码所有通过观测 $\left\{X_t(\omega)\right\}_0^t$ 而得到的事件信息.

性质：随机过程适应于自身诱导的自然滤流。

# 随机过程的概率测度

## 轨迹空间的σ-代数和Borel集

### 全体柱集生成的σ-代数

定义｜**柱集**：区间$T\sube\R$，在轨迹空间$C(T;\R^n)$中，在有限个时刻都落在给定Borel集$B\in \mathscr B(\R^{n\times m})$内的轨道所构成的集合称柱集，记作$C_B$，即
$$
C_B:=\{\omega\in C(T;\R^n)| (\omega(t_1),\omega(t_2),\cdots,\omega(t_m))\in B\}
$$
由**全体柱集**构成的集族生成的σ-代数记作$\mathscr B(T;\R^n)$
$$
\mathscr B(T;\R^n):=\sigma\big(\{C_B| B\in\mathscr B(\R^{n \times m}),t_i\in T,m\in \N^+\}\big)
$$
性质：

*

$$
\mathscr B(T;\R^n)
=\sigma\big(\{C_{A_1\times\cdots\times A_m}| A_i\in\mathscr B(\R^n);t_i\in T;i=1,2,\cdots,m;m\in \N^+\}\big)\\
=\sigma\big(\{C_{A_1\times\cdots\times A_m}|开集A_i\in\R^n;t_i\in T;i=1,2,\cdots,m;m\in \N^+\}\big)\\
=\sigma\big(\{C_{A_1\times\cdots\times A_m}|A_i=\prod_{j=1}^n(a_{ij},b_{ij})\in\R^n;t_i\in T;i=1,2,\cdots,m;m\in \N^+\}\big)
$$

### **紧收敛拓扑**生成的σ-代数

*   定义｜**紧致子集**：拓扑空间$(X,\tau)$，$A\sube X$，若$A$在$X$上的任意开覆盖，有有限子覆盖，则称$A$是$X$上的紧致子集。
    *   特例：在欧氏空间$(\R^n,d_2)$，$A\sube X$：$A$是闭集，且$A$有界$\Leftrightarrow A$是$(\R^n,d_2)$​的紧致子集。

下面[引自](https://math.fandom.com/zh/wiki/一致收敛拓扑)

*   定义｜**一致收敛**：非空集合$X$，度量空间$(Y,d)$，$f_n:X\mapsto Y(n\in \N)$，若$\exists f:X\mapsto Y$，使
    $$
    \lim_{n\rightarrow \infty}\sup_{x\in X} d(f_n(x),f(x))=0
    $$
    则称$f_n$在$X$上一致收敛（到$f$）。

*   定义｜**一致收敛度量**：非空集合$X$，度量空间$(Y,d)$，从$X$到$Y$的映射全体记作集合$Y^X$，定义度量$\bar d:Y^X\times Y^X\mapsto\R$，
    $$
    \bar d(f,g):=\min\bigg(1,\sup_{x\in X}d\big(f(x),g(x)\big)\bigg)
    $$
    可以证明$\bar d$是$Y^X$上的度量，称$\bar d$​为一致收敛度量。

    解释：

    *   使用一致收敛度量，能保证$\lim_{n\rightarrow \infty}\bar d(f_n,f)=0\Leftrightarrow f_n$一致收敛到$f$。

    *   使用一致收敛拓扑定义出来的开球$B(f,\epsilon)$，表示$f$在$X$上处处取值抖动小于$\epsilon(\epsilon>0)$后得到的全体函数。

*   定义｜**度量诱导的拓扑**：度量空间$(X,d)$，可以定义开集族/拓扑：$A\sube X$是开集，当且仅当$\forall x\in A, \exists \epsilon>0$, 开球$B(x,\epsilon)\sube A$）。

*   定义｜**一致收敛拓扑**：由一致收敛度量诱导出来的拓扑，称一致收敛拓扑。

    特别地，$C(X,Y)$配备一致收敛度量，称为一致收敛度量决定的连续函数空间。

*   定义｜**紧收敛/在诸紧集上一致收敛**：拓扑空间$(X,\tau)$，度量空间$(Y,d)$，$f_n:X\mapsto Y(n\in \N)$：若对$\forall 紧 K\sube X$，都有$f_n$在$K$上一致收敛，则称$f_n$​​紧收敛/在诸紧集上一致收敛。

*   定义｜**拓扑基**：

    *   拓扑空间$(X,\tau)$，$\mathscr U=\{U_\alpha\} \sube \tau$，$\forall A\in\tau$，使得$A=\mathscr U\text{中若干（不必可数、不必有限）元素的并}$，则称$\mathscr U$为$(X,\tau)$的拓扑基，$\tau$为$\mathscr U$生成的拓扑。
    *   集合$X$，子集族$\mathscr U=\{U_\alpha\} \sube \tau$，由$\mathscr U$生成的子集族$\bar{\mathscr U}:=\{A\sub X|A=\mathscr U\text{中若干（不必可数、不必有限）元素的并}\}$，若$\bar {\mathscr U}$是一个拓扑，则称$\mathscr U$为$X$的拓扑基，$\bar {\mathscr U}$为$\mathscr U$生成的拓扑。

    解释：若任何开集都能写成子集族 $\mathscr U$中若干（不必可数、不必有限）元素的并，则$\mathscr U$是拓扑基。

*   定义｜**紧收敛拓扑**：拓扑空间$(X,\tau)$，度量空间$(Y,d)$，$x\in X$，$K\sube X$，$f\in Y^X$，定义$Y^X$上关于$K$的开球
    $$
    B_K(f,\epsilon):=\{g\in Y^X|\sup_{x\in K} d(g(x),f(x))<\epsilon\}
    $$
    关于$Y^X$上相对于紧子集的开球构成的集族
    $$
    \mathscr U=\{B_K(x,\epsilon)|f\in Y^X,x\in X,紧K\sube X,\epsilon>0\}
    $$
    可以证明$\mathscr U$是$Y^X$上的拓扑基，由$\mathscr U$生成的拓扑$\bar{\mathscr U}$**称紧收敛拓扑**。参考：[Topology of compact convergence - Part 1](https://www.youtube.com/watch?v=IWbtYSg1Cm8)

    特别地，$C(X,Y)$配备紧收敛度量，称为紧收敛度量决定的连续函数空间。

    解释：

    *   基于上述对开球的定义，能保证$\forall 紧K\sube X,\forall \epsilon >0, \exists N\geq0, \forall n>N, f_n\in B_K(f,\epsilon)\Leftrightarrow f_n紧收敛到f$

    *   对于紧$K\sube X$，相对于$K$的开球$B_K(f,\epsilon)$，表示$f$在$K$上处处取值抖动小于$\epsilon(\epsilon>0)$得到的全体函数。

*   定义｜**紧收敛度量**：对于集合$X$，度量空间$(Y,d)$，从$X$到$Y$的映射全体记作集合$Y^X$，参考：[Borel sets for function space](http://www.ma.huji.ac.il/raumann/pdf/66.pdf)

    *   若$X$紧，则紧收敛度量就是一致收敛度量，定义度量$\tilde d:Y^X\times Y^X\mapsto\R$，
        $$
        \tilde d(f,g)=\bar d(f,g):=\min\bigg(1,\sup_{x\in X}d\big(f(x),g(x)\big)\bigg)
        $$

    *   若$X=\R_{\geq0}$，定义度量$\tilde d:Y^X\times Y^X\mapsto\R$，

    $$
    \tilde d(f,g)=\sum_{n=1}^\infty\frac{1}{2^n}\min\bigg(1,\sup_{0\leq t\leq n} d\big(f(t),g(t)\big)\bigg)\label{compact-converge-measure}
    $$
    *   若$X=(\R^m,d_2)$，则可定义度量$\tilde d:Y^X\times Y^X\mapsto\R$，
        $$
        \tilde d(f,g)=\sum_{n=1}^\infty\frac{1}{2^n}\min\bigg(1,\sup_{x\in \bar B(\boldsymbol 0,n)} d\big(f(x),g(x)\big)\bigg)
        $$
        可以证明$\tilde d$是$Y^X$上的度量，称$\tilde d$为紧收敛度量。由紧收敛度量诱导出来的拓扑，称紧收敛拓扑。

    解释：

    *   使用紧收敛度量，能保证$\lim_{n\rightarrow \infty}\tilde d(f_n,f)=0\Leftrightarrow f_n$紧收敛到$f$。
    *   $X=\R_{\geq0}$，使用紧收敛度量定义出 开球$B(f,\epsilon):=\{g\in Y^X|\tilde d(f,g)<\epsilon \}$，表示$f$在$[0,n]$上各时刻取值抖动小于$O(a^n \epsilon) (1<a<2,\forall n\in \N^+)$得到的全体函数。
    *   比起一致收敛，紧收敛允许在$n$趋近无穷时，取值距离$d(f(x),g(x))$也趋近无穷，但后者增长的速度慢于$2^n$即可。推而广之，对于$X=(\R^m,d_2)$欧氏空间，紧收敛度量允许紧集$K$的边界趋近$X$的无穷远处时，距离$d(f(x),g(x))$也趋近无穷，但后者增长的速度慢于$2^{diam(K)}$，$diam(K)$表示$K$的直径，$diam(K):=\sup_{x,y\in K}d(x,y) $。

*   对比：

    *   在非紧空间$X$（如$[0,\infty)$）上，紧收敛$\Leftarrow\nRightarrow$一致收敛，$\tau$是紧收敛拓扑$\Leftarrow\nRightarrow$$\tau$是一致收敛拓扑，紧收敛度量$\neq$一致收敛度量度量，$\forall f,g\in Y^X, \tilde d(f,g)\geq \bar d(f,g)  $
    *   在紧空间$X$（如$[0,1]$）上，紧收敛$\Leftrightarrow$一致收敛，$\tau$是紧收敛拓扑$\Leftrightarrow$$\tau$是一致收敛拓扑，紧收敛度量$=$一致收敛度量度量，$\forall f,g\in Y^X, \tilde d(f,g)=\bar d(f,g)  $​​

### 贯通开区域生成的σ-代数

我定义｜**贯通开区域**：$A\sube T\times \R^n$，

*   $\exists f\in C(T;\R^n)$，使得$\forall t\in T, (t,f(t))\in A$，则称$A$贯通；否则，称$A$中断；
*   若$A\cap(T^o\cup\times\R^n)$在$T^o\cap\R^n$上是开集，$A\cap((T \backslash T^o)\times \R^n)$在$(T\backslash T^o)\times \R^n$上是开集，则称$A$是开区域（$T^o$表示$T$的内部，比如，$T=[0,\infty),t^o=(0,\infty),T\backslash T^o=\{0\}$）；
*   若满足上述两个条件，则称$A$​​是贯通开区域。
*   若$A$是贯通开区域，则称$\hat A:=\{f\in C(\R_{\geq0};\R^n)|(t,f(t))\in A, \forall t\in \R_{\geq 0}\}$为**过贯通开区域$A$的函数集**。
*   称$\mathscr H:=\{\hat A|A\sube \R_{\geq 0}\times \R^n,A是贯通开区域\}$为**贯通开区域全体**。
*   称$\mathscr G:=\{\hat A|A\sube \R_{\geq 0}\times \R^n,A是贯通开区域\}$​为**过贯通开区域的函数集全体**。

### 三个σ-代数等价

在轨迹空间$C(T;\R^n)$上，有下列三个的σ-代数，且三者相同：<a name='轨迹空间的sigma代数'></a>

**定理1：**全体柱集生成的σ-代数$\mathscr B(T;\R^n)=$由$C(T;\R^n)$上的**紧收敛拓扑**生成的σ-代数$\sigma(\bar{\mathscr U})$​。

*   证明：见[Lecture 2. Measure theory in function spaces](https://fabricebaudoin.blog/2012/03/24/lecture-2-measure-theory-in-function-spaces/)

**定理2**（我自己提的，有待查证）：由$C(T;\R^n)$上的**紧收敛拓扑**生成的σ-代数$\sigma(\bar{\mathscr U})=$由 过**贯通开区域**的函数集全体 生成的σ-代数$\sigma(\mathscr G)$

*   证明：等我誊抄一下纸质草稿

**定理3**：定义在 $(\R_{\geq 0}\times \R^n,\mathscr H)$ 上的非平凡（即不恒为0）测度（比如$n+1$维欧氏空间的体积），**无法诱导出**$(C(\R_{\geq0};\R^n),\mathscr G)$上的测度。<a name='无法诱导'></a>

*   证明：

![image-20240625165328485](assets/image-20240625165328485.png)

## 轨迹空间的测度

### 轨迹的概率的直观解释

指标空间：测度空间$(T,\mathscr B(T))$，时间集合$T\sube\R$，是一个区间，通常取$[0,\infty)$或$[0,1]$。

样本空间：概率空间$(\Omega,\Sigma,P)$​。

随机变量：$X:\Omega\mapsto C(T;\R^n), \omega\mapsto x_\omega$。

为方便定义轨迹的概率，需将表示轨迹表示为曲线。
$$
\begin{gather}
样本空间 & & 函数空间 && 曲线空间\\
\Omega &\xrightarrow[可以多对一]{X} & C(T;\R^n)& \xleftrightarrow[双射]{l} &L \\
\omega & \rightarrow & x_\omega&\leftrightarrow & l(x_\omega)
\end{gather}
$$

*   $X$是一个映射，即每个随机种子$\omega\in\Omega$都对应一个从$[0,1]$到$\R^n$的连续函数$x_\omega(t)$，可以多个随机种子对应同一个函数/同一条轨迹。
*   双射：$l:C(T;\R^n)\mapsto L, l(f):=\{(t,f(t))|t\in T\}, \forall f\in C(T;\R^n)$，$l(f)$是一条连续曲线，称连续函数$f$的轨迹。

*   曲线空间：$L:=\{l(f)|f\in C(T;\R^n)\}$​​
*   轨迹空间：指函数空间或曲线空间（因为二者之间存在双射，故不加区分）。
*   任意贯通开区域$A\in \mathscr H$，$\hat A:=\{f\in C(T;\R^n)|l(f)\sube A\}$，即轨迹落在$A$内的函数组成的集合。

定义｜**函数空间上的概率测度**：上前叙假设下，$(C(T;\R^n),\mathscr G)$可以定义概率测度$\hat P$，使其由样本空间上的概率测度$P$决定：任意贯通开区域$A\in \mathscr H$，$\hat P(\hat A):=P(X^{-1}(\hat A))=P(\{\omega\in\Omega|l(x_\omega)\sube A\})$，简记作$P(l(x_\omega)\sube A)$，即**轨迹落在贯通开区域内的概率**。

注意：**不能用**n+1维欧式子空间$(T\times \R^n,\mathscr B(T\times \R^n))$或$(T\times \R^n,\mathscr H)$上的测度$\mu$去**诱导出**$\hat P$和$P$，使得$P(\{\omega\in\Omega|l(x_\omega)\sube A\}):=\hat P(\hat A):=\mu(A)$。证明见：[前文](#无法诱导)。

**性质**：

*   $P(l(x_\omega)\sube\Omega)=1$

*   $\forall t\in T$，$t$处$A$的取值区域为空集，则$P(l(x_\omega)\sube A)=0$

*   由轨迹的连续性可知，若$A$中断，则$P(l(x_\omega)\sube A)=0$​

    ![草稿-2](assets/%E8%8D%89%E7%A8%BF-2.jpg)

### **柱测度**的直观解释

选定有限个时间$t_1,t_2,\cdots,t_m\in T$，$A_i\in\mathscr B(\R^n)$，定义轨迹$\omega$经过这$m$个截面的概率为$\hat P(C_B)$，也即**有限个时间的联合边缘分布**，其中
$$
B={\prod_{i=1}^m A_i}\\
C_B=\{f\in C(T;\R^n)|f(t_i)\in A_i,i=1,2\cdots m\}
$$

![image-20240622182906413](assets/image-20240622182906413.png)

若将$\prod_{i=1}^m A_i$进行可数次交并补，这个测度也随之做加减法，则延拓得到对任意柱集$C_B$都有定义的测度，此时称做**柱测度**；

若再对全体柱集做可数次交并补，则延拓得到对任意$C\in\mathscr B(T;\R^n)$都定义了轨迹经过$C$的测度；

若再利用轨迹的连续性，则可延拓得到对任意贯通开区域$A$，都有轨迹落在$A$内的测度，这是在$(C(T;\R^n),\mathscr H)$上的概率测度$\hat P$。

**性质**：

若随机过程是马尔可夫过程，$t_1<t_2<\cdots<t_m\in T$，

*   若$B\in \mathscr B(\R^{n\times m})$，则$\hat P(C_B)$可以分解为

$$
\hat P(C_B)=\int\cdots\int_{(x_1,\cdots,x_m)\in B} \prod_{i=1}^m \rho(X_{t_i}=x_i|X_{t_{i-1}}=x_{i-1})\dd x_1\cdots \dd x_m
$$

*   若$B={\prod_{i=1}^m A_i}$，$A_i\in\mathscr B(\R^n)$，则$\hat P(C_B)$可以分解为
    $$
    \hat P(C_B)=\int_{x_1\in A_1}\cdots \int_{x_m\in A_m} \prod_{i=1}^m \rho(X_{t_i}=x_i|X_{t_{i-1}}=x_{i-1})\dd x_1\cdots \dd x_m
    $$

上式中$\rho(\cdot|\cdot)$为条件概率密度。

### 密度函数

对于欧式空间$\R^n$上的随机变量$X$，若概率测度$P$对Lebesgue测度$\mu$绝对连续($P<<\mu)$，则概率测度可以分解为概率密度和Lebesgue测度的乘积，

*   即对于$A_n\sube A_{n-1}, P(A_n)\neq 0, \bigcap_{n=1}^{\infty}A_n=\{x\}$， $\frac{P(A_n)}{\mu(A_n)}$收敛，记$\rho(x):=\frac{\dd P}{\dd \mu}\big|_{x}:=\frac{P(\dd x)}{\mu(\dd x)}:=\lim_{n\rightarrow \infty}\frac{P(A_n)}{\mu(A_n)}$，$\frac{\dd P}{\dd \mu}$是Radon–Nikodym导数。
*   概率变换记作$P(\dd x)=\rho(x)\mu(\dd x)$或$\dd P=\rho(x) \dd \mu $，通常简记作$dP=\rho(x)\dd x$，用$\dd x$代表$\mu(\dd x)$
*   $P(A)=\int _{x\in A}\rho(x)\dd x$

然而，轨迹空间$C(T;\R^n)$是无穷维空间。详见：[Why can’t we define PDFs in infinite dimensions?](https://aalexan3.math.ncsu.edu/articles/nopdf_infdim.pdf)

*   无穷维空间无法定义Lebesgue测度，因此无法定义概率密度函数，使得概率密度分解为概率密度和Lebesgue测度的乘积。

*   但是，在无穷维空间上，Radon–Nikodym定理仍成立，即若有两个测度$\mu_1,\mu_2$，仍可以定义Radon–Nikodym导数$\frac{\dd\mu_1}{\dd\mu_2}$；
*   因此，无穷维空间上若有概率测度$P$和参考测度$\mu$，仍可以用，去做测度变换，定义出$P$【相对于】$\mu$的密度函数$\rho^P_{\mu}:=\frac{\dd P}{\dd \mu}$。

*   例如，在无穷维空间上，Bayes定理仍成立：若$\mu$是先验分布，$P$是后验证分布，则后验概率相对于先验概率的密度函数$\rho$ 是归一的似然。比较Radon–Nikodym定理$A\sube X, P(A)=\int _{x\in A}\rho(x)\mu(\dd x)$，和Bayes定理$p(A|\theta)=\int _{x\in A}\frac{p(\theta|x)}{p(\theta)}p(\dd x)$，发现$\mu(\dd x)=p(\dd x)$是先验分布（的微分），$P(A)=p(A|\theta)$是后验分布，$p(\theta|x)$是似然，$\rho(x)=\frac{p(\theta|x)}{p(\theta)}$是归一的似然.

## Wiener测度

[Wiener测度的定义](https://www.math.pku.edu.cn/teachers/lidf/course/stochproc/stochprocnotes/html/_book/bm.html#bm-app-constr); [百度百科Wiener测度](https://baike.baidu.com/item/维纳测度/18936558)

Wiener测度：初值为0的标准布朗运动的轨迹的概率测度。

轨迹空间：$C([0,\infty);\R^n)$，也有将其记作$\R^{[0,\infty)}$的。

定义柱测度$\hat P$：任意柱集$C\in \mathscr F$，可以表示成$C=\{f\in C([0,\infty);\R^n)|A_i\in\mathscr B(\R^n), f(t_i)\in A_i, i=1,2,\cdots,m\}$，其测度$\hat P(C)$都有如下定义，
$$
\hat P(C)=[(2\pi)^{mn} t_1(t_2-t_1)\cdots(t_m-t_{m-1})]^{-\frac{1}{2}} \int _{A_1}\cdots \int _{A_m}\exp[-\frac{1}{2}\sum_{i=1}^n \frac{\Vert x_i-x_{i-1}\Vert^2}{t_i-t_{i-1}}]\dd x_1\cdots\dd x_m\\
t_0=0, x_0=\boldsymbol 0
$$
[维纳](https://baike.baidu.com/item/维纳/489424?fromModule=lemma_inlink)(Wiener，N.)证明了，利用轨道的连续性，柱测度$\hat P$可以延拓成$\{C(T;\R^n),\mathscr B(T;\R^n)\}$​上的测度$P^W$​，满足可数可加性，称它为Wiener测度。（维纳于1921年发表的关于布朗运动的论文中提出了这种测度）

## 路径积分计算布朗运动路径的概率

参考：[路径积分系列：3.路径积分](https://spaces.ac.cn/archives/3757)

在布朗运动$\dd x\sim N(0,\sigma^2 \dd t)$中，采样出一条路径$x(t)$，粒子依次经过 $x_1, x_2, \ldots, x_{n-1}, x_n$ 的概率密度为
$$
P_n[x(t)]:=\left(\frac{1}{\sqrt{2 \pi  \Delta t}\sigma}\right)^n \exp \left(-\frac{\left(x_1-x_0\right)^2+\left(x_2-x_1\right)^2+\cdots+\left(x_n-x_{n-1}\right)^2}{2 \sigma ^2\Delta t}\right),
$$
暂时省略前面的因子, 然后取 $\Delta t \rightarrow 0$ 的极限, 我们认为 $x_0, x_1, x_2, \ldots, x_{n-1}, x_n$ 这些点, 确定了一条从 $\left(x_0, 0\right)$ 到 $\left(x_n, T\right)$ 的路径 $x(t)$, 而
$$
\hat P_n[x(t)]:=\frac{\left(x_1-x_0\right)^2+\left(x_2-x_1\right)^2+\cdots+\left(x_n-x_{n-1}\right)^2}{2 \sigma^2 \Delta t}=\frac{1}{2 \sigma^2} \sum_{k=0}^{n-1}\left(\frac{x_{k+1}-x_k}{\Delta t}\right)^2 \Delta t,
$$

在 $\Delta \rightarrow 0$ 时, 我们认为 $\frac{x_{k+1}-x_k}{\Delta t}$ 等于 $x(t)$ 在 $t_k$ 的导数 $\dot{x}\left(t_k\right)$, 这样上式正是积分 $\frac{1}{2 \sigma^2}\int \dot{x}^2 d t$ 的离散表达式.综上, 我们得到粒子沿着路径 $x=x(t)$ 走过的“概率密度“, **正比于**
$$
\mathcal P[x(t)]=\exp \left(-\frac{1}{2 \sigma^2} \int \dot{x}^2 d t\right) .
$$

这就得到了粒子经过路径 $x(t)$ 的“概率”, 它是关于 $x(t)$ 的泛函. 这也就是布朗运动路径的”概率“.

### 布朗运动不可导

*   几乎必然 布朗运动的轨迹处处不可导，或者说几乎必然 布朗运动的瞬时速度处处无穷大，证明见下图（[来自](https://physics.stackexchange.com/questions/417852/proof-that-the-wiener-process-is-non-differentiable)）

    ![enter image description here](assets/UVlea.png)

    即$\forall A>0, \forall \epsilon >0, \exists \delta>0, \forall \Delta t\in(0,\delta), P(|\frac{\Delta B}{\Delta t}|>A)>1-\epsilon$，

    即$|\frac{\dd B}{\dd t}| = \infty\ \ a.s.\  P$

*   布朗运动导数的方差趋近无穷大，$\mathbb E(\frac{\dd x}{\dd t})^2=\mathbb E(\frac{\sigma^2\dd t}{\dd t^2})=\frac{\sigma^2}{\dd t}\rightarrow \infty$。

*   但是$\dot x_t^2\dd t$若视作随机变量$Z_t$，用和上图同样的方法可以算出它服从分布$P(Z_t\leq a)=2\Phi(\frac{\sqrt a}{\sigma})-1$，其中$\Phi(x)$是高斯分布$N(0,1)$的累积分布函数。做随机变量变换可得$Z_t=Y_t^2, Y_t\sim N(0,\sigma^2)$。即$\dot x_t^2\dd t\sim \chi^2(1)$。其整体期望 $\mathbb E(\dot x^2\dd t)=\mathbb E(Y_t^2)=\sigma^2$。

    *   这会造成$\int \dot x^2\dd t=\int Z_t=\lim_{n\in \infty}\sum^n_{i=1} Y^2_{t_i}=\lim_{n\rightarrow \infty} \hat Z_n$，其中$\hat Z_n\sim\chi^2(n)\rightarrow N(n,2n)(n\rightarrow \infty)$。故可以证明$\int\dot x^ 2\dd  t=\infty\ \ a.s.\ \ P$​，即$\mathcal P[x(t)]=0 \ \ a.s. \ \ P$，即$P(\{x(t)\in C(T;\R^n)|\mathcal P[x(t)]=0\})=1$

*   为避免不可导的问题，可将定义修改为，取布朗运动路径$x(t)$的平滑近似$\tilde x(t)$，近似误差小于$\epsilon$（在$C(T;\R^n)$上的紧收敛度量下），对所有这样的平滑路径的路径概率求和，然后令$\epsilon$趋近0，即得到布朗运动路径的“概率”（这一段是我问chatgpt的，有待查证）：
    $$
    \mathcal P[x(t)]:=\lim_{\epsilon \rightarrow 0+}\int _{\tilde x\in B(x,\epsilon)\cap C^1(T;\R^n)} \exp(-\frac{1}{2\sigma^2}\int \dot {\tilde x}^2\dd t)\mathscr D\tilde x (t)
    $$

*   在实际计算路径积分时，通常把时间离散化去算求和；在使用路径积分做理论推导时，无需在意布朗运动不可导的问题，只需要形式上演算，最终得到可计算的式子就行。

### 轨迹概率之比

*   这个路径积分并轨迹的概率密度，因为轨迹空间是无穷维空间，无法定义概率密度。
*   但是，不同轨迹$f,g\in C(T;\R^n)$附近的开球（定义见式$\eqref{compact-converge-measure}$，表示$f,g$在指定幅度范围内抖动）上的概率测度$P$之比会随半径趋近0而收敛，即存在$\lim_{k\rightarrow \infty} \frac{P(B(f,\frac{1}{k}))}{P(B(g,\frac{1}{k}))}$。它表示了轨迹的概率之比，即$f$**相对于**$g$的概率密度。

*   在计算路径积分时，舍弃了会随$n\rightarrow \infty$而趋近$\infty$的系数$\left(\frac{1}{\sqrt{2 \pi \Delta t}\sigma }\right)^n$，能够这样舍弃是因为，

$$
\frac{P_n[f(t)]}{P_n[g(t)]}=\frac{\hat P_n[f(t)]}{\hat P_n[g(t)]}
$$

​	这保证了当$n\rightarrow \infty$时，通过$n$个离散时刻连乘出来的轨迹概率之比能收敛，
$$
\lim_{n\rightarrow \infty}\frac{P_n[f(t)]}{P_n[g(t)]}=\lim_{n\rightarrow \infty}\frac{\hat P_n[f(t)]}{\hat P_n[g(t)]}\xlongequal{因为\lim_{n\rightarrow \infty}\hat P[x(t)]=\mathcal P[x(t)]}\frac{\mathcal P[f(t)]}{\mathcal P[g(t)]}
$$
​	从而能通过 半径趋近0的开球概率之比 等于 路径积分之比例（下式），去构造可计算的 轨迹空间上的概率测度$P$
$$
\lim_{k\rightarrow \infty} \frac{P(B(f,\frac{1}{k}))}{P(B(g,\frac{1}{k}))}=\frac{\mathcal P[f(t)]}{\mathcal P[g(t)]}
$$

### 路径积分对路径进行求和

我们已经得到了某条路径的概率 $P[x(t)]$ 的表达式，那么从 $\left(x_0, 0\right)$ 到 $\left(x_n, T\right)$ 的概率，应该是 $\left(x_0, 0\right)$ 到 $\left(x_n, T\right)$ 的所有路径的概率之和. 换言之, 我们要遍历两点间的所有路径求和.

遍历是通过离散化路径来实现的, 如图1所示, 依然将时间 $T$ 进行划分, 对于每一条路径, 我们都可以用折线 $x_0, x_1, x_2, \ldots, x_{n-2}, x_{n-1}, x_n$ 来逼近它, 因此, 如果要遍历所有路径 $x(t)$, 那么只需要遍历所有 $x_1, x_2, \ldots, x_{n-2}, x_{n-1}$ （想象着上下“拨动” $x_1, x_2, \ldots, x_{n-2}, x_{n-1}$​ 各点.）.

![离散化一条路径，然后遍历](assets/4129770139.png)

离散化一条路径, 然后遍历
如果用 $P\left(x_0, 0 ; x_n, T\right)$ 表示从 $\left(x_0, 0\right)$ 到达 $\left.x_n, T\right)$ 的概率, 那么（简洁起见, 我们省略了前面的常数因子 , 在实际问题中我们再恢复就行, 现在我们先要把概念讲清楚)
$$
\begin{aligned}
& P\left(x_0, 0 ; x_n, T\right) \\
= & \lim _{n \rightarrow \infty} \int_{-\infty}^{\infty} \exp \left(-\frac{1}{2 \sigma^2} \sum_{k=0}^{n-1}\left(\frac{x_{k+1}-x_k}{\Delta t}\right)^2 \Delta t\right) d x_1 d x_2 \ldots d x_{n-2} d x_{n-1},
\end{aligned}
$$

积分共有 $n-1$ 次, 然后取 $n \rightarrow \infty$ 的极限. 我们把上式简记为
$$
P\left(x_0, 0 ; x_n, T\right)=\int_{x_0}^{x_n} P[x(t)] \mathscr{D} x(t)=\int_{x_0}^{x_n} \exp \left(-\frac{1}{2 \sigma^2} \int_0^T \dot{x}^2 d t\right) \mathscr{D} x(t) \text {, }
$$

若$x_0,x_n$也可活动，则$x(t)$在$t\in[t_0,t_n]$上都落在贯通开区域$A$内的概率为，
$$
P(x(t)\in A)= \lim _{n \rightarrow \infty} \int_{(t_i,x_i)\in A} \exp \left(-\frac{1}{2 \sigma^2} \sum_{k=0}^{n-1}\left(\frac{x_{k+1}-x_k}{\Delta t}\right)^2 \Delta t\right) \dd x_0 \dd x_1 \ldots \dd x_{n-1} \dd x_{n}\\
=\int_{A} P[x(t)]\mathscr D x(t)=\int_{A} \exp \left(-\frac{1}{2 \sigma^2} \int_0^T \dot{x}^2 d t\right) \mathscr D x(t)
$$
这称为泛函 $P[x(t)]$​ 的路径积分（或者叫泛函积分）, 这是一个无穷维的积分.

# 测度变换

## 绝对连续

参考：[[隨機分析] Girsanov Theory (0) - 測度變換](https://ch-hsieh.blogspot.com/2010/04/girsanov-theory-0-change-of-measure.html)

定义｜**零测集**：测度空间$(\Omega,\sigma,\mu)$，若$A\in\Sigma, \mu(A)=0$，则称$A$是该测度空间上的零测集。

定义｜**绝对连续**（测度对测度的）：可测空间$(\Omega,\Sigma)$上有两个测度$\mu,\nu$，若$\forall A\in \Sigma$，$\mu(A)=0\Leftarrow \nu(A)=0 $，则称$\mu$对$\nu$绝对连续，记作$\mu<<\nu$.

定义｜**等价测度**：可测空间$(\Omega,\Sigma)$上有两个测度$\mu,\nu$，若$\mu<<\nu$且$ \mu<<\nu$，则称$\mu,\nu$等价。（即$\mu,\nu$有相同的零测集）。

## Radon-Nikodym定理

[符号测度](https://math.fandom.com/zh/wiki/符号测度)

[Radon-Nikodym 定理](https://math.fandom.com/zh/wiki/Radon-Nikodym_定理?variant=zh)

定义｜**符号测度**：可测空间$(\Omega,\Sigma)$，函数$\varphi:\Sigma\mapsto \R\cup\{+\infty,-\infty\}$，$\varphi$是可测空间上的*符号测度*，需满足：

*   规范性：$\varphi(\varnothing)=0$
*   可数可加性：若$A_i\cap A_j=\varnothing (\forall i\neq j)$，则$\varphi(\bigcup_{i=1}^\infty A_i)=\sum_{i=1}^\infty\varphi(A_i)$；且如果$\varphi(\bigcup_{i=1}^\infty A_i)$有限，则$\sum_{i=1}^\infty\varphi(A_i)$收敛。

说明：虽然符号测度的值域可以取到正负无穷，但是最多只能取到正负无穷中的一个，我们在研究符号测度时总是约定符号测度不取负无穷。

定义｜**Radon-Nikodym导数**：假设 $\varphi$ 是测度空间 $(X, \Sigma, \mu)$ 上的符号测度, 如果存在**几乎处处**意义下唯一的可测函数 $f:X\mapsto \R$ ，使得
$$
\varphi(A)=\int_A f \mathrm{~d} \mu, \quad \forall A \in \Sigma.
$$

我们就称 $f$ 是 $\varphi$ 对 $\mu$ 的 Radon-Nikodym 导数, 简称为 R-N 导数, 记作 $\frac{\mathrm{d} \varphi}{\mathrm{d} \mu}=f$​.

说明：上述定义中“**几乎处处**”的定义是：$\varphi$ 是测度空间 $(X, \Sigma, \mu)$ 上的符号测度，若存在唯一可测函数$f：X\mapsto \R$，使得任意和某个零测集不交的集合$A\in\Sigma$ (即如下式子)
$$
\exists N\in\Sigma, \mu(N)=0,\forall A\in\{B\in \Sigma|B\cap N=\varnothing\}
$$
都有$\varphi(A)=\int_A f \dd \mu$，则称 $f$ 是 $\varphi$ 对 $\mu$ 的 Radon-Nikodym 导数, 简称为 R-N 导数, 记作 $\frac{\mathrm{d} \varphi}{\mathrm{d} \mu}=f$，或记作$\dd\varphi=f\dd\mu$.

定义｜**绝对连续**（符号测度对测度）：假设 $\varphi$ 是测度空间 $(X, \mathcal{F}, \mu)$ 上的符号测度, 如果$A\in\Sigma$，
$$
\mu(A)=0 \Longrightarrow \varphi(A)=0 .
$$

我们就称 $\varphi$ 是对 $\mu$ 绝对连续，记作$\varphi<<\mu$。

**Radon-Nikodym 定理**：测度空间$(\Omega,\Sigma,\mu)$上$\mu$是σ-有限的，$\varphi$是符号测度，则 $\varphi<<\mu\Leftrightarrow \dfrac{\dd \varphi}{\dd \mu}$存在。

等价表述：测度空间$(\Omega,\Sigma,\mu)$上$\mu$是σ-有限的，$\varphi$是符号测度，则

*   $\varphi<<\mu\Leftrightarrow$**几乎处处**意义下存在唯一可测函数$f：X\mapsto \R$，使得$\varphi(A)=\int_A f\dd \mu, \forall A\in \Sigma$​

### R-N导数的性质

$R-N$ 导数有类似于通常的导数那样的性质。

**定理1**
**（换元公式）**假设 $\varphi$ 是测度空间 $(X, \mathcal{F})$ 上 $\sigma$ 有限的符号测度, 且 $\mu$ 是测度空间 $(X, \mathcal{F})$ 上 $\sigma$ 有限的测度, 且 $\varphi \ll \mu$, 那么
如果 $g \in L^1(X, \varphi)$, 那么 $g\left(\frac{\mathrm{d} \varphi}{\mathrm{d} \mu}\right) \in L^1(X, \mu)$ 且
$$
\int g \mathrm{~d} \varphi=\int g( \frac{\mathrm{d} \varphi}{\mathrm{d} \mu} )\mathrm{d} \mu .
$$

**定理2
(链式法则)** 假设 $\varphi$ 是测度空间 $(X, \mathcal{F})$ 上 $\sigma$ 有限的符号测度, 且 $\mu, \lambda$ 是测度空间 $(X, \mathcal{F})$ 上 $\sigma$ 有限的测度, 且 $\varphi \ll \mu \ll \lambda$, 那么 $\mu \ll \lambda$ 且
$$
\frac{\mathrm{d} \varphi}{\mathrm{d} \lambda}=\frac{\mathrm{d} \varphi}{\mathrm{d} \mu} \frac{\mathrm{d} \mu}{\mathrm{d} \lambda}, \quad \lambda \text {-a.e. }
$$

**定理3**
**（反函数的导数）**假设 $\mu, \lambda$ 是测度空间 $(X, \mathcal{F})$ 上 $\sigma$ 有限的测度，且 $\lambda \ll \mu \ll \lambda$, 那么
$$
\frac{\mathrm{d} \lambda}{\mathrm{d} \mu} \frac{\mathrm{d} \mu}{\mathrm{d} \lambda}=1, \quad \lambda \text {-a.e. and } \mu \text {-a.e. }
$$

## 前置知识

### 停时

定义｜**停时**：域流概率空间$(\Omega,\Sigma,F,P)$​上，时间$T\sube\R$​，有随机变量$\tau:\Omega\mapsto T$​，$\forall t\geq 0$​，事件$\{\tau\leq t\}\in \mathcal F_t$​，则称$\tau$是$F$-的停时。

性质：记$T_{\leq t}:=T\cap (-\infty,t]$，构造随机变量$\tau_t:\Omega\mapsto T_{\leq t}$，$\tau_t:=\min(\tau,t)$（或记作$\tau\and t$)，有如下性质：

*   $\tau$是$F$-停时
*   $\Leftrightarrow \forall t\geq0, \{\tau\leq t\}\in \mathcal F_t$
*   $\Leftrightarrow \forall t\in T$，$\tau_t$是$\mathcal F_t$-可测的
*   $\Leftrightarrow \forall t\in T$,对$\forall B\in \mathscr B(T_{\leq t})$，事件$\{\tau \in B\}:=X^{-1}(B)\in \mathcal F_t $。比如，$\forall s\leq t, \{\tau \leq s\}\in \mathcal F_t$​

理解：

*   停时是否在小于$t$的某个可测的范围$B$内，只取决于$t$及以前可观测的信息$\mathcal F_t$，而于无关$t$以后的信息。
    *   比如，**首达时是自然域流下的停时**：$X$是$(\Omega,\Sigma,P)$上的随机过程，$X$的状态空间为$(S,\mathscr S)$，$\tau$定义为$X$首次到达$A\in \mathscr S$的时间，即首达时$\tau=\inf\{t\in T|X_t\in A\}$，则$\tau$是$F^X$-停时，$F^X$是$X$的自然域流。

### 鞅

定义|**（连续）鞅**：域流概率空间$(\Omega,\Sigma,F,P)$上，状态空间$(\R^n,\mathscr B(\R^n))$，时间$T\sube\R$（$T=\R_{\geq0}$），有$F$-适应随机过程$X$，($X$轨迹连续)，$X$是$F$-（连续）鞅，若$\forall t\in T$，都有：

*   $\mathbb E(|X_t|)<\infty$
*   $\mathbb E(X_t|\mathcal F_s)=X_s, \forall t\geq s$​

说明：上述“连续”表示$X$的轨迹连续，即$\forall \omega\in \Omega: X(\cdot,\omega)\in C(\R_{\geq0};\R^n)$

定义|**（连续）局部鞅**：域流概率空间$(\Omega,\Sigma,F,P)$上，，状态空间$(\R^n,\mathscr B(\R^n))$，时间$T\sube\R$（$T=\R_{\geq0}$），有$F$-适应随机过程$X$，$X$是$F$-$P$-局部鞅，若存在一列$F$-停时$\tau_k, k\in \N$

*   $\tau_k$几乎必然单调递增：$P(\tau_k<\tau_{k+1})=1$;
*   $\tau_k$几乎必然趋近无穷：$P(\lim_{k\rightarrow\infty}\tau_k=\infty)=1$;
*   停止过程(stopped processs)$X_t^{\tau_k}:=X_{\tau_k\and t}$是（连续）鞅，$\forall k\in \N$。

简明定义：存在一列几乎必然**增加到正无穷的停时**，使得此随机过程对应的每个**停时过程**都是**鞅**，则称此随机过程为一个局部鞅。

理解：如果不是停时无界，就差一点是鞅了。

性质：局部鞅并不都是鞅，但鞅一定是局部鞅。



### 二次变差

[wiki：二次变差](https://zh.wikipedia.org/wiki/二次变差)

定义（不严格）｜**二次变差/平方变差**： $X:\R_{\geq0}\times\Omega\mapsto \R$ 是定义在概率空间 $(\Omega,\Sigma,P)$ 上的值随机过程。其二次变差也是一个随机过程, 定义为
$$
[X]_t=\lim _{\|K\| \rightarrow 0} \sum_{k=1}^n\left(X_{t_k}-X_{t_{k-1}}\right)^2
$$

其中$K$是取遍区间 $[0, t]$ 所有的划分，范数 $\|K\|$ 等于$K$​ 中最长的子区间的长度，极限使用依概率收敛来定义。

定义（严格）｜**二次变差/平方变差**：$X$是连续局部鞅，$[X]_t:=X_t^2-2\int _0^t X_s\dd X_s,(\forall t\geq 0)$，则过程$[X]$称$X$的平方变差过程。

理解：$[X]_t=X_t^2-2\int_0^tX_s\dd X_s=\int_0^t \dd(X_s^2)-\int_0^t 2 X_s\dd X_s=\int_0^t[(2X_s \dd X_s+\dd X_s \dd X_s)-2X_s\dd X_s]=\int_0^t \dd X^2_s$，故和定义（不严格）等价。

**定理**：若$X$是连续局部鞅，则：

连续增过程$Y$，$X^2-Y$是连续局部鞅$\Leftrightarrow$ $Y=[X]$ <a name='二次差变的定理'></a>

>   证明：？

*   $Y=[X]\Leftrightarrow X^2-Y$是连续局部鞅，且$Y$​时间连续、单调递增

定义｜**协/互变差**： $X_t:\R_{\geq0}\times\Omega\mapsto \R$ 是定义在概率空间 $(\Omega,\Sigma,P)$ 上的值随机过程。其协/互变差也是一个随机过程，定义为
$$
[X, Y]_t=\lim _{\|K\| \rightarrow 0} \sum_{k=1}^n\left(X_{t_k}-X_{t_{k-1}}\right)\left(Y_{t_k}-Y_{t_{k-1}}\right)
$$

**性质**：

*   $\dd{} [X]_t=(\dd X_t)^2, [X]_t=\int_0^t (\dd X_\tau)^2$​
*   $\dd{} [X,Y]_t=\dd X_t\dd Y_t, [X,Y]_t=\int_0^t \dd X_t\dd Y_t$
*   互变差可以用二次变差表达：

$$
[X, Y]_t=\frac{1}{2}\left([X+Y]_t-[X]_t-[Y]_t\right)
$$

>   证明：$xy=\frac1 2((x+y)^2-x^2-y^2)$，带入$x=X_{t_{k+1}}-X_{t_k}$，$y=Y_{t_{k+1}}-Y_{t_k}$，然后求和，即得上式。

*    标准布朗运动存在二次变差$[W]_t=t, \dd{} [W]_t=\dd t$​​

### Itô公式

[Itô公式课件](https://www.math.pku.edu.cn/teachers/liuyong/asa/Ito.pdf)

**定理｜Itô公式I**：若$F(x)$二次连续可微，$W$是标准布朗运动，则
$$
F(W_t)=F(W_0)+\int_0^t F'(W_s)\dd W_s+\int _0^t \frac 1 2 F''(W_s)\dd{} [W]_s\\
=F(W_0)+\int_0^t F'(W_s)\dd W_s+\int _0^t \frac 1 2 F''(W_s)\dd s\\
等价于d F(W_t)=F'(W_t)\dd W_t+\frac{1}{2}F''( W_t)\dd t
$$
**定理｜Itô公式II**：若$F(t,x)$关于$t$一次连续可微，关于$x$二次连续可微，$W$​是标准布朗运动，则
$$
F(t,W_t)=F(0,W_0)+\int_0^t F'_{x}(s,W_s)\dd W_s+\int _0^t \frac 1 2 F''_{xx}(s,W_s)\dd s+\int_0^tF'_t(s,W_s)\dd s\\
等价于 d F(W_t)=F'_x(t,W_t)\dd W_t+\frac{1}{2}F_{xx}''( t,W_t)\dd t+F_t'(t,W_t)\dd t
$$
特例：

$X$是扩散过程，其积分形式（Itô积分）为：（下式中$W$是标准布朗运动）
$$
X_t=X_0+\int_0^t \mu(t,X_t)\dd {[B]_t} +\int_0^t\sigma(s,X_s)\dd W_s\\
=X_0+\int_0^t \mu(t,X_t)\dd t +\int_0^t\sigma(s,X_s)\dd W_s
$$
其等价的微分形式（Itô方程）为：
$$
\dd X_t=\mu(t,X_t)\dd t+\sigma(t,X_t)\dd W_t
$$
其二次变差为
$$
[X]_t=\int_0^t\sigma^2(s,X_s)\dd s\label{[x]t}\\ \dd{[X]_t}=(\dd X_t)^ 2=\sigma^2(t,X_t)\dd t
$$
**定理｜Itô公式III**：扩散过程的SDE（Itô方程）为$\dd X_t=\mu(t,X_t)\dd t+\sigma(t,X_t)\dd W_t$，$W$是标准布朗运动，若$F(t,x)$关于$t$一次连续可微，关于$x$二次连续可微，则
$$
F(t,X_t)=F(0,X_0)+\int_0^t F'_{x}(s,X_s)\dd X_s+\int _0^t \frac 1 2 F''_{xx}(s,X_s)(\dd X_s)^2（即\dd{ [X]_t}）+\int_0^tF'_t(s,X_s)\dd s\\
=F(0,X_0)+\int_0^t F'_{x}(s,X_s)\sigma(s,X_s) \dd W_s+\int_0^t [F'_{x}(s,X_s)\mu(s,X_s)\dd s+\frac 1 2 F''_{xx}(s,X_s)\mu^2(s,X_s)\dd s+F'_t(s,X_s)]\dd s\\
等价于 d F(W_t)=F'_x(t,X_t)\dd X_t+\frac{1}{2}F_{xx}''( t,X_t)\dd t+F_t'(t,X_t)\dd t\\
=F'_{x}(s,X_s)\sigma(s,X_s) \dd W_s+[F'_{x}(s,X_s)\mu(s,X_s)\dd s+\frac 1 2 F''_{xx}(s,X_s)\mu^2(s,X_s)\dd s+F'_t(s,X_s)]\dd s
$$


### Levy定理

**Levy‘s Brown 运动的鞅刻画定理** (Levy’s characterization of Brownian motion)：域流概率空间$(\Omega,\Sigma,F,P)$上，时间$T=\R_{\geq0}$，适应随机过程$X:\Omega\mapsto C(T;\R^n)$， $X_0=0$，以下命题等价：

1.   $X$是布朗运动，
1.   $X$是$F$-局部鞅，且$[X]_t=t\ (\forall t\geq0)$，
1.   $\forall \alpha \in \R, Z_t^\alpha := \exp \left\{i \alpha X_t+\frac{1}{2} \alpha^2 t\right\}(t \geq 0)$ 为 $F$​​-鞅.

证明见：[北京师范大学 本科生毕业论文 (设计) 毕业论文 (设计) 题目: Girsanov 定理及其应用](http://math0.bnu.edu.cn/~lizh/supervise/theses/02baiy.tex)/定理2.1

>   1推2：因为$X$是布朗运动，故易证$X$是连续鞅，$X^2-t$也是连续鞅。由[二次差变的定理](#二次差变的定理)，由于$X^2-t$是连续局部鞅，$t$是连续增过程，故$[X]_t=t$
>
>   2推3：$\forall \alpha\in \R$，令$f(t,x)=\exp\{i\alpha x+\frac1 2 \alpha^2 t\}$，有$f'_x=i \alpha f,f'_t=\frac 1 2 \alpha^2 f,f''_{xx}=-\alpha^2 f$，故由Itô公式得：
>   $$
>   Z^\alpha_t=f(t,X_t)=f(u,X_u)+\int_u^t f'_x(s,X_s)\dd X_s+\int_0^t f_t'(s,X_s)\dd s+\frac 1 2\int_0^t f''_xx(s,X_s)\dd{ [X]_s}\\
>   =Z^\alpha_u+\int_u^t i\alpha f(s,X_s)\dd X_s+\int_0^t \frac 1 2 \alpha^2 f(s,X_s)\dd s+\frac 1 2\int_0^t -\alpha^2f(s,X_s)\dd s\\
>   =Z^\alpha_u+i\alpha\int_u^t  f(s,X_s)\dd X_s
>   $$
>   因为$X$是局部鞅，故$\forall s\geq u,\mathbb E[X_s|\mathcal F_u]=0$，故$\mathbb E (\dd X_s|\mathcal F_u)=0$，故利用$\mathbb E[XY]=\mathbb E [X\mathbb E[Y|X]]$，有
>   $$
>   \mathbb E[\int _u^t f(s,X_s)\dd X_s|\mathcal F_u]=\mathbb E[ \int_u^t f(s,X_s)\mathbb E[\dd X_s|\mathcal F_s]|\mathcal F_u] = \mathbb E[\int_u^tf(s,X_s)0|\mathcal F_u] =0
>   $$
>   故$\mathbb E[Z_t^\alpha|\mathcal F_u]=Z_u^\alpha(\forall 0\leq u\leq t)$， 故$Z^\alpha$是$F$-鞅。
>
>   3推1：$\forall 0\leq s\leq t,\forall \alpha\in\R$，有$\mathbb E[Z_t^\alpha |\mathcal F_s]=Z_s^\alpha$，即
>   $$
>   \mathbb E[\exp\{i\alpha X_t+\frac 1 2 \alpha^2 t\}|\mathcal F_s]=\exp\{i\alpha X_s+\frac 1 2 \alpha^2 s\}
>   $$
>   左右同除$\exp\{i\alpha X_s+\frac 1 2 \alpha^2 t\}$，得
>   $$
>   \mathbb E[\exp\{i\alpha( X_t-X_s)\}|\mathcal F_s]=\exp\{-\frac 1 2 \alpha^2(t- s)\}
>   $$
>   即 $X_t-X_s$ 在条件 $\mathcal {F}_s$ 下的特征函数为正态变量 $N(0, t-s)$ 的特征函数。因此 $X_t-X_s$ 独立于 $\mathcal{F}_s$ , 且服从正态 $N(0, t-s)$ 分布,。即 $X$ 为布朗运动。

## Girsanov定理

参考1：[【FinE】Girsanov定理](https://blog.csdn.net/qq_18822147/article/details/107904463)

参考2：[Wikipedia: Girsanov theorem](https://en.wikipedia.org/wiki/Girsanov_theorem)

参考3：[北京师范大学 本科生毕业论文 (设计) 毕业论文 (设计) 题目: Girsanov 定理及其应用](http://math0.bnu.edu.cn/~lizh/supervise/theses/02baiy.tex)

### 抽象版本

$W_t$为概率空间$(\Omega,\Sigma, P)$上的布朗运动，$X_t$为连续局部鞅，适应于$W_t$的自然域流$F^W$。定义随机过程$Z_t$
$$
Z_t=\exp\{X_t-\frac1 2[X]_t\},
$$
其中，$[X]_t$是$X_t$的二次变差。

若$Z_t$是一致可积正鞅，则可定义概率$P^*$：
$$
\frac{\dd P^*}{\dd P}(\omega)\bigg|_{\mathcal F_t}=Z_\omega(t),\\
即 P^*(A):=\int _{\omega\in A} Z_\omega(t) P(\dd \omega),\forall A\in \mathcal F_t
$$
若随机过程$Y_t$在$(\Omega,\Sigma,F,P)$中是局部鞅，则随机过程$Y^*_t=Y_t-[Y,X]_t$在$(\Omega,\Sigma,F,Q)$​中是$Q$-局部鞅，且
$$
[Y^*]^Q_t=[Y]_t, \forall t\geq 0
$$
其中，$[Y^*]^Q_t$是$Q$下的$Y^*_t$​的平方变差。



证明：

第一步：证明$\Phi_t Z_t$是连续$P$-局部鞅

令$\Phi_t^\alpha=\exp\{\alpha Y^*_t -\frac 1 2\alpha ^2 [Y^*]^Q_t\}$，则

$$
\Phi_t ^\alpha Z_t= \exp\{\alpha Y^*_t -\frac 1 2\alpha ^2 [Y^*]^Q_t + X_t-\frac1 2[X]_t  \}\\
=\exp\{\alpha Y_t -\alpha [Y,X]_t -\frac 1 2\alpha ^2 [Y]_t + X_t-\frac1 2[X]_t  \}\\
=\exp\{M_t-\frac 1 2 [M]_t\}
$$

其中$M_t=X_t+\alpha Y_t$。因为$X_t,Y_t$都是连续$P$-局部鞅，故$M_t$也是连续$P$-局部鞅。

记$\Phi_t^\alpha Z_t=f(x,y)=\exp\{x-\frac1 2 y\}$，有$f'_x=f,f'_y=-\frac 1 2f,f''_{xx}=f$

$$
\dd f=f'_x\dd x+\frac 1 2 f''_{xx} (\dd x)^2+f'_y \dd y\\
即\dd (\Phi_t^\alpha Z_t)=\Phi_t^\alpha Z_t (\dd M_t+\frac 1 2\dd [M]_t-\frac 1 2\dd [M]_t)=\Phi_t^\alpha Z_t\dd M_t
$$

因为$M_t$是连续$P$-局部鞅，故$\Phi_t Z_t$是连续$P$-局部鞅。

第二步：

$\forall t>s, \forall A\in \mathcal F_s,\forall \alpha\in\R$，有

$$
\int_A \Phi_t^\alpha\dd Q=\int _A \Phi_t^\alpha Z_t \dd P\\
\mathbb E^Q[\Phi_t^\alpha|A]=\int_A \Phi_t^\alpha\dd Q=\int _A \Phi_t^\alpha Z_t \dd P=\mathbb E^P[\Phi_t^\alpha Z_t|A]\\
故 \mathbb E^Q[\Phi_s^\alpha|\mathcal F_s]=\mathbb E^P[\Phi_s^\alpha Z_\alpha|\mathcal F_s]=\Phi_s^\alpha Z_s
$$

当$\Phi^\alpha\Z$是$P$-局部鞅，则$\Phi^\alpha=\exp\{\alpha Y^* -\frac 1 2\alpha ^2 [Y^*]^Q\}$是$Q$-局部鞅。

故，$$

### 通用版本

$W_t$为概率空间$(\Omega,\Sigma, P)$上的布朗运动，时间$[0,\infty)$，令$\Theta_\omega(t)$为$W_t$的自然域流$ F^W$上的适应过程。定义随机过程$Z_t$
$$
Z_\omega(t):=\exp\{-\frac 1 2\int _0^t\Theta^2_\omega(s)\dd s-\int_0^t \Theta_\omega(s)\dd W_s\}
$$
有性质：$\forall t\in [0,\infty), \mathbb E Z_t=1, Z_t\geq0$。

构造随机运动$ W^*_t$:
$$
\dd W^*_t=\dd W_t+\Theta_\omega(t)\dd t,\\
即 W^*_t:=W_t+\int_0^t \Theta_\omega(s)\dd s;
$$
在可测空间$(\Omega,\Sigma)$上构造概率测度$P^*$:
$$
\frac{\dd P^*}{\dd P}(\omega)\bigg|_{\mathcal F_t}=Z_\omega(t)
$$
则在$(\Omega,\Sigma,F^W,P^*)$中，$ W^*_t$​是布朗运动。

证明：

*   直接证明：见[【FinE】Girsanov定理](https://blog.csdn.net/qq_18822147/article/details/107904463)。

*   用抽象版本的Girsanov定理去证明：

    令$X_t=-\int_0^t \Theta_\omega(s)\dd W_s$，则由性质$\eqref{[x]t}$有， $ [X]_t=\int_0^t \Theta^2_\omega(s)\dd s$。

    故$\frac{\dd P^*}{\dd P}=Z_t=\exp\{X_t-\frac 1 2[X]_t\}=\exp\{-\frac 1 2\int _0^t\Theta^2_\omega(s)\dd s-\int_0^t \Theta_\omega(s)\dd W_s\}$。

    取$Y_t=W_t$，则$\dd{}[Y,X]_t=\dd X_t \dd Y_t=-\Theta_\omega(t)\dd W_t \dd W_t=-\Theta_\omega(t)\dd t$。

    此时$ Y^*_t=Y_t- [Y,X]_t= W_t+\int_0^t\Theta_\omega(s)\dd s=: W^*_t$，在概率测度$Q$​下是局部鞅。

    又因为$[Y^*]_t=\int_0^t \dd (Y^*_s)^2=\int_0^s \dd W_t^2+o(\dd s)= t, \forall t\geq0$；$Y^*_\omega(t)$连续($\forall \omega\in\Omega$)；$Y^*_0=W_0+\int_0^0\Theta_\omega(s)\dd s=W_0=0$；

    $Y^*_t$在$Q$下是局部鞅。故由Levy定理，$Y^*_t$是$Q$-标准布朗运动。

### 扩散过程版本

在测度空间$(\Omega,\Sigma,P)$，有标准布朗运动$W_t$，和由他决定的随机过程$X_t$（或记作$X_\omega(t),\omega$对应一条轨迹），满足扩散方程：
$$
\dd X_t=f(t,X_t)+\sigma(t,X_t)\dd W_t
$$
若$f^*(t,x)$为新的漂移方程，$\dfrac{f^*-f}{\sigma}(t,x)$有界，则可

*   定义测度$P^*$：

$$
\frac{\dd P^*}{\dd P}(\omega)\bigg|_{\mathcal F_t}=\exp\{-\frac{1}{2}\int_0^t \left(\frac{f^*(s,X_\omega(s))-f(s,X_\omega(s))}{\sigma(s,X_\omega(s))}\right)^2\dd s +\int_0^t \frac{f^*(s,X_\omega(s))-f(s,X_\omega(s))}{\sigma(s,X_\omega(s))}\dd W_s \}
$$

* 构造随机过程$W^*$：

$$
\dd W^*_t=-\frac{f^*(t,x_t)-f(t,x_t)}{\sigma(t,x_t)}\dd t+\dd W_t
$$

则在$(\Omega,\Sigma,P^*)$中$W^*$是布朗运动，且$\dd X_t=f^*(t,X_t)\dd t+\sigma(t,X_t)\dd W^*_t$。

证明：

假设同一个随机过程$X_t$有两种等价的参数化方式：
$$
\dd X_t=f(t,X_t)+\sigma(t,X_t)\dd W_t, W_t在(\Omega,\Sigma,P)中是标准布朗运动\\
\dd X_t=f^*(t,X_t)+\sigma(t,X_t)\dd W^*_t, W^*_t在(\Omega,\Sigma,P^*)中是标准布朗运
$$
想求$\dd W_t^*$与$\dd W_t$的关系，和$P^*$和$P$的关系。

上下两式相减，有$f(t,X_t)-f^*(t,X_t)+\sigma(t,X_t)(\dd W_t-\dd W^*_t)=0$

令随机过程$\Theta_\omega(t):=-\dfrac{f^*(t,X_\omega(t))-f(t,X_\omega(t))}{\sigma(t,X_\omega(t))}$，则有$\dd W_t^*=\Theta(t)\dd t+\dd W_t$。

由通用版本的Girsanov定理，
$$
\frac{\dd P^*}{\dd P}(\omega)\bigg|_{\mathcal F_t}=Z_\omega(t):=\exp\{-\frac 1 2\int _0^t\Theta^2_\omega(s)\dd s-\int_0^t \Theta_\omega(s)\dd W_s\}\\
=\exp\{-\frac{1}{2}\int_0^t \left(\frac{f^*(s,X_\omega(s))-f(s,X_\omega(s))}{\sigma(s,X_\omega(s))}\right)^2\dd s +\int_0^t \frac{f^*(s,X_\omega(s))-f(s,X_\omega(s))}{\sigma(s,X_\omega(s))}\dd W_s \}
$$
