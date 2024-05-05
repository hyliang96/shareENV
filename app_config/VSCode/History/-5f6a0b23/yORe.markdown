# Diffusion介绍

图解：

神奇画笔的养成：解密 ai 生成图片的原理与应用[https://edge.aif.tw/aicafe-0830-diffusion-mode/](https://edge.aif.tw/aicafe-0830-diffusion-mode/)

![1706288785108](assets/1706288785108.png)

全网最简单的扩散模型DDPM教程[https://zhuanlan.zhihu.com/p/566618077](https://zhuanlan.zhihu.com/p/566618077)

训练：

![1706288821321](assets/1706288821321.png)

生成：

![1706288871169](assets/1706288871169.png)

文转图：UNET、CLIP、Diffusion、stable diffusion

十分钟读懂Diffusion：图解Diffusion扩散模型[https://zhuanlan.zhihu.com/p/599887666](https://zhuanlan.zhihu.com/p/599887666)

①可以输入来自CLIP的text embedding、image embedding（如从depth map获得的），还可以二者concate起来

![1706288948682](assets/1706288948682.png)

UNet模型结构：Downsampe、Middle block、Upsample中都包含了ResNet残差网络。

![1706288987645](assets/1706288987645.png)

UNet网络中如何使用文字embedding：在UNet的每个ResNet之间添加一个Attention，而Attention一端的输入便是文字embedding：

![1706289015100](assets/1706289015100.png)

![1706289106471](assets/1706289106471.png)

使用CLIP模型生成输入文字embedding：

![1706289201791](assets/1706289201791.png)

CLIP：生成成对的image embedding和text embedding

CLIP论文：[https://arxiv.org/pdf/2103.00020.pdf](https://arxiv.org/pdf/2103.00020.pdf)

![1706289296954](assets/1706289296954.png)

Diffusion模型的缺点及改进版——Stable Diffusion ([https://zhuanlan.zhihu.com/p/599887666](https://zhuanlan.zhihu.com/p/599887666))

前面我们在介绍整个文字生成图片的架构中，图里面用的都是Stable Diffusion，后面介绍又主要介绍的是Diffusion。其实Stable Diffusion是Diffusion的改进版。

Diffusion的缺点是在反向扩散过程中需要把完整尺寸的图片输入到U-Net，这使得当图片尺寸以及time step t足够大时，Diffusion会非常的慢。Stable Diffusion就是为了解决这一问题而提出的。后面有时间再介绍下Stable Diffusion是如何改进的。

补充4：DDPM为什么要引入时间步长t ([https://zhuanlan.zhihu.com/p/599887666](https://zhuanlan.zhihu.com/p/599887666))

引入时间步长 t 是为了模拟一个随时间逐渐增强的扰动过程。每个时间步长 t 代表一个扰动过程，从初始状态开始，通过多次应用噪声来逐渐改变图像的分布。因此，较小的 t 代表较弱的噪声扰动，而较大的 t 代表更强的噪声扰动。

这里还有一个原因，DDPM中的 UNet 都是共享参数的，那如何根据不同的输入生成不同的输出，最后从一个完全的一个随机噪声变成一个有意义的图片，这还是一个非常难的问题。我们希望这个UNet模型在刚开始的反向过程之中，它可以先生成一些物体的大体轮廓，随着扩散模型一点一点往前走，然后到最后快生成逼真图像的时候，这时候希望它学习到高频的一些特征信息。由于UNet 都是共享参数，这时候就需要 time embedding 去提醒这个模型，我们现在走到哪一步了，现在输出是想要粗糙一点的，还是细致一点的。

所以加入时间步长 t 对生成和采样过程都有帮助。

推公式：

* 由浅入深了解Diffusion Model[https://zhuanlan.zhihu.com/p/525106459](https://zhuanlan.zhihu.com/p/525106459)
* 一文读懂Diffusion Model[https://zhuanlan.zhihu.com/p/599160988](https://zhuanlan.zhihu.com/p/599160988)

用公式解读代码：

* AIGC爆火的背后——扩散模型DDPM浅析[https://zhuanlan.zhihu.com/p/590840909](https://zhuanlan.zhihu.com/p/590840909)
* 一文弄懂 Diffusion Model[https://zhuanlan.zhihu.com/p/586936791](https://zhuanlan.zhihu.com/p/586936791)
