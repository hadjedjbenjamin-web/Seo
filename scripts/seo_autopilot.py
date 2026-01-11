import re
import json
import time
from datetime import date, datetime
from pathlib import Path

# =========================
# CONFIG
# =========================
OUT_BASE = "pages/blog"
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

# Image fixe (simple et propre)
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

def fm(title: str, lang: str) -> str:
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

def md_article(title: str, lang: str) -> str:
    if lang == "fr":
        return f"""# {title}

> **BK Tech** — Création d’applications sur mesure (France • UAE • International)

## Résumé
Dans cet article, on te donne une méthode claire pour estimer **le budget**, **les délais** et cadrer ton projet sans mauvaises surprises.

---

## 1) Les facteurs qui font varier le prix
- **Fonctionnalités** (auth, paiement, chat, admin, etc.)
- **Design UI/UX** (maquettes, parcours, responsive)
- **Backend & base de données**
- **Intégrations** (Stripe, CRM, API externes, analytics)
- **Qualité & sécurité** (tests, perf, RGPD)
- **Maintenance** (correctifs, évolutions)

## 2) Les fourchettes de délais (réalistes)
- MVP simple : **4 à 8 semaines**
- App standard : **8 à 14 semaines**
- Produit complexe : **3 à 6 mois**

## 3) La méthode BK Tech (simple et efficace)
1. Cadrage (objectif + périmètre + priorités)
2. UI/UX (wireframes → maquettes)
3. Dev itératif (sprints)
4. Tests + mise en production
5. Suivi / évolutions

---

## FAQ
**Combien coûte une application ?**  
Ça dépend du périmètre. Le plus important est de définir un MVP clair.

**Puis-je démarrer vite ?**  
Oui : on peut cadrer un MVP et itérer ensuite.

---

## Prendre rendez-vous
👉 Remplir le formulaire : {BOOK_CALL_URL}
"""
    else:
        return f"""# {title}

> **BK Tech** — Custom app development (France • UAE • International)

## Summary
In this article, you’ll learn a clear way to estimate **budget**, **timeline**, and scope your app without surprises.

---

## 1) What drives the cost
- **Features** (auth, payments, chat, admin, etc.)
- **UI/UX design** (flows, mockups, responsive)
- **Backend & database**
- **Integrations** (Stripe, CRM, external APIs, analytics)
- **Quality & security** (testing, performance)
- **Maintenance** (fixes, updates)

## 2) Realistic timelines
- Simple MVP: **4–8 weeks**
- Standard app: **8–14 weeks**
- Complex product: **3–6 months**

## 3) BK Tech process
1. Scoping (goals + scope + priorities)
2. UI/UX (wireframes → mockups)
3. Iterative development (sprints)
4. QA + production launch
5. Maintenance / upgrades

---

## FAQ
**How much does an app cost?**  
It depends on scope. The key is defining a clear MVP.

**Can we start fast?**  
Yes—scope an MVP and iterate.

---

## Book a call
👉 Fill the form: {BOOK_CALL_URL}
"""

def write_article(lang: str, title: str, run_id: str) -> str:
    out_dir = Path(OUT_BASE) / lang
    out_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    slug = slugify(title)
    filename = f"{today}-{slug}-{run_id}.md"
    path = out_dir / filename

    content = fm(title, lang) + "\n" + md_article(title, lang)
    path.write_text(content, encoding="utf-8")

    return str(path)

def main():
    run_id = datetime.utcnow().strftime("%H%M%S")
    print(f"[SEO AUTOPILOT] run_id={run_id}")

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
