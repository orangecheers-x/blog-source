---
title: 在JupyterHub使用基于sqlite3的第三方Authenticator
date: 2020-05-21 21:48:52
tags:
---

默认JupyterHub是使用PAM, 与系统用户绑定的认证方式, 这使得JupyterHub的多用户非常不灵活,参见这个Issue:    https://github.com/jupyterhub/jupyterhub/issues/710.

JupyterHub默认支持了很多第三方的OAuth的认证渠道,但是这些大部分是在线的,不适合我的需求. 于是我在GitHub上找到了一个基于sqlite3数据库的离线认证器: https://github.com/sparkingarthur/jupyterhub-localsqliteauthenticator

按照Readme文件的步骤,安装成功后,在JupyterHub配置文件中将认证器修改为这个认证器:

![image-20200521213734811](/img/JupyterHubAuth/1.png.webp.webp)

<!--more-->

注意export修改环境变量并不是永久的,如果出现如下错误一般是环境变量出了问题,可以重新添加环境变量或者直接修改文件永久添加环境变量.

![image-20200521173137534](/img/JupyterHubAuth/2.png.webp.webp)

如果出现这样的问题,请使用sudo运行JupyterHub

![image-20200521205520398](/img/JupyterHubAuth/3.png.webp.webp)

登录第三方认证器自带的admin用户,登陆成功.

![image-20200521211235194](/img/JupyterHubAuth/4.png.webp.webp)

此时管理员面板中的的添加用户仍然是添加系统用户,并不是在我们的认证器中添加用户.

![image-20200521211405293](/img/JupyterHubAuth/5.png.webp.webp)

![image-20200521211412070](/img/JupyterHubAuth/6.png.webp.webp)

可以使用认证器提供的api来添加用户,右边就是这个认证器使用的数据库,默认是/etc/jupyterhub/jupyterhub-users.db

使用api添加用户后,会在数据库中生成记录,密码是用AES加密后存储的.

![image-20200521212626837](/img/JupyterHubAuth/7.png.webp.webp)

添加用户后,登陆成功.(**注意如果不需要白名单功能应该在配置文件中将白名单配置删掉,否则不在白名单中的用户还是登陆不了**)

![image-20200521212651326](/img/JupyterHubAuth/8.png.webp.webp)

~~邦邦pico沙雕小剧场更新了快去看~~