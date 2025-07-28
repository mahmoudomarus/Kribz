'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface RealEstateBackgroundProps {
  className?: string;
}

export const RealEstateBackground: React.FC<RealEstateBackgroundProps> = ({
  className,
}) => {
  return (
    <div className={cn("absolute inset-0 overflow-hidden", className)}>
      {/* Main gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-indigo-900" />
      
      {/* Subtle pattern overlay */}
      <div className="absolute inset-0 opacity-10 dark:opacity-5">
        <svg width="100%" height="100%" className="absolute inset-0">
          <defs>
            <pattern id="real-estate-pattern" x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
              <rect width="60" height="60" fill="transparent" />
              <circle cx="30" cy="30" r="1" fill="currentColor" className="text-blue-400 dark:text-blue-300" />
              <circle cx="0" cy="0" r="1" fill="currentColor" className="text-blue-400 dark:text-blue-300" />
              <circle cx="60" cy="60" r="1" fill="currentColor" className="text-blue-400 dark:text-blue-300" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#real-estate-pattern)" />
        </svg>
      </div>

      {/* Floating property icons */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="relative w-full h-full">
          {/* Building silhouettes */}
          <div className="absolute bottom-0 left-0 right-0 flex justify-center items-end opacity-20 dark:opacity-10">
            <svg width="100%" height="400" viewBox="0 0 1200 400" className="max-w-6xl">
              {/* Building 1 */}
              <rect x="50" y="200" width="80" height="200" fill="currentColor" className="text-slate-600 dark:text-slate-400" />
              <rect x="60" y="220" width="12" height="12" fill="currentColor" className="text-blue-400 dark:text-blue-300" />
              <rect x="80" y="220" width="12" height="12" fill="currentColor" className="text-blue-400 dark:text-blue-300" />
              <rect x="100" y="220" width="12" height="12" fill="currentColor" className="text-blue-400 dark:text-blue-300" />
              <rect x="60" y="250" width="12" height="12" fill="currentColor" className="text-blue-400 dark:text-blue-300" />
              <rect x="100" y="250" width="12" height="12" fill="currentColor" className="text-blue-400 dark:text-blue-300" />
              
              {/* Building 2 */}
              <rect x="160" y="150" width="100" height="250" fill="currentColor" className="text-slate-600 dark:text-slate-400" />
              <rect x="175" y="170" width="15" height="15" fill="currentColor" className="text-amber-400 dark:text-amber-300" />
              <rect x="200" y="170" width="15" height="15" fill="currentColor" className="text-amber-400 dark:text-amber-300" />
              <rect x="225" y="170" width="15" height="15" fill="currentColor" className="text-amber-400 dark:text-amber-300" />
              <rect x="175" y="210" width="15" height="15" fill="currentColor" className="text-amber-400 dark:text-amber-300" />
              <rect x="200" y="210" width="15" height="15" fill="currentColor" className="text-amber-400 dark:text-amber-300" />
              <rect x="225" y="210" width="15" height="15" fill="currentColor" className="text-amber-400 dark:text-amber-300" />
              
              {/* Building 3 */}
              <rect x="290" y="180" width="70" height="220" fill="currentColor" className="text-slate-600 dark:text-slate-400" />
              <rect x="300" y="200" width="10" height="10" fill="currentColor" className="text-green-400 dark:text-green-300" />
              <rect x="320" y="200" width="10" height="10" fill="currentColor" className="text-green-400 dark:text-green-300" />
              <rect x="340" y="200" width="10" height="10" fill="currentColor" className="text-green-400 dark:text-green-300" />
              
              {/* Building 4 - Modern skyscraper */}
              <rect x="400" y="80" width="90" height="320" fill="currentColor" className="text-slate-700 dark:text-slate-300" />
              <rect x="415" y="100" width="12" height="12" fill="currentColor" className="text-blue-500 dark:text-blue-400" />
              <rect x="435" y="100" width="12" height="12" fill="currentColor" className="text-blue-500 dark:text-blue-400" />
              <rect x="455" y="100" width="12" height="12" fill="currentColor" className="text-blue-500 dark:text-blue-400" />
              <rect x="415" y="130" width="12" height="12" fill="currentColor" className="text-blue-500 dark:text-blue-400" />
              <rect x="435" y="130" width="12" height="12" fill="currentColor" className="text-blue-500 dark:text-blue-400" />
              <rect x="455" y="130" width="12" height="12" fill="currentColor" className="text-blue-500 dark:text-blue-400" />
              
              {/* Houses */}
              <polygon points="550,350 580,320 610,350 610,380 550,380" fill="currentColor" className="text-slate-500 dark:text-slate-400" />
              <rect x="560" y="360" width="8" height="8" fill="currentColor" className="text-yellow-400 dark:text-yellow-300" />
              <rect x="580" y="360" width="8" height="8" fill="currentColor" className="text-yellow-400 dark:text-yellow-300" />
              
              <polygon points="650,360 680,330 710,360 710,390 650,390" fill="currentColor" className="text-slate-500 dark:text-slate-400" />
              <rect x="660" y="370" width="8" height="8" fill="currentColor" className="text-yellow-400 dark:text-yellow-300" />
              <rect x="680" y="370" width="8" height="8" fill="currentColor" className="text-yellow-400 dark:text-yellow-300" />
              
              {/* More buildings */}
              <rect x="750" y="190" width="85" height="210" fill="currentColor" className="text-slate-600 dark:text-slate-400" />
              <rect x="860" y="160" width="75" height="240" fill="currentColor" className="text-slate-600 dark:text-slate-400" />
              <rect x="950" y="220" width="65" height="180" fill="currentColor" className="text-slate-600 dark:text-slate-400" />
              <rect x="1030" y="170" width="80" height="230" fill="currentColor" className="text-slate-600 dark:text-slate-400" />
            </svg>
          </div>

          {/* Floating geometric shapes */}
          <div className="absolute top-20 left-10 w-3 h-3 bg-blue-400 dark:bg-blue-300 rounded-full opacity-60 animate-pulse" />
          <div className="absolute top-40 right-20 w-4 h-4 bg-indigo-400 dark:bg-indigo-300 rounded-full opacity-40 animate-pulse delay-1000" />
          <div className="absolute bottom-1/3 left-1/4 w-2 h-2 bg-amber-400 dark:bg-amber-300 rounded-full opacity-50 animate-pulse delay-2000" />
          <div className="absolute top-1/3 right-1/3 w-3 h-3 bg-green-400 dark:bg-green-300 rounded-full opacity-30 animate-pulse delay-3000" />

          {/* Subtle grid overlay */}
          <div className="absolute inset-0 opacity-5 dark:opacity-3">
            <div className="grid grid-cols-12 h-full w-full">
              {Array.from({ length: 12 }).map((_, i) => (
                <div key={i} className="border-r border-slate-400 dark:border-slate-600" />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Gradient overlay for depth */}
      <div className="absolute inset-0 bg-gradient-to-t from-transparent via-transparent to-white/20 dark:to-slate-900/20" />
    </div>
  );
}; 