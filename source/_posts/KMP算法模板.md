---
title: "KMP算法模板"
date: 2023-04-24 21:23:35
updated: 2023-04-24 21:32:48
tags:
  - 算法
categories:
  - 学习笔记
toc: true
legacy_source: "2023/04/24/KMP算法模板/index.html"
---
## 模板题 AcWing 831. KMP字符串

<!-- more -->

```cpp
#include<bits/stdc++.h>

using namespace std;

const int N = 1e6 + 5;


int n, m;
char p[N], s[N];

int ne[N];


int main()
{
	cin >> n >> p+1 >> m >> s+1;
	for (int i = 2,j=0; i <= n; i++)
	{
		while (j && p[i] != p[j + 1])
			j = ne[j];
		if (p[i] == p[j + 1])
			j++;
		ne[i] = j;
	}

	for (int i = 1, j = 0; i <= m; i++)
	{
		while (j && p[j + 1] != s[i])
			j = ne[j];
		if (s[i] == p[j + 1])
			j++;
		if (j == n)
		{
			cout << i - j<<' ';
			j = ne[j];

		}
	}
	return 0;
}
```
