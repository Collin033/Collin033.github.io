# Collin 博客写作、预览与发布使用说明

> 博客地址：<https://collin033.github.io/>  
> GitHub 仓库：<https://github.com/Collin033/Collin033.github.io>  
> 本说明面向第一次接触 Git、Hexo 和 GitHub Pages 的用户。

## 1. 开始之前：先了解当前博客的状态

当前博客已经完成源码重建。平时应在 `D:\blog-source` 中写作和维护，`D:\blog` 只保留旧静态站点及恢复记录。

现有网站由以下工具生成：

- Hexo 7.3.0；
- Yilia 风格主题；
- GitHub Pages；
- `source` 分支保存 Markdown、配置、主题和依赖清单；
- GitHub Actions 在每次推送 `source` 分支后自动构建并发布网站。

旧电脑上的 Hexo 源码曾经丢失，但已经从生成后的网页完成恢复：

- 已恢复 25 篇旧文章；
- 已保留 98 个代码块；
- 已找回 2 张仍存在于网页或 Git 历史中的图片；
- 7 张从未上传到 Git 的旧电脑本地图片无法找回，文章中已用提示替代死链；
- 已建立 `source` 分支和自动部署工作流。

以后不要再从 HTML 反向恢复文章，Markdown 源稿会直接备份到 GitHub 的 `source` 分支。

### 1.1 两个目录分别做什么

以后建议使用两个目录：

| 目录 | 用途 | 是否直接编辑 |
| --- | --- | --- |
| `D:\blog-source` | Hexo 源码、Markdown 文章、主题和配置 | 是，平时主要使用这里 |
| `D:\blog` | 旧静态站点和恢复工具 | 否，只用于检查或紧急恢复 |

简单理解：

```text
在 blog-source 写 Markdown 并本地预览
                    ↓
推送到 GitHub 的 source 分支
                    ↓
GitHub Actions 自动运行 Hexo
                    ↓
GitHub Pages 发布到 collin033.github.io
```

## 2. 最重要的警告

旧文章迁移已经完成。今后日常发布**不需要执行 `hexo deploy`**，只需推送 `source` 分支，由 GitHub Actions 自动发布。

不要直接修改 `main` 分支，也不要手工上传 `public` 目录，否则可能绕过源码备份和自动检查。

现在正确的日常顺序是：

1. 拉取 `source` 分支；
2. 编写 Markdown；
3. 本地预览；
4. 提交并推送 `source` 分支；
5. 等待 GitHub Actions 自动发布；
6. 检查线上文章。

## 3. 第一次使用：重建 Hexo 源码工程

这一章只需要做一次。如果 `D:\blog-source` 已经建好并且可以执行 `npx hexo server`，以后可以直接跳到第 5 章。

### 3.1 检查基础软件

打开 PowerShell，依次运行：

```powershell
node --version
npm --version
git --version
```

只要三条命令都能显示版本号即可。当前电脑已经安装 Node.js、npm 和 Git。

### 3.2 配置 Git 用户信息

运行：

```powershell
git config --global user.name "Collin033"
git config --global user.email "3337934741@qq.com"
```

检查配置：

```powershell
git config --global user.name
git config --global user.email
```

### 3.3 代理设置

当前 Clash Verge 的 HTTP 代理端口是 `7897`。只有在无法连接 GitHub 或 npm 时才需要设置。

设置 Git 代理：

```powershell
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897
```

查看当前代理：

```powershell
git config --global --get http.proxy
git config --global --get https.proxy
```

如果以后不使用代理，可以删除：

```powershell
git config --global --unset http.proxy
git config --global --unset https.proxy
```

如果 npm 下载依赖失败，可以临时设置 npm 代理：

```powershell
npm config set proxy http://127.0.0.1:7897
npm config set https-proxy http://127.0.0.1:7897
```

不再需要时删除：

```powershell
npm config delete proxy
npm config delete https-proxy
```

### 3.4 给旧网站创建恢复标签

