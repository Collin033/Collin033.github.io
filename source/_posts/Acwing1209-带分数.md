---
title: "Acwing1209. 带分数"
date: 2023-04-07 15:29:53
updated: 2023-04-07 15:48:18
tags:
  - 算法
categories:
  - 学习笔记
toc: true
legacy_source: "2023/04/07/Acwing1209-带分数/index.html"
---
#### 题目

<!-- more -->

100 可以表示为带分数的形式：100=3+69258/714

还可以表示为：100=82+3546/197

注意特征：带分数中，数字 1∼9 分别出现且只出现一次（不包含 0）。

类似这样的带分数，100 有 11 种表示法。

#### 输入格式

一个正整数。

#### 输出格式

输出输入数字用数码 1∼9 不重复不遗漏地组成带分数表示的全部种数。

#### 数据范围

1≤N<1e6

#### 输入样例1：

```text
100
```

#### 输出样例1：

```text
11
```

#### 输入样例2：

```text
105
```

#### 输出样例2：

```text
6
```

#### 题解

n=a+b/c 可以表示为nc=ac+b,既对于该题可以dfs a跟c的值，再用nc-ac求b的值。

#### 代码

```cpp
#include<bits/stdc++.h>
#define int long long

using namespace std;

int n,ans=0;

int st[105],stt[105];

bool check(int a,int c)
{
    int b=n*c-a*c;
    if(!a || !b || !c)
        return false;
    for(int i=1;i<=9;i++)
    {
        stt[i]=st[i];
    }
    while(b)
    {
        int tmp=b%10;
        if(stt[tmp]!=0 || !tmp)
            return false;
        stt[tmp]=1;
        b/=10;
    }
    for(int i=1;i<=9;i++)
    {
        if(stt[i]==0)
            return false;
    }
    return true;
}

void dfs_c(int u,int a,int c)
{
    if(u>9)
        return ;
    if(check(a,c)==true)
        ans++;
    for(int i=1;i<=9;i++)
    {
        if(st[i]==0)
        {
            st[i]=1;
            dfs_c(u+1,a,c*10+i);
            st[i]=0;
        }
    }
}

void dfs_a(int u,int a)
{
    if(a>=n)
        return ;
    if(a)
        dfs_c(u,a,0);
    for(int i=1;i<=9;i++)
    {
        if(st[i]==0)
        {
            st[i]=1;
            dfs_a(u+1,a*10+i);
            st[i]=0;
        }
    }
}

signed main()
{
    cin>>n;
    dfs_a(0,0);
    cout<<ans<<endl;
    return 0;
}
```
