import type { Metadata } from "next";
import { Inter } from "next/font/google";

import { AppChrome } from "@/components/layout/AppChrome";
import { APP_NAME } from "@/lib/constants";

import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: `${APP_NAME} — Delhi NCR`,
  description: "Trip Pilot — AI day trip planner for Delhi NCR",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} min-h-screen font-sans antialiased`}>
        <AppChrome>{children}</AppChrome>
      </body>
    </html>
  );
}
