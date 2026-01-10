import os
import re
import json
import time
import base64
from datetime import date
from pathlib import Path
import requests

OUT_BASE = "pages/blog"                 # ✅ tes articles visibles
IMAGE_DIR = Path("public/blog/images")  # ✅ images visibles sur le site
BOOK_CALL_URL = "https://www.bktech.dev/contact"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_IMAGE_MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")  # modèle image

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

def slugify(s: str) -> str:
    s = s.lower().strip()
    s = (s.replace("é", "e").replace("è", "e").replace("ê", "e")
           .replace("à", "a").replace("â", "a")
           .replace("ù", "u").replace("û", "u")
           .replace("ô", "o").replace("î", "i").replace("ï", "i")
           .replace("ç", "c"))
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:90].strip("-") or "article"

def openai_generate_image(title: str, out_path: Path) -> str:
    """
    Génère une image PNG via OpenAI Images API et l'enregistre dans public/.
    Docs: Images API /v1/images/generations. :contentReference[oaicite:0]{index=0}
    """
    if out_path.exists():
        return f"/blog/images/{out_path.name}"

    if not OPENAI_API_KEY:
        # fallback si la clé n'est pas dispo
        return "https://placehold.co/1200x630/png?text=BK+Tech"

    prompt = (
        "Create a clean, modern, premium blog header image. "
        "Theme: custom app development / technology. "
        f"Topic: {title}. "
        "Style: minimal, professional, soft gradients, blue/white palette, "
        "abstract shapes, subtle tech elements (no logos), NO TEXT."
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

    # retry simple (évite les erreurs temporaires)
    for attempt in range(1, 6):
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        if r.status_code == 200:
            data = r.json()
            b64 = data["data"][0].get("b64_json")
            if not b64:
                # fallback si format différent
                return "https://placehold.co/1200x630/png?text=BK+Tech"

            IMAGE_DIR.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(base64.b64decode(b64))
            return f"/blog/images/{out_path.name}"

        # 429 / 5xx => on attend et on retente
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(2 * attempt)
            continue

        # autres erreurs
        return "https://placehold.co/1200x630/png?text=BK+Tech"

    return "https://placehold.co/1200x630/png?text=BK+Tech"

def make_front_matter(title: str, lang: str, image_url: str) -> str:
    today = date.today().isoformat()
    d = DEFAULTS[lang]

    if lang == "fr":
        description = f"Guide BK Tech : {title}. Prix, délais, étapes et bonnes pratiques pour réussir votre application."
    else:
        description = f"BK Tech guide: {title}. Costs, timelines, process and best practices to build your app."

    tags_json = json.dumps(d["tags"], ensure_ascii=False)

    return f"""---
title: "{title}"
date: "{today}"
image: "{image_url}"
category: "{d['category']}"
tags: {tags_json}
description: "{description}"
author: "BK Tech"
---
"""

def make_body(title: str, lang: str) -> str:
    if lang == "fr":
        return f"""
# {title}

## Points clés
- Ce qui influence le prix et les délais
- Les erreurs fréquentes à éviter
- Une méthode simple pour cadrer votre projet

## Les facteurs de coût
Expliquez : fonctionnalités, UI/UX, backend, intégrations, sécurité, maintenance.

## Notre approche chez BK Tech
- Atelier de cadrage
- Design UI/UX
- Développement itératif
- QA, mise en production, suivi

## FAQ
**Combien de temps pour développer une app ?**  
Cela dépend du périmètre : généralement de quelques semaines à plusieurs mois.

**Quel budget prévoir ?**  
Le budget dépend de la complexité et des intégrations.

## Prendre rendez-vous
👉 Remplir le formulaire : {BOOK_CALL_URL}
""".lstrip()
    else:
        return f"""
# {title}

## Key takeaways
- What drives cost and timeline
- Common mistakes to avoid
- A simple process to scope your project

## Cost drivers
Features, UI/UX, backend, integrations, security, maintenance.

## BK Tech approach
- Scoping workshop
- UI/UX design
- Iterative development
- QA, production release, support

## FAQ
**How long does it take to build an app?**  
Depends on scope—typically weeks to months.

**How much does an app cost?**  
Varies by complexity and integrations.

## Book a call
👉 Fill the form: {BOOK_CALL_URL}
""".lstrip()

def write_article(lang: str, title: str) -> str:
    today = date.today().isoformat()
    slug = slugify(title)

    out_dir = Path(OUT_BASE) / lang
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{today}-{slug}.md"
    md_path = out_dir / filename

    # évite de régénérer si déjà là
    if md_path.exists():
        return str(md_path)

    # image liée au sujet
    img_path = IMAGE_DIR / f"{today}-{slug}.png"
    image_url = openai_generate_image(title, img_path)

    fm = make_front_matter(title, lang, image_url)
    body = make_body(title, lang)

    md_path.write_text(fm + "\n" + body, encoding="utf-8")
    return str(md_path)

def main():
    created = []
    for lang, titles in KEYWORDS.items():
        for title in titles:
            created.append(write_article(lang, title))
            time.sleep(1)

    print("Created files:")
    for p in created:
        print("-", p)

if __name__ == "__main__":
    main()
