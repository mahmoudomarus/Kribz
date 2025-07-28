import { ThemeProvider } from '@/components/home/theme-provider';
import { siteConfig } from '@/lib/site';
import type { Metadata, Viewport } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';
import { Toaster } from '@/components/ui/sonner';
import { Analytics } from '@vercel/analytics/react';
import { GoogleAnalytics } from '@next/third-parties/google';
import { SpeedInsights } from '@vercel/speed-insights/next';
import Script from 'next/script';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const viewport: Viewport = {
  themeColor: 'black',
};

export const metadata: Metadata = {
  metadataBase: new URL(siteConfig.url),
  title: {
    default: siteConfig.name,
    template: `%s - ${siteConfig.name}`,
  },
  description:
    'Krib AI is an intelligent rental platform that helps you find, book, and manage property rentals with ease. From short-term stays to long-term leases, Krib AI streamlines the entire rental process.',
  keywords: [
    'AI',
    'artificial intelligence',
    'rental platform',
    'property booking',
    'real estate',
    'AI assistant',
    'property management',
    'rental properties',
    'short-term rentals',
    'long-term rentals',
  ],
  authors: [{ name: 'Krib AI Team', url: 'https://krib.ai' }],
  creator:
    'Krib AI Team - Building the future of intelligent property rentals',
  publisher:
    'Krib AI Team - Building the future of intelligent property rentals',
  category: 'Technology',
  applicationName: 'Krib AI',
  formatDetection: {
    telephone: false,
    email: false,
    address: false,
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
    },
  },
  openGraph: {
    title: 'Krib AI - Your AI Rental Agent',
    description:
      'Krib AI is an intelligent rental platform that helps you find, book, and manage property rentals with ease.',
    url: siteConfig.url,
    siteName: 'Krib AI',
    images: [
      {
        url: '/banner.png',
        width: 1200,
        height: 630,
        alt: 'Krib AI - Your AI Rental Agent',
        type: 'image/png',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Krib AI - Your AI Rental Agent',
    description:
      'Krib AI is an intelligent rental platform that helps you find, book, and manage property rentals with ease.',
    creator: '@kribai',
    site: '@kribai',
    images: [
      {
        url: '/banner.png',
        width: 1200,
        height: 630,
        alt: 'Krib AI - Your AI Rental Agent',
      },
    ],
  },
  icons: {
    icon: [{ url: '/favicon.svg', sizes: 'any' }],
    shortcut: '/favicon.svg',
  },
  // manifest: "/manifest.json",
  alternates: {
    canonical: siteConfig.url,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        {/* Google Tag Manager */}
        <Script id="google-tag-manager" strategy="afterInteractive">
          {`(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
          new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
          j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
          'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
          })(window,document,'script','dataLayer','GTM-PCHSN4M2');`}
        </Script>
      </head>

      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased font-sans bg-background`}
      >
        <noscript>
          <iframe
            src="https://www.googletagmanager.com/ns.html?id=GTM-PCHSN4M2"
            height="0"
            width="0"
            style={{ display: 'none', visibility: 'hidden' }}
          />
        </noscript>
        {/* End Google Tag Manager (noscript) */}

        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <Providers>
            {children}
            <Toaster />
          </Providers>
          <Analytics />
          <GoogleAnalytics gaId="G-6ETJFB3PT3" />
          <SpeedInsights />
        </ThemeProvider>
      </body>
    </html>
  );
}
