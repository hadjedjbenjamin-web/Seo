import Link from "next/link";

export default function BlogHome() {
  return (
    <main style={{ maxWidth: 900, margin: "40px auto", padding: "0 16px" }}>
      <h1 style={{ fontSize: 34, fontWeight: 800 }}>Blog BK Tech</h1>
      <p style={{ opacity: 0.8 }}>Choisis une langue :</p>

      <div style={{ display: "flex", gap: 12, marginTop: 18 }}>
        <Link href="/blog/fr" style={{ padding: 12, border: "1px solid #ddd", borderRadius: 10 }}>
          🇫🇷 Français
        </Link>
        <Link href="/blog/en" style={{ padding: 12, border: "1px solid #ddd", borderRadius: 10 }}>
          🇬🇧 English
        </Link>
      </div>
    </main>
  );
}
