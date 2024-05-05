刘雯：在荣耀公司工作，在该公司和朱老师的合作中担任驻场甲方

# Diffusion应用有关工作

* [Chi Zhang：生成多人头像](https://icoz69.github.io)，有论文，未开源，在cross-attention上实现多人头像的拼图
* [InstantID : Zero-shot Identity-Preserving Generation in Seconds](https://instantid.github.io)：无论文，未开源，类似regional prompt: 多句prompt分别控制不同区域骨架（是骨架吗？）的latent，latent再融合
* [Face0: Instantaneously Conditioning a Text-to-Image Model on a Face](https://arxiv.org/abs/2306.06638)：google的论文


diffusion中特征融合的方法：

* Adapter：

  * 过cross attention后相加
    * 比如：ControlNet
  * concat(image embedding, text embedding)
    * T2I Adapter
    * IP Adapter
    * 现在荣耀的思路是
