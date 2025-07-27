import { Metadata } from 'next';
import { siteConfig } from '@/lib/site';

export const metadata: Metadata = {
  title: siteConfig.name,
  description: siteConfig.description,
  keywords: ['Krib AI', 'AI', 'Rental Platform', 'Property Booking', 'Real Estate'],
  authors: [
    {
      name: 'Krib AI Team',
      url: 'https://krib.ai',
    },
  ],
  creator: 'Krib AI Team',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: siteConfig.url,
    title: siteConfig.name,
    description: siteConfig.description,
    siteName: siteConfig.name,
  },
  twitter: {
    card: 'summary_large_image',
    title: siteConfig.name,
    description: siteConfig.description,
    creator: '@kribai',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
};
