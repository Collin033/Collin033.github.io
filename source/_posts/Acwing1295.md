---
title: "Acwing1295"
date: 2023-04-04 23:51:31
updated: 2023-04-06 23:06:45
tags:
  - 算法
categories:
  - 学习笔记
toc: true
legacy_source: "2023/04/04/Acwing1295/index.html"
---
# 前置知识

<!-- more -->

## 算数基本定理

$$
N=P_1^{d_1}P_2^{d_2}……P_k^{d_k}，其中P_i为质数，d_k>0
$$

## 素数筛

```cpp
int prime[maxn],cnt=0;//prime[i]记录质数，cnt记录质数个数
bool p[maxn];//某个数是否为质数
void eulerSieve(int n)
{
	for(int i=2;i<=n;i++)
	{
		if(p[i]==false)
		{
			prime[++cnt]=i;
		}
		for(int j=1;j<=cnt && i*prime[j]<=n;j++)
		{
			p[i*prime[j]]=true;
			if(i%prime[j]==0)
				break;
		}
	}
}
```

## 多重集组合数

可以理解为是高中数学排列组合的一个应用，应用场合是在排列是去除重复相同项排列的情况
公式为 n!(总排列的数目)/n1!n2!n3!….(每种组合内部的排列数)

# 题目详细

输入正整数 X，求 X 的大于1的因子组成的满足任意前一项都能整除后一项的严格递增序列的最大长度，以及满足最大长度的序列的个数。

## 输入格式

输入包含多组数据，每组数据占一行，包含一个正整数表示 X。

## 输出格式

对于每组数据，输出序列的最大长度以及满足最大长度的序列的个数。

每个结果占一行。

## 数据范围

$$
1≤X≤2^{20}
$$

## 输入样例：

```text
2
3
4
10
100
```

## 输出样例：

```text
1 1
1 1
2 1
2 2
4 6
```

## 代码详细

```cpp
#include<bits/stdc++.h>
#define int long long

using namespace std;

const int N = (1 << 20) + 10;

bool isPrime[N];
int prime[N],minp[N],sum[N];
int cnt,x;

void search_prime()
{
    for(int i=2;i<N;i++)
    {
        if(!isPrime[i])
        {
            minp[i]=i;
            prime[++cnt]=i;
        }
        for(int j=1;j<=cnt && i*prime[j]<N;j++)
        {
            isPrime[i*prime[j]]=true;
            minp[i*prime[j]]=prime[j];
            if(i%prime[j]==0)
                break;
        }
    }
}

signed main()
{
    search_prime();
    while(scanf("%d", &x) != -1)
    {
        int tot=0,res=1,k=0;
        while(x>1)
        {
            int p=minp[x];
            sum[k]=0;
            while(x%p==0)
            {
                x/=p;
                sum[k]++;
                tot++;
            }
            k++;
        }
        for(int i=1;i<=tot;i++)
            res*=i;
         for (int i = 0; i < k; i ++ )
            for (int j = 1; j <= sum[i]; j ++ )
                res /= j;
        printf("%d %lld\n", tot, res);
    }
}
```
