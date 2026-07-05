import type { Metadata, Viewport } from "next";
import { Instrument_Sans, Instrument_Serif } from "next/font/google"; 
import "./globals.css";
import { ThemeProvider } from "@/components /providers/theme-provider";



const instrumentSans = Instrument_Sans({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-instrument-sans",
});

const instrumentSerif = Instrument_Serif({
  subsets: ["latin"],
display: "swap",
  weight: "400",
  style: ["normal", "italic"],
 variable: "--font-instrument-serif",
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export const metadata: Metadata = {
  title: "ZELTA AI",
  description: "",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${instrumentSans.variable} ${instrumentSerif.variable}`} 
      suppressHydrationWarning
    >
      <body className="min-h-full flex flex-col font-sans bg-background  text-white antialiased">
        <ThemeProvider>
        {children}
        </ThemeProvider>
      </body>
    </html>
  );
}