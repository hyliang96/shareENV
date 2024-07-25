---
title: cuda安装教程
categories:
  - 器
  - linux杂项
abbrlink: 3078800000000
date: 2021-08-02 01:24:20
updated:
tags:
---

# 文件夹组织

```
cuda_cudnn/
	cuda/
		各个版本的cuda安装包
	cudnn/
		各个版本的cuda对应的各个版本的cudnn的安装包
	README.md
```

# cuDNN与cuda之间的关系

cuda：显卡计算的加速库，可用于渲染、神经网络等等

cudnn：神经网络加速库文件，依赖于cuda，大幅优化显卡上的神经网络计算，比cuda加速两倍以上

nccl：多显卡通讯加速，可加速神经网络多卡训练

# 直接用apt安装

[参见](https://gist.github.com/bogdan-kulynych/f64eb148eeef9696c70d485a76e42c3a)

# 徒手安装教程

参考：

* http://www.rignitc.com/2018/12/29/install-cuda-10-with-ubuntu-16-04/
* https://blog.csdn.net/qq_32408773/article/details/84112166
* https://zhuanlan.zhihu.com/p/47330858
* https://blog.csdn.net/qq_38231807/article/details/83780336

## 从NVIDIA官网下载安装包的技巧

- 需要翻墙开全局模式，才能下载链接/下载按钮才能工作

- 可再本地用浏览器(w3m不可)登录账号、下载，传到服务器

- 直接下载到服务器：

    - 不可在网页上直接拷贝下载按钮的链接，去服务器wget，这样无法下载成功。

    - 必需用（本地）浏览器（`w3m`终端浏览器不可以）访问下载页，登录账号。

    - 再点下载网页上的按钮，开始下载了，再从浏览器的下载栏处复制链接。

    - 然后到服务器`wget [此链接]`，下载得到的文件名结尾有一串乱码，形如

        > ```
        > 'cudnn-10.1-linux-x64-v7.6.3.30.tgz?ziMqZ3giGG1v5v90de6Of-_NpBtGVRLIR4O7hkSQ4Hu5RE_Qr-qxE98NFILK6B89iL1xitgZGQMy1ZH_o3ayiKsoYVbK1K3GmYUbNkFKUTn-jDCpEv726d61fCYT5SC6rI17tKt8hDVHxC-4zDH5XJtEjSovwJn5obx_04zS72ohX8HvmNEI8MxqTrq97Jq55krHcKU5l'
        > ```

        只需 `mv  cudnn-10.1-linux-x64-v7.6.3.30.tgz?xxxxxxx cudnn-10.1-linux-x64-v7.6.3.30.tgz`

    - 之后解压必需用`tar -xzvf  cudnn-x.x-linux-x64-vxx.tgz`，用其他`7z`解压会得到一个文件而不是文件夹。

## 安装cuda

[cuda-9.0下载cuda](https://developer.nvidia.com/cuda-90-download-archive)

```bash
sudo sh cuda_x.x.x_xxx.xx_linux.run
```

`⌃C`滑到协议的结尾，然后依下选项选择

```bash
Do you accept the previously read EULA?
accept/decline/quit: accept

Install NVIDIA Accelerated Graphics Driver for Linux-x86_64 384.81?
(y)es/(n)o/(q)uit: n  # 这是因为已经安装了NVIDIA的驱动

Install the CUDA 9.0 Toolkit?
(y)es/(n)o/(q)uit: y

Enter Toolkit Location
 [ default is /usr/local/cuda-9.0 ]: # 直接回车

Do you want to install a symbolic link at /usr/local/cuda?
(y)es/(n)o/(q)uit: y

Install the CUDA 9.0 Samples?
(y)es/(n)o/(q)uit: y

Enter CUDA Samples Location
 [ default is /home/xxxx ]: # 直接回车

Installing the CUDA Toolkit in /usr/local/cuda-9.0 ...
```

安装完成返回

> ```bash
> Installing the CUDA Toolkit in /usr/local/cuda-9.0 ...
> Installing the CUDA Samples in /home/haoyu ...
> Copying samples to /home/haoyu/NVIDIA_CUDA-9.0_Samples now...
> Finished copying samples.
>
> ===========
> = Summary =
> ===========
>
> Driver:   Not Selected # 这是因为上面 Install NVIDIA Accelerated Graphics Driver 选了n
> Toolkit:  Installed in /usr/local/cuda-9.0
> Samples:  Installed in /home/haoyu
>
> Please make sure that
>  -   PATH includes /usr/local/cuda-9.0/bin
>  -   LD_LIBRARY_PATH includes /usr/local/cuda-9.0/lib64, or, add /usr/local/cuda-9.0/lib64 to /etc/ld.so.conf and run ldconfig as root
>
> To uninstall the CUDA Toolkit, run the uninstall script in /usr/local/cuda-9.0/bin
>
> Please see CUDA_Installation_Guide_Linux.pdf in /usr/local/cuda-9.0/doc/pdf for detailed information on setting up CUDA.
>
> ***WARNING: Incomplete installation! This installation did not install the CUDA Driver. A driver of version at least 384.00 is required for CUDA 9.0 functionality to work.
> To install the driver using this installer, run the following command, replacing <CudaInstaller> with the name of this run file:
>     sudo <CudaInstaller>.run -silent -driver
>
> Logfile is /tmp/cuda_install_51161.log
> Signal caught, cleaning up
> ```
>

## 测试cuda

```bash
cd /usr/local/cuda/samples/1_Utilities/deviceQuery
sudo make clean && sudo make
./deviceQuery
```

返回

> ```bash
> > Peer access from GeForce GTX TITAN X (GPU0) -> GeForce GTX TITAN X (GPU1) : Yes
> > Peer access from GeForce GTX TITAN X (GPU0) -> GeForce GTX TITAN X (GPU2) : No
> > Peer access from GeForce GTX TITAN X (GPU0) -> GeForce GTX TITAN X (GPU3) : No
> > Peer access from GeForce GTX TITAN X (GPU1) -> GeForce GTX TITAN X (GPU0) : Yes
> > Peer access from GeForce GTX TITAN X (GPU1) -> GeForce GTX TITAN X (GPU2) : No
> > Peer access from GeForce GTX TITAN X (GPU1) -> GeForce GTX TITAN X (GPU3) : No
> > Peer access from GeForce GTX TITAN X (GPU2) -> GeForce GTX TITAN X (GPU0) : No
> > Peer access from GeForce GTX TITAN X (GPU2) -> GeForce GTX TITAN X (GPU1) : No
> > Peer access from GeForce GTX TITAN X (GPU2) -> GeForce GTX TITAN X (GPU3) : Yes
> > Peer access from GeForce GTX TITAN X (GPU3) -> GeForce GTX TITAN X (GPU0) : No
> > Peer access from GeForce GTX TITAN X (GPU3) -> GeForce GTX TITAN X (GPU1) : No
> > Peer access from GeForce GTX TITAN X (GPU3) -> GeForce GTX TITAN X (GPU2) : Yes
>
> deviceQuery, CUDA Driver = CUDART, CUDA Driver Version = 10.1, CUDA Runtime Version = 9.0, NumDevs = 4
> ```
>

结果最后一行若有`Result = PASS`则测试成功

## 安装cudnn

参考：

* [官方文档](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html#installlinux-deb)
* https://blog.csdn.net/qq_32408773/article/details/84112166

[下载cudnn官网](https://developer.nvidia.com/rdp/cudnn-archive)

* 进入网页首先需要注册账号

### 法一 dpkg安装

下载`[cuDNN Runtime Library for UbuntuXX.X (Deb)]`

然后执行

```bash
sudo dpkg -i libcudnnX_X.X.X.XX-X+cudaX.X_amd64.deb
```

即完成安装

### 法二 cp安装

* 请选择下载

  `Download cuDNN vx.x.x (月 日, 年), for CUDA x.x`

  *  `cuDNN vx.x.x Library for Linux` cuDNN 动态库文件
  * `cuDNN vx.x.x Developer Library for Ubuntu16.04 (Deb)` cuDNN 测试代码

* 下载得到`.tar`文件，解压之

```bash
tar -xzvf cudnn-x.x-linux-x64-vxx.tgz
```

**进入解压的文件夹后**

通过拷贝来安装cudnn，并修改权限

```bash
CUDA_TO_INSTALL=cuda-x.x  # 设置版本号
sudo cp cuda/include/cudnn.h /usr/local/$CUDA_TO_INSTALL/include/
sudo cp cuda/lib64/libcudnn* /usr/local/$CUDA_TO_INSTALL/lib64/
sudo chmod a+r /usr/local/$CUDA_TO_INSTALL/include/cudnn.h
sudo chmod a+r /usr/local/$CUDA_TO_INSTALL/lib64/libcudnn*
sudo ldconfig /usr/local/$CUDA_TO_INSTALL/lib64
```

## [测试cudnn](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html)

cuDNN v7.0 Code Samples and User Guide for Ubuntu16.04 (Deb)

### 获得测试代码

* 法一，从官网获得：下载方法见[安装cudnn]-[cuDNN 测试代码]

测试cuDNN

```bash
sudo dpkg -i cudnn7.1.4_for_cuda9.0_sample_and_doc.deb
```

返回

> ```
> (Reading database ... 263943 files and directories currently installed.)
> Preparing to unpack cudnn7.1.4_for_cuda9.0_sample_and_doc.deb ...
> Unpacking libcudnn7-doc (7.1.4.18-1+cuda9.0) over (7.1.4.18-1+cuda9.0) ...
> dpkg: dependency problems prevent configuration of libcudnn7-doc:
>  libcudnn7-doc depends on libcudnn7-dev; however:
>   Package libcudnn7-dev is not installed.
>
> dpkg: error processing package libcudnn7-doc (--install):
>  dependency problems - leaving unconfigured
> Errors were encountered while processing:
>  libcudnn7-doc
> ```

虽然上面报错，但不影响，因为这一步已经把`/usr/src/cudnn_samples_v7/`创建好，可以开始测试了

Copy the cuDNN sample to a writable path.

```bash
sudo cp -r /usr/src/cudnn_samples_v7/ /home/$USER
```

* 法二：`本目录/cudnn/cudnn_samples_v7`，适用于所有`cudnn7.x.x_for_cudax.x`

Copy the cuDNN sample to a writable path.

```bash
cp -r ./cudnn/cudnn_samples_v7/ /home/$USER
```

### 开始测试

Go to the writable path.

```bash
cd /home/$USER/cudnn_samples_v7/mnistCUDNN
```

Compile the mnistCUDNN sample.

```bash
sudo make clean && sudo make
```

Run the mnistCUDNN sample

```bash
./mnistCUDNN
```

> ```
>
> Test passed!
>
> Testing half precision (math in single precision)
> Loading image data/one_28x28.pgm
> Performing forward propagation ...
> Testing cudnnGetConvolutionForwardAlgorithm ...
> Fastest algorithm is Algo 1
> Testing cudnnFindConvolutionForwardAlgorithm ...
> ^^^^ CUDNN_STATUS_SUCCESS for Algo 1: 0.024896 time requiring 3464 memory
> ^^^^ CUDNN_STATUS_SUCCESS for Algo 0: 0.030912 time requiring 0 memory
> ^^^^ CUDNN_STATUS_SUCCESS for Algo 2: 0.039712 time requiring 28800 memory
> ^^^^ CUDNN_STATUS_SUCCESS for Algo 7: 0.098592 time requiring 2057744 memory
> ^^^^ CUDNN_STATUS_SUCCESS for Algo 5: 0.149504 time requiring 203008 memory
> Resulting weights from Softmax:
> 0.0000001 1.0000000 0.0000001 0.0000000 0.0000563 0.0000001 0.0000012 0.0000017 0.0000010 0.0000001
> Loading image data/three_28x28.pgm
> Performing forward propagation ...
> Resulting weights from Softmax:
> 0.0000000 0.0000000 0.0000000 1.0000000 0.0000000 0.0000714 0.0000000 0.0000000 0.0000000 0.0000000
> Loading image data/five_28x28.pgm
> Performing forward propagation ...
> Resulting weights from Softmax:
> 0.0000000 0.0000008 0.0000000 0.0000002 0.0000000 1.0000000 0.0000154 0.0000000 0.0000012 0.0000006
>
> Result of classification: 1 3 5
>
> Test passed!
> ```

此即测试成功

## [安装nccl](https://docs.nvidia.com/deeplearning/sdk/nccl-install-guide/index.html#usingnccl)

NCCL是Nvidia Collective multi-GPU Communication Library的简称，它是一个实现多GPU的collective communication通信库，Nvidia做了很多优化，以在PCIe、Nvlink、InfiniBand上实现较高的通信速度。

[参考](https://docs.ksyun.com/documents/2594) [参考](https://docs.ksyun.com/documents/2593)

* 访问[官方下载页](https://developer.nvidia.com/nccl/nccl-download)注册、登录、选择和cuda、系统适配的安装包、下载
    * 下载` local NCCL repository` 必需用浏览器(w3m不可)登录账号、下载，传到服务器。不可在网页上直接拷贝下载按钮的链接，去服务器wget，这样无法下载成功。
    * 下载`For the network repository `可以直接在网页上的下载按钮复制下载链接用wget获取。

* Install the repository.
    * For the local NCCL repository:

    ```
    sudo dpkg -i nccl-repo-<version>.deb
    ```

    * For the network repository:

    ```
    sudo dpkg -i nvidia-machine-learning-repo-<version>.deb
    ```

* Update the APT database:

    ```
    sudo apt update
    ```

* Install the libnccl2 package with APT. Additionally, if you need to compile applications with NCCL, you can install the libnccl-dev package as well:
    * If you are using the network repository, the following command will upgrade CUDA to the latest version.

    ```
    sudo apt install libnccl2 libnccl-dev
    ```

	*  装不是全网最新版本的cuda的nccl，则需执行

    ```
    sudo apt install libnccl2=2.0.0-1+cuda8.0 libnccl-dev=2.0.0-1+cuda8.0
    ```

## 测试nccl

### 查看版本

```
python -c 'import torch; print(torch.cuda.nccl.version())'
```

### [专门的测试程序](https://github.com/NVIDIA/nccl-tests)

These tests check both the performance and the correctness of [NCCL](http://github.com/nvidia/nccl) operations.

下载

```bash
git clone https://github.com/NVIDIA/nccl-tests.git
```

#### 编译

```bash
cd nccl-tests
make clean
make # (我们的服务器就跑这个)
```

If CUDA is not installed in `/usr/local/cuda`, you may specify CUDA_HOME. Similarly, if NCCL is not installed in `/usr`, you may specify NCCL_HOME.

```
make CUDA_HOME=/path/to/cuda NCCL_HOME=/path/to/nccl
```

NCCL tests rely on MPI to work on multiple processes, hence multiple nodes. If you want to compile the tests with MPI support, you need to set MPI=1 and set MPI_HOME to the path where MPI is installed. (我们的服务器无需跑这个)

```
make MPI=1 MPI_HOME=/path/to/mpi CUDA_HOME=/path/to/cuda NCCL_HOME=/path/to/nccl
```

`make`成功会返回

```
make -C src build
make[1]: Entering directory '/home/haoyu/nccl-tests/src'
Compiling  all_reduce.cu                       > ../build/all_reduce.o
Compiling  common.cu                           > ../build/common.o
Linking  ../build/all_reduce.o               > ../build/all_reduce_perf
Compiling  all_gather.cu                       > ../build/all_gather.o
Linking  ../build/all_gather.o               > ../build/all_gather_perf
Compiling  broadcast.cu                        > ../build/broadcast.o
Linking  ../build/broadcast.o                > ../build/broadcast_perf
Compiling  reduce_scatter.cu                   > ../build/reduce_scatter.o
Linking  ../build/reduce_scatter.o           > ../build/reduce_scatter_perf
Compiling  reduce.cu                           > ../build/reduce.o
Linking  ../build/reduce.o                   > ../build/reduce_perf
make[1]: Leaving directory '/home/haoyu/nccl-tests/src'
```

#### Usage

NCCL tests can run on multiple processes, multiple threads, and multiple CUDA devices per thread. The number of process is managed by MPI and is therefore not passed to the tests as argument. The total number of ranks (=CUDA devices) will be equal to (number of processes)*(number of threads)*(number of GPUs per thread).

#### Quick examples

Run on 8 GPUs (`-g 8`), scanning from 8 Bytes to 128MBytes : (我们的服务器就跑这个)

```
./build/all_reduce_perf -b 8 -e 128M -f 2 -g 8
```

Run with MPI on 40 processes (potentially on multiple nodes) with 4 GPUs each :

```
mpirun -np 40 ./build/all_reduce_perf -b 8 -e 128M -f 2 -g 4
```

测试结果会返回

> ```
> # nThread 1 nGpus 8 minBytes 8 maxBytes 134217728 step: 2(factor) warmup iters: 5 iters: 20 validation: 1
> #
> # Using devices
> #   Rank  0 Pid  12164 on   jungpu30 device  0 [0x1a] GeForce RTX 2080 Ti
> #   Rank  1 Pid  12164 on   jungpu30 device  1 [0x1b] GeForce RTX 2080 Ti
> #   Rank  2 Pid  12164 on   jungpu30 device  2 [0x3d] GeForce RTX 2080 Ti
> #   Rank  3 Pid  12164 on   jungpu30 device  3 [0x3e] GeForce RTX 2080 Ti
> #   Rank  4 Pid  12164 on   jungpu30 device  4 [0x88] GeForce RTX 2080 Ti
> #   Rank  5 Pid  12164 on   jungpu30 device  5 [0x89] GeForce RTX 2080 Ti
> #   Rank  6 Pid  12164 on   jungpu30 device  6 [0xb1] GeForce RTX 2080 Ti
> #   Rank  7 Pid  12164 on   jungpu30 device  7 [0xb2] GeForce RTX 2080 Ti
> #
> #                                                     out-of-place                       in-place
> #       size         count    type   redop     time   algbw   busbw  error     time   algbw   busbw  error
> #        (B)    (elements)                     (us)  (GB/s)  (GB/s)            (us)  (GB/s)  (GB/s)
>            8             2   float     sum    35.93    0.00    0.00  1e-07    35.72    0.00    0.00  1e-07
>           16             4   float     sum    37.01    0.00    0.00  1e-07    36.77    0.00    0.00  1e-07
>           32             8   float     sum    36.74    0.00    0.00  6e-08    36.44    0.00    0.00  6e-08
>           64            16   float     sum    37.21    0.00    0.00  6e-08    36.61    0.00    0.00  6e-08
>          128            32   float     sum    36.98    0.00    0.01  6e-08    36.97    0.00    0.01  6e-08
>          256            64   float     sum    37.26    0.01    0.01  3e-08    36.42    0.01    0.01  3e-08
>          512           128   float     sum    37.47    0.01    0.02  3e-08    37.28    0.01    0.02  3e-08
>         1024           256   float     sum    37.54    0.03    0.05  1e-07    36.81    0.03    0.05  1e-07
>         2048           512   float     sum    38.50    0.05    0.09  2e-07    37.57    0.05    0.10  2e-07
>         4096          1024   float     sum    38.97    0.11    0.18  2e-07    38.46    0.11    0.19  2e-07
>         8192          2048   float     sum    39.49    0.21    0.36  2e-07    38.23    0.21    0.37  2e-07
>        16384          4096   float     sum    41.20    0.40    0.70  2e-07    40.58    0.40    0.71  2e-07
>        32768          8192   float     sum    67.22    0.49    0.85  2e-07    67.61    0.48    0.85  2e-07
>        65536         16384   float     sum    124.9    0.52    0.92  2e-07    126.4    0.52    0.91  2e-07
>       131072         32768   float     sum    237.0    0.55    0.97  2e-07    236.7    0.55    0.97  2e-07
>       262144         65536   float     sum    207.2    1.27    2.21  2e-07    204.7    1.28    2.24  2e-07
>       524288        131072   float     sum    325.5    1.61    2.82  2e-07    325.4    1.61    2.82  2e-07
>      1048576        262144   float     sum    615.4    1.70    2.98  2e-07    613.0    1.71    2.99  2e-07
>      2097152        524288   float     sum   1289.4    1.63    2.85  2e-07   1290.3    1.63    2.84  2e-07
>      4194304       1048576   float     sum   2740.9    1.53    2.68  2e-07   2740.6    1.53    2.68  2e-07
>      8388608       2097152   float     sum   5830.5    1.44    2.52  2e-07   5829.7    1.44    2.52  2e-07
>     16777216       4194304   float     sum    11991    1.40    2.45  2e-07    11981    1.40    2.45  2e-07
>     33554432       8388608   float     sum    23923    1.40    2.45  2e-07    23913    1.40    2.46  2e-07
>     67108864      16777216   float     sum    47784    1.40    2.46  2e-07    47781    1.40    2.46  2e-07
>    134217728      33554432   float     sum    95470    1.41    2.46  2e-07    95477    1.41    2.46  2e-07
> # Out of bounds values : 0 OK
> # Avg bus bandwidth    : 1.20304
> #
> ```

见此状完整的结果，即通过测试。

## 多版本cuda的管理

### 设置默认cuda版本

* 当装了多个版本的cuda，要设置哪个版本的cuda为系统默认的cuda，只需修改`/usr/local/cuda`

```bash
sudo rm /usr/local/cuda && sudo ln -s /usr/local/cuda-x.x /usr/local/cuda
```

* 当`/usr/local/cuda`链接变更后，需要更新共享库缓存

```bash
sudo ldconfig /usr/local/cuda/lib64
```

`lbconfig`是一个动态链接库管理命令，为了让动态链接库为系统所共享。linux下的共享库机制采用了类似于高速缓存的机制，即将库信息保存在`/etc/ld.so.cache`文件里边。运行上述命令，可搜索`/usr/local/cuda/lib64`内`lib*.so.*`文件，将其路径等信息添加到`/etc/ld.so.cache`文件里。

### 使用非默认版本的cuda

一个用户若想使用非默认版本的cuda, 则在当前终端执行如下命令, 修改环境变量:

```bash
export PATH=/usr/local/cuda-x.x/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-x.x/lib64:$LD_LIBRARY_PATH
```

这样, 此终端将使用`cuda-x.x`版本运行各种程序. 此时若执行 `nvcc -V` 查看cuda版本会返回此版本.

# 报错日志与解决方案

## cuda-8.0 安装

```bash
cd /home/xxx/NVIDIA_CUDA-8.0_Samples
make
```

报错

> ```
> nvcc warning : The 'compute_20', 'sm_20', and 'sm_21' architectures are deprecated, and may be removed in a future release (Use -Wno-deprecated-gpu-targets to suppress warning).
> In file included from /usr/local/cuda-8.0/bin/..//include/cuda_runtime.h:78:0,
>                  from <command-line>:0:
> /usr/local/cuda-8.0/bin/..//include/host_config.h:119:2: error: #error -- unsupported GNU version! gcc versions later than 5 are not supported!
>  #error -- unsupported GNU version! gcc versions later than 5 are not supported!
>   ^~~~~
> Makefile:250: recipe for target 'simplePrintf.o' failed
> make[1]: *** [simplePrintf.o] Error 1
> make[1]: Leaving directory '/usr/local/cuda-8.0/samples/0_Simple/simplePrintf'
> Makefile:52: recipe for target '0_Simple/simplePrintf/Makefile.ph_build' failed
> make: *** [0_Simple/simplePrintf/Makefile.ph_build] Error 2
> ```
>

解决办法：手动给cuda-8.0添加gcc和g++（版本<5）的链接

```bash
sudo apt-get install gcc-4.9 g++-4.9
sudo ln -s /usr/bin/g++-4.9 /usr/local/cuda-8.0/bin/g++
sudo ln -s /usr/bin/gcc-4.9 /usr/local/cuda-8.0/bin/gcc
```

## cudnn 测试

### 编译

```bash
sudo make clean && sudo make
```

返回

> ```
> /usr/bin/ld:/usr/local/cuda/lib64/libcudnn.so: file format not recognized; treating as linker script
> ```

**[解决方法](https://blog.csdn.net/qq_33144323/article/details/85465975)**

```bash
cd /usr/local/cuda/lib64
ls -l | grep libcudnn.so
```

```bash
sudo rm -rf libcudnn.so libcudnn.so.7
sudo ln -s libcudnn.so.7.x.x libcudnn.so.7
sudo ln -s libcudnn.so.7 libcudnn.so
```

然后回到测试代码的目录

```bash
sudo make clean && sudo make
```

即编译成功

### 运行

```bash
./mnistCUDNN
```

返回

> ```
> ./mnistCUDNN: error while loading shared libraries: libcudart.so.9.0: cannot open shared object file: No such file or directory
> ```

**[解决方法](https://github.com/BVLC/caffe/issues/4944)**

这是由于装了多个版本的cuda，当链接`/usr/local/cuda->cuda-x.x`变更后，需要再进行如下操作

```bash
sudo ldconfig /usr/local/cuda/lib64
```

> ```
> /sbin/ldconfig.real: /usr/local/cuda-10.1/targets/x86_64-linux/lib/libcudnn.so.7 is not a symbolic link
>
> /sbin/ldconfig.real: /usr/local/cuda-10.1/targets/x86_64-linux/lib/libcudnn.so.5 is not a symbolic link
> ```

```bash
./mnistCUDNN
```

则测试成功

