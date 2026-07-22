# Collin 博客源码

这是 <https://collin033.github.io/> 的 Hexo 源码工程。

## 常用命令

```powershell
npm install
npx hexo new post "article-slug"
npx hexo clean
npx hexo server
npx hexo generate
git add .
git commit -m "Add post: 文章标题"
git push origin source
```

- `source` 分支保存本目录中的 Markdown、配置和主题源码。
- 推送 `source` 分支后，GitHub Actions 会自动构建并发布到 GitHub Pages。
- `main` 分支保留最后一次手动部署的静态网页，不再作为日常写作目录。
- 请勿直接在 `main` 分支中编写新文章。