在第一次用新 Hexo 工程部署前，建议给当前版本创建一个永久标签：

```powershell
Set-Location D:\blog
git pull origin main
git tag legacy-site-2023 c8b2930
git push origin legacy-site-2023
```

如果提示标签已经存在，说明之前创建过，可以跳过。

这个标签相当于旧网站的恢复点。

### 3.5 安装 Hexo 命令行工具

```powershell
npm install --global hexo-cli
```

安装后检查：

```powershell
hexo version
```

如果系统提示找不到 `hexo`，后面的命令统一使用 `npx hexo` 即可。

### 3.6 创建源码目录

请注意：不要在 `D:\blog` 内执行 `hexo init`。

```powershell
Set-Location D:\
hexo init blog-source
Set-Location D:\blog-source
npm install
```

如果没有全局安装 Hexo，可以使用：

```powershell
Set-Location D:\
npx hexo-cli init blog-source
Set-Location D:\blog-source
npm install
```

完成后，目录大致如下：

```text
D:\blog-source
├─ node_modules
├─ scaffolds
├─ source
│  └─ _posts
├─ themes
├─ _config.yml
└─ package.json
```

### 3.7 安装部署插件和内容索引插件

在 `D:\blog-source` 中运行：

```powershell
npm install --save hexo-deployer-git
npm install --save hexo-generator-json-content
```

### 3.8 安装 Yilia 主题

旧网站使用的是 Yilia 风格主题。为了尽量接近旧网站，可以运行：

```powershell
Set-Location D:\blog-source
git clone https://github.com/litten/hexo-theme-yilia.git themes\yilia
```

Yilia 是较老的主题。如果它与新版 Node.js 或 Hexo 不兼容，可以改用维护中的新主题，但网站外观会发生变化。

### 3.9 配置 Hexo

用 VS Code 或记事本打开：

```text
D:\blog-source\_config.yml
```

找到对应配置并修改。不要在文件末尾重复添加已经存在的同名配置。

推荐的关键配置如下：

```yaml
title: Collin
subtitle: ''
description: ''
author: Collin
language: zh-CN
timezone: Asia/Shanghai

url: https://collin033.github.io
root: /
permalink: :year/:month/:day/:title/
permalink_defaults:
pretty_urls:
  trailing_index: true
  trailing_html: true

theme: yilia
post_asset_folder: true

deploy:
  type: git
  repo: https://github.com/Collin033/Collin033.github.io.git
  branch: main
```

YAML 文件对缩进很敏感：

- 使用空格，不要使用 Tab；
- `deploy:` 下方的三行要缩进两个空格；
- 英文冒号后要有一个空格；
- 标题中如果含有冒号，最好使用引号包住。

### 3.10 把源码保存到 source 分支

`source` 分支用于保存 Hexo 源码，也是自动部署工作流的触发分支。`main` 仅保留历史手动部署快照，不再作为日常发布入口。

在 `D:\blog-source` 中运行：

```powershell
git init
git branch -M source
git remote add origin https://github.com/Collin033/Collin033.github.io.git
git add .
git commit -m "Initialize Hexo source"
git push -u origin source
```

如果 `git remote add origin` 提示 `origin already exists`，改用：

```powershell
git remote set-url origin https://github.com/Collin033/Collin033.github.io.git
```

然后继续执行 `git add`、`git commit` 和 `git push`。

### 3.11 恢复旧文章

旧网站现有 25 篇文章，生成后的页面位于：

```text
D:\blog\2022\...
D:\blog\2023\...
```

需要把每篇 HTML 中的标题、日期、标签、正文和代码块恢复为 Markdown，并保存到：

```text
D:\blog-source\source\_posts
```

例如：

```text
D:\blog-source\source\_posts\线段树.md
```

恢复后的文章至少应包含：

```yaml
---
title: 线段树
date: 2023-09-08 16:02:33
tags:
  - 数据结构
categories:
  - 算法
---

这里是从旧网页恢复的正文……
```

