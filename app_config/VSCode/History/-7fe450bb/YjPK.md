***老梁私有教程，收费购买的，勿外传***

# shadowsocks客户端

适用：mac

## ss,ssr,ssrr辨析

| 代理内核 | 来源                                                | 还在维护吗 | gtihub                                                       | 客户端下载                                                   |
| -------- | --------------------------------------------------- | ---------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ss       | 最早用socks5代理的                                  | 在         | [ss的github](https://github.com/shadowsocks)                 | [shadowsocks官网下载ss客户端](https://shadowsocks.org/en/download/clients.html) |
| ssr      | 破娃酱copy自ss, 添加了ssr协议                       | 否         | 原作者已删除ssr的repo, 请访问[ssr的备份github](https://github.com/shadowsocksr-rm/shadowsocksr) | [ss.ssr,ssrr各种客户端下载](https://github.com/xcxnig/ssr-download) (2020-10还在更新) |
| ssrr     | 在ssr死后, 被接手维护, 起名ssrr, 添加了一些混淆方式 | 在         | [ssrr的github](https://github.com/shadowsocksrr)             | 见上                                                         |

## 下载客户端

下载最新版本即可

| SS的mac客户端                                                | 还在维护吗 | 说明                         | 支持SSR协议否 |
| ------------------------------------------------------------ | ---------- | ---------------------------- | ------------- |
| ShadowsocksX                                                 | 否         | 原版的mac的shadowsocks客户端 | 否            |
| [ShadowsocksX-NG](https://github.com/shadowsocks/ShadowsocksX-NG/releases) | 在         | 新版的mac的shadowsocks客户端 | 否            |
| ShadowsocksX-R                                               | 否         | fork自ShadowsocksX           | 是            |
| [ShadowsocksX-NG-R](https://github.com/qinyuhang/ShadowsocksX-NG-R/releases/) | 否         | fork自ShadowsocksX-NG        | 是            |
| **SS的安卓客户端**                                           |            |                              |               |
| [ss的安卓客户端](https://github.com/shadowsocks/shadowsocks-android) | 在         | 原版的ss安卓客户端           | 否            |
| [ssr的安卓客户端](https://github.com/shadowsocksr-rm/shadowsocksr-android) | 否         | fork自 原版ss的安卓客户端    | 是            |
| [ssrr的安装客户端下载](https://github.com/shadowsocksrr/shadowsocksr-android) | 在         | fork自 ssr的安卓客户端       | 是            |

## 配置方法

![image-20190219195214013](assets/image-20190219195214013.png)

* 从`应用`打开Shadowsocks
* 按如下点击`服务器设置`
* 填入设置

![image-20190219195224889](assets/image-20190219195224889.png)

## 订阅号

向ss客户端填写一个订阅网址，能获得一堆“飞机场”（商业ss服务）的账号，并能实时更新这些账号

### 适用的ss客户端

[shadowsocksx-ng-r8](https://github.com/qinyuhang/ShadowsocksX-NG-R/releases)

- 不支持负载均衡（即同时使用多个飞机场账号，均衡其负载）

### 使用教程

![屏幕快照 2019-01-24 15.17.03](assets/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-01-24%2015.17.03.png)

![屏幕快照 2019-01-24 15.17.12](assets/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-01-24%2015.17.12.png)

点手动更新订阅，ss客户端会从这个网址抓取一堆飞机场账号

![屏幕快照 2019-01-24 15.24.22](assets/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-01-24%2015.24.22-8315028.png)

订阅完成后，能获得一堆“飞机场”（商业ss服务）的账号，直接切换到此即可

![屏幕快照 2019-01-24 15.31.28](assets/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-01-24%2015.31.28.png)

点击自动更新订阅

![屏幕快照 2019-01-24 15.36.52](assets/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-01-24%2015.36.52.png)

### bug

#### 订阅号不单独分为一个文件夹了

当重启电脑时，此时点开ss的菜单，看见如下![image-20190216104817910](assets/image-20190216104817910.png)

这是ss的bug，电脑重启时，ss未关闭，而是延续重启前的状态，但由于ss内核有bug，故出现上述情况。

解决方法：

- 退出ss

![image-20190216105142174](assets/image-20190216105142174.png)

- 从`Application/`重启ss

![屏幕快照 2019-02-16 10.52.00](assets/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-02-16%2010.52.00.png)

- 而后，点到ss的菜单里，恢复成这个样子

    ![image-20190216105708054](assets/image-20190216105708054.png)




## 命令行翻墙

### 方法

要想在终端下也能翻墙，需要先执行（理由见下[对pip的干扰](#对pip的干扰)）

```bash
pip install pysocks
```

然后将以下写到`~/.profile`

```bash
#  翻墙代理设置，使得命令行下可以翻墙
# 国内网站不代理
export no_proxy="localhost,127.0.0.1,localaddress,.localdomain.com,.souche.com"
# 法一
# export http_proxy=socks5://127.0.0.1:1086
# export https_proxy=socks5://127.0.0.1:1086
# export ftp_proxy=socks5://127.0.0.1:1086
# alias unproxy='unset all_proxy'
# 法二
export ALL_PROXY=socks5://127.0.0.1:1086
alias unproxy='unset ALL_PROXY'
```

其功能是，将终端下的所有的http、https、ftp访问（no_proxy的除外），先经由socks5协议被shadowsocks监听，再由shadowsocks判断是翻墙访问还是直接访问。

### 查看sock5端口

其中，`socks5://127.0.0.1:1086`是shadowsocks默认监听端口，从这里查看：

![屏幕快照 2019-02-19 19.55.39](assets/屏幕快照 2019-02-19 19.55.39.png)

![image-20190219195552132](assets/image-20190219195552132.png)

### 对pip的干扰

若没有执行`pip install pysocks`，就做上述`~/.profile`的修改，会对造成`pip`使用干扰——输入`pip install <包>`，会有如下报错

```
InvalidSchema: Missing dependencies for SOCKS support.
```

解决方法

* 注释掉.profile中的上述设置

```bash
# export http_proxy=socks5://127.0.0.1:1086
# export https_proxy=socks5://127.0.0.1:1086
# export ftp_proxy=socks5://127.0.0.1:1086
# export no_proxy="localhost,127.0.0.1,localaddress,.localdomain.com,.souche.com"
# alias unproxy='unset all_proxy'
```

重启一个终端，输入

```bash
pip install pysocks
```

会正常执行，安装完后，将.profile中的修改再解除注释。之后即便重启终端，pip依旧能不被代理干扰。

