---
title: nlogn最长不上升子序列
date: 2018-04-05 22:21:49
catagories: 算法
tags:
- 基础算法
- 二分
- dp
---

# nlogn的最长不上升子序列

nlogn的最长不上升子序列虽然不难,也很常用,但是很容易打错,~~一不注意就把变量名打错了~~.

主要思想是用二分优化"寻找a[j]>=a[i]中f[j]最大的j"

```cpp
for(int i = 1;i <= N;i++)
{
    int maxx = -INF;
    for(int j = 1;j < i;j++)//优化这个循环
    {
        if(a[j] >= a[i])maxx = max(maxx,f[j]);
    }
    f[i] = (maxx == INF)?1:maxx+1;
}
```

既然使用二分,就要寻找一个有单调性的东西.

<!--more-->

在原有的基础上新开一个数组temp[],temp[i]表示f[j] = i的最大的a[j],翻译成人话就是f值等于i的最大的数是多少.

因为是最长不上升子序列,所以在f值相同时,这个数越大越有价值.

可以发现这个temp是有单调性的,严格证明我不会,可以用反证法瞎搞搞证出来.

因为要找到一个最大的i,即f值,所以二分是要注意下一个小细节.

假如按照temp[1]到temp[N]这样从左到右写出来,我们要做的就是找出满足temp[k] >= a[nown]的最右边的值

所以在二分时,如果当前二分的中点值等于a[nown],应当把左区间端点的值设置为mid,而不是mid+1,防止丢失解.

如果二分中点小于a[nown],可以大胆的将右端点设为mid-1

二分部分程序:

```cpp
int l,r;
while(l + 1 <= r)
{
    int mid = ((l+r)>>1);
    if(temp[l] >= a[nown])
    {
        l = mid;
    }else{
        r = mid-1;
    }
}
if(l < r && temp[r] >= a[nown])l = r;
temp[l+1] = maxx(temp[l+1],a[nown]);
```

这样就实现了去掉f并优化时间复杂度到O(nlogn).

2018.4.5 22:20