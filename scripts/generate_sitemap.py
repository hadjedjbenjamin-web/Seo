from pathlib import Path
from datetime import date

BASE_URLS = [
    "https://www.bktech.dev",
    "https://bktech.dev",
]

BLOG_DIR = Path("pages/blog")
OUT_FILE = Path("pages/sitemap.xml")

def collect_urls():
    urls = set()

    # Pages fixes
    for base in BASE_URLS:
        urls.add(f"{base}/")
        urls.add(f"{base}/blog")
        urls.add(f"{base}/blog/fr")
        urls.add(f"{base}/blog/en")

    # Articles
    for lang in ["fr", "en"]:
        lang_dir = BLOG_DIR / lang
        if not lang_dir.exists():
            continue

        for md in lang_dir.glob("*.md"):
            if md.name == "index.md":
                continue
            slug = md.stem
            for base in BASE_URLS:
                urls.add(f"{base}/blog/{slug}?lang={lang}")

    return sorted(urls)

def main():
    urls = collect_urls()
    today = date.today().isoformat()

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{url}</loc>")
        xml.append(f"    <lastmod>{today}</lastmod>")
        xml.append("  </url>")

    xml.append("</urlset>")
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text("\n".join(xml), encoding="utf-8")

    print("✅ sitemap generated:", str(OUT_FILE))
    print("✅ urls:", len(urls))

if __name__ == "__main__":
    main()
