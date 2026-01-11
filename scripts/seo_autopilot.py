import re
import json
import time
from datetime import date, datetime
from pathlib import Path

# =========================
# CONFIG
# =========================
OUT_BASE = Path("pages/blog")
BOOK_CALL_URL = "https://www.bktech.dev/contact"

KEYWORDS = {
    "fr": [
        "Combien coûte une application mobile en 2026",
        "Création d’application sur mesure : étapes, budget et délais",
    ],
    "en": [
        "Mobile app development cost in 2026",
        "Custom app development: timeline, budget and process",
    ],
}

DEFAULTS = {
    "fr": {
        "category": "Développement d'applications",
        "tags": ["application mobile", "startup", "budget", "bk tech"],
    },
    "en": {
        "category": "App Development",
        "tags": ["mobile app", "startup", "budget", "bk tech"],
    },
}

DEFAULT_IMAGE = "https://placehold.co/1200x630/png?text=BK+Tech"

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
    return text[:90].strip("-") or "article"

def front_matter(title: str, lang: str) -> str:
    today = date.today().isoformat()
    d = DEFAULTS[lang]
    description = (
        f"Guide BK Tech : {title}. Méthode, budget, délais et conseils concrets."
        if lang == "fr"
        else f"BK Tech guide: {title}. Process, budget, timeline and practical tips."
    )
    return f"""---
title: "{title}"
date: "{today}"
image: "{DEFAULT_IMAGE}"
category: "{d['category']}"
tags: {json.dumps(d['tags'], ensure_ascii=False)}
description: "{description}"
author: "BK Tech"
---
"""

def article_body(title: str, lang: str) -> str:
    if lang == "fr":
        return f"""# {title}

> **BK Tech** — Création d’applications sur mesure (France • UAE • International)

## Résumé
Dans cet article, on te donne une méthode claire pour estimer **le budget**, **les délais** et cadrer ton projet sans mauvaises surprises.

---

## 1) Les facteurs qui font varier le prix
- Fonctionnalités (auth, paiement, chat, admin…)
- Design UI/UX (parcours, maquettes)
- Backend & base de données
- Intégrations (Stripe, CRM, API externes)
- Qualité & sécurité (tests, perf, RGPD)
- Maintenance (correctifs, évolutions)

## 2) Délais réalistes
- MVP simple : **4 à 8 semaines**
- App standard : **8 à 14 semaines**
- Projet complexe : **3 à 6 mois**

## 3) La méthode BK Tech
1. Cadrage (objectif + périmètre)
2. UI/UX (wireframes → maquettes)
3. Développement itératif (sprints)
4. Tests + mise en production
5. Suivi / évolutions

---

## Prendre rendez-vous
👉 {BOOK_CALL_URL}
"""
    else:
        return f"""# {title}

> **BK Tech** — Custom app development (France • UAE • International)

## Summary
A clear way to estimate **budget**, **timeline**, and scope your app without surprises.

---

## 1) Cost drivers
- Features (auth, payments, chat, admin…)
- UI/UX (flows, mockups)
- Backend & database
- Integrations (Stripe, CRM, external APIs)
- Quality & security (testing, performance)
- Maintenance (fixes, upgrades)

## 2) Realistic timelines
- Simple MVP: **4–8 weeks**
- Standard app: **8–14 weeks**
- Complex product: **3–6 months**

## 3) BK Tech process
1. Scoping
2. UI/UX
3. Iterative development
4. QA + launch
5. Maintenance / upgrades

---

## Book a call
👉 {BOOK_CALL_URL}
"""

def write_article(lang: str, title: str, run_id: str) -> Path:
    out_dir = OUT_BASE / lang
    out_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    slug = slugify(title)

    filename = f"{today}-{slug}-{run_id}.md"
    path = out_dir / filename

    content = front_matter(title, lang) + "\n" + article_body(title, lang)
    path.write_text(content, encoding="utf-8")

    return path

def update_index(lang: str) -> None:
    """
    Met à jour pages/blog/<lang>/index.md avec une liste de liens vers les articles.
    Les URLs suivent ton format actuel : /blog/<slug>?lang=fr|en
    """
    lang_dir = OUT_BASE / lang
    index_path = lang_dir / "index.md"

    posts = sorted(
        [p for p in lang_dir.glob("*.md") if p.name != "index.md"],
        reverse=True
    )

    title = "Blog BK Tech (FR)" if lang == "fr" else "BK Tech Blog (EN)"
    intro = (
        "Derniers articles (clique pour lire) :"
        if lang == "fr"
        else "Latest posts (click to read):"
    )

    lines = [f"# {title}", "", intro, ""]

    for p in posts[:50]:
        slug = p.stem  # filename without .md
        # Important: tes articles sont accessibles via /blog/<slug>?lang=xx
        url = f"/blog/{slug}?lang={lang}"
        # titre lisible : on enlève la date-runid du filename
        pretty = slug
        pretty = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", pretty)
        pretty = re.sub(r"-\d{6}$", "", pretty)  # run_id si 6 chiffres
        pretty = pretty.replace("-", " ").strip().capitalize()
        lines.append(f"- [{pretty}]({url})")

    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[INDEX] updated: {index_path}")

def main():
    run_id = datetime.utcnow().strftime("%H%M%S")
    print(f"[SEO AUTOPILOT] run_id={run_id}")

    created = []
    for lang, titles in KEYWORDS.items():
        for title in titles:
            created.append(write_article(lang, title, run_id))
            time.sleep(1)

    # ✅ met à jour les pages de listing
    update_index("fr")
    update_index("en")

    print("Created files:")
    for p in created:
        print("-", p)

if __name__ == "__main__":
    main()
