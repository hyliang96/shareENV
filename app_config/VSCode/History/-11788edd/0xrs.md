---
title: AWS
date: 2021-10-13 22:11:54
updated:
categories:
  - 器
  - private.科学上网
  - 云计算平台
tags:
---
# AWS

AWS在墙内能访问, 不需要先有个梯子登录

[AWS服务器搭建教程](https://belen.one/blog/2016/05/create-amazon-web-services/)

登陆：[AWS官网](https://aws.amazon.com)

## 优惠政策

[查看AWS有哪些免费产品](https://aws.amazon.com/cn/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%2312monthsfree&awsf.Free%20Tier%20Categories=*all#Free_Tier_details)：

*   [查看AWS有哪些短期免费试用的产品](https://aws.amazon.com/cn/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%23trial&awsf.Free%20Tier%20Categories=*all#Free_Tier_details)

*   [查看AWS有哪些12个月免费的产品](https://aws.amazon.com/cn/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%2312monthsfree&awsf.Free%20Tier%20Categories=*all#Free_Tier_details)

*   [查看AWS有哪些永久免费的产品](https://aws.amazon.com/cn/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%23always-free&awsf.Free%20Tier%20Categories=*all#Free_Tier_details)：只提供非计算服务



您在首次注册后, 有[**12个月免费套餐**](https://aws.amazon.com/cn/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%2312monthsfree&awsf.Free%20Tier%20Categories=*all#Free_Tier_details), 包括如下内容

* 内存/磁盘/机器 均按机时计价:

  * 公网IP：

      *   12个月试用期的免费额度：
          *   公网IPv4 地址用量： 750 小时\* IP个数/月，即**全月不停机只能开1个公网IPv4**
          *   公网IPv6免费
          *   弹性IP：有1个弹性IP的免费额度，但算到公网IPv4里，合在一起**只能开1个**
      *   非12个月试用期/试用免费额度之外的IP使用：
          *   从2024年2月1日起，**公网ipv4要收费**， [详见](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/)
              *   非弹性IP（闲置就给别人用）：每小时0.005美元（只有在用才收费）
              *   弹性IP（闲置时也占用）：每小时0.005美元（不论闲置还是在用都收费）
          *   公网IPv6免费

  * 网络流量

      *   网络带宽： 100GB
      *   入站流量（即进入所在AWS区域的流量）：0美元/GB
      *   出站流量（即离开所在AWS区域的流量）：
          *   **站间流量**（即访问其他AWS区域的流量）：0.09美元/GB
          *   出AWS流量（即访问AWS所有区域之外的流量，所有 AWS 服务合计）：
              *   出AWS流量 的**免费上限**： [100GB /月](https://aws.amazon.com/cn/blogs/china/aws-free-tier-data-transfer-expansion-100-gb-from-regions-and-1-tb-from-amazon-cloudfront-per-month/) （从每月1日起开始计算）
              *   **超出免费上限**的 出AWS流量：0.12美元/GB
      *   [网络流量详细价目表](https://aws.amazon.com/cn/ec2/pricing/on-demand/)：

      ![image-20230401171907457](assets/image-20230401171907457.png)

* [12月免费AWS EC2 (即普通主机)](https://amazonaws-china.com/cn/premiumsupport/knowledge-center/free-tier-windows-instance/)

  * 以下免费服务，仅限于免费系统镜像+免费内核
      * 免费系统镜像：包括最新两个偶数版本的Ubuntu
      * 免费内核：t2.micro（或者，在未推出 t2.micro 的区域中是 t3.micro），都是高频 Intel Xeon 处理器，性能可突增的 CPU ，单核
  * 每月送 750机时 (>31d/mx24h/d=744h/m)，即**全月不停机只能开1台**
  * 存储卷的访问次数限制为200万次读写
  * 1GB 的快照存储

* 所有 AWS 服务 合计**最大EBS存储**（弹性存储）： 30GiB

* 机时超限/流量超限/过了体验期时, **继续运行不停机, 并自动扣费**. 但可以**设置预算, 实际开销超阈值则邮件通知自己**. 收到提醒后, 可以[解绑信用卡 避免自动扣费](#解绑信用卡 避免自动扣费)



### [1 个月免费试用 AWS LightSail](https://amazonaws-china.com/cn/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc)

* 非常便宜的轻量级vps, 最低配置 3.5刀/月, 支持银联卡, 推荐使用日本或新加坡.

|                        | EC2                                                                                                                                                                  | Lightsail  |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| 适合                   | 计算                                                                                                                                                                 | 存储和传输 |
| **新用户免费**   |                                                                                                                                                                      |            |
| 免费时长               | 12个月                                                                                                                                                               | 1个月      |
| 存储 (SSD)             | 30GiB                                                                                                                                                                | 20GiB      |
| 流量                   | 15GB/月                                                                                                                                                              | 1TB        |
| 内存                   | 1GB                                                                                                                                                                  | 512MB      |
| 新用户免费时限         | 12个月                                                                                                                                                               | 1个月      |
| **新用户免费后** |                                                                                                                                                                      |            |
| 最便宜的价格 (linux)   | [t2.micro **$8.63/月**](https://amazonaws-china.com/cn/ec2/instance-types/t2/) | [最低配置 $3.5/月](https://amazonaws-china.com/cn/lightsail/pricing/?opdp1=pricing) |            |



## 试用结束再次注册

### 注册新账号

在上一个账号的12个月试用期结束前一个月内, 可以去注册一个新账号

先用**新邮箱**注册新账号, **信用卡/地址/姓名可以与之前的账号相同**, 特能再次获得12个月的免费试用期.

如下就是有12个月试用期的

![image-20211013162643773](assets/image-20211013162643773.png)

![image-20211013162800924](assets/image-20211013162800924.png)

### 注销旧账号

当新账号创建完成, 实例开设完成, 旧账号实例上的数据已经导入到新账号上后, 要在使用期结束前, 注销旧账号, 避免试用期结束开始自动收费. 操作步骤依次如下，[具体操作步骤详见](#注销账号要做的事情)：

* [详见: 解绑信用卡避免自动扣费](#解绑信用卡避免自动扣费)

* [详见：把联系信息换成非实名的](#把联系信息换成非实名的)

* **先终止实例所有实例**, **若实例绑定弹性ip或EBS均要解绑**, 不然关闭账号90天内反悔期内会产生扣费。操作方法如下：

    * [终止实例](#终止实例)
    * [释放弹性IP](#释放弹性IP)
    * [解绑EBS卷](#解绑EBS卷)

* 关闭账号后的反悔期:

  * 关闭帐户后90天内, 若关闭帐户前绑定了可用的支付方式，则**未关停的付费项目还是会自动扣费**。

  * 关闭帐户后90天内, 只能进入[支付管理页面](https://console.aws.amazon.com/billing/home?#/account), 无法进入[实例页面](https://us-west-1.console.aws.amazon.com/ec2/v2/)（会显示如下错误）

      ![image-20240713164417901](assets/image-20240713164417901.png)

  * 若关闭帐户后，要重新激活账号, 需要在关闭帐户后60天内, 按照[重新激活账号指南](https://aws.amazon.com/cn/premiumsupport/knowledge-center/reopen-aws-account/)去操作，**并支付未结清费用**。

  * 在关闭帐户后60天内若不重新激活账号，则之后无法重新激活账号。

  * 关闭帐户后第90天，账号中所有数据注销。

  * 关闭帐户后90天后，彻底注销了AWS账号，但此后，**原先所使用的邮箱无法再次用于注册新的AWS账号**。

* **关闭账号**的操作方法:

    * **新界面**

        ![image-20240713162112170](assets/image-20240713162112170.png)

        ![image-20240713162324804](assets/image-20240713162324804.png)



        ![image-20240713162438149](assets/image-20240713162438149.png)

        ![image-20240713162740399](assets/image-20240713162740399.png)

        这个邮件只是通知你账号关闭了，**不需要再去这个邮件里点确认按钮**。

        而后，**再点`关闭帐户`**，将会看见“该账户已关闭“

        ![image-20240713162324804](assets/image-20240713162324804.png)

        ![image-20240713164111416](assets/image-20240713164111416.png)

    * **旧界面**


![image-20211013162643773](assets/image-20211013162643773.png)

然后滑到页面最下方

![image-20211013220500135](assets/image-20211013220500135.png)

然后，再次访问此页面，就会显示无法再次点击 `关闭帐户`，“您的帐户已关闭”，这说明帐户已经关闭完成。

![iShot_2022-11-19_17.25.05](assets/iShot_2022-11-19_17.25.05.png)

## 注册账号

访问[AWS](http://aws.amazon.com), 点创建账号

### 填邮箱

注册和登录时，都要选择”**根用户**”, 填入邮箱, 密码, 姓名, 地址.

![image-20211013153912943](assets/image-20211013153912943.png)

### 填联系方式

**可以用[外国人身份生成器](https://www.shenfendaquan.com/)，生成假身份（推荐）**；也可以填中国的地址, 中国的电话。

这里填的信息是AWS存下来的用户联系方式，**但不用于注册时接收验证码以验证身份**（详见：[电话验证](#电话验证)）

为防止AWS收集你的实名信息，识别出你在多次用不同的邮箱注册账号来反复享受一年免费，从而阻止你再次注册新账号薅羊毛（尽管至2023年5月我还没遇到这种情况），建议最好使用假身份。

**要选个人，不要选商用，**不然无法享受一年免费试用。

![iShot2021-10-13 15.53.47](assets/iShot2021-10-13%2015.53.47.png)

### 绑定信用卡

支持银联, visa, master信; 支持人民币, 美元支付.

会先扣费1美刀, 三到五个工作日后返还. [参见](https://amazonaws-china.com/cn/premiumsupport/knowledge-center/aws-authorization-charges/)

若一周后未收到, 可往[AWS支持中心](https://console.aws.amazon.com/support/home#/), 创建case, 选”Billing” - “Charge Inquiry”, 进行申诉. Contact options 选 “chat”, 以便立即和客服聊天.

### 电话验证

电话验证需要填入真实电话，**可以填中国的手机号**，能收到短信验证码。

这个电话**只用于验证身份，之后不再使用**；前面[填联系方式](#填联系方式)时，不必填写此接收验证码的电话。多次注册账号可以用同一个手机号去验证身份。

![image-20211013160159275](assets/image-20211013160159275.png)

填入区号和电话号, 点验证, 优先选”短信”

如果”短信”短信，可以选”语音呼叫”, 则要等AWS打电话给你, 接通之, 把网页上显示的验证码输入到手机上.如果没有收到电话，则申请手动激活账户——打开 [AWS Support 控制台](https://amazonaws-china.com/support/)，然后选择**创建案例**:

* 选择**账户和账单支持**
* 对于**类型**，请选择**账户**
* 对于**类别**，请选择**激活**
* 在**案例描述**部分，说明激活时没接到电话, 要求手动激活, 并提供可以联系到您的日期和时间
* 在**联系选项**部分，为**联系方式**选择**聊天**, 可以立即有客服与你在线打字聊天
* 选择**提交**

**注意：**即使您的账户尚未激活，您也可以使用 AWS Support 创建一个案例。

### 选免费账号类型

**选基础方案, 即12个月免费的**

![ScreenShot2020-10-30 21.36.46](assets/ScreenShot2020-10-30%2021.36.46.png)

### 等24小时完成验证

[参考](https://www.jianshu.com/p/4ff11db6d9c6)

选择支持计划后，系统随即显示确认页面，说明您的账户正在激活。**账户通常会在几分钟内激活，但最长可能需要 24 小时**。

您可以在此期间可以登录您的 AWS 账户，但无法使用计算服务（如开启实例）。即使您已完成注册过程中的所有步骤，在此期间点`开启实例`，AWS 主页还是会显示如下“Complete sign-up”的页面：

![iShot_2024-07-13_20.18.49](assets/iShot_2024-07-13_20.18.49.png)

，你点`Complete your AWS registration`后，会显示“恭喜！感谢您注册AWS”，但再继续点`跳转管理控制台`，然后点 `开启实例`，还是会显示上面的“Complete sign-up”页面，直到帐户激活完成，才能开启实例。

![iShot_2024-07-13_20.19.27](assets/iShot_2024-07-13_20.19.27.png)



**在您的账户完全激活后，您会收到确认电子邮件**（如下）。收到此电子邮件后，您就可以完全访问所有 AWS 服务（如开启实例）。

![iShot_2024-07-13_20.20.56](assets/iShot_2024-07-13_20.20.56.png)

### 账户激活延迟问题排查

[参考](https://www.jianshu.com/p/4ff11db6d9c6)

账户激活有时可能会延迟。如果该过程耗时 24 小时以上，请检查以下各项：

-   **完成账户激活过程。** 在添加所有必要信息之前，您可能意外关闭了注册过程的窗口。如要完成注册过程，请打开 [https://aws-portal.amazon.com/gp/aws/developer/registration/index.html](https://links.jianshu.com/go?to=https%3A%2F%2Faws-portal.amazon.com%2Fgp%2Faws%2Fdeveloper%2Fregistration%2Findex.html)，并使用您为账户选择的电子邮件地址和密码登录。
-   **检查与您的付款方式相关的信息。** 在 AWS 账单和成本管理控制台中检查[付款方式](https://links.jianshu.com/go?to=https%3A%2F%2Fconsole.aws.amazon.com%2Fbilling%2Fhome%23%2Fpaymentmethods)。修复信息中的所有错误。
-   **联系您的金融机构。** 金融机构偶尔会出于各种原因拒绝 AWS 的授权请求。请联系您的付款方式的发卡机构，并请他们批准来自 AWS 的授权请求。
    **注意：**AWS 会在您的金融机构批准后立即取消授权请求。您不需要为 AWS 的授权请求付费。但在金融机构为您提供的对账单上，授权请求可能仍显示为小额费用（通常为 1 USD）。
-   **查看电子邮件中的请求以获取更多信息。** 请查看您的电子邮件，了解 AWS 是否需要您提供更多信息来完成激活过程。
-   **尝试使用其他浏览器。**
-   **联系 AWS Support。** 如需帮助，请联系 [AWS Support](https://links.jianshu.com/go?to=https%3A%2F%2Faws.amazon.com%2Fsupport)。请务必提及您已尝试过的任何问题排查步骤。
    **注意：**请勿在与 AWS 的任何通信中提供敏感信息，例如信用卡卡号。

## 账号安全设置

### 不再支持[安全问题]

**从2024年1月6日起，AWS不再允许设置安全问题，只提供多重身份验证（MFA）（但不强制）。**

薅一年试用期羊毛的，其实不必设置安全问题，也不必设置多重身份验证。

![iShot_2024-07-13_16.18.47](assets/iShot_2024-07-13_16.18.47.png)

## 创建新实例

访问[俄勒冈 us-weat-2的主页面](https://us-west-2.console.aws.amazon.com/console/home?region=us-west-2#)

**免费套餐内容：** 第一年包括每月免费套餐 AMI 上的 750 小时（即24小时\*31天） t2.micro（在 t2.micro 非默认激活的区域中则为 t3.micro）实例使用量、30GiB EBS 存储、200 万个输入和输出、1GB 快照，以及 100GB 互联网带宽。

### 选位置

美国位置：我选上面这些美国位置, 是因此我**注册的美区paypal, 需要用此处固定的美国ip及地理位置, 去登录此paypay账号, 才能不被风控**。

*   推荐美国**俄勒冈**（`us-west-2`），这是所有可以免费试用的美国节点中，到中国延迟最短的（测试于2023年7月16日）。

*   我之前选的是加利福尼亚北部（`us-west-1` ），这是AWS最早的机房所在地，设备老旧，但用来搭梯子够用。

若没有躲避payapl风控的需求，则不必选择美国，推荐东亚的位置，到中国的延迟很低：

*   首尔（`ap-northeast-2`）、大阪（`ap-northeast-3`）、东京（`ap-northeast-1`）

不要选择中国的：

*   不要选中国大陆的，因为无法访问外网。

*   不要选香港的，香港的流量都会被墙劫持，频繁（几周或几月）就让节点的IP列入墙的禁止访问名单，让你不得不更换IP，十分麻烦，且流量杯墙劫持，很不安全。

### 开启实例

![image-20240713205519442](assets/image-20240713205519442.png)

### 实例配置｜新界面

#### 名称和标签

随便填写实例名称

![image-20240713211149896](assets/image-20240713211149896.png)

#### 应用程序和操作系统映像（Amazon Machin Image）

![iShot_2023-07-16_16.41.03](assets/iShot_2023-07-16_16.41.03.png)

#### 实例类型

![iShot_2023-07-16_16.41.14的副本](assets/iShot_2023-07-16_16.41.14%E7%9A%84%E5%89%AF%E6%9C%AC.png)

#### 密钥对（登陆）

若未创建过密钥，则先创建密钥，点 `创建新秘钥对`。然后在下面的页面里如下下图设置，填入密钥对名称，然后保持默认设置，再点`创建秘钥对`, **浏览器会自动下载 `xxx.pem` 私钥文件, 需要存放好，之后要用它从ssh登陆实例**：

![iShot_2023-07-16_16.41.11](assets/iShot_2023-07-16_16.41.11.png)

![image-20211013164702359](assets/image-20211013164702359.png)

若已经创建过密钥，则直接勾选前面创建的密钥：

![iShot_2023-07-16_16.41.14](assets/iShot_2023-07-16_16.41.14.png)

#### 网络设置

在*新版本*的界面中，界面变成了下图的样子，请勾选 `创建新的安全组`，允许来自 `ssh` `http` `https`的流量；

![network](assets/network.png)

但在创建实例时，不要在上图点 `编辑`并加入允许所有ipv4和ipv6点ICMP流量、允许8888、888、20、21端口的规则，不然会无法启动（如下图）

![iShot_2023-07-19_15.32.13](assets/iShot_2023-07-19_15.32.13.png)

#### 配置存储

![iShot_2023-07-16_16.42.01](assets/iShot_2023-07-16_16.42.01.png)

只有通用型才有30GB免费，通用型只包括gp3、gp2。推荐选择gp3，选默认的gp2也可，因为gp3性能好过gp2，详见[体验与对比新版EBS gp3 vs gp2](https://zhuanlan.zhihu.com/p/351198152)：

> gp3因为基准线iops非常高，适合持续高频的小数据大io。
> 如果数据库需要高频小量的io，使用gp3非常合适，但是如果数据库需要持续向外传送很大的数据（例如传送体积比较大的生交易），那么throuput的上限就会挤占iops，导致超时或者无法发挥iops的作用。
> 从各个场景来看，选择gp3都是优于gp2的。

[Amazon EBS 卷类型之间有什么区别？](https://repost.aws/zh-Hans/knowledge-center/ebs-volume-type-differences)

> gp2 卷达到的每卷最大吞吐量 (250 MiB/s) 低于 gp3 卷 (1000 MiB/s)。
> gp2 卷的 IOPS 性能随卷大小线性扩展，并且 gp2 突增性能适用于具有高 IOPS 突增速率的工作负载。gp3 卷不使用突增性能。
> 但是，无论卷大小如何，gp3 卷都能提供稳定的 3,000 IOPS 基准性能和 125 MiB/s 的吞吐量性能。使用 gp3 卷，您可以不受存储大小的影响预置 IOPS 和吞吐量。

[AWS存储磁盘的收费标准](https://aws.amazon.com/cn/ebs/pricing/)

#### 高级详细信息

**保持默认，不用修改**

<img src="assets/image-20240713211012759.png" alt="image-20240713211012759" style="zoom: 10%;" />



#### 点启动实例

检查实例配置信息，确认无误，然后点 `启动实例`。和旧版本的AWS界不同，新版本点完后，不会发生1美元扣款。

<img src="assets/iShot_2023-07-16_16.42.13.png" alt="iShot_2023-07-16_16.42.13" style="zoom:50%;" />

### 实例配置｜旧界面

#### 选AMI (Amazon Machine Image)

 选 Linux (**推荐Ubuntu**) **且 标明了是免费的**. Windows的操作系统太占硬盘, 不要开.

![ScreenShot2020-11-02 23.56.59](assets/ScreenShot2020-11-02%2023.56.59.png)

#### 选择实例类型

注意要选免费的, 即 t2.micro （在 t2.micro 非默认激活的区域中则为 t3.micro）

![ScreenShot2020-11-02 23.56.46](assets/ScreenShot2020-11-02%2023.56.46.png)

#### 配置实例

不要改, 直接用默认的, 然后点 `下一步`

![image-20211013173254224](assets/image-20211013173254224.png)

#### 添加存储

加到30GiB, 这是12个月免费套餐中各项aws服务合计支持最大的存储.

![image-20211013173406821](assets/image-20211013173406821.png)

#### 添加标签

不用添加, 直接点 `下一步`

![image-20211013173500532](assets/image-20211013173500532.png)

#### 创建新安全组

初次创建实例, 则创建安全组如下; 若已有自己创建的安全组, 则选用它

![ScreenShot2020-11-03 00.09.42](assets/ScreenShot2020-11-03%2000.09.42.png)

需要设置允许以下端口访问:

* 22端口：ssh
* 80端口：http，443端口：https
* ICMP 所有端口：ping；IPv6 ICMP 所有端：ping6
* 8888端口：宝塔；888端口：宝塔phpmyadmin（数据库管理后台）
* 20端口：ftp传输数据端口；21端口：ftp传输控制信息端口

#### 检查信息

然后会弹出如下页面, 检查之, 无误则点 `启动`

![image-20201130174843913](assets/image-20201130174843913.png)

#### 使用前面创建的密钥

![img](assets/9-1024x554.jpg)

#### 点启动实例

创建新实例时, 若选用的磁盘大小不是默认的8GiB, 比如是最大免费大小 30GiB, 则AWS会先报错如下, 即AWS需要验证信用卡有效才给创建实例,

![ScreenShot2020-11-03 00.21.14](assets/ScreenShot2020-11-03%2000.21.14.png)

过最多4小时, AWS会先**再次扣1美元**, 验证支付方式有效, 然后允许使用此实例, 此时会收到email通知.

受到email通知后, 重新创建新实例, 就会创建成功.

![ScreenShot2020-11-03 01.00.19](assets/ScreenShot2020-11-03%2001.00.19.png)

## 设置安全组

**在首次开启实例，会首个创建安全组，需立即对它进行设置**，操作如下：

### 允许所有ICMP IPv4/IPv6端口入站

如不加此规则，则无法在aws以外的网络中，ping通实例的公网ip，但不影响ssh登录实例。

在 `安全组`中选中刚创建的新安全组（即不是“default”的那个安全组），再点 `编辑`-`编辑入站规则`；

![iShot_2023-07-19_15.34.03](assets/iShot_2023-07-19_15.34.03.png)

加入新规则，允许任何来源的ivp4和ipv6的ICMP流量入站

![image-20240713221716586](assets/image-20240713221716586.png)

### 需要开放的端口及其功能

必须设置允许以下端口入站访问:

* 22端口：ssh
* 80端口：http，443端口：https
* ICMP 所有端口：ping；IPv6 ICMP 所有端：ping6

如需用到以下功能，必须允许以下端口入站访问:

* 8888端口：宝塔；888端口：宝塔phpmyadmin（数据库管理后台）
* 20端口：ftp传输数据端口；21端口：ftp传输控制信息端口

## 密钥管理

### 创建密钥对

在创建首个实例时会顺带创建首个密钥对。

其他时候，可在密钥管理界面里，创建密钥对。

![ScreenShot2020-11-03 00.13.32](assets/ScreenShot2020-11-03%2000.13.32.png)

![image-20211013164702359](assets/image-20211013164702359.png)

点 `创建秘钥对`, 浏览器会自动下载 `xxx.pem` 私钥文件, 需要存放好，之后要用它从ssh登陆实例。

### ssh登陆使用密钥

AWS上**刚新建的实例**只能用从AWS上下载的密钥登陆，不能用密码登陆/用自己上传的密钥登陆。需要先用AWS下载的密钥登陆到实例，然后配置一下，才能启用密码登陆/用自己上传的密钥登陆。

在AWS的管理页面，从浏览器下载的 `xxx.pem` 私钥文件，放到 `~/.ssh/` 下, 而后登录服务器时, 使用此密钥登陆实例：

```bash
PEM_NAME=<xxxx.pem>
mv /Users/mac/Downloads/$PEM_NAME$ ~/.ssh/cloud/
chmod 400 ~/.ssh/cloud/$PEM_NAME$
# 连接服务器
ssh -i ~/.ssh/cloud/$PEM_NAME$ <username>@<host>
```

注释: 若想获得对应的公钥

```bash
ssh-keygen -y -f <path-to-xxxx.pem>
```

如果执行 `ssh`访问服务器时如下报错，作说明没有 `.pem`证书的读写权限设置没有更改（从AWS下载下来的证书的权限是“-rw-r--r--“），需要执行 `chmod 400 <path-to-xxxx.pem>`更改为“-rw-------”，然后 `ssh`访问节点即可登录成功。

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for '<path-to-xxxx.pem>' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "<path-to-xxxx.pem>": bad permissions
ubuntu@xx.xxx.xxx.xxx: Permission denied (publickey).
```

### 密钥丢失怎么办

如果在首次启动后丢失了 SSH 密钥对，该如何连接到 Amazon EC2 实例？[参见](https://aws.amazon.com/cn/premiumsupport/knowledge-center/user-data-replace-key-pair-ec2/)

## 用户初始化

### 登录默认用户

#### 法一: 在浏览器上登陆

![iShot2020-11-30 17.41.47](assets/iShot2020-11-30%2017.41.47.png)

![image-20201130174519919](assets/image-20201130174519919.png)

#### 法二: 用ssh登陆

使用上面创建并下载的证书, 登陆默认用户

```bash
ssh -o IdentitiesOnly=yes  -i <path-to-xxx.pem> <default-username>@<实例的公网ip>
```

| 系统       | 默认用户            |
| ---------- | ------------------- |
| RHEL5      | root 或 ec2-user    |
| Ubuntu     | ubuntu              |
| Fedora     | fedora 或 ec2-user  |
| SUSE Linux | 是 root 或 ec2-user |

实例的公网ip，可以在实例页面查看

![image-20240713222333680](assets/image-20240713222333680.png)

另外，如果默认用户无法使用，请与您的 AMI 供应商核实

### 用户初始化

```bash
sudo -i

# 创建sudo密码, 然后输入两次密码
passwd

# 允许root登录, 包括密码与密钥登录
sed -i -E  's/^#?[ ]*PermitRootLogin .+$/PermitRootLogin yes/g' /etc/ssh/sshd_config
# 允许密码登录
sed -i -E  's/^#?[ ]*PasswordAuthentication .+$/PasswordAuthentication yes/g' /etc/ssh/sshd_config

# 让ssh连接不中断
# #  可以让连接无活动一段时间后，发送一个空 ack，使 TCP 连接不会被防火墙等关闭
# sed -i -E  's/^#?[ ]*TCPKeepAlive .+$/TCPKeepAlive yes/g' /etc/ssh/sshd_config
# # 服务端主动向客户端请求响应的间隔
# sed -i -E  's/^#?[ ]*ClientAliveInterval .+$/ClientAliveInterval 60/g' /etc/ssh/sshd_config
# # 服务器发出请求后客户端没有响应的次数达到该数量就自动断开
# sed -i -E  's/^#?[ ]*ClientAliveCountMax .+$/ClientAliveCountMax 3/g' /etc/ssh/sshd_config

# 重启sshd服务
# # CentOS6操作系统
# service sshd restart
# # ubuntu/CentOS7/EulerOS操作系统
# 永久开启ssh服务
systemctl enable ssh.service # 如不执行此行，直接执行下一行，会报错“Failed to start sshd.service: Unit sshd.service not found.”
# 重启sshd服务
systemctl restart sshd
# systemctl restart sshd.service

# 开2GB的交互内存
dd if=/dev/zero of=/swapfile count=2048 bs=1M
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
free -h

# 创建新用户
new_username="hyliang"       # 你要创建的用户名
adduser ${new_username}      # 创建用户, 输入两次密码
usermod -aG sudo ${new_username}  # 添加到root

# 修改hostname
new_hostname=【new-hostname】 # 【new-hostname】 如“aws-oregon”
hostnamectl set-hostname "${new_hostname}"
echo -n "current hostname: " ; hostnamectl | head -n 1
( echo "127.0.0.1 ${new_hostname}"; cat /etc/hosts ) | sudo tee /etc/hosts > /dev/null
echo "current /etc/hosts:" ; cat /etc/hosts | grep --color 127.0.0.1
```


而后尝试用密码登录新建用户和root,

```bash
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no root@<服务器-ip>
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no <新建用户>@<服务器-ip>
```

若登陆成功, 则将本地之前已有的密钥发送到服务器 (这样就不怕丢失之前aws给的默认密钥), 然后输入登录密码

```bash
ssh-copy-id -o PreferredAuthentications=password [-i <公钥或对应私钥的路径>] root@<服务器-ip>
ssh-copy-id -o PreferredAuthentications=password [-i <公钥或对应私钥的路径>] <新建用户>@<服务器-ip>
```

然后尝试用上述指定的密钥登录新建用户和root,

```bash
ssh root@<服务器-ip>
ssh <新建用户>@<服务器-ip>
```

若登录成功，则说明设置好了。

而后则可登录root或hyliang用户(而非登录在ubuntu用户上), 然后删除ubuntu用户：

```bash
sudo userdel -r ubuntu
```

然后分别执行下面的命令，如果返回都是空的，说明ubuntu账号删除完成

```
getent passwd | grep ubuntu
ls /home | grep ubuntu
```

#### debug：`systemctl restart sshd`报错

如果执行`systemctl restart sshd`时有如下报错，

>   Failed to start sshd.service: Unit sshd.service not found.

则先尝试`systemctl enable ssh.service`，然后再执行`systemctl restart sshd`，然后再执行`ystemctl status sshd`。

如果执行`systemctl status sshd`时有如下报错，说明`22`端口被某个不是sshd.service的进程（`1042`）占用着，造成sshd.service无法重启，从而无法把上文中ssd_config更新的配置运行起来，造成无法用密码做ssh登陆、无法ssh登陆root。

```
root@ip-172-31-17-55:~#
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/usr/lib/systemd/system/ssh.service; enabled; preset: enabled)
    Drop-In: /usr/lib/systemd/system/ssh.service.d
             └─ec2-instance-connect.conf
     Active: active (running) since Sat 2024-07-13 15:11:23 UTC; 23s ago
TriggeredBy: ● ssh.socket
       Docs: man:sshd(8)
             man:sshd_config(5)
    Process: 2023 ExecStartPre=/usr/sbin/sshd -t (code=exited, status=0/SUCCESS)
   Main PID: 2025 (sshd)
      Tasks: 2 (limit: 1130)
     Memory: 5.2M (peak: 6.5M)
        CPU: 22ms
     CGroup: /system.slice/ssh.service
             ├─1042 "sshd: /usr/sbin/sshd -D -o AuthorizedKeysCommand /usr/share/ec2-instance-connect/eic_run_authorized_keys %u %f -o AuthorizedKeysCommandUser ec2-instance-connect [listener] 0 of 10-10>
             └─2025 "sshd: /usr/sbin/sshd -D -o AuthorizedKeysCommand /usr/share/ec2-instance-connect/eic_run_authorized_keys %u %f -o AuthorizedKeysCommandUser ec2-instance-connect [listener] 0 of 10-10>

Jul 13 15:11:23 aws-oregon systemd[1]: Starting ssh.service - OpenBSD Secure Shell server...
Jul 13 15:11:23 aws-oregon systemd[1]: ssh.service: 【Found left-over process 1042 (sshd) in control group while starting unit. Ignoring.】
Jul 13 15:11:23 aws-oregon systemd[1]: ssh.service: 【This usually indicates unclean termination of a previous run, or service implementation deficiencies.】
Jul 13 15:11:23 aws-oregon sshd[2025]: Server listening on :: port 22.
Jul 13 15:11:23 aws-oregon systemd[1]: Started ssh.service - OpenBSD Secure Shell server.
```

只需要`reboot`，就能解决这个问题。重启后，再执行`ystemctl status sshd`，返回如下，上述占用22端口的进程不存在了，上文中ssd_config更新的配置就运行起来。

```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/usr/lib/systemd/system/ssh.service; enabled; preset: enabled)
    Drop-In: /usr/lib/systemd/system/ssh.service.d
             └─ec2-instance-connect.conf
     Active: active (running) since Sat 2024-07-13 15:14:49 UTC; 2min 21s ago
TriggeredBy: ● ssh.socket
       Docs: man:sshd(8)
             man:sshd_config(5)
    Process: 557 ExecStartPre=/usr/sbin/sshd -t (code=exited, status=0/SUCCESS)
   Main PID: 642 (sshd)
      Tasks: 1 (limit: 1130)
     Memory: 3.3M (peak: 4.9M)
        CPU: 102ms
     CGroup: /system.slice/ssh.service
             └─642 "sshd: /usr/sbin/sshd -D -o AuthorizedKeysCommand /usr/share/ec2-instance-connect/eic_run_authorized_keys %u %f -o AuthorizedKeysCommandUser ec2-instance-connect [listener] 0 of 10-100>

Jul 13 15:14:49 aws-oregon systemd[1]: Started ssh.service - OpenBSD Secure Shell server.
```

#### debug：无法用密码登陆

如果执行`ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no <新建用户>@<服务器-ip>`报错如下：

> <新建用户>@<服务器-ip>: Permission denied (publickey).

可以检查一下sshd的配置，里面若有`Include /etc/ssh/sshd_config.d/*.conf`之类的东西：

```
cat /etc/ssh/sshd_config
```

> Include /etc/ssh/sshd_config.d/*.conf

就去看看这些引用的配置文件：

```
ls -l /etc/ssh/sshd_config.d/*.conf
```

> -rw-r--r-- 1 root root 26 Jul  1 16:02 /etc/ssh/sshd_config.d/60-cloudimg-settings.conf
> <新建用户>@<服务器-ip>:/home/ubuntu# cat /etc/ssh/sshd_config.d/60-cloudimg-settings.conf
> PasswordAuthentication no

则只需修改

```
sed -i -E  's/^#?[ ]*PasswordAuthentication .+$/PasswordAuthentication yes/g' /etc/ssh/sshd_config.d/60-cloudimg-settings.conf
```

然后就能用密码登陆新间用户和root了

## 查看账目和创建预算报警

### 查看免费套餐内的使用情况

查看所有区域的总开支：进入[成本管理页面](https://us-east-1.console.aws.amazon.com/cost-management/home)，点 `Free Tier`，会显示已使用多少免费套餐内的流量和计算量

![image-20230508163259723](assets/image-20230508163259723.png)

查看一个区域的开支：进入开了实例的区域的aws控制台页面，如[俄勒冈州的控制台](https://us-west-2.console.aws.amazon.com/ec2/)，会显示免费试用套餐内的每月机时和EBS的使用量/免费总量：

![image-20240713160242598](assets/image-20240713160242598.png)

### 查看每日流量和费用

进入[成本管理页面](https://us-east-1.console.aws.amazon.com/cost-management/home)，点 `Cost Explorer`，在右侧 `报告参数`中选则：

* `粒度`为“每日”，并选择折线图，则显示：

![image-20230401175839879](assets/image-20230401175839879.png)

* 再将 `维度`改为“使用类型”，则显示：

  ![image-20230401180231075](assets/image-20230401180231075.png)
* 再将 `使用类型组`为“EC: Data Transfer - Internet (Out)”（出AWS流量，每月1日起，超过100GB后开始收费），则显示：

  ![image-20230401182703101](assets/image-20230401182703101.png)
* 再将 `使用类型租`为“EC: Data Transfer - Region to Region (Out)”（访问其他AWS区域的流量），则显示：

  ![image-20230401182519031](assets/image-20230401182519031.png)

收费是从**每月1日**开始，如希望统计每日从**月首到当日**的**累计流量和累计费用**，需要点 `以CSV格式下载`，用Excel来统计：

![image-20230401184122348](assets/image-20230401184122348.png)

#### 查看账单

[查看免费服务的使用情况](https://console.aws.amazon.com/billing/home?region=us-west-1#/)

<img src="assets/ScreenShot2020-11-09%2020.47.32.png" style="zoom:50%;" />

![](assets/image-20201109204646842.png)

[查看付费服务的账单](https://console.aws.amazon.com/billing/home?region=us-west-1#/bills?year=2020&month=11)

![ScreenShot2020-11-09 20.45.20](assets/ScreenShot2020-11-09%2020.45.20.png)

### 账单首选项：超免费使用量限制时报警

2023年及以后的界面：

不要开 `Cloud Watch`，它需要收费，一点开启就不能关闭，详见[Cloud Watch收费标准](https://aws.amazon.com/cn/cloudwatch/pricing/)。

![iShot_2023-07-18_17.33.36](assets/iShot_2023-07-18_17.33.36.png)

2022年及以前的界面：

![ScreenShot2020-11-03 01.02.19](assets/ScreenShot2020-11-03%2001.02.19.png)

### 开销超预算报警

点 `Budgets`，分别设定每月预算和每日预算，超过预算就发邮件给自己

![ScreenShot2020-11-08 02.39.27](assets/ScreenShot2020-11-08%2002.39.27.png)下面以设置每日预算为例，每月预算同理：不要点 `使用模版`中点 `零支出预算`，因为这默认是每月预算，不是每天预算。

![iShot_2023-03-05_22.26.25](assets/iShot_2023-03-05_22.26.25.png)

![iShot_2023-03-05_22.28.30](assets/iShot_2023-03-05_22.28.30.png)

![iShot_2023-03-05_22.29.44](assets/iShot_2023-03-05_22.29.44.png)

![iShot_2023-03-05_22.47.41](assets/iShot_2023-03-05_22.47.41.png)

### 勿用"Budgets Reports”, 要付费

每条预算报告\$0.01

![image-20201108025423303](assets/image-20201108025423303.png)

## 正常使用一月后无扣费请解绑信用卡避免自动扣费

[详见](#解绑信用卡避免自动扣费)

# 注销账号要做的事情

## 出现大额费用待支付怎么办

当遇到因流量超标等等原因造成的**大额费用不愿支付**时，**请在每月AWS向信用卡完成结算前，立即解绑信用卡避免自动扣费，并注销AWS账号**，这样信用卡不会实际扣费。注销账号的原因是，因为信用卡解绑，按照AWS的规定，60天内将丢失资源、90天内将无法重开账号，详见[下文](#解绑信用卡避免自动扣费)。

## 解绑信用卡避免自动扣费

### 用法1、在注销账户前解绑信用卡

在注销账户前，将能支付的信用卡，并绑定一个虚假的信用卡，以免因注销账户前没有关闭收费项目（如超过免费限额的弹性IP和EBS存储），造成注销账户后的90天反悔期内产生扣费。

### 用法2、在开户后一个月后解绑信用卡

在开好所需实例后, 并收到AWS退回的1美元后, 观察了一个月能正常使用且**不产生扣费**后, 为了避免不小心被扣费，可以将能支付的信用卡，并绑定一个虚假的信用卡。

优点：在这样换绑信用卡后，即使使用流量超过限额，或误点了收费项目，产生了费用，也会因为信用卡无效，而不会实际扣费；

缺点：但这样会产生未支付费用，从而造成账户停用，这会有以下两个后果（详见[aws规定](https://amazonaws-china.com/cn/premiumsupport/knowledge-center/reactivate-suspended-account/)）：

>   *   如果**您未支付所有逾期费用**，且未在**暂停的 60 天内重新激活您的账户，则账户上的资源可能会丢失**。
>
>   *   如果您未支付所有逾期费用，且未在暂停的 90 天内重新激活您的账户，则您的账户会被终止。终止的账户无法再重新打开，账户中的所有资源都将丢失。

注意:

* 必需在开好所需实例后, 再解绑信用卡. 不然解绑后, 无可支付的信用卡, 此时如果创建新实例, 选用的磁盘大小不是默认的8GiB, 比如是最大免费大小 30GiB, 则因为没有有效的信用卡, 造成无法创建实例. 详见[确认创建](#确认创建).
* 必需受到AWS退回的1美元后,  再解绑信用卡, 不然无法收到退回的数次1刀的验证金 (已经实验证实).

### 解绑/替换信用卡的方法

 [来源](https://www.zhihu.com/question/42790946/answer/1077658435):

原理：**当且仅当一个信用卡不是默认支付方式（这意味着有其他信用卡是默认支付方式），才能将这个信用卡删除**。**默认支付方式不必是可以支付的。**

下面以旧版界面为例：

* 点击右上角的“我的账户”（旧版界面）或[“付款首选项“（新版界面）](https://us-east-1.console.aws.amazon.com/billing/home#/paymentpreferences/paymentmethods), 点击左边的付款方式，可以看到绑定的原信用卡，但 `删除`按钮是灰色的

  ![m1](assets/m1.jpg)
* 我们可以 `添加`一张随机生成的信用卡（操作图略）

  * 自己谷歌搜索“**Credit Card Generator**”, 例如用[vccgenerator](https://www.vccgenerator.org/result/)可以随机生成信用卡号
  * 填写随机信用卡的地址信息, 手机号. [随机生成手机号](https://phonenumbertools.com/generator-us/) [随机生成美国人身份](http://www.shenfendaquan.com)
* 将其 `验证`

  ![0](assets/0.jpg)
* 利用验证的空档赶紧将其 `作为默认卡`

![iShot_2022-11-19_17.21.07](assets/1.jpg)

* 注：**在新版界面中**，可以在绑定新卡的时候，就直接勾选它作为默认支付方式，这样就无需像上面那样先添加新卡、然后在主页面变更默认支付方式。

    ![iShot_2024-07-13_15.14.01](assets/iShot_2024-07-13_15.14.01.png)

* 然后就可以 `删除`自己的信用卡了

![2](assets/2.jpg)

* 然后 ，系统才反应过来新信用卡验证失败，弹出警告，这说明替换信用卡已经成功

![4](assets/4.jpg)

## 把联系信息换成非实名的

为防止AWS收集你的实名信息，识别出你在多次用不同的邮箱注册账号来反复享受一年免费，从而阻止你再次注册新账号薅羊毛（尽管至2023年5月我还没遇到这种情况），最好把联系信息换成非实名的。

操作如下：在[主页](https://us-east-1.console.aws.amazon.com/billing/home#/account)，点击下图中的 `联系信息`，点 `编辑`，用[外国人身份生成器](https://www.shenfendaquan.com/)生成身份信息，填入。

![image-20230508170541607](assets/image-20230508170541607.png)

## 换IP

### 临时IP

aws 给实例的默认的公网ip 是临时的, 每次示例重启会换一个ip.

先点 `停止实例`, 再点 `启动实例`.

![image-20201130160842610](assets/image-20201130160842610-0858425.png)

### 弹性IP

在AWS的控制台，选择左侧的 `弹性IP`

![image-20240713161601566](assets/image-20240713161601566.png)

#### 更换弹性IP

在AWS的控制台，选择左侧的 `弹性IP`，点击 `分配新地址` 按钮，分配一个新的IP地址。然后选中新分配的地址，点击 `操作`按钮，选择 ` 关联地址`，并依次选择实例，网络接口，私有IP地址。最后点击 `关联` 即可。在 私有IP地址 选择时，如果选择了既有的公网IP关联的私有IP地址，既意味着解绑了原来的绑定关系，也就是更换了**公网IP地址**。[参见](AWS 如何更换IP？ - 王博的回答 - 知乎 https://www.zhihu.com/question/26452160/answer/105574759)

#### 释放弹性IP

当实例停止运行/终止实例/注销账号/更换弹性ip等时, 会造成**弹性 IP 没有捆绑到 EC2 实例，**这依旧会对弹性IP收费。

因此，一定要记立即得释放弹性IP。操作方法如下：

*   在AWS的控制台，选择左侧的 `弹性IP`，选中需要释放的弹性IP，
*   先点`取消关联`（若该弹性IP绑定的实例已终止，则会自动取消关联，这一步不需要操作）
*   然后点 **`释放`弹性IP**，不然它会按小时收费。

#### 弹性IP收费

[收费标准](https://amazonaws-china.com/ec2/pricing/on-demand/):

* 闲置 (未绑定实例, 或实例未在运行) 弹性IP: \$0.005/小时\*个
* 每月绑定前100个弹性IP: 免费
* 每月绑定>100个的弹性IP, 超出部分的IP: \$0.1/月*个

[参见如下](https://amazonaws-china.com/cn/premiumsupport/knowledge-center/elastic-ip-charges/), 只要满足以下所有条件，弹性 IP 地址便不会产生费用：

- 弹性 IP 地址与 EC2 实例关联。
- 与该弹性 IP 地址关联的实例正在运行。
- 该实例仅关联了一个弹性 IP 地址。
- 弹性 IP 地址与连接的网络接口（如 Network Load Balancer 或 NAT 网关）相关联。

## 解绑EBS卷

先将绑定此卷的实例 `停止`；

然后：

* 若此卷要复用, 即绑定在其他实例上，则点 `分离卷`, 以解绑实例与卷。

  ![iShot_2022-11-19_16.43.27](assets/iShot_2022-11-19_16.43.27.png)

![iShot_2022-11-19_16.44.10](assets/iShot_2022-11-19_16.44.10.png)

* 若次卷不复用, 则点 `操作`-`删除卷`, 会不可逆地删除卷。

<img src="assets/image-20201130165546781.png" style="zoom:33%;" />

## 终止实例

aws中必需点 `终止实例`, 才能不再从实例产生资费. `终止实例`是不可逆地注销实例. `停止实例`是可逆的, 还能点 `启动实例`.

![image-20211013220855020](assets/image-20211013220855020.png)

被停止和被终止的实例收费: 仅Amazon EBS 卷的存储收费, 和限制弹性ip的费用, 不受EC2机时和流量费用.

**注意**: 凡绑定了弹性ip或EBS的实例, 一旦实例已终止, **要立即手动[释放弹性IP](#释放弹性IP) 和 [解绑EBS卷](#解绑EBS卷)**, 不然会产生资费.

实例并不存在”删除”,”注销”等操作, 只有”终止”. 当EC2实例终止, 并解绑弹性ip和EBS 卷后, 此实例无需手动清除, 过些时间 (比如一两小时) 会被系统自动清除.
