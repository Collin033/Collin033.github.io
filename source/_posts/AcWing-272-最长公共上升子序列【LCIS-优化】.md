---
title: "AcWing 272. 最长公共上升子序列【LCIS + 优化】"
date: 2023-05-29 20:11:13
updated: 2023-05-29 20:16:50
tags:
  - "题解"
categories:
  - 学习笔记
toc: true
legacy_source: "2023/05/29/AcWing-272-最长公共上升子序列【LCIS-优化】/index.html"
---
# [AcWing 272]([272. 最长公共上升子序列 - AcWing题库](https://www.acwing.com/problem/content/274/))

<!-- more -->

## 朴素版

```cpp
#include <iostream>

using namespace std;

const int N = 3010;

int n;
int a[N], b[N];
int f[N][N];

int main()
{
    //input
    cin >> n;
    for (int i = 1; i <= n; ++ i) cin >> a[i];
    for (int i = 1; i <= n; ++ i) cin >> b[i];

    //dp
    for (int i = 1; i <= n; ++ i)
    {
        for (int j = 1; j <= n; ++ j)
        {
            f[i][j] = f[i - 1][j];
            if (a[i] == b[j])
            {
                for (int k = 0; k < j; ++ k)
                {
                    if (b[j] > b[k])
                    {
                        f[i][j] = max(f[i][j], f[i - 1][k] + 1);
                    }
                }
            }
        }
    }

    //find result
    int res = 0;
    for (int i = 0; i <= n; ++ i) res = max(res, f[n][i]);
    cout << res << endl;

    return 0;
}
```

## 优化

```cpp
#include<bits/stdc++.h>


using namespace std;

const int N=3e3+10;

int a[N],b[N];
int f[N][N];

signed main()
{
    int n;
    cin>>n;
    for(int i=1;i<=n;i++)
        cin>>a[i];
    for(int i=1;i<=n;i++)
        cin>>b[i];
        
    for(int i=1;i<=n;i++)
    {
        int maxv=1;
        
        for(int j=1;j<=n;j++)
        {
            f[i][j]=f[i-1][j];
            if(a[i]==b[j])
                f[i][j]=max(f[i][j],maxv);
            if(b[j]<a[i])
                maxv=max(maxv,f[i][j]+1);
        }
    }
    
    int res=0;
    for(int i=1;i<=n;i++)
        res=max(res,f[n][i]);
    cout<<res<<endl;
}
```

## 参考

[题解](https://www.acwing.com/solution/content/52304/)
