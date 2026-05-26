import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";

import { AppChrome } from "@/components/layout/AppChrome";
import { SiteFooter } from "@/components/layout/SiteFooter";
import { APP_NAME } from "@/lib/constants";

import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  display: "swap",
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: `${APP_NAME} — Delhi NCR`,
  description: "AI-assisted day trip planner for Delhi NCR",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${geistSans.variable} ${geistMono.variable} min-h-screen`}>
        <AppChrome>{children}</AppChrome>
        <SiteFooter />
      </body>
    </html>
  );
}
