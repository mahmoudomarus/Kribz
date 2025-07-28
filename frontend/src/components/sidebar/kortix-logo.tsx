'use client';

import { useTheme } from 'next-themes';
import { useEffect, useState } from 'react';
import Image from 'next/image';

interface KribLogoProps {
  size?: number;
}

export function KribLogo({ size = 24 }: KribLogoProps) {
  const { theme, systemTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  // After mount, we can access the theme
  useEffect(() => {
    setMounted(true);
  }, []);

  const shouldUseWhite = mounted && (
    theme === 'dark' || (theme === 'system' && systemTheme === 'dark')
  );

  return (
    <Image
        src={shouldUseWhite ? "/krib-logo-white.svg" : "/krib-symbol.svg"}
        alt="Krib AI"
        width={size}
        height={size}
        className="flex-shrink-0"
      />
  );
}

// Backward compatibility export
export const KortixLogo = KribLogo;
