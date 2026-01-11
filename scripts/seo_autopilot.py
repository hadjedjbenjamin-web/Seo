import os
import re
import json
import time
import base64
from datetime import date, datetime
from pathlib import Path

import requests

# =========================
# CONFIG
# =========================
OUT_BASE = "pages/blog"
IMAGE_DIR = Path("public/blog/images")
BOOK_CALL_URL = "https://www.bktech.dev/contact"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
OPENAI_IMAGE_MODEL = "gpt-image-1"

KEYWORDS = {
    "fr": ["Combien coûte une application mobile"],
    "en": ["Mobile app development cost"],
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

# =========================
# HELPERS
# =========================
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
    return text[:80].strip("-") or "article"

def placeholder_image() -> str:
    return "https://placehold.co/1536x1024/png?text=BK+Tech"

# =========================
# OPENAI IMAGE (CORRECT PAYLOAD)
# =========================
def openai_generate_image(title: str, filename: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY missing")

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = IMAGE_DIR / filename

    if out_path.exists():
        return f"/blog/images/{filename}"

    prompt = (
        "Modern premium blog header image. "
        "Theme: custom software and mobile app development. "
        f"Topic: {title}. "
        "Style: minimal, professional, abstract tech, blue and white palette, "
        "soft gradients, NO TEXT."
    )

    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_IMAGE_MODEL,
        "prompt": prompt,
        "size": "1536x1024"
    }

    r = requests.post(url, headers=headers, json=payload, timeout=120)

    if r.status_code != 200:
        raise RuntimeError(f"OpenAI image generation failed: {r.status_code} {r.text}")

    data = r.json()
    b64 = data["data"][0]["b64_json"]
    out_path.write_bytes(base64.b64decode(b64))

    return f"/blog/images/{filename}"

# =========================
# CONTENT
# =========================
def front_matter(title: str, lang: str, image_url: str) -> str:
    today = date.today().isoformat()
    d = DEFAULTS[lang]

    description = (
        f"Guide BK Tech : {title}. Prix, délais et bonnes pratiques."
        if lang == "fr"
        else f"BK Tech guide: {title}. Costs, timelines and best practices."
    )

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
        return f"""
# {title}

## Ce que vous devez savoir
- Facteurs de coût réels
- Délais de développement
- Bonnes pratiques BK Tech

## Prendre rendez-vous
👉 {BOOK_CALL_URL}
""".lstrip()

    return f"""
# {title}

## What you need to know
- Real cost drivers
- Development timelines
- BK Tech best practices

## Book a call
👉 {BOOK_CALL_URL}
""".lstrip()

# =========================
# WRITE ARTICLE
# =========================
def write_article(lang: str, title: str, run_id: str) -> str:
    out_dir = Path(OUT_BASE) / lang
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = slugify(title)
    today = date.today().isoformat()

    md_filename = f"{today}-{slug}-{run_id}.md"
    md_path = out_dir / md_filename

    img_filename = f"{today}-{slug}-{run_id}.png"

    try:
        image_url = openai_generate_image(title, img_filename)
    except Exception as e:
        print("[WARN] Image generation failed:", e)
        image_url = placeholder_image()

    content = front_matter(title, lang, image_url) + "\n" + body(title, lang)
    md_path.write_text(content, encoding="utf-8")

    return str(md_path)

# =========================
# MAIN
# =========================
def main():
    run_id = datetime.utcnow().strftime("%H%M%S")
    print(f"[SEO AUTOPILOT] run_id={run_id}")

    created = []
    for lang, titles in KEYWORDS.items():
        for title in titles:
            created.append(write_article(lang, title, run_id))
            time.sleep(1)

    print("Created files:")
    for f in created:
        print("-", f)

if __name__ == "__main__":
    main()
