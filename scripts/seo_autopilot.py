import os
import re
import json
import time
import base64
from datetime import date
from pathlib import Path
import requests

# =========================
# CONFIG
# =========================
OUT_BASE = "pages/blog"                 # là où le site lit les articles
IMAGE_DIR = Path("public/blog/images")  # images visibles sur le site
BOOK_CALL_URL = "https://www.bktech.dev/contact"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_IMAGE_MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")

KEYWORDS = {
    "fr": [
        "Combien coûte une application mobile",
        "Création d’application sur mesure",
    ],
    "en": [
        "Mobile app development cost",
        "Custom app development company",
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

# =========================
# UTILS
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
    return text[:90].strip("-") or "article"

# =========================
# IMAGE GENERATION (OPENAI)
# =========================
def openai_generate_image(title: str, out_path: Path) -> str:
    if out_path.exists():
        return f"/blog/images/{out_path.name}"

    if not OPENAI_API_KEY:
        return "https://placehold.co/1200x630/png?text=BK+Tech"

    prompt = (
        "Create a clean, modern, premium blog header image. "
        "Theme: custom app development and technology. "
        f"Topic: {title}. "
        "Style: minimal, professional, blue/white palette, "
        "abstract tech shapes, soft gradients, NO TEXT."
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
        "output_format": "png",
    }

    for attempt in range(1, 6):
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        if r.status_code == 200:
            data = r.json()
            b64 = data["data"][0].get("b64_json")
            if not b64:
                break

            IMAGE_DIR.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(base64.b64decode(b64))
            return f"/blog/images/{out_path.name}"

        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(2 * attempt)
            continue

        break

    return "https://placehold.co/1200x630/png?text=BK+Tech"

# =========================
# CONTENT
# =========================
def make_front_matter(title: str, lang: str, image_url: str) -> str:
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

def make_body(title: str, lang: str) -> str:
    if lang == "fr":
        return f"""
# {title}

## Points clés
- Facteurs de coût et de délai
- Erreurs fréquentes
- Méthode BK Tech

## Comment estimer le budget
Fonctionnalités, design, backend, sécurité, maintenance.

## Notre approche
- Cadrage
- UI/UX
- Développement itératif
- Mise en production

## Prendre rendez-vous
👉 {BOOK_CALL_URL}
""".lstrip()
    else:
        return f"""
# {title}

## Key takeaways
- Cost and timeline drivers
- Common mistakes
- BK Tech methodology

## How to estimate budget
Features, design, backend, security, maintenance.

## Our approach
- Scoping
- UI/UX
- Iterative development
- Production release

## Book a call
👉 {BOOK_CALL_URL}
""".lstrip()

# =========================
# WRITE ARTICLE (OPTION 1 FIX)
# =========================
def write_article(lang: str, title: str) -> str:
    today = date.today().isoformat()
    slug = slugify(title)

    out_dir = Path(OUT_BASE) / lang
    out_dir.mkdir_
