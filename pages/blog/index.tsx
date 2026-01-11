import Link from "next/link";
import "./blog.css";

export default function BlogHome() {
  return (
    <main className="blog-shell">
      <section className="blog-article" style={{ textAlign: "center" }}>
        <h1>Blog BK Tech</h1>

        <p style={{ opacity: 0.8, maxWidth: 560, margin: "0 auto 36px" }}>
          Choisis ta langue pour lire nos articles sur le développement
          d’applications, le SEO et les technologies.
        </p>

        <div
          style={{
            display: "flex",
            gap: 16,
            justifyContent: "center",
            flexWrap: "wrap",
          }}
        >
          <Link
            href="/blog/fr"
            style={{
              padding: "14px 22px",
              borderRadius: 14,
              border: "1px solid #e5e7eb",
              background: "#ffffff",
              fontWeight: 700,
              textDecoration: "none",
              color: "#0f172a",
            }}
          >
            🇫🇷 Français
          </Link>

          <Link
            href="/blog/en"
            style={{
              padding: "14px 22px",
              borderRadius: 14,
              border: "1px solid #e5e7eb",
              background: "#ffffff",
              fontWeight: 700,
              textDecoration: "none",
              color: "#0f172a",
            }}
          >
            🇬🇧 English
          </Link>
        </div>
      </section>
    </main>
  );
}
