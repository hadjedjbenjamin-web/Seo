from pathlib import Path
from datetime import date

BASE_URL = "https://www.bktech.dev"
BLOG_DIR = Path("pages/blog")

urls = []

# Pages fixes
urls.append(f"{BASE_URL}/")
urls.append(f"{BASE_URL}/blog")
urls.append(f"{BASE_URL}/blog/fr")
urls.append(f"{BASE_URL}/blog/en")

# Articles
for lang in ["fr", "en"]:
    for md in (BLOG_DIR / lang).glob("*.md"):
        if md.name == "index.md":
            continue
        slug = md.stem
        urls.append(f"{BASE_URL}/blog/{slug}?lang={lang}")

today = date.today().isoformat()

xml = ['<?xml version="1.0" encoding="UTF-8"?>']
xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

for url in urls:
    xml.append("  <url>")
    xml.append(f"    <loc>{url}</loc>")
    xml.append(f"    <lastmod>{today}</lastmod>")
    xml.append("  </url>")

xml.append("</urlset>")

Path("public").mkdir(exist_ok=True)
Path("public/sitemap.xml").write_text("\n".join(xml), encoding="utf-8")

print("sitemap.xml generated with", len(urls), "urls")
