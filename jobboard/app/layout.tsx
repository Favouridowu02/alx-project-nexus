import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { JobProvider } from "@/context/JobContext";
import { Header } from "@/components/layouts/Header";
import { Footer } from "@/components/layouts/Footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Job Board - Find Your Dream Job",
  description: "Explore thousands of job opportunities with all the information you need. Filter by category, location, experience level, and more.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased flex flex-col min-h-screen`}
      >
        <JobProvider>
          <Header />
          <main className="grow">
            {children}
          </main>
          <Footer />
        </JobProvider>
      </body>
    </html>
  );
}
