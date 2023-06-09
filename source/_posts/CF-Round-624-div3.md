---
title: 'CF-Round-#624-div3'
date: 2020-02-29 17:41:18
categories: 练习赛记录
tags:
---
# CF Round #624 div.3

unrated,佛系比赛,不急不躁,不怒不争.

## A.Add Odd or Subtract Even

若 $a > b$ ,且$a-b$为偶数,直接减去$a-b$即可,答案为1.

若 $a > b$ ,且$a-b$为奇数,减去一个偶数再加上一个奇数,答案为2.

若 $a < b$ ,且$b-a$为偶数,加上一个奇数再加上一个奇数,答案为2.

若 $a > b$ ,且$b-a$为奇数,直接加上$b-a$即可,答案为1.



<!--more-->

## B. WeirdSort

对每个可以相互交换的连续区间排序,最后判断是否单调不减即可.

## C. Perform the Combo

记录在每个位置断连的次数,扫字符串的同时更新答案即可.

最后要加一次全连.

## D. Three Integers

刚开始写的$O(N\sqrt N)$算法：

枚举B,令A为离A最近的B的一个因数,C为离C最近的B的一个倍数,维护最优解即可.

找最近的因数只需枚举B的因数,与C最近的倍数一定是$(C/B)*B$,$(C/B-1)*B$,$(C/B+1)*B$之一.

把枚举上界设成15000可以卡过

题解是枚举A,然后枚举A的倍数作为B,然后确定C.

根据调和级数求和,可知该算法复杂度$O(nlogn)$

## E. Construct the Binary Tree

自然地想到可以从一条链的情况开始,每一次移动节点让答案减一.

不考虑非叶节点的移动一定不会让答案更坏,所以只考虑叶节点的移动.

因为移动是从下往上移动,所以如果先移动下方叶节点可能会在移动过程中被上方叶节点“挡住”,所以先考虑上方叶节点的移动.

因为初始是一条链,并且按从上到下编号依次增大的顺序排列,所以初始只有一个叶节点,编号为$N$.

用N个栈来维护第i层可以用来当作父节点的节点编号,如果一个节点为叶节点,那么他的编号将在对应的栈中出现两次,这样方便节点移动后更新栈的内容.使用栈来维护是因为这题没有对节点位置的要求,所以移动是只要是同一层的,选择哪个节点作为新的父节点都无所谓,并且入栈和出栈操作都是$O(1)$.

移动时注意不仅要更新新父节点的那一层的栈的状态,还要更新父节点和自己本身那一层的栈的状态.

当一个叶节点无法继续移动时,由于初始是一条从上往下编号递增的链,所以如果这棵树还有可以移动的叶节点,那么他的编号一定是上一个叶节点编号-1.并且如果一个新的叶节点已经无法移动了,这棵树的答案就已经到了最小,如果此时的答案还未满足题目要求,那么题目的要求就不可能满足.方便写代码,可以当指定的叶节点的编号变为0时输出NO.

另外,题解给出了一种简单的方法判断题目的要求是否能满足：节点数固定时,这棵树答案最大的形态是一条链,最小的形态是一颗满二叉树,因为可以通过一个节点的上下移动来在这两个形态之间变换,所以这两种形态的答案之间的所有答案都能满足,在这之外的都不能满足.

## F. Moving Points

因为速度是常量,时间没有限制,所以两个点要么距离越来越小,最后相遇,要么距离越来越大或不变,永远不会相遇.

不失一般性地,考虑$a_{i}$和$a_{j}$两点,其中$x_{i}>x_{j}$.若$v_{j} \leqslant v_{i}$,这两点就永远不会相遇,d(i,j)为初始时两点的距离,即$x_{i} - x_{j}$,否则两点一定会在某一时刻相遇,d(i,j)为0.

对于一个点$a_{i}$,需要找到所有初始坐标小于这个点并且速度小于等于这个点的点,来$a_{i}$计算对答案的贡献.

这是一个二维偏序问题,不同的是为了计算贡献,我们不仅仅要计算满足这个条件的点的个数,同时也要计算满足这个条件的点的坐标之和.离散化之后使用两个树状数组,分别维护这两个信息即可.