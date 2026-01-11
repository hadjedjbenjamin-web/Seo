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
OPENAI_IMAGE_MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")

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

def safe_placeholder_image(title: str) -> str:
    # fallback si OpenAI échoue
    return "https://placehold.co/1200x630/png?text=BK+Tech"

# =========================
# OPENAI IMAGE
# =========================
def openai_generate_image(title: str, filename: str) -> str:
    """
    Génère une image OpenAI et l'enregistre dans public/blog/images.
    Retourne une URL relative: /blog/images/<file>.png
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing")

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = IMAGE_DIR / filename

    # si déjà générée, on réutilise
    if out_path.exists():
        return f"/blog/images/{filename}"

    prompt = (
        "Create a modern, premium blog header image. "
        "Theme: custom software and mobile app development. "
        f"Topic: {title}. "
        "Style: minimal, professional, blue and white palette, abstract tech shapes, "
        "soft gradients, no logos, NO TEXT."
    )

    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_IMAGE_MODEL,
        "prompt": prompt,
        "size": "1200x630",
        "response_format": "b64_json",
    }

    # retries simples (429 / 5xx)
    last_err = None
    for attempt in range(1, 6):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=120)
            if r.status_code == 200:
                data = r.json()
                b64 = data["data"][0].get("b64_json")
                if not b64:
                    raise RuntimeError("No b64_json in response")
                out_path.write_bytes(base64.b64decode(b64))
                return f"/blog/images/{filename}"

            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 * attempt)
                continue

            # autre erreur: on stop
            r.raise_for_status()

        except Exception as e:
            last_err = e
            time.sleep(1 * attempt)

    raise RuntimeError(f"OpenAI image generation failed: {last_err}")

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

## Points clés
- Facteurs de coût et de délai
- Bonnes pratiques
- Méthode BK Tech

## Prendre rendez-vous
👉 {BOOK_CALL_URL}
""".lstrip()

    return f"""
# {title}

## Key takeaways
- Cost and timeline drivers
- Best practices
- BK Tech methodology

## Book a call
👉 {BOOK_CALL_URL}
""".lstrip()

# =========================
# WRITE ARTICLE (ALWAYS CREATES)
# =========================
def write_article(lang: str, title: str, run_id: str) -> str:
    out_dir = Path(OUT_BASE) / lang
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = slugify(title)
    today = date.today().isoformat()

    # ✅ force un nouveau fichier par run
    md_filename = f"{today}-{slug}-{run_id}.md"
    md_path = out_dir / md_filename

    # image name unique aussi (évite overwrite)
    img_filename = f"{today}-{slug}-{run_id}.png"

    # Image OpenAI (avec fallback)
    try:
        image_url = openai_generate_image(title, img_filename)
    except Exception as e:
        print("[WARN] Image generation failed:", e)
        image_url = safe_placeholder_image(title)

    content = front_matter(title, lang, image_url) + "\n" + body(title, lang)
    md_path.write_text(content, encoding="utf-8")

    return str(md_path)

# =========================
# MAIN
# =========================
def main() -> None:
    run_id = datetime.utcnow().strftime("%H%M%S")
    print(f"[SEO AUTOPILOT] run_id={run_id}")
    print(f"[SEO AUTOPILOT] OUT_BASE={OUT_BASE}")
    print(f"[SEO AUTOPILOT] IMAGE_DIR={IMAGE_DIR}")

    created = []
    for lang, titles in KEYWORDS.items():
        for title in titles:
            created.append(write_article(lang, title, run_id))
            time.sleep(1)

    print("Created files:")
    for p in created:
        print("-", p)

if __name__ == "__main__":
    main()
