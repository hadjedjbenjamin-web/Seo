import os
import re
import json
import time
from datetime import date
from pathlib import Path

OUT_BASE = "pages/blog"  # ✅ IMPORTANT: c'est ici que ton site lit les .md

# Ajuste tes keywords ici
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
    # remplace accents simples
    s = (s.replace("é", "e").replace("è", "e").replace("ê", "e")
           .replace("à", "a").replace("â", "a")
           .replace("ù", "u").replace("û", "u")
           .replace("ô", "o").replace("î", "i").replace("ï", "i")
           .replace("ç", "c"))
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:80].strip("-") or "article"

def make_front_matter(title: str, lang: str) -> str:
    today = date.today().isoformat()
    d = DEFAULTS[lang]

    # image placeholder (tu peux remplacer plus tard)
    image = "https://placehold.co/1200x630/png"

    # description courte SEO
    if lang == "fr":
        description = f"Guide BK Tech : {title}. Prix, délais, étapes et bonnes pratiques pour réussir votre application."
    else:
        description = f"BK Tech guide: {title}. Costs, timelines, process and best practices to build your app."

    tags_json = json.dumps(d["tags"], ensure_ascii=False)

    return f"""---
title: "{title}"
date: "{today}"
image: "{image}"
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

## Ce que vous allez apprendre
- Les facteurs qui influencent le prix et les délais
- Les erreurs fréquentes à éviter
- Une méthode claire pour cadrer votre projet

## Les facteurs clés (budget, délai, complexité)
Expliquez ici les éléments : fonctionnalités, design, backend, intégrations, maintenance.

## Notre approche chez BK Tech
- Atelier cadrage
- UI/UX
- Développement itératif
- Tests & mise en production

## FAQ
**Combien de temps pour développer une app ?**  
Cela dépend du périmètre, en général de quelques semaines à plusieurs mois.

**Quel budget prévoir ?**  
Le budget varie selon la complexité et les intégrations.

## Contact
👉 Réserver un appel : https://bktech.com
""".lstrip()
    else:
        return f"""
# {title}

## What you’ll learn
- What drives cost and timeline
- Common mistakes to avoid
- A clear process to scope your project

## Key drivers (budget, timeline, complexity)
Cover features, design, backend, integrations, maintenance.

## BK Tech approach
- Scoping workshop
- UI/UX
- Iterative development
- QA & production release

## FAQ
**How long does it take to build an app?**  
It depends on scope—typically weeks to months.

**How much does an app cost?**  
It varies by complexity and integrations.

## Contact
👉 Book a call: https://bktech.com
""".lstrip()

def write_article(lang: str, title: str) -> str:
    today = date.today().isoformat()
    slug = slugify(title)

    out_dir = Path(OUT_BASE) / lang
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{today}-{slug}.md"
    path = out_dir / filename

    # évite d’écraser si déjà généré aujourd’hui
    if path.exists():
        return str(path)

    fm = make_front_matter(title, lang)
    body = make_body(title, lang)

    with open(path, "w", encoding="utf-8") as f:
        f.write(fm + "\n" + body)

    return str(path)

def main():
    created = []
    for lang, titles in KEYWORDS.items():
        if lang not in ("fr", "en"):
            continue
        for title in titles:
            created.append(write_article(lang, title))
            time.sleep(1)  # petite pause pour éviter des commits trop “agressifs”

    print("Created files:")
    for p in created:
        print("-", p)

if __name__ == "__main__":
    main()
