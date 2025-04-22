# download_bbs_logs.py
#!/usr/bin/env python3
import os
import sys
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

# 1) 対象 URL のリスト
URLS = [
    "https://web.archive.org/web/20040730011817/http://www3.aaacafe.ne.jp/free/hakke/cdr.bbs?i1=20",
    "https://web.archive.org/web/20040611070603/http://www3.aaacafe.ne.jp/free/hakke/cdr.bbs"
]

OUTDIR = "HAKKE SYOUKAI CD-R BBS LOG"
os.makedirs(OUTDIR, exist_ok=True)

def scrape_posts(html: str):
    # <hr> ごとに分割
    parts = re.split(r'<hr[^>]*>', html, flags=re.IGNORECASE)
    posts = []
    for chunk in parts[1:]:
        # テキスト化（<br> → 改行）
        soup = BeautifulSoup(chunk, "html.parser")
        text = soup.get_text(separator="\n")
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if len(lines) < 4:
            continue
        name  = lines[0].split("：",1)[-1]
        title = lines[1].split("：",1)[-1]
        date  = lines[2].split("：",1)[-1]
        message = "\n".join(lines[3:])
        posts.append({
            "name": name,
            "title": title,
            "date": date,
            "message": message
        })
    return posts

def main():
    for url in URLS:
        print(f"Fetching {url} …")
        try:
            r = requests.get(url, timeout=15)
            # Archive.org の日本語ページは shift_jis の場合もあるので、文字化けがあれば適宜調整してください
            r.encoding = r.apparent_encoding
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            continue

        posts = scrape_posts(r.text)
        # query からページ番号を抽出（無ければ「1」とみなす）
        qp = parse_qs(urlparse(url).query)
        page = qp.get("i1", ["1"])[0]
        fname = f"cdr_page_{page}.txt"
        out_path = os.path.join(OUTDIR, fname)

        with open(out_path, "w", encoding="utf-8") as f:
            for p in posts:
                f.write(f"投稿者名: {p['name']}\n")
                f.write(f"投稿題名: {p['title']}\n")
                f.write(f"投稿日時: {p['date']}\n")
                f.write("投稿メッセージ:\n")
                f.write(p["message"] + "\n")
                f.write("\n" + "="*40 + "\n\n")
        print(f"→ Saved {out_path} ({len(posts)} posts)")

if __name__ == "__main__":
    main()
