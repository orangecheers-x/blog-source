---
title: Raft为什么是对的? 以及一些小细节
date: 2023-04-05 00:39:31
tags:
---

![Untitled](/img/understand-raft/raft.png.webp.webp)

Understand the understandable consensus algorithm.

直接介绍Raft的每一部分干什么, 然后直接告诉你这样是对的未免太无趣了, 不如来更深层次的观察一下Raft.

这篇文章可以说是鸽了一年了, 一年前我在做6.824的lab的时候就觉得, 虽然我理解了raft每一步要干什么, 但是我不理解为什么要这样做, 或者如果不这样做会发生什么事情, 以及为什么这样做就可以保证强一致性.

这几天终于有时间重新来整理一下, 重新仔细读一下raft的论文.
<!--more-->

Raft确实是一个非常漂亮的算法, 看似没什么关联的松散的几部分互相结合就组成了一个无懈可击的共识算法, 并且每一部分都非常的形象容易理解. 论文也强调了这个算法相对于paxos的更好的可理解性, 虽然最后用学生考试成绩来证明这一点看得我有点乐.

Raft的很多操作其实是说不上道理的, 因为我认为这个算法更像是一个“构造性的算法”, 我们只需要关心构造出来之后正不正确, 而具体为什么要这样做, 其实是拿不出一个很能说服人的理由的. 就像几块互相依赖组成一个稳定结构的积木, 你无法说每一个积木为什么要这样摆放, 只能说现在这些积木处在一个稳定状态, 并且任何一个积木不这样摆放的话, 整个结构就会塌. 至于可不可以同时去修改这个结构的多个部分让他继续保持稳定, 如果有的话, 那这个可能就是一个新的共识算法了.

## Raft保证的五点

先来复习一下Raft的投票规则, 这个规则是保证正确性的核心:

voter只会投票给log至少跟自己up-to-date的candidate, 这个up-to-date的定义如下:

1. 最后一个log的term比自己的最后一个log的term要大, 或者
2. 这俩一样, 但是他log的长度比我的长.

首先, Raft保证了这五点, 这五点是理解正确性的核心.

1. Election Safety, 在一个term内, 最多只有一个leader.
2. Leader Append-Only, leader只会添加log, 不会删除或者覆盖自己的log.
3. Log Matching, 如果两个服务器的某一个log的index和term相同, 那他们之前的所有log都是相同的.
4. Leader Completeness, 如果一个log在一个term内被commit了, 那么所有比这个term大的leader都一定有这个log.
5. State Machine Safety, 如果一个log在一个index下被apply到了state machine, 那么其他所有服务器不会再这个index去apply其他的log.

分别简单证明一下:

1. 这是因为一个candidate必须获得绝对多数票才能成为leader, 而一个server在一个term内只会投一个票. 
2. 这个没啥要证明的. 所有有Leader的共识算法, Leader最终都会拥有所有需要被commit的log, 在一些算法中, 即使一个server没有全部被commit的log, 也有可能被选举为Leader. 但是这些算法在选举过程中, 或者之后的很短时间内都会拥有所有被commit的log. Raft不这样做, Raft保证只有拥有被commit的log的server才会被选举为Leader. 即, **数据只会从Leader流向Follower, Leader不会删除或者复写自己之前的log**.
3. 这个可以分成两个来讨论
    1. 如果某两个服务器某一个log的index和term相同, 那这两个log就一定相同(存储的命令).
        1. 这个是对的, 因为term相同就代表, 这条命令一定都是从这个term的唯一的leader那里拿来的. leader在同步log的时候, 一定会要求他们在同样的位置去记录这个log. 而这个leader把这个log同步给他们之后, 即使这个leader死了, 如果这个log还在, term没变, 那就一定是这个leader的衣钵, 如果这个index上的log被人改了, 那term一定会变.
    2. 如果两个服务器有两个log完全相同, 那他们之前的所有log都完全相同.
        1. 这个是由AppendEntries的操作来实现的: 一个Follower在收到AppendEntries请求的时候, 会检查请求中带有的prevLogIndex和prevLogTerm, 只有这两个跟自己的一样, 这个follower才会接受这些log. Follower接收这些log意味着至少从prevLogIndex开始到最后的log都跟Leader的一样. 然而prevLogIndex对应的那条log也是由AppendEntries得到的, 所以这其实是一个 **数学归纳法**, 结果就是每次成功AppendEntries之后Follower的所有log都跟Leader一样
            1. 上面说的是这两个服务器在这个log所在的term内都是Follower的情况, 即认为在这两个服务器上这个log一定都是通过AppendEntries得来的. 其实也有可能他们其中一个是Leader, 这个log是Leader自己放进去的, 不过这个Leader要想把log传递给其他人, 还是要进行AppendEntries, 所以不用单独考虑这种情况.
4. 论文的5.4.3用反证法证明了. 后面仔细说.
5. 跟着4一起就证明了.

### Leader Completeness的证明

使用反证法, 假设term T的时候commit了一个log, 但是在后来的某些term的leader中没有了, 假设第一个没有这个log的Term是U. U>T.

