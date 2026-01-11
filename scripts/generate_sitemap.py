from pathlib import Path

BASE_URL = "https://www.bktech.dev"
BLOG_DIR = Path("pages/blog")

# ✅ TXT sitemap (Google accepte)
OUT_FILE = Path("pages/sitemap.txt")  # sera accessible sur /sitemap.txt si .txt est autorisé

def collect_urls():
    urls = []

    # Pages principales blog
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

    # Dédoublonnage
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            out.append(u)
            seen.add(u)
    return out

def main():
    urls = collect_urls()
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text("\n".join(urls) + "\n", encoding="utf-8")
    print("✅ sitemap.txt generated:", OUT_FILE)
    print("✅ urls:", len(urls))

if __name__ == "__main__":
    main()
