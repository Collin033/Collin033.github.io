---
title: "AcWing 154. 滑动窗口(单调队列)"
date: 2023-05-30 21:21:16
updated: 2023-05-30 21:23:18
tags:
  - "数据结构"
categories:
  - 学习笔记
toc: true
legacy_source: "2023/05/30/AcWing-154-滑动窗口-单调队列/index.html"
---
# 单调队列 —— 模板题 AcWing 154. 滑动窗口

<!-- more -->

```cpp
#include<bits/stdc++.h>

using namespace std;

const int N = 1e6 + 10;

int q[N];
int a[N];
int n, k;
int hh = 1, tt = 0;

signed main()
{
	cin >> n >> k;
	for (int i = 1; i <= n; i++)
		cin >> a[i];

	for (int i = 1; i <= n; i++)
	{
		while (hh<=tt && (i - k + 1)>q[hh])
			hh++;
		while (hh <= tt && a[i] <= a[q[tt]])
			tt--;
		q[++tt] = i;
		if (i >= k)
			cout << a[q[hh]] << ' ';
	}
	cout << '\n';

	hh = 1, tt = 0;
	for (int i = 1; i <= n; i++)
	{
		while (hh <= tt && (i - k + 1) > q[hh])
			hh++;
		while (hh <= tt && a[i] >= a[q[tt]])
			tt--;
		q[++tt] = i;
		if (i >= k)
			cout << a[q[hh]] << ' ';
	}
}
```
