export default function HomePage() {
  return (
    <main style={{ padding: 24 }}>
      <h1>コドモアッテ</h1>
      <p>Next.js フロントエンドの基盤です。</p>
      <p>API: {process.env.NEXT_PUBLIC_API_URL}</p>
    </main>
  );
}
