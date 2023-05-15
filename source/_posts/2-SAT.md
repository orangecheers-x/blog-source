---
title: 2-SAT问题
date: 2020-03-11 01:22:19
categories: 算法
tags: 
- 图论
- 强连通分量
- 2-SAT
---

有N个变量,每个变量都能取T或F，需要满足M个条件: $X_{i} = T$ or $X_{j} = F$

要给每个变量赋值,满足所有条件.

构造有向图G,每个$X_{i}$拆成两个点2i和2i+1, 分别表示$X_{i}$取T或者F. 每个变量选其中的一个进行标记,标记了节点2i表示$X_{i}=T$,标记2i+1表示$X_{i}=F$.

对于每个条件,如$X_{i} = T$ or $X_{j} = F$,可以从表示点i为F的节点到表示点j为F的节点连一条边,表示如果点i为F,那么点j一定是F. 同时,还要从表示点j为T的点向表示点i为T的点连一条边.

### DFS方法

<!--more-->

逐个考虑每个未赋值的变量$X_{i}$,先假定为真,标记结点2i,然后沿着边标记所有可以标记的点,并记录这个过程中标记了的点,方便更换这个变量的赋值.如果发现某个变量的两个点都被标记了,说明这个变量不可能为真,就要按照刚刚的记录,将标记去掉,**清空记录**,标记节点2i+1,重复过程.**注意在假定为真的dfs之前也要清空记录**. 如果这时候还不行,这个问题就无解,即使改变之前变量的值也没用.

**luogu P4782 模板**

```cpp
#include <iostream>
#include <cstdio>
#include <cstring>
#include <vector>
#include <set>
#include <algorithm>
#define MAXN 1000005
#define INF 0x3f3f3f3f
#define lovelive long long int
#define osu(a,b,i) for(int i = (a);i <= (b);i++)
#define nso(a,b,i) for(int i = (a);i >= (b);i--)
inline int homax(int a,int b)
{
    if(a > b) return a;
    return b;
}
inline int homin(int a,int b)
{
    if(a > b) return b;
    return a;
}
using namespace std;
bool vis[MAXN*2];
vector<int> sv;
vector<int> G[MAXN*2];
bool dfs(int x)
{
    if(vis[x^1]) return false;
    if(vis[x]) return true;
    vis[x] = true;
    sv.push_back(x);
    for(auto to : G[x])
    {
        if(!dfs(to)) return false;
    }
    return true;
}
void addcons(int x,int vx,int y,int vy)
{
    G[(x << 1 | vx)^1].push_back(y << 1 | vy);
    G[(y << 1 | vy)^1].push_back(x << 1 | vx);
    return ;
}
int N,M;
bool sat2()
{
    osu(1,N,i)
    {
        if(vis[i << 1] || vis[i << 1 | 1]) continue;
        sv.clear();//假定为真的dfs之前清空记录
        if(!dfs(i << 1))
        {
            while(!sv.empty()) vis[sv.back()] = false, sv.pop_back();
            if(!dfs(i << 1 | 1))
            {
                return false;
            }
        }
    }
    return true;
}
int main()
{
    scanf("%d%d",&N,&M);
    osu(1,M,i)
    {
        int a,b,c,d;
        scanf("%d%d%d%d",&a,&b,&c,&d);
        addcons(a,b,c,d);
    }
    if(sat2())
    {
        cout << "POSSIBLE" << endl;
        osu(1,N,i)
        {
            if(vis[i << 1])
            {
                cout << 0 << " ";
            }else{
                cout << 1 << " ";
            }
        }
    }else{
        cout << "IMPOSSIBLE" << endl;
    }
    return 0;
}
```

复杂度$O(n(n+m))$

这个方法还可以保证答案的字典序,对于大部分的题目已经够用了.

### SCC方法

用Tarjan对每个SCC缩点,如果某个变量对应的两个节点在一个SCC中,则问题无解,否则一定有解.

如果一个变量的T结点所在SCC的拓扑序大于F结点的,那么就给这个变量赋T,否则赋F,用这个方法一定给所有有解的情况构造出答案.

