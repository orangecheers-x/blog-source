---
title: 梯度下降实现线性拟合矩阵推导及实现
date: 2021-02-11 09:58:27
categories: 机器学习
mathjax: true

tags: 
- 机器学习
- 数理


---



# 梯度下降实现线性拟合矩阵推导及实现

acm退役选手正在尝试新东西, 刚开的机器学习的坑.

实现线性拟合实际上还是用高中最小二乘的那种东西, 只不过不是通过计算直接求得拟合的参数, 而是用梯度下降的方法计算逼近参数.


用一个二维的直线拟合做例子. 高中就学过拟合实际上就是要找到一个直线  来尝试代表一组数据, 来达到预测的目的. 为了让预测的结果更加准确, 所以要让这个直线尽可能的逼近仅有的数据. 最小二乘法里衡量这个直线对这些仅有的数据的准确程度是用每个数据的真实值与估计值差的平方和, 也就是 $\Sigma_{i=1}^{n} (y_i-\hat{y_i})^2$, 这个值越小, 就说明这个直线对这些数据越准确. 

在这里给这些东西换个名字, 把 $h(x) = \theta_0 + \theta_1 x$ 叫做估计函数, 把 $J(\theta_0,\theta_1) = \frac{1}{2m}\Sigma_{i=1}^{n} (y_i-h(x_i))^2$ 叫做误差函数, 也就是loss.

梯度下降算法是很好理解的, 但是因为矩阵的运算我运用不是很灵活, 线代当时也是速成的, 所以刚开始我并没有用矩阵来实现, 后来想了一段时间才写出来了矩阵形式的梯度下降.

因为我之前没看过别人怎么实现的梯度下降, 所以下面的推导和实现方法的一些细节都是我自己决定的, 很可能与主流写法不一样, 麻烦许多, 这里先记录一下我自己的思考过程, 一会学习了别人的代码之后再来补充.

因为要用矩阵实现, 所以首先要把这些函数矩阵化. 对于多参数的估计函数, 我们要估计的参数可以写成一个向量 $[\theta_0, \theta_2,\dots, \theta_{n}]^T$, 先叫他参数向量, 记作 $\Theta$ . 因为有个常数项, 所以要估计的 $\theta$ 个数要比数据的参数多一个. 同时我们把训练数据写成向量形式, 因为训练数据的第一个要与参数向量的 $\theta_0$ 相乘, 所以这一位可以用一个 $1$ 来补上, 这样这个向量就可以写成 $[1,x_1,\dots,x_n]$,  这样估计函数就可以写成:
$$
h(X) = X \cdot \left[ \begin{matrix}  \theta_0 \\ \theta_1 \\ \theta_2 \\ \vdots \\ \theta_n  \end{matrix}  \right] = X \cdot \Theta
$$


同时我们可以把训练集写成矩阵形式:
$$
X = trainx = 
\left[ \begin{matrix}   
1 & x_1^{(1)} & x_2^{(1)} & \cdots & x_n^{(1)} \\
1 & x_1^{(2)} & x_2^{(2)} & \cdots & x_n^{(2)} \\
1 & x_1^{(3)} & x_2^{(3)} & \cdots & x_n^{(3)} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & x_1^{(m)} & x_2^{(m)} & \cdots & x_n^{(m)}

\end{matrix}    \right]
$$

$$
\space \space 
Y = trainy = \left[ \begin{matrix} y^{(1)} \\ y^{(2)} \\ y^{(3)} \\ \vdots \\ y^{(n)}  \end{matrix}  \right]
$$



这样我们计算 $h(trainx)$, 就可以惊奇的发现得到一个估计量组成的矩阵.

这是loss函数就可以写成
$$
J(\Theta) = \frac{1}{2m}||h(X) - Y||^2
$$
然后我们需要求 $J(\Theta)$ 对 $\Theta$ 的偏导, 这是一个标量对向量的偏导, 但是这个模长不是很好处理, 所以我们转化成向量对向量的偏导, 即把loss函数写为:
$$
J(\Theta) = \frac{1}{2m}(X\Theta - Y)^T (X\Theta - Y)
$$
求全微分:
$$
dJ = (Xd\Theta)^T(X\Theta-Y) + (X\Theta-Y)^T(Xd\Theta)
$$
整理得:
$$
dJ = 2(X\Theta - Y)^TX d\Theta
$$
可得:
$$
\frac{\partial J}{\partial \Theta} = 2X^T(X\Theta-Y)
$$
每次迭代让当前的 $\Theta := \Theta - \alpha\frac{\partial J}{\partial \Theta}$ 即可, 其中 $\alpha$ 为学习率.

这样, 梯度下降的所有过程都有了数学形式, 也就很好实现了.

第一次写觉得自己不可能写对, 跑一遍果然成了梯度上升算法, 查了半天没查出错, 把学习率调低就行了...我居然一遍写对了.

矩阵求导还是太难了, 很不熟练, 以后再多研究研究这些数学基础, 好喜欢这种用数学推导出的有用的东西.

附上代码:

```python
import numpy as np



datax = [0.50,0.75,1.00,1.25,1.50,1.75,1.75,2.00,2.25,2.50,2.75,3.00,3.25,3.50,4.00,4.25,4.50,4.75,5.00,5.50]
datay = [10,  22,  13,  43,  20,  22,  33,  50,  62,  48,  55,  75,  62,  73,  81,  76,  64,  82,  90,  93]
n = 1
m = len(datax)


trainx = np.zeros((m,n+1))
trainy = np.zeros((m,1))
def calch(t):
	return np.dot(trainx,t)

def calcJ(t):
	loss = calch(t) -trainy
	loss = np.dot(loss.T,loss)
	return loss/(2*m)

def calcJd(t):
	lossd = 0
	lossd = np.dot(trainx.T,np.dot(trainx,t) - trainy)

	return lossd/m



def init():
	global trainx
	global trainy
	for i in range(m):
		trainx[i] = [1,datax[i]]
		trainy[i] = datay[i]
	return 


learning_rate = 0.001
def gradient_descent(t):
	tt = t - learning_rate * calcJd(t)
	#print(t0,t1,calcJ(tt0,tt1))
	return tt

print(datax)
init()

t = np.zeros((2,1))
for i in range(1,100000):
	t = gradient_descent(t)
	print(t)

print(t)


```

###### 