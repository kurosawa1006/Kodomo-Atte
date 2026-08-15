import type { ReactNode } from "react";
import "./globals.css";

export const metadata = {
  title: "コドモアッテ",
  description: "こども園サポート",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ja">
      <body className="min-h-screen bg-slate-50 text-slate-800 antialiased">{children}</body>
    </html>
  );
}
