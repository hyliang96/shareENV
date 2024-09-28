---
title: 我的python使用tips
categories:
  - 器
  - python
abbrlink: 53bbc892
date: 2019-05-25 04:03:03
updated:
tags:
---

[TOC]

## 运行
### 命令行
mac/unix/Linux
进入：`python`、`ipython`
退出：`ctrl+d`，显示是否退出，输y，回车
挂起：`ctrl+z`
杀死：`ctrl+c`

### sublime内
长按`command`，调出sublime的快捷键清单，点击清单上的快捷键即可执行

## 版本
### 包的存放位置
python的包存放在site-packages/文件夹内，包可以是文件夹（内含.py等文件）、单独的.py等文件。
#### import的方法
需要从当前python的site-packages开始，逐层写import。例如，要导入这个包：“当前python的site-packages/文件夹1/文件夹2/目标文件.py”，需写

~~~python
import 文件夹1.文件夹2.目标文件
~~~
#### 如何确定当前python的"site-packages/"位置
即相当于确定`which python`那个python的site-packages/的位置

**法一** 在命令行中

~~~bash
python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"
~~~

**法二** 在python中sad

~~~python
from distutils.sysconfig import get_python_lib;
print(get_python_lib())
~~~

均会返回形如“/Users/mac/anaconda/lib/python3.6/site-packages”的地址。若在mac系统，按`command+shift+G`，输入该地址，回车即到达包所在目录。

## 输出

### 整行输出

python的print输出的特性：

* 在出现换行符(可以是sleep 尾巴自带的，或字符串里的)前，不会输出

* 要在未出现换行符时强行输出，有两种情况

  * 用`sys.stdout.flush()`输出尽stdout所存，输出后换不行，光标在行尾

    ```python
    from time import sleep
    import sys
    # 先输出'a'并换行，过一秒才输出'bc'并换行
    print 'a\nb', # 字符串里有'\n',print结尾不带'\n'
    sleep(1)
    print 'c'     # pritn结尾有'\n'

    # 先输出'a\nb'，过一秒在'b'后紧接着输出'c\n'
    print 'a\nb', # 字符串里有'\n',print结尾不带'\n'
    sys.stdout.flush()
    sleep(1)
    print 'c'     # pritn结尾有'\n'
    ```

  * python脚本执行完毕，输出尽stdout所存

    ```python
    # 在ipython中
    print 'abc\r'   # 然后回车
    # 输出
    # abc
    #       //下面换了一行

    print 'abc\r',  # 然后回车
    # 输出
    # abc   //下面没有换一行了
    ```

### 同一行反复输出

* `'\r'`表示光标回到屏幕上光标所在行之首，但不清除本行已输出字符，之后新输出的字符会覆盖已有字符。

* 不是两个'\n'之间称为一行，而是屏幕上一行输出叫一行

  ```python
  print '---------------------------------------------------------------------------------------------------------------------\ra'
  # 得到
  # -------------------------------------------------------------------------------------
  # a----------------------------------
  ```

* **同一行反复输出的方法**

  ```python
  import sys
  # 循环
  	print "就地覆盖的内容\r",
   	sys.stdout.flush()
  # 循环
  	print "不断向后延长的内容",
    	sys.stdout.flush()
  ```

  #### 进度条

  ```python
  import sys

  def progess_bar(p, precision=2,num_block=30):
  # 输出到屏幕
  # p 是[0,1]的float，表示百分之多少的进度
  # precision小数点位数
  # 进度条的'>'块数
  	# 以防之前stdout修改，如"屏幕文件双向输出"功能
      original = sys.stdout
      sys.stdout = sys.__stdout__
      # 右对齐输出百分数
      print ('%%%ds'%(precision+4))  % \
          (('%%.%df'%precision)%(100*p)),'%',
      print '   |',
      n = int(p*num_block)
      for i in range(n):
          print '>',
      for i in range(num_block-n):
          print ' ',
      if p!=1:
          print '|\r',
      else:
          print
      # 还原sys.stdout
      sys.stdout.flush()
      sys.stdout = original

  # 效果
  from time import sleep
  for p in range(101):
      p=p/100.0
      progess_bar(p, precision=3,num_block=20)
      sleep(0.01)
  # 0.01秒变化一下
  #  94.000 %   | > > > > > > > > > > > > > > > > > >     |
  ```

* 一些对比实例

  ```python
  import sys
  from time import sleep
  # 例1
  for x in range(10):
      print 'asdasdasdas',
      print "\r%d"%x,        # 回到行首
      print "hahah\r",       # 光标回到行首
      sys.stdout.flush()
      sleep(0.1)
  # 输出
  # x ha  asdas
  # x=0,1,2,...9 (每0.1秒一变化)
  # asdas未被清除

  # 例2
  for x in range(10):
      print 'asdasdasdas',
      print "%d"%x,        # 不回到行首
      print "hahah\r",
      sys.stdout.flush()
      sleep(0.1)
  # 输出
  # asdasdasdas x hahah
  # x=0,1,2,...9 (每0.1秒一变化)

  # 例3
  print 'asdasdasdas',     # 未换行
  for x in range(10):
      print "%d"%x,        # 不回到行首
      print "hahah\r",
      sys.stdout.flush()
      sleep(0.1)
  # 输出
  # x hahahsdas 0 hahah
  # x=1,2,...9 (每0.1秒一变化)

  # 例4
  print 'asdasdasdas',     # 未换行
  for x in range(10):
      print "%d"%x,        # 不回到行首
      print "hahah\r",
      sleep(0.1)
  # 1秒后输出
  # x hahahsdas 9 hahah
  ```

## 路径

获得当文件(而不是其所在文件夹)的绝对路径

```python
dir_path = os.path.dirname(os.path.realpath(__file__))
```

从路径取得文件名字

```python
<string> = os.path.basename(<filepath_string>)
# Linux下相当于 <filepath_string>.split('/')[-1]
# 若<filepath_string>为文件路径，返回文件名(带扩展名)
# 若<filepath_string>为文件夹路径，返回“”
```

从路径取得文件夹名字

```bash
<dir_string> = os.path.dirname(<path_string>)
# 若<path_string>为文件夹路径，则返回 <path_string>
# 若<path_string>为文件路径，  则返回其所在文件夹的路径
```

一路向下创建文件夹

```bash
os.makedirs(<path_string>) # 此文件夹已经存在则报错
os.makedirs(<path_string>, exist_ok=True) # 此文件夹已经存在不报错
```

连接路径名，在不同操作系统下都work

```bash
<path_string> = os.path.join(<path_string1>,<path_string2>,...)
```