复杂度$O(n+m)$,达到了输入下限.但由于无法保证解的字典序,一般只用于判断是否有解.

## 例题

### Now or later, UVA-1146

https://vjudge.net/problem/UVA-1146

#### 题目大意

每个飞机都有2个降落时间,早降落时间和晚降落时间,每个飞机都可以选择早或者晚降落,每个飞机的早晚降落时间是固定的,但是可以和其他飞机不同.

你可以任意指定每个飞机的早晚降落情况,使每个飞机真正的降落时间之间的间隔最大.

#### 解法

二分答案T,用$A[x][0/1]$代表第x个飞机的早降落时间和晚降落时间,如果$|A[x_{1}][y_{1}] - A[x_{2}][y_{2}]| < P$, 说明$A[x_{1}][y_{1}]$与$A[x_{2}][y_{2}]$不能同时选,即$!(A[x_{1}][y_{1}] \& A[x_{2}][y_{2}])$, 由狄摩根定律,这个条件等价于$A[x_{1}][!y_{1}]$ | $A[x_{2}][!y_{2}]$,这就转化为了2-SAT判断有解性问题.

https://vjudge.net/solution/24649633

```cpp
#include <iostream>
#include <cstdio>
#include <cstring>
#include <vector>
#include <set>
#include <algorithm>
#define MAXN 2005
#define INF 0x3f3f3f3f
#define lovelive long long int
#define osu(a,b,i) for(int i = (a);i <= (b);i++)
#define nso(a,b,i) for(int i = (a);i >= (b);i--)
inline int homax(int a,int b)
{
    if(a > b) return a;
    return b;
}
inline int homin(int a,int b)
{
    if(a > b) return b;
    return a;
}
inline int hoabs(int a)
{
    if(a > 0) return a;
    return -a;
}
using namespace std;
struct twosat{
    int N;
    bool vis[MAXN*2];
    vector<int> sv;
    vector<int> G[MAXN*2];
    bool dfs(int x)
    {
        if(vis[x^1]) return false;
        if(vis[x]) return true;
        vis[x] = true;
        sv.push_back(x);
        for(auto to : G[x])
        {
            if(!dfs(to)) return false;
        }
        return true;
    }
    void init()
    {
        memset(vis,false,sizeof vis);
        sv.clear();
        for(auto &v : G) v.clear();
        return ;
    }
    void addcons(int x,int vx,int y,int vy)
    {
        G[(x << 1 | vx)^1].push_back(y << 1 | vy);
        G[(y << 1 | vy)^1].push_back(x << 1 | vx);
        return ;
    }
    bool sat2()
    {
        osu(1,N,i)
        {
            if(vis[i << 1] || vis[i << 1 | 1]) continue;
            sv.clear();
            if(!dfs(i << 1))
            {
                while(!sv.empty()) vis[sv.back()] = false, sv.pop_back();
                if(!dfs(i << 1 | 1))
                {
                    return false;
                }
            }
        }
        return true;
    }
}ts;
int N;
int tb[MAXN][2];
bool judge(int x)
{
    ts.init();
    ts.N = N;
    osu(1,N,i) osu(i+1,N,j)
    {
        osu(0,1,k) osu(0,1,l)
        {
            if(hoabs(tb[i][k] - tb[j][l]) < x)
            {
                ts.addcons(i,k^1,j,l^1);
            }
        }
    }
    return ts.sat2();
}
int solve()
{
    int l = 0,r = 2e7;
    while(l < r)
    {
        int mid = ((l + r + 1) >> 1);
        if(judge(mid))
        {
            l = mid;
        }else{
            r = mid-1;
        }
    }
    return l;
}

int main()
{
    
    while(~scanf("%d",&N))
    {
        memset(tb,0,sizeof tb);
        osu(1,N,i)
        {
            osu(0,1,j)
            {
                scanf("%d",&tb[i][j]);
            }
        }
        cout << solve() << endl;
    }
}
```

(明明UVALive-3211和UVA-1146是一样的题,但是在vjudge上一样的代码只能过UVA-1146...刚开始交UVALive-3211怎么都过不去,换了个一模一样的题交就过了,魔幻)