这是一次性迁移工作。文章中有大量代码时，不建议直接从浏览器复制，因为代码块、公式和图片路径可能损坏。可以使用脚本或让 Codex 辅助批量恢复，然后逐篇检查。

在 25 篇旧文章全部恢复并验证之前，不要执行第 6.3 节的正式部署命令。

## 4. Markdown 写作基础

Markdown 是一种简单的纯文本格式。文章文件以 `.md` 结尾。

### 4.1 标题

```markdown
# 一级标题

## 二级标题

### 三级标题
```

文章顶部已经有文章标题，所以正文通常从 `## 二级标题` 开始。

### 4.2 普通段落和换行

```markdown
这是第一段。

这是第二段。两段之间需要保留一个空行。
```

### 4.3 加粗、斜体和删除线

```markdown
**加粗文字**

*斜体文字*

~~删除线~~
```

### 4.4 列表

```markdown
- 第一项
- 第二项
- 第三项

1. 第一步
2. 第二步
3. 第三步
```

### 4.5 链接

```markdown
[GitHub](https://github.com/)
```

### 4.6 行内代码和代码块

行内代码：

```markdown
使用 `npm install` 安装依赖。
```

C++ 代码块：

````markdown
```cpp
#include <iostream>

int main() {
    std::cout << "Hello, world!" << std::endl;
    return 0;
}
```
````

常见语言标记：

- C++：`cpp`
- Python：`python`
- Java：`java`
- JavaScript：`javascript`
- Shell：`bash`
- PowerShell：`powershell`
- 纯文本：`text`

### 4.7 引用

```markdown
> 这是一段引用或提示。
```

### 4.8 表格

```markdown
| 名称 | 说明 |
| --- | --- |
| Hexo | 静态博客生成器 |
| GitHub Pages | 网站托管服务 |
```

## 5. 日常使用：写一篇新文章

以下步骤假设 `D:\blog-source` 已经重建完成，旧文章也已经迁移。

### 5.1 进入源码目录并拉取最新版本

每次开始写作前，打开 PowerShell：

```powershell
Set-Location D:\blog-source
git pull origin source
```

这一步可以避免在不同电脑上修改时产生冲突。

### 5.2 创建文章

建议命令中的文件名使用简短英文，文章中文标题在文件中修改：

```powershell
npx hexo new post "my-first-post"
```

Hexo 会创建：

```text
D:\blog-source\source\_posts\my-first-post.md
```

当 `post_asset_folder: true` 时，通常还会创建同名图片目录：

```text
D:\blog-source\source\_posts\my-first-post\
```

### 5.3 编辑文章头部信息

打开 `my-first-post.md`，修改为：

```yaml
---
title: 我的第一篇新文章
date: 2026-07-21 20:00:00
updated: 2026-07-21 20:00:00
tags:
  - 随笔
  - Hexo
categories:
  - 博客
description: 这篇文章记录如何使用 Hexo 写博客。
---

这里开始写正文。
```

说明：

- `title`：网页显示的文章标题；
- `date`：首次发布时间；
- `updated`：最后更新时间；
- `tags`：标签，一篇文章可以有多个；
- `categories`：文章所属分类；
- `description`：文章摘要，可以省略。

### 5.4 添加图片

把图片复制到文章同名目录：

```text
D:\blog-source\source\_posts\my-first-post\demo.png
```

在 Markdown 中使用 Hexo 图片标签：

```markdown
{% asset_img demo.png 图片说明 %}
```

建议：

- 图片名使用英文、数字和短横线；
- 不要使用空格；
- 不要直接引用 `C:\Users\...` 之类的本地绝对路径；
- 发布前确认图片能在本地预览中显示。

### 5.5 本地预览

在 `D:\blog-source` 中运行：

```powershell
npx hexo clean
npx hexo generate
npx hexo server
```

看到类似下面的提示后：

```text
INFO  Hexo is running at http://localhost:4000/
```

在浏览器打开：