1. 这个log一定是在U被选为leader之前就没有了, 因为他被选为leader后就不会更改自己的log.
2. leaderT把这个log复制到了绝对多数的server上, U也必须要收到绝对多数的票才能成为Leader. 所以, 一定有一个server既收到了这个log, 又投票给了U. 这个voter是关键.
3. 这个voter一定是先收到包含这个log的AE才投票给U的, 因为如果他先收到了U的RequestVote, 他的term就会比T大, 会拒绝leaderT的AE.
4. 这个voter在U之前的所有term都保留着这个log(因为假设U是第一个没有这个log的term), 如果他是leader, 他不会删除自己的log, 如果他不是leader, 当时的leader也会有这个log(根据假设), 也不会把这个log删掉.
5. voter投票给了U, 说明U的log肯定要up-to-date voter的log. (up-to-date的定义文中给出了, 即最后一个log的term的比他大, 或者最后一个log的term一样但是log比他长). 这样以下两个必定有一个是矛盾的.
6. 如果他们的lastTermId一样, 那就说明U的log要比voter的长, 但是如果U的log要比voter的长, U就一定要有voter的这个log. 不可能出现一个term里不同的server的log还不一样的, 因为AE同步的时候都是保证顺序一样的. 要不然你就没有, 你要是有顺序肯定就一样.
7. 如果U的lastTermId比voter的要大, 那么一定要比T大, 因为voter的lastTermId至少是T. 那么, 给U创建最后一个log的leader W一定会有这条关键的log, 因为假设的是U才是第一个没有这个log的leader. 那因为U最后一个log是W给的, 根据Log Matching Property, U一定有那条关键的log.

证明很妙, 反证法上来给的条件“U是第一个没有这个log的server”很强, 证明中起到了关键的作用.

用这个也能证明State Machine Safety, 这个就很容易理解了.

## 关于Figure 8

![Untitled](/img/understand-raft/figure8.png.webp.webp)

这个图讲的是我是一个Leader, 即使一个log在我这看来确实有绝大多数server都有这个log, 但是这个logA是之前term产生的, 我还是不敢贸然commit这个logA. 因为我如果是刚上任, 根基不稳, 有些server还不知道改朝换代, 他们的term还没更新到我的term, 如果我和我让的几个人commit了, 然后我就驾崩了, 那些不知道改朝换代的人可能会成为跟我一样term或者甚至比我更小term的的candidate, 如果他们的term比现在这个logA的term大, 那那些刚刚commit这个logA的server会投票给他的, 他一上任如果没有这个logA就会把这个logA覆写掉的.

在c图中, S1刚上任, 先把2给复制到S3, 然后收到log 4. 这时候如果S1贸然commit这个黄色的log2, 并且就死了, d图中S5赢得选举后就会把log2给干掉, 造成不一致.

解决这个问题的就是新皇登基的时候不要上来就直接commit前朝的log, 要等自己的第一个log复制到大多数之后, 根基稳了之后, 连同着自己的第一个log一起再commit前朝的log. 

重点在于, 对于一个前朝的log, commit之后, 有这个log的人可能会投票给没有这个log的人, 因为这个log的term小. 但是对于现在的term的log, 把他传递给大多数server之后, 他们都不会投票给没有这个log的server, 就不会产生一个没有这个log的Leader. 

在没有把他传递给大多数的时候, 倒是有可能产生一个新Leader, 然后那个Leader的term更大, 并且收到了一些请求, 这样就能把复写之前term的log, 但是把他们传递给大多数之后, Leader就只会在这大多数里产生了.

## 关于AppendEntries的优化

一个在log不一致的时候优化AppendEntries次数的方法是server在拒绝AppendEntries的时候附加两个信息: 本机上冲突的log的term和本机上这个term的第一个log的index. 这样leader在收到这个RPC的返回的时候, 就把这个server的nextIndex直接设置为返回的index-1. 

对于AppendEntries的优化, 其实无论怎么做都不会影响他的正确性, 比如上面这个优化, 这样设置nextIndex可能是不必要的, 即nextIndex往前移太多了, 但也可能是还不够的, 即这样做下一次follower收到这个AE的时候还是找不到匹配项, 导致还需要再一次AE. 但是无论怎么样, 正确性都是可以保证的, 往前移太多了只是传递的log多了一点, 往前移少了也只是再来几次AE而已. 具体还是RPC的次数和传递的log量的trade-off.

论文里也提到, 他们在怀疑这样做的必要性, 因为出现不一致的情况不多, 但是每次RPC多两个参数是实打实的.

## 一些常见的简单问题

### 为什么不能是投票给最长的log, 也就是投票的时候只看log长度:

```nasm
S1 5 6 7
S2 5 8
S3 5 8
```

首先, 上述情况是完全可以发生的:

- 三个服务器都达成了5的共识.
- 网络问题, S1 term++=6,
- 网络好了, S2 S3投票给S1, S1变成leader, 收到请求6
- 还没发送AppendEntries, 网络又出问题, term++=7, 收到请求7
- 网络好了, S1变成leader, 这时候因为S1变成的leader, 所以肯定有人给他投票, 既然给他投票, 就一定知道这时候的term是7.
- S1寄了, S2term++=8, 当选leader, 收到请求8, 成功发送AppendEntries, commit了8.

这时候如果S1活了, 并且只看了log长度, 8就被覆盖掉了.

### 只选term最大的会出什么问题, 为什么要比较最后一个log的term?

term高可能只是自嗨行为, 一个server断网他能把自己的term刷的很大.

最后一个log的term就不是自嗨就能拿到的了, 他证明了你要么是这个term的leader, 要么至少在这个term内跟leader取得了联系, 说明至少这个term之前commit的log他都有.(Leader Completeness)