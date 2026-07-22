---
title: "Acwing1010"
date: 2023-05-28 23:18:27
updated: 2023-05-28 23:21:08
tags:
  - "题解"
categories:
  - 学习笔记
toc: true
legacy_source: "2023/05/28/Acwing1010/index.html"
---
# AcWing1010_拦截导弹(LIS)

<!-- more -->

```cpp
#include <iostream>

using namespace std;
#define endl "\n"

const int N = 1e05;

int a[N];
int f[N];
int q[N], g[N];
int n = 0;

int main() {
    while (cin >> a[n])
        n++;

    int lon = 0;
    for (int i = 0; i < n; i++)
    {
        f[i] = 1;
        for (int j = 0; j < i; j++)
        {
            if (a[j] > a[i])
            {
                f[i] = max(f[i], f[j] + 1);
                lon = max(f[i], lon);
            }
        }
    }

    cout << lon << endl;

    int cnt = 0;
    for (int i = 0; i < n; i++)
    {
        int k = 0;
        while (k<cnt && g[k] < a[i] )
            k++;
        g[k] = a[i];
        if (k >= cnt)
            cnt++;
    }
    cout << cnt << endl;
    return 0;
}
```
