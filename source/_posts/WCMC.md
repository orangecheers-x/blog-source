---
title: Win10+CMake+MinGW+CLion环境配置
date: 2020-03-27 21:56:00
tags: 
categories: 其他
---

# Win10+CMake+MinGW+CLion环境配置

在知乎上看到一篇简单介绍make,makefile,cmake的文章,原文链接https://zhuanlan.zhihu.com/p/111110992.

了解了这些东西之后,可以开始配置Windows上的C++环境了,这里使用CLion+MingW的配置.

首先在MinGW上下载mingw-get.exe.

http://www.mingw.org/

在mingw-get.exe所在目录下执行命令:

```powershell
.\mingw-get.exe install gcc g++ gdb mingw32-make
```

安装gcc,g++,gdb以及mingw32-make,并将bin文件夹添加到PATH环境变量中.

安装CMake,在安装时可以勾选添加到PATH.

<!-- more --> 

为了进一步了解CMake,可以利用CMake在windows下的gui试验一下编译.

![1](/img/WCMC环境配置/1.png.webp.webp)

编写a.cpp和CMakeLists.txt文件,其中CMakeLists.txt文件内容为

```plain
#需要的最低cmake版本
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
#项目名称
PROJECT(GGZKA)
#把当前目录(.)下所有源代码文件和头文件加入变量SRC_LIST
AUX_SOURCE_DIRECTORY(. SRC_LIST)
#生成应用程序 hello (在windows下会自动生成hello.exe)
ADD_EXECUTABLE(ggzka ${SRC_LIST})
```

这就是一个最简单的CMakeLists.txt文件,足以将a.cpp编译成hello.exe.

打开CMake-gui,选择源码文件夹和二进制文件输出文件夹.

![2](/img/WCMC环境配置/2.png.webp.webp)

点Generate.

![3](/img/WCMC环境配置/3.png.webp.webp)

因为使用的是MinGW,所以选择MinGW Makefiles,也就是mingw32-make可以处理的makefiles文件.

要使用之前自己安装的MinGW,所以选择第二项,之后自己选择编译器.

![4](/img/WCMC环境配置/4.png.webp.webp)

选择好编译器后,正常的话已经可以在bin文件夹下生成Makefiles文件了,然后在bin文件夹下执行

```powershell
mingw32-make
```

![5](/img/WCMC环境配置/5.png.webp.webp)

就可以看到bin文件夹下已经编译出hello.exe文件了.



懂得了基本概念之后,配置CLion也就很简单了.

![6](/img/WCMC环境配置/6.png.webp.webp)

Environment选择MinGW所在的文件夹.Make选择mingw32-make,C编译器选择gcc,c++编译器g++即可.

