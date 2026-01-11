import os
import re
import json
import time
from datetime import datetime, date
from pathlib import Path

OUT_BASE = "pages/blog"
BOOK_CALL_URL = "https://www.bktech.dev/contact"

KEYWORDS = {
    "fr": [
        "Combien coûte une application mobile",
    ],
    "en": [
        "Mobile app development cost",
    ],
}

DEFAULTS = {
    "fr": {
        "category": "Développement d'applications",
        "tags": ["application mobile", "startup", "prix", "bk tech"],
    },
    "en": {
        "category": "App Development",
        "tags": ["mobile app", "startup", "pricing", "bk tech"],
    },
}

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = (
        text.replace("é", "e").replace("è", "e").replace("ê", "e")
            .replace("à", "a").replace("â", "a")
            .replace("ù", "u").replace("û", "u")
            .replace("ô", "o").replace("î", "i")
            .replace("ï", "i").replace("ç", "c")
    )
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:90].strip("-") or "article"

def front_matter(title: str, lang: str, image_url: str, description: str) -> str:
    today = date.today().isoformat()
    d = DEFAULTS[lang]
    return f"""---
title: "{title}"
date: "{today}"
image: "{image_url}"
category: "{d['category']}"
tags: {json.dumps(d['tags'], ensure_ascii=False)}
description: "{description}"
author: "BK Tech"
---
"""

def body(title: str, lang: str) -> str:
    if lang == "fr":
        return f"""# {title}

## Points clés
- Budget, délais, facteurs importants
- Bonnes pratiques
- Méthode BK Tech

## Prendre rendez-vous
👉 {BOOK_CALL_URL}
"""
    return f"""# {title}

## Key takeaways
- Budget, timeline, key drivers
- Best practices
- BK Tech methodology

## Book a call
👉 {BOOK_CALL_URL}
"""

def write_article(lang: str, title: str, run_id: str) -> str:
    out_dir = Path(OUT_BASE) / lang
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = slugify(title)

    # ✅ force un nouveau fichier à chaque run
    filename = f"{date.today().isoformat()}-{slug}-{run_id}.md"
    md_path = out_dir / filename

    # ✅ placeholder image (on remet OpenAI image après)
    image_url = "https://placehold.co/1200x630/png?text=BK+Tech"

    description = (
        f"Guide BK Tech : {title}. Prix, délais et bonnes pratiques."
        if lang == "fr"
        else f"BK Tech guide: {title}. Costs, timelines and best practices."
    )

    content = front_matter(title, lang, image_url, description) + "\n" + body(title, lang)
    md_path.write_text(content, encoding="utf-8")

    return str(md_path)

def main():
    run_id = datetime.utcnow().strftime("%H%M%S")  # ex: 184233
    print(f"[SEO AUTOPILOT] run_id={run_id}")
    print(f"[SEO AUTOPILOT] OUT_BASE={OUT_BASE}")

    created = []
    for lang, titles in KEYWORDS.items():
        for t in titles:
            created.append(write_article(lang, t, run_id))

    print("Created files:")
    for p in created:
        print("-", p)

if __name__ == "__main__":
    main()
