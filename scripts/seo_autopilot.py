def write_article(lang: str, title: str) -> str:
    today = date.today().isoformat()
    slug = slugify(title)

    out_dir = Path(OUT_BASE) / lang
    out_dir.mkdir(parents=True, exist_ok=True)

    # Nom de base
    filename = f"{today}-{slug}.md"
    md_path = out_dir / filename

    # 🔁 Si le fichier existe déjà, on crée une variante (-2, -3, etc.)
    i = 2
    while md_path.exists():
        md_path = out_dir / f"{today}-{slug}-{i}.md"
        i += 1

    # Image liée au sujet
    img_path = IMAGE_DIR / f"{today}-{slug}.png"
    image_url = openai_generate_image(title, img_path)

    # Contenu
    fm = make_front_matter(title, lang, image_url)
    body = make_body(title, lang)

    md_path.write_text(fm + "\n" + body, encoding="utf-8")

    return str(md_path)
