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
            maxWidth: 520,
            margin: "0 auto 36px",
            lineHeight: 1.6,
          }}
        >
          Analyses, conseils et retours d’expérience sur le développement
          d’applications, le SEO et les technologies modernes.
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
              fontWeight: 600,
              textDecoration: "none",
              color: "#0f172a",
              transition: "all 0.2s ease",
            }}
          >
            🇫🇷 Lire en français
          </Link>

          <Link
            href="/blog/en"
            style={{
              padding: "14px 22px",
              borderRadius: 14,
              border: "1px solid #e5e7eb",
              background: "#ffffff",
              fontSize: 16,
