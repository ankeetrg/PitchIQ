import type { Metadata } from "next";
import Script from "next/script";
import { Analytics } from "@vercel/analytics/react";
import { Barlow_Condensed, Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/pitchiq/ThemeProvider";
import { ToastProvider } from "@/components/pitchiq/Toast";

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-inter",
  display: "swap",
});

const barlowCondensed = Barlow_Condensed({
  subsets: ["latin"],
  weight: ["400", "600", "700", "800", "900"],
  variable: "--font-barlow-condensed",
  display: "swap",
});

export const metadata: Metadata = {
  title: "PitchIQ - World Cup 2026 Predictions, Odds, Fantasy Picks",
  description:
    "Live World Cup 2026 predictions, fantasy soccer intelligence, AI-labeled analysis, and legal-review betting line education.",
  metadataBase: new URL("https://getpitchiq.net"),
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "PitchIQ - World Cup 2026 Intelligence",
    description:
      "AI-labeled match previews, live odds context, standings, fantasy picks, and alerts for World Cup 2026.",
    url: "https://getpitchiq.net",
    siteName: "PitchIQ",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" data-theme="dark" suppressHydrationWarning>
      <body className={`${inter.variable} ${barlowCondensed.variable} font-sans`}>
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=G-N9PX9ZKHLR"
          strategy="afterInteractive"
        />
        <Script id="ga4-pitchiq" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-N9PX9ZKHLR');
          `}
        </Script>
        <ThemeProvider>
          <ToastProvider>{children}</ToastProvider>
        </ThemeProvider>
        <Analytics />
      </body>
    </html>
  );
}
