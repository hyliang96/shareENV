## 实验室的信息

瑞莱（RealAI）旗下又开了生数公司，鲍凡在生数当合伙人。

刘雯：在荣耀公司工作，在该公司和生数合作中担任驻场甲方工作人员。

生数还和许多公司有合作。

荣耀公司在工业应用的要求：换脸、换衣服、真实照片、像本人的风格画（而非高度夸张的卡通画），这些可用于图像编辑，比如妙鸭相机

## Diffusion应用有关工作

* [Chi Zhang：生成多人头像](https://icoz69.github.io)，有论文，未开源，在cross-attention上实现多人头像的拼图
* [InstantID : Zero-shot Identity-Preserving Generation in Seconds](https://instantid.github.io)：无论文，未开源，类似regional prompt: 多句prompt分别控制不同区域骨架（是骨架吗？）的latent，latent再融合
* [Face0: Instantaneously Conditioning a Text-to-Image Model on a Face](https://arxiv.org/abs/2306.06638)：google的论文
* [AnyDoor](https://github.com/ali-vilab/AnyDoor)：有论文，已开源，图像编辑，可以移动目标物体
* Face Studio：从promt生成保真的（即照片那样的，而不是风格化的）人脸图像
* Adobe firefly：在云端完成计算，风格迁移、用文本propmt修补图像、文生图，比如换发型

## diffusion中特征融合的方法

* Adapter：
  * 过cross attention后相加
    * 比如：ControlNet
  * concat(image embedding, text embedding)
    * T2I Adapter（是concat吗？）
    * IP Adapter（是concat吗？）
    * 现在荣耀的思路是将T2I Adapter和IP Adapter结合起来

## graph和diffusion结合

**diffusionSeg：2023年3月，用stable diffusion产生的feature，经过graph Net，去做分割。**

UniGS：统一分割和生成

我的idea：在UniGS基础上加个graph，就像diffusionSeg那样

## 资源库

[CititAI模型库](https://civitai.com)：许多人自己训练的模型，上传了预训练模型参数，可以下载到本地

## 现有问题

* 手部生成的不好，堆数据可以降低次品率，但仍有次品
* 相对全图的小目标生成的不好，比如头像中的耳环生成不好，比如全身像中的五官会乱飞
* 精细属性控制：对策多是用图像做prompt；用文本prompt很难实现，因为缺少相应的带有精细属性文本prompt标注的图像数据

图像形式的promt类型：边缘、骨架、涂鸦、深度图、简笔画、分割图、点云
