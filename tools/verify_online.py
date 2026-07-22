"""Verify the published GitHub Pages site after deployment."""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import ProxyHandler, Request, build_opener


BASE_URL = "https://collin033.github.io/"
PROXY_URL = "http://127.0.0.1:7897"
PUBLIC_DIR = Path(__file__).resolve().parents[1] / "public"


opener = build_opener(ProxyHandler({"http": PROXY_URL, "https": PROXY_URL}))


def fetch(path: str) -> tuple[int, bytes]:
    separator = "&" if "?" in path else "?"
    url = BASE_URL + quote(path, safe="/%?=&") + separator + f"qa={int(time.time())}"
    request = Request(url, headers={"Cache-Control": "no-cache", "User-Agent": "blog-verifier"})
    try:
        with opener.open(request, timeout=30) as response:
            return response.status, response.read()
    except Exception as error:
        status = getattr(error, "code", 0)
        body = error.read() if hasattr(error, "read") else str(error).encode()
        return status, body


def main() -> None:
    local_posts = json.loads((PUBLIC_DIR / "content.json").read_text(encoding="utf-8"))
    failures: list[dict[str, object]] = []

    for post in local_posts:
        status, body = fetch(post["path"])
        text = body.decode("utf-8", errors="replace")
        valid = (
            status == 200
            and post["title"] in text
            and "/false" not in text
            and "涓婚〉" not in text
            and "闅忕瑪" not in text
            and "褰掓。" not in text
        )
        if not valid:
            failures.append({"title": post["title"], "status": status, "bytes": len(body)})

    checks = {
        "home": ("", "博客恢复与发布测试"),
        "test": ("2026/07/22/blog-recovery-test/", "Hello, restored blog!"),
        "guide": ("BLOG_GUIDE.md", "GitHub Actions"),
        "archive": ("archives/", "博客恢复与发布测试"),
        "tag": ("tags/测试/", "博客恢复与发布测试"),
        "category": ("categories/博客维护/", "博客恢复与发布测试"),
        "image": ("2023/04/03/最短路/image-20230402203922876.png", None),
        "missing_note": ("2023/04/04/最小生成树/", "历史图片缺失"),
    }

    check_results: dict[str, dict[str, object]] = {}
    for name, (path, expected) in checks.items():
        status, body = fetch(path)
        text = body.decode("utf-8", errors="replace")
        check_results[name] = {
            "status": status,
            "bytes": len(body),
            "content": expected is None or expected in text,
        }

    status, body = fetch("content.json")
    online_posts = json.loads(body.decode("utf-8")) if status == 200 else []
    result = {
        "posts_checked": len(local_posts),
        "post_failures": failures,
        "online_post_count": len(online_posts),
        "checks": check_results,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    checks_ok = all(
        item["status"] == 200 and item["content"] for item in check_results.values()
    )
    if failures or len(online_posts) != len(local_posts) or not checks_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
