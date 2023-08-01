---
title: VMware中Ubuntu 20.04下JupyterHub的安装与配置
date: 2020-05-08 23:45:38
tags:
categories: 其他
---

昨天研究了一下JupyterHub的安装与配置,记录一下安装过程.

因为不想折腾双系统,也不太信任现在的WSL,选择了在VMware中运行Ubuntu.

## 1. 安装Ubuntu 20.04

前几天看到了Ubuntu的新LTS版本20.04出来了,一直想体验一把,正好趁这个机会看看长什么样.

镜像我直接在官网上下的,安装用VMware的简易安装就行了.注意虚拟机的网卡改成桥接模式,让虚拟机直接从路由器上获取ip,方便搭建好在主机上访问JupyterHub.装好Ubuntu后别忘了安装openssh和net-tools:

<!--more-->

```bash
sudo apt install openssh-server
sudo apt install net-tools
```

安装成功后,在终端里使用ifconfig -a查看路由器分发的ip地址,在主机上使用ssh连接就可以搭建环境了.

![](/img/JupyterHub/1.png.webp)

## 2. 安装Anaconda3

去清华的镜像站(TUNA)上找到了Anaconda最新的包的地址:https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2020.02-Linux-x86_64.sh, 使用wget下载到虚拟机中,然后执行安装脚本,按照他的指示来就行了.

```bash
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2020.02-Linux-x86_64.sh
sh ./Anaconda3-2020.02-Linux-x86_64.sh
```

默认是安装到~/anaconda3中.

顺便,这里我选择的是yes,我也不知道是干啥的.

![](/img/JupyterHub/2.png.webp)

执行

```bash
export PATH=~/anaconda3/bin:$PATH
```

将anaconda添加到PATH中.

输入conda,如果显示conda的提示,说明安装成功.

## 3.安装JupyterHub

JupyterHub的官方文档(https://jupyterhub.readthedocs.io/en/stable/ )提供了两种安装方法:

![](/img/JupyterHub/3.png.webp)

这里选择第二种安装.注意如果使用第一种安装的话还需要先额外安装nodejs环境,官方给的命令是:

```bash
sudo apt-get install npm nodejs-legacy
```

我使用

```bash
sudo apt install npm
```

也可以完成最终的安装.

还有一点就是conda的默认源在国外,如果没有特殊工具的话需要换源.

一般在网络终端上的工具都是不能实现完美的全局代理的,特别对于在虚拟机上的流量,即使使用Proxifier这样的东西也不能达到很好的效果.我是在路由器上直接使用了工具,所以没有考虑这一点.(不能再说了这网站备案了).

判断是否安装成功:

```bash
jupyterhub -h
configurable-http-proxy -h
```

运行jupyterhub:

```bash
jupyterhub
```

出现此界面,安装成功.

![](/img/JupyterHub/4.png.webp)

下面进行用户的配置.



## 4.用户配置

使用

```bash
jupyterhub --generate-config
```

生成默认的jupyterhub配置文件.

官方文档建议将此文件放在/etc/jupyterhub目录下.可以自行创建此文件夹后在该文件夹下执行命令.

![](/img/JupyterHub/5.png.webp)

此时出现了一个棘手的问题:

![](/img/JupyterHub/6.png.webp)

我们没有权限在这个文件夹下进行写文件的操作.

一般遇到这样的情况都是直接sudo,但是当我执行

```bash
sudo jupyterhub --generate-config
```

![](/img/JupyterHub/7.png.webp)

他提示没有找到jupyterhub这个命令.

去网上搜索,找到了解决方法:

切换到root用户,编辑/etc/sudoers文件.

将其中`Defaults env_reset`这一行改成`Defaults !env_reset`

如果你没有为root用户设置过密码,应该先使用`sudo passwd root`来给root设置密码,然后使用`su`来切换到root账户.

![](/img/JupyterHub/8.png.webp)

如果没有安装vim,使用apt安装即可.

编辑好后,切换回刚刚的用户.

编辑/etc/bash.bashrc文件,向最后添加

```bash
alias sudo='sudo env PATH=$PATH'
export PATH=~/anaconda3/bin:$PATH
```

如果出现文件无法保存,使用`:wq!`试试,还是不行直接`sudo vim`.

让修改的配置生效:

```bash
source /etc/bash.bashrc
```

这时就可以在/etc/jupyterhub下执行

```bash
sudo jupyterhub --generate-config
```



还有一种方法,可以解决无法在此文件夹读写的问题,即使用

```bash
sudo chmod 777 /etc/jupyterhub
```

修改这个文件夹的权限,生成这个配置文件.但是到后期还是需要在sudo下运行jupyterhub,所以在现在直接解决这个问题就好了.



通过查阅官方文档,我们可以找到配置文件的基本配置.

![](/img/JupyterHub/9.png.webp)

按照官方文档的说法,默认的用户认证管理器是PAM,ubuntu系统上的用户都被允许登录.

所以我们可以先切换到root用户,在系统里添加一个用户:

```bash
adduser kasumi
```

设置好密码后,返回原来的用户.

修改配置文件,将一个用户添加到管理员列表中(这里是honokasumi),另一个普通用户(这里是kasumi)添加到白名单中.(按照官方文档的说法,在管理员列表中的非白名单中的用户会被自动添加到白名单中):

![](/img/JupyterHub/10.png.webp)

指定配置文件,启动jupyter

```bash
sudo jupyterhub -f /etc/jupyterhub/jupyterhub_config.py
```

访问http://ip:8000 ,输入账号密码,登录成功.

 ![](/img/JupyterHub/11.png.webp)

## 5.安装其他语言的内核

![](/img/JupyterHub/12.png.webp)

默认已经安装了Python3的内核,要想支持其他语言,需要安装其他语言的内核.



这里以安装C++系列内核为例.

使用

```bash
conda install xeus-cling -c conda-forge
```

安装xeus-cling,一个在jupyter上支持c++系列的内核.

安装成功后,可以在这里切换使用内核:

![](/img/JupyterHub/13.png.webp)

![](/img/JupyterHub/14.png.webp)

https://github.com/jupyter/jupyter/wiki/Jupyter-kernels 这里列出了jupyter上其他语言的内核,可以自己寻找并安装.

