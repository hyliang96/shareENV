---
title: 谷歌云
date: 2021-10-13 22:10:13
updated:
categories:
  - 器
  - private.科学上网
  - 云计算平台
tags:
---

# 谷歌云

如果流量不大，推荐用谷歌云，有台湾服务器，到大陆时延短。

谷歌云在墙外, 需要先有个梯子登录它

## 优惠政策

(2020-8撰)

*   谷歌云免费体验时长调整为90天, 还是送300刀; 但不影响老用户的免费试用

(2020-3撰)

谷歌云为了吸引用户，有以下优惠：

* 用邮箱注册，赠送300刀，限用一年，称试用期。
* 绑定可付美元信的用卡，注册时扣一刀，测试卡能用，后立即退款。
* 一年期满，通知你续费，并冻结你的谷歌云服务器，而不会自动开始续费。
* 一年期满时注销账号，再用新邮箱注册新谷歌账号，需要用新手机号验证身份。
* 新谷歌账号绑定原信用卡，又得到300刀优惠，又可用一年。

## 创建一个服务器

登录[谷歌云](https://console.cloud.google.com/)，注册账号

然后创建服务器

![屏幕快照% 2019-08-15 23.15.03](assets/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-08-15%2023.15.03.png)

![屏幕快照% 2019-08-15 23.15.20](assets/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-08-15%2023.15.20.png)

设置详情请参考[本地资料](./GoogleCloud使用教程.pdf) 即 [网页](https://lala.im/3353.html)

选择说明：

* 线路选择，`asia-east1-a`  `asia-east1-b` 稳定，`asia-east1-c`时延短 但容易被墙发现

## 修改静态ip

一个ip长期使用，可能被墙识别，变得翻墙缓慢乃至无法翻墙，可以尝试换ss服务端的端口，若仍不行，则需要换ss服务器的ip。如现在想改主机sshost5的ip——将原始静态ip改成另一个新的静态ip，在谷歌云上操作方法如下几步：

### 更换为新临时ip

云谷歌云可以不关机时，直接改ip，步骤如下：

先将本地使用**另一个ss的服务账号来翻墙**，不然换ip后，客户端ip未换, 则谷歌云的网页刷新不出来，无法显示新ip。

[教程来源](https://odcn.top/2019/01/08/2024/更换google-cloud-platform（谷歌云）vm实例外部ip/)

登陆到[Google Cloud Platform](https://cloud.google.com/)

点击“转至控制台”，选择菜单——Compute Engine——VM实例

![img](assets/%E6%9B%B4%E6%8D%A2google-cloud-platform%EF%BC%88%E8%B0%B7%E6%AD%8C%E4%BA%91%EF%BC%89vm%E5%AE%9E%E4%BE%8B%E5%A4%96%E9%83%A8ip.png)

看到在运行的实例状态

![img](assets/%E6%9B%B4%E6%8D%A2google-cloud-platform%EF%BC%88%E8%B0%B7%E6%AD%8C%E4%BA%91%EF%BC%89vm%E5%AE%9E%E4%BE%8B%E5%A4%96%E9%83%A8ip-1.png)

开始更换外部IP，找到菜单——VPC网络——外部IP地址

![img](assets/%E6%9B%B4%E6%8D%A2google-cloud-platform%EF%BC%88%E8%B0%B7%E6%AD%8C%E4%BA%91%EF%BC%89vm%E5%AE%9E%E4%BE%8B%E5%A4%96%E9%83%A8ip-2.png)

附加在实例的IP不能被释放，所以找到附加在运行这个实例的IP，点击“更改”

![img](assets/%E6%9B%B4%E6%8D%A2google-cloud-platform%EF%BC%88%E8%B0%B7%E6%AD%8C%E4%BA%91%EF%BC%89vm%E5%AE%9E%E4%BE%8B%E5%A4%96%E9%83%A8ip-3.png)

在附加到的选项里选择“无”，确定完成

![img](assets/%E6%9B%B4%E6%8D%A2google-cloud-platform%EF%BC%88%E8%B0%B7%E6%AD%8C%E4%BA%91%EF%BC%89vm%E5%AE%9E%E4%BE%8B%E5%A4%96%E9%83%A8ip-4.png)

这时会重新分配一个临时IP给运行的这个实例，并且弹出计费警告。不用在意，点击确定完成

![img](assets/%E6%9B%B4%E6%8D%A2google-cloud-platform%EF%BC%88%E8%B0%B7%E6%AD%8C%E4%BA%91%EF%BC%89vm%E5%AE%9E%E4%BE%8B%E5%A4%96%E9%83%A8ip-5.png)

等待完成会出现一个未附加到实例的静态IP和一个临时IP，一个实例只能绑定一个IP，未绑定的IP将单独计费，所以把不再需要的IP释放掉。选中需要释放IP点击“释放静态地址”，这样这个IP就被释放掉了。

![img](assets/%E6%9B%B4%E6%8D%A2google-cloud-platform%EF%BC%88%E8%B0%B7%E6%AD%8C%E4%BA%91%EF%BC%89vm%E5%AE%9E%E4%BE%8B%E5%A4%96%E9%83%A8ip-6.png)

使用静态IP类型重启系统后IP不会发生改变，所以新IP类型选择“静态”，点击“更改”，名称随便填，点击“保留”并附加到需要绑定的实例上

![img](assets/%E6%9B%B4%E6%8D%A2google-cloud-platform%EF%BC%88%E8%B0%B7%E6%AD%8C%E4%BA%91%EF%BC%89vm%E5%AE%9E%E4%BE%8B%E5%A4%96%E9%83%A8ip-7.png)

保留实例更换外部IP完成. 然后，修改本地的ss客户端中 对应的ss账号ip，测试它能否流畅翻墙.

## 再薅一年羊毛并续命项目

每个谷歌账号，初次使用谷歌云，需凭信用卡开启一个结算账号，获得一年试用期。

期满，谷歌云会自动关停用此结算账号结算的项目下的**实例**，而不会自动扣费。

![ScreenShot 2020-03-16 02.12.51](assets/ScreenShot%202020-03-16%2002.12.51.png)

![ScreenShot 2020-03-15 13.56.04](assets/ScreenShot%202020-03-15%2013.56.04.png)

2019年初之前，可以用旧谷歌账号获得第二次一年试用：旧谷歌账号，在谷歌云平台，解绑信用卡，然后在绑定新/旧银行卡号。自2019年中旬起，此方法无效了。

此后，只能用**新谷歌账号**开通谷歌云，绑定**新/旧**信用卡，获得一年试用。一个信用卡可以绑定多个谷歌云账号，使其均获得一年试用。而后可用新谷歌云账号来结算旧谷歌云账号的项目，以此为到期的项目续命一年。

### 注册新谷歌账号

有两种方法获得谷歌账号：

*   在淘宝购买google voice账号，会赠送一个谷歌账号
*   使用一个未注册过谷歌账号的的手机号

以下介绍使用国内手机号注册谷歌账号的注意事项和步骤。

#### 注意事项

*   从2019年中旬开始，注册谷歌账号需要手机号验证身份。

*   此手机号仅是注册用手机号，不是“辅助手机号”（用来找回密码、发送安全通知）。注册成功后，辅助电话号码是空的，需要的话自行绑定。

    ![image-20200315185617581](assets/image-20200315185617581.png)

*   一个手机号**只能注册一个谷歌账号**

*   国内手机号，用浏览器无法用来注册谷歌账号，会卡在手机号验证这一步，显示如下。对策：用手机的谷歌服务框架、或gmail手机app来注册。

![ScreenShot 2020-03-06 15.45.33](assets/ScreenShot%202020-03-06%2015.45.33.png)

*   存疑：频繁试图注册新谷歌账号（及未遂）的ip，会被谷歌列为不信任，用此ip注册谷歌账号，不论使用什么手机号，均会显示如上。
*   存疑：频繁试图注册新谷歌账号（及未遂）的手机号，会被谷歌列为不信任，用此手机号注册谷歌账号，不论用什么ip，均会显示如上。

#### 注册步骤

步骤如下

*   找一个未注册谷歌账号的手机号，将其手机卡插入手机中。（如，用亲友的手机）
*   手机安装翻墙软件，并开启翻墙
*   安装了谷歌服务框架 (有的安卓手机预装了，如华为) 或 安装gmail
*   在谷歌服务框架注册新账号（步骤如下），或在gmail中注册新账号（会跳转到谷歌服务框架，进入如下步骤）

<img src="assets/WechatIMG129.jpeg" alt="WechatIMG129" style="zoom:25%;" />

<img src="assets/WechatIMG128.jpeg" alt="WechatIMG128" style="zoom:25%;" />

<img src="assets/WechatIMG127.jpeg" alt="WechatIMG127" style="zoom:25%;" />

<img src="assets/WechatIMG126.jpeg" alt="WechatIMG126" style="zoom:25%;" />

<img src="assets/WechatIMG125.jpeg" alt="WechatIMG125" style="zoom:25%;" />

<img src="assets/WechatIMG124.jpeg" alt="WechatIMG124" style="zoom:25%;" />

<img src="assets/WechatIMG123.jpeg" alt="WechatIMG123" style="zoom:25%;" />

<img src="assets/WechatIMG122.jpeg" alt="WechatIMG122" style="zoom:25%;" />

注意：

*   需使用当前手机自己的手机号号。若系统未自动填写之，可自行填写。
*   一个手机号只能注册一个谷歌账号。如果用以前注册过的手机号，则会提示如下：

<img src="assets/WechatIMG121.jpeg" alt="WechatIMG121" style="zoom:25%;" />

### 开启谷歌云领取一年试用

法同初次注册谷歌云账号的方法。

一个信用卡可以绑定多个谷歌云账号以获得一年试用。故此时，可以使用旧谷歌云账号的信用卡。

### 用新账号代老账号结算

*   新谷歌云账号：将结算账号 添加旧谷歌云账号 作为 结算账号管理员

![ScreenShot 2020-03-15 12.32.37](assets/ScreenShot%202020-03-15%2012.32.37.png)

![ScreenShot 2020-03-15 12.47.21](assets/ScreenShot%202020-03-15%2012.47.21.png)

此时，就谷歌云账号，就会看见这个结算账号

![image-20200315201409914](assets/image-20200315201409914.png)

*   旧谷歌云账号：将需要续命的项目，更改使用新结算账号支付

![ScreenShot 2020-03-15 02.31.35](assets/ScreenShot%202020-03-15%2002.31.35.png)

### 停用（将）到期的结算账号

旧谷歌云账号：快要试用到期的结算账号停用, 从此此结算账号不会产生扣费。若此谷歌云账号获得了新谷歌云账号给的新结算账号，则此谷歌云账号开创的任何新项目，会使用新结算账号。

![ScreenShot 2020-03-16 02.31.34](assets/ScreenShot%202020-03-16%2002.31.34.png)

已经试用到期的的结算账号：已经自动停用。
![ScreenShot 2020-03-16 02.12.51](assets/ScreenShot%25202020-03-16%252002.12.51.png)

将以已经停用的账号的项目逐一关停结算功能：

![ScreenShot 2020-03-16 02.31.34的副本](assets/ScreenShot%202020-03-16%2002.31.34%E7%9A%84%E5%89%AF%E6%9C%AC.png)

![ScreenShot 2020-03-15 02.14.01](assets/ScreenShot%202020-03-15%2002.14.01.png)

