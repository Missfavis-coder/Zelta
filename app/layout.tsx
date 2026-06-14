import type { Metadata, Viewport } from "next";
import { Instrument_Sans } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const instrumentSans = Instrument_Sans({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-instrument-sans",
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export const metadata: Metadata = {
  title: "Liftoff | Find incredible people, through people you trust",
  description: "Find incredible people, though people you trust. A hiring and networking platform where incredible people connect - and start working together.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${instrumentSans.variable} `} suppressHydrationWarning
    >
      <body className="min-h-full flex flex-col ">{children}</body>
    </html>
  );
}
