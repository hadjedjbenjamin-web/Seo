import os
import re
import json
import base64
import requests
import time
from datetime import date, datetime
from pathlib import Path

# =========================
# CONFIG
# =========================
OUT_BASE = "pages/blog"
IMAGE_DIR = Path("public/blog/images")
BOOK_CALL_URL = "https://www.bktech.dev/contact"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

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
    return text[:80].strip("-") or "article"

# =========================
# OPENAI IMAGE
# =========================
def openai_generate_image(title: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY missing")

    prompt = (
        "Modern premium blog header image. "
        "Theme: custom software and mobile app development. "
        f"Topic: {title}. "
        "Style: minimal, professional, blue and white, abstract tech, NO TEXT."
    )

    r = requests.post(
        "https://api.openai.com/v1/images/generations",