<http://localhost:4000/>

重点检查：

- 首页是否出现新文章；
- 标题、日期、分类和标签是否正确；
- 中文是否乱码；
- 图片是否能显示；
- 代码块是否完整；
- 文章链接是否正常；
- 25 篇旧文章是否仍然存在。

停止预览时，在 PowerShell 窗口按 `Ctrl+C`。

如果 4000 端口被占用，可以改用：

```powershell
npx hexo server --port 4001
```

然后打开 <http://localhost:4001/>。

## 6. 保存源码并发布到网站

### 6.1 再次检查改动

```powershell
Set-Location D:\blog-source
git status
```

确认只包含本次文章和相关图片、配置改动。

不要提交以下目录：

- `node_modules`；
- `public`；
- `.deploy_git`；
- 包含密码或访问令牌的文件。

Hexo 默认的 `.gitignore` 通常已经忽略这些目录。

### 6.2 先备份 Markdown 源码

```powershell
git add .
git commit -m "Add post: 我的第一篇新文章"
git push origin source
```

这一步把 Markdown 源稿保存到 GitHub 的 `source` 分支。以后即使换电脑，也能恢复源码。

### 6.3 通过 GitHub Actions 自动部署

第 6.2 节的 `git push origin source` 完成后，GitHub Actions 会自动执行：

```text
npm ci
npx hexo clean
npx hexo generate
上传 public 构建产物
部署到 GitHub Pages
```

命令含义：

可以在 GitHub 仓库的 `Actions` 页面查看 `Deploy Hexo site to Pages` 工作流。显示绿色对勾表示发布成功。

不要在日常流程中运行 `npx hexo deploy`，也不要手动强制推送 `main`。

### 6.4 检查线上结果

部署成功后等待约 30 秒到 3 分钟，然后访问：

<https://collin033.github.io/>

如果仍显示旧页面：

1. 按 `Ctrl+F5` 强制刷新；
2. 等待一两分钟；
3. 打开 GitHub 仓库的 `Actions` 页面；
4. 确认 `Deploy Hexo site to Pages` 工作流为绿色对勾；
5. 检查仓库的 `Settings` → `Pages`，发布来源应为 `GitHub Actions`。

## 7. 修改、删除和暂存文章

### 7.1 修改已发布文章

1. 打开 `D:\blog-source\source\_posts` 中对应的 `.md` 文件；
2. 修改正文；
3. 更新文章头部的 `updated` 时间；
4. 本地预览；
5. 提交 `source` 分支；
6. 重新生成并部署。

示例：

```powershell
Set-Location D:\blog-source
npx hexo clean
npx hexo server
```

确认无误后：

```powershell
git add .
git commit -m "Update post: 文章标题"
git push origin source
```

推送后等待 GitHub Actions 自动发布。

### 7.2 删除文章

删除对应的 Markdown 文件和同名图片目录，例如：

```powershell
Remove-Item -LiteralPath "D:\blog-source\source\_posts\my-first-post.md"
Remove-Item -LiteralPath "D:\blog-source\source\_posts\my-first-post" -Recurse
```

删除前请确认路径正确。然后执行本地预览、提交源码和部署流程。

### 7.3 使用草稿

创建草稿：

```powershell
Set-Location D:\blog-source
npx hexo new draft "future-post"
```

草稿位于：

```text
D:\blog-source\source\_drafts
```

预览草稿：

```powershell
npx hexo server --draft
```

草稿写完后转为正式文章：

```powershell
npx hexo publish "future-post"
```

## 8. 换电脑后如何恢复

因为源码已经保存在 `source` 分支，所以换电脑后不需要从网页反向恢复。

安装 Node.js 和 Git 后运行：

```powershell
Set-Location D:\
git clone --branch source https://github.com/Collin033/Collin033.github.io.git blog-source
Set-Location D:\blog-source
npm install
```

然后本地预览：

```powershell
npx hexo clean
npx hexo server
```

