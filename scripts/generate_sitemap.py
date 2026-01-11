from pathlib import Path
from datetime import date

BASE_URL = "https://www.bktech.dev"
BLOG_DIR = Path("pages/blog")
OUT_FILE = Path("pages/blog/sitemap.xml")  # ✅ sitemap servi sous /blog/sitemap.xml

def collect_urls():
    urls = []

    # Pages blog
    urls.append(f"{BASE_URL}/blog")
    urls.append(f"{BASE_URL}/blog/fr")
    urls.append(f"{BASE_URL}/blog/en")

    # Articles
    for lang in ["fr", "en"]:
        lang_dir = BLOG_DIR / lang
        if not lang_dir.exists():
            continue

        for md in sorted(lang_dir.glob("*.md"), reverse=True):
            if md.name == "index.md":
                continue
            slug = md.stem
            urls.append(f"{BASE_URL}/blog/{slug}?lang={lang}")

    # dédoublonnage
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            out.append(u)
            seen.add(u)
    return out

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

    print("✅ sitemap generated:", OUT_FILE)
    print("✅ urls:", len(urls))

if __name__ == "__main__":
    main()
