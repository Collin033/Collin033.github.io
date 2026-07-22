---
title: 博客恢复与发布测试
date: 2026-07-22 23:55:00
updated: 2026-07-22 23:55:00
tags:
  - 测试
  - Hexo
categories:
  - 博客维护
toc: true
---

这是一篇用于验证博客恢复结果的测试文章。

<!-- more -->

## 本次测试内容

本次发布用于确认以下功能已经恢复：

- Hexo 源码可以正常安装和构建；
- Markdown 文章可以生成网页；
- 首页、归档、分类和标签页面可以正常访问；
- 中文标题、正文和链接可以正常显示；
- 代码块可以正常高亮；
- GitHub Pages 可以从 `main` 分支完成发布；
- 博客源码会保存在 `source` 分支，换电脑后可以重新克隆。

## Markdown 示例

下面是一段 C++ 测试代码：

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, restored blog!" << std::endl;
    return 0;
}
```

## 发布结果

如果你能在 <https://collin033.github.io/> 看到这篇文章，说明新的写作、备份和部署流程已经生效。

以后只需要在 `D:\blog-source\source\_posts` 中编写 Markdown，先本地预览，再把源码推送到 `source` 分支并部署即可。