最终静态网站由 GitHub Actions 作为 Pages 构建产物保存，通常不需要克隆 `main` 分支。

## 9. 常见问题排查

### 9.1 `hexo` 不是内部或外部命令

直接改用：

```powershell
npx hexo version
```

或者重新安装：

```powershell
npm install --global hexo-cli
```

### 9.2 `npm install` 下载失败

先确认 Clash Verge 已启动，再设置 npm 代理：

```powershell
npm config set proxy http://127.0.0.1:7897
npm config set https-proxy http://127.0.0.1:7897
npm install
```

### 9.3 GitHub 推送连接到 `127.0.0.1:7890` 失败

说明 Git 仍使用旧代理端口。修改为当前端口：

```powershell
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897
```

### 9.4 `Authentication failed` 或令牌失效

Windows 通常会弹出 Git Credential Manager 登录窗口。使用 `Collin033` 的 GitHub 账号重新授权。

也可以先执行一次：

```powershell
git push origin source
```

然后按照浏览器提示登录。

不要把 Personal Access Token 写入 Markdown、配置文件或聊天记录。

### 9.5 本地页面中文乱码

检查：

- Markdown 文件是否保存为 UTF-8；
- `_config.yml` 中 `language` 是否为 `zh-CN`；
- 从旧 HTML 恢复文章时是否使用了错误编码；
- 文件名和正文是否在编辑器中已经乱码。

乱码一旦保存并提交，很难自动判断原文，因此发布前一定要本地检查。

### 9.6 YAML 配置报错

常见原因：

- 冒号后缺少空格；
- 缩进不一致；
- 使用 Tab；
- 标题中含冒号但没有加引号；
- 同一个配置项重复出现。

例如下面是错误写法：

```yaml
title:我的文章
```

正确写法：

```yaml
title: 我的文章
```

### 9.7 部署后旧文章不见了

立即停止继续部署。这通常表示旧文章没有完整恢复到 `source\_posts`。

不要随意强制推送或删除 Git 历史。当前旧站点可以通过 `legacy-site-2023` 标签或 Git 历史恢复，建议先检查生成目录和文章迁移情况。

### 9.8 图片本地正常、线上不显示

检查：

- 图片是否真正放在文章同名目录；
- 图片文件是否已被 `git add`；
- 文件名大小写是否完全一致；
- 是否误用了本地绝对路径；
- 图片扩展名是否正确。

GitHub Pages 区分文件名大小写，例如 `Demo.png` 和 `demo.png` 会被视为不同文件。

## 10. 每次发文章的最简清单

当源码工程完全恢复后，每次只需要记住下面的流程：

```powershell
# 1. 进入源码目录并同步
Set-Location D:\blog-source
git pull origin source

# 2. 创建文章
npx hexo new post "article-slug"

# 3. 编辑 source\_posts\article-slug.md

# 4. 本地预览
npx hexo clean
npx hexo server

# 5. 保存 Markdown 源码
git add .
git commit -m "Add post: 文章标题"
git push origin source

# 6. git push 完成后，等待 GitHub Actions 自动发布
```

发布完成后访问：

<https://collin033.github.io/>

## 11. 推荐的使用习惯

1. 永远在 `D:\blog-source` 写文章，不要直接编辑 `D:\blog` 中生成的 HTML。
2. 每次写作前先执行 `git pull origin source`。
3. 每次部署前先本地预览。
4. 推送 `source` 分支后等待 GitHub Actions 自动部署，不要手动强推 `main`。
5. 图片和文章一起提交。
6. 不要提交密码、Cookie、令牌、私钥和个人隐私文件。
7. 不要删除 `.git` 目录。
8. 不要使用 `git push --force`，除非已经明确知道要恢复哪个版本。
9. `node_modules` 可以重新安装，不需要备份。
10. 定期确认 GitHub 的 `source` 分支中确实能看到 Markdown 源稿。

---

旧站点迁移已经完成。今后的日常发文只需要第 5、6 章中的几个命令。
