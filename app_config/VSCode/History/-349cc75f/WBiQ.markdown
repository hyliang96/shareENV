---
title: 所见即所得的markdown编辑器
categories:
  - 器
  - 文档编辑
abbrlink: d2e1cbe8
date: 2024-01-17 00:07:37
updated:
tags:
---

# Markdown软件对比

| 软件                                | Typora                                                       | MarkText                                                     | vscode插件`Office Viewer(Markdown Editor)`                   | 浏览器端markdown编辑器`vditor`                               | Obsidian                                                     |
| ----------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 所见即所得                          | 支持                                                         | 支持                                                         | 支持                                                         | 支持                                                         | 支持                                                         |
| 左代码右预览                        | 不支持                                                       | 不支持                                                       | 支持                                                         | 支持                                                         | 支持                                                         |
| 第三方插件                          | 支持([插件管理器的下载安装链接](https://github.com/typora-community-plugin/typora-community-plugin)，但插件管理器bug多，社区不成熟） | [计划在 v1.0.0 发布之后添加插件机制，以及自定义主题](https://github.com/marktext/marktext/issues/224#issuecomment-385655314) | 需要与其他vscode插件兼容                                     | 不支持                                                       | 是                                                           |
| 官方下载链接                        | https://typora.io                                            | https://www.marktext.cc                                      | https://marketplace.visualstudio.com/items?itemName=cweijan.vscode-office | 在线工具： https://vditor.vercel.app ；支持本地部署，需要安装node | https://obsidian.md/                                         |
| 操作系统                            | Mac、windows、Linux                                          | Mac、windows、Linux                                          | Mac、windows、Linux                                          | 所有操作系统                                                 | Mac、windows、Linux、iOS、安卓                               |
| 开源否                              | 2021年底前在beta版本期间开源、免费于https://github.com/typora；之后闭源、付费 | 开源  https://github.com/marktext/marktext                   | 开源 https://github.com/cweijan/vscode-office                | 开源 https://github.com/Vanessa219/vditor                    | 闭源                                                         |
| 收费否                              | 过往版本(<=0.11.18版本)免费，之后版本付费，或去[MacTorrents](https://www.torrentmac.net)下载破解版 | 免费                                                         | 免费                                                         | 下同`Office Viewer(Markdown Editor)`，因为其内核是`vditor`   | 个人免费，商用组织收费                                       |
| 表格                                | 支持                                                         | 支持                                                         | 支持                                                         |                                                              | 支持                                                         |
| 图                                  | 支持                                                         | 支持                                                         | 支持                                                         |                                                              | 支持                                                         |
| 公式                                | 支持                                                         | 支持                                                         | 支持                                                         |                                                              | 支持                                                         |
| 内嵌html                            | 支持                                                         | 支持                                                         | 支持                                                         |                                                              | 支持                                                         |
| 中文界面                            | 支持                                                         | 原版不支持。请往[汉化版官网](https://marktext.weero.net)，但这个版本无法在打开文件夹时向当中的markdown文件内插图。 | 不支持                                                       |                                                              | 支持，但界面汉化不充分                                       |
| 流畅度                              | 图/公式/字数多时卡顿                                         | 图/公式/字数多时流畅                                         | 图/公式/字数多时流畅                                         |                                                              |                                                              |
| 用 `\tag{}` 手动编号                | 支持                                                         | 支持                                                         | 支持                                                         |                                                              | 支持                                                         |
| 公式块中align或equation环境自动编号 | 支持                                                         | 支持                                                         | 支持                                                         |                                                              | 不支持（除非安装下述插件，但不能设置只给equation和align环境自动编号） |
| 公式块全部自动编号                  | 支持，可在Typora设置里勾选                                   | **不支持**                                                   | **不支持**                                                   |                                                              | 支持（但需要安装插件`MathLinks`和`LaTeX-like Theorem & Equation Referencer`，可以设置仅被引用的公式会自动编号、或任何公式都自动编号） |
| 公式中使用`\label` `\eqref` `\ref`  | 支持                                                         | **不支持，整个公式块无法渲染 并报错**                        | **不支持，整个公式块能渲染，但这几条命令处渲染错误并报错**   |                                                              | 不支持？(偶尔能渲染正确，但一编辑公式，公式引用就报错)       |
| 在文件夹内显示`*.textbundle`        | **不支持**                                                   | 支持                                                         | 支持                                                         |                                                              | 支持，但无法打开                                             |
| 直接打开`*.textbundle`              | 支持（打开方式见下文说明）                                   | 支持（打开方式同Typora）                                     | 支持（无需额外设置）                                         |                                                              | **不支持**，详见[TextBundle support](https://forum.obsidian.md/t/textbundle-support/3585) |
| 向`*.textbundle`插入图片            | 支持（需要配置插图自动复制到`./assets`）                     | 支持不充分：<br />1. 原版：当设置插图路径为`assets`时：若打开一markdown文件，则把插图复制到此文件所在目录下的`assets`子文件夹内；但若打开一文件夹，则复制插图到文件夹根目录下的`assets`子文件夹内。详见 [官方说明](https://github.com/marktext/marktext/blob/develop/docs/IMAGES.md)。<br />2.[汉化版](https://marktext.weero.net)：不管如何设置插图路径，在打开文件夹时，都无法向当中的markdown文件内插图 | 支持（需要配置插图自动复制到`./assets`，即向vscode的用户配置文件添加：`"vscode-office.pasterImgPath": "${workspaceDir}/assets/${now}.png", "vscode-office.workspacePathAsImageBasePath": true,`） |                                                              | 不支持                                                       |
| 在文件夹内搜索文本                  | 支持                                                         | 支持                                                         | 支持                                                         |                                                              |                                                              |
| 打开`.markdown` `.txt`文件          | 支持                                                         | 支持                                                         | 支持                                                         |                                                              | 支持（需要安装插件`Custom File Extensions`, 并设置`{ "markdown": [ "", "md", "markdown", "txt", 等 ] }` 表示这些后缀的文件都用markdown格式打开） |
| 打开任何位置的文件                  | 支持                                                         | 支持                                                         | 支持                                                         |                                                              | 不支持（除非安装[脚本](https://gitlab.com/BvdG/obsidian-everywhere)） |
| sequence制图                        | 支持                                                         | 汉化版支持                                                   | 不支持                                                       |                                                              | 不支持                                                       |
| flow制图                            | 支持                                                         | 汉化版不支持                                                 | 不支持                                                       |                                                              | 不支持                                                       |
| mermaid制图                         | 支持（但我的电脑上有bug，Typora 1.8.4，MacOS 10.15.7，会显示`Painting Diagram ...`） | 汉化版支持                                                   | 支持                                                         |                                                              | 支持                                                         |

说明：

* `*.textbundle`的打开方式方式：

  * Typora和MarkText打开`*.textbundle`的方式：

    * 在Typora和MarkText内，点`文件`-`打开`(不论是以文件还是文件夹)，无法打开`*.textbundle`

    * 在`Finder`-单击右键-`打开方式`-`其它`-选择用Typora或MarkText打开，可以打开。

    * 在`Finder`-单击右键-`显示简介`-`打开方式`-设置用Typora或MarkText打开，然后双击`*.textbundle`，可以打开。

    * 在终端，`open -a Typora或Marktext xxxx.textbundle`，可以打开。

  * 在vscode（使用插件`Office Viewer(Markdown Editor)`）中，上述方法都能打开`*.textbundle`。

* vscode插件`Office Viewer(Markdown Editor)`插件的内核和前身：

  * vscode插件`Markdown Editor`  https://marketplace.visualstudio.com/items?itemName=zaaack.markdown-editor 在2021年后就不再更新发布了。不推荐使用。

  * vscode插件`Office Viewer(Markdown Editor)`集成了`Markdown Editor` 的功能，并且还支持office文档（ppt、word、excel）的预览。更新发布至今（2023年底）。推荐使用。

  * `Markdown Editor`和`Office Viewer(Markdown Editor)`的内核都是 浏览器端markdown编辑器`vditor`。

# Typora卡顿

解决Typora字数过多造成卡顿现象 https://blog.csdn.net/qq_46921028/article/details/131896316

win10上Typora卡顿的问题及其解决方案 https://blog.csdn.net/Mao_Jonah/article/details/120533879

# 解决KaTex不支持`\label` `\eqref` `\ref`

* KaTex不打算官方支持`\label` `\eqref` `\ref`

* 可以自行修改KaTex配置

## 本地html

参照 [#2033 (comment)](https://github.com/KaTeX/KaTeX/issues/2003#issuecomment-843991794)的思路 和 [样例配置](https://github.com/KaTeX/KaTeX/issues/2003#issuecomment-1236245418)，有如下demo代码。新建文件`demo.html`，将下面代码复制进去，然后用浏览器打开，

```html
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>

        <title>KaTeX-DOM Eq. Ref Test</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css" integrity="sha384-AfEj0r4/OFrOo5t7NnNe46zW/tFgW6x/bCJG8FqQCEo3+Aro6EYUG4+cU+KJWu/X" crossorigin="anonymous">
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js" integrity="sha384-g7c+Jr9ZivxKLnZTDUhnkOnsh30B4H0rpLUpJ4jAIKs4fnJI+sEnkvrMWph2EDg4" crossorigin="anonymous"></script>
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/contrib/auto-render.min.js" integrity="sha384-mll67QQFJfxn0IYznZYonOWZ644AWYC+Pt2cHqMaRhXVrursRwvLnLaebdGIlYNa" crossorigin="anonymous"
          onload="renderMathInElement(document.body);"></script>
        <script src="main.js"></script>

        <script>
            document.addEventListener("DOMContentLoaded", function() {
                renderMathInElement(document.body, {
                    // auto-render specific keys
                    delimiters: [
                        {left: '$$', right: '$$', display: true},
                        {left: '$', right: '$', display: false},
                        {left: '\\(', right: '\\)', display: false},
                        {left: '\\[', right: '\\]', display: true}
                    ],
                    // render equation with bug
                    throwOnError : false,
                    // support eqref
                    trust: (context) => ['\\htmlId', '\\href'].includes(context.command),
                    macros: {
                        "\\eqref": "\\href{###1}{(\\text{#1})}",
                        "\\ref": "\\href{###1}{\\text{#1}}",
                        "\\label": "\\htmlId{#1}{}"
                    }
                });
            });
        </script>
    </head>

    <body>
        In Eq. $\eqref{eq:1}$ or $\ref{eq:1}$.<br/>

        $$
        \begin{aligned}
        \sin 2\theta = 2\sin \theta \cos \theta \\ = \cfrac{2 \tan \theta}{1+\tan^2 \theta}
        \end{aligned}
        \label{eq:1} \tag{1}
        $$
    </body>
</html>
```

渲染结果如下：

![image-20240126164406069](assets/image-20240126164406069.png)

但本法有个缺点： `$\ref{eq:1}$` `$\eqref{eq:1}$` 渲染为'eq:1'而非 '1'（即公式编号）。不知是否有方法修补此bug？或是否有其他支持\label \ref \eqref的方法可避免此bug?

## vscode插件Markdown+Math

[思路来源](https://github.com/goessner/mdmath/issues/116#issuecomment-1296210637)

安装vscode插件: [Markdown+Math](https://github.com/goessner/mdmath)

Reference: [KaTeX/KaTeX#2003 (comment)](https://github.com/KaTeX/KaTeX/issues/2003#issuecomment-843991794)

在vscode的配置文件中加入如下配置，则vscode的自带markdown分栏预览就能支持`\label` `\eqref` `\ref`，效果见下图

```json
"mdmath.katexoptions": {
    "trust": "(context) => ['\\htmlId', '\\href'].includes(context.command)"
},
"mdmath.macros": {
    "\\eqref": "\\href{###1}{(\\text{#1})}",
    "\\ref": "\\href{###1}{\\text{#1}}",
    "\\label": "\\htmlId{#1}{}"
},
```

![image-20240126165126318](assets/image-20240126165126318.png)

相关讨论：

* KaTex issue: Support \eqref and \label  https://github.com/KaTeX/KaTeX/issues/2003

* Referencing formula numbers in articles https://github.com/falgon/roki-web/issues/34

* vscode-markdown公式引用：https://github.com/yzhang-gh/vscode-markdown/issues/985

* https://github.com/yzhang-gh/vscode-markdown/issues/985#issuecomment-1108580333

    由于这是非官方的做法，不太可能加入到正式支持之中，但是你可以自行修改插件的本地文件在 `$HOME/.vscode/extensions/yzhang.markdown-all-in-one-3.4.x/dist/extension.js` 中搜索 `l={throwOnError:!1}` 并替换为 `l={throwOnError:!1, trust: true}`

我的github评论：

* demo html:

  * https://github.com/KaTeX/KaTeX/issues/2003#issuecomment-1911672998

* Markdown+Math配置：

  * https://github.com/falgon/roki-web/issues/34#issuecomment-1911694713
  * https://github.com/yzhang-gh/vscode-markdown/issues/985#issuecomment-1911700106

