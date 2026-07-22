---
title: "Acwing 187导弹防御系统"
date: 2023-05-29 11:18:19
updated: 2023-05-29 11:20:14
tags:
  - "题解"
categories:
  - 学习笔记
toc: true
legacy_source: "2023/05/29/Acwing-187导弹防御系统/index.html"
---
# LIS＋贪心

<!-- more -->

```cpp
#include <iostream>

using namespace std;

const int N = 1e2+5;

int a[N];
int f[N];
int up[N], down[N];
int n, ans;

void dfs(int u, int su, int sd)
{
    if (su + sd >= ans)
        return;
    if (u == n)
    {
        ans = su + sd;
        return;
    }

    int k = 0;
    while (k < su && up[k] >= a[u])
        k++;
    int t = up[k];
    up[k] = a[u];
    if (k < su)
        dfs(u + 1, su, sd);
    else
        dfs(u + 1, su + 1, sd);
    up[k] = t;

    k = 0;
    while (k < sd && down[k] <= a[u])
        k++;
    t = down[k];
    down[k] = a[u];
    if (k < sd)
        dfs(u + 1, su, sd);
    else
        dfs(u + 1, su, sd + 1);
    down[k] = t;
}

int main() 
{
    while (cin >> n && n)
    {
        ans = n;
        for (int i = 0; i < n; i++)
            cin >> a[i];
        dfs(0, 0, 0);
        cout << ans << '\n';
    }
    return 0;
}
```
