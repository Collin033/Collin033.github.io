---
title: "C++中string类的一些常用操作"
date: 2023-08-29 17:10:43
updated: 2023-09-02 11:37:51
tags:
  - 算法
categories:
  - 学习笔记
toc: true
legacy_source: "2023/08/29/C-中string类的一些常用操作/index.html"
---
# strcpy函数

<!-- more -->

strcpy()将字符串复制到字符数组中

```text
char* strcpy( char* dest, const char* src );
```

## **cppreference中定义**

将 src 指向的字符串（包括空结束符）复制到第一个元素由 dest 指向的字符数组中。

如果 dest 数组不够大，则行为未定义。如果字符串重叠，则行为未定义。

## 例子

```cpp
#include<iostream>
#include<cstring>

using namespace std;


int main() 
{
	char charr1[20];
	char charr2[20] = "charr2";
	string str1 = "str1";
	strcpy_s(charr1, charr2);
	cout << charr1;
}
```

输出：

```text
charr2
```

# strcat函数

strcat（）函数将字符串附加到字符数组末尾

```text
char *strcat( char *dest, const char *src );
```

## **cppreference中定义**

将 src 指向的字符串副本追加到 dest 指向的字符串末尾。字符 src[0] 会替换 dest 末尾的空结束符。这样得到的字节字符串是空结束符。

如果目标数组的大小不足以同时容纳 src 和 dest 的内容以及空字符结束符，则会出现未定义的行为。

如果字符串重叠，则行为未定义。

## 例子

```cpp
#include<iostream>
#include<cstring>

using namespace std;


int main() 
{
	char charr1[20];
	char charr2[20] = "charr2";
	string str1 = "str1";
	strcpy_s(charr1, charr2);
	strcat_s(charr1, charr2);
	cout << charr1;
}
```

输出

```text
charr2charr2
```

# string类I/O

## cin.getline()

用于将一行输入读取到数组中：

```cpp
cin.getline(charr1,20);
```

我们熟知想输入charr1[20]，不能直接cin>>charr1来整行输入，所以对于字符数组的整行输入使用cin.getline(charr1,20);

这种句点表示法表明，函数getline是istream类的一个类方法。第一个参数是目标数组；第二个参数数组长度，getline()使用它来避免超越数组边界。

## gitline()

用于将一行输入读取到string对象中的代码:

```cpp
getline(cin,str)
```

这里没有使用句点表示法，这表明这个getline()不是类方法。它将cin作为参数，指出哪里去查找输入。另外，也没有指出字符串长度的参数，因为string对象将根据字符串长度自动调整自己的大小。

# strcmp函数

用于检测相等或排列顺序：

可以使用strcmp()来测试C风格字符串是否相等（排列顺序）。如果str1和str2相等，则下面的表达式为true：

```cpp
strcmp(str1,str2)==0
```

如果str1和str2不相等，则下面两个表达式都为true：

```cpp
strcmp(str1,str2)!=0
strcmp(str1,str2)
```

如果str1在str2前面，则下面的表达式为true：

```cpp
strcmp(str1,str2)<0
```

如果str1在str2后面，则下面的表达式为true：

```cpp
strcmp(str1,str2)>0
```
