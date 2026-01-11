import Link from "next/link";

export default function BlogHome() {
  return (
    <main
      style={{
        padding: "80px 16px",
        background: "linear-gradient(180deg, #f8fafc 0%, #ffffff 100%)",
        minHeight: "100vh",
      }}
    >
      {/* ✅ TEST VISUEL (tu dois le voir en bas à droite) */}
      <div
        style={{
          position: "fixed",
          bottom: 12,
          right: 12,
          background: "#ef4444",
          color: "white",
          padding: "8px 10px",
          borderRadius: 10,
          fontWeight: 700,
          zIndex: 999999,
        }}
      >
        BLOG OK
      </div>

      <section
        style={{
          maxWidth: 860,
          margin: "0 auto",
          textAlign: "center",
          fontFamily:
            'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Inter, Arial, sans-serif',
          color: "#0f172a",
        }}
      >
        <h1
          style={{
            fontSize: 42,
            fontWeight: 800,
            letterSpacing: "-0.02em",
            marginBottom: 12,
          }}
        >
          Blog BK Tech
        </h1>

        <p
          style={{
            fontSize: 18,
            opacity: 0.8,
            maxWidth: 560,
            margin: "0 auto 36px",
            lineHeight: 1.7,
          }}
        >
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
              fontSize: 16,
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
              fontSize: 16,
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
