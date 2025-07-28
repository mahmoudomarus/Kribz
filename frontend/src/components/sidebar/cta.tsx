import { Button } from '@/components/ui/button';
import Link from 'next/link';
import { Home, ExternalLink, Star } from 'lucide-react';

export function CTACard() {
  return (
    <div className="rounded-xl bg-gradient-to-br from-blue-50 to-blue-200 dark:from-blue-950/40 dark:to-blue-900/40 shadow-sm border border-blue-200/50 dark:border-blue-800/50 p-4 transition-all">
      <div className="flex flex-col space-y-4">
        <div className="flex flex-col">
          <span className="text-sm font-medium text-foreground">
            List Your Property
          </span>
          <span className="text-xs text-muted-foreground mt-0.5">
            Start earning with Krib AI
          </span>
        </div>

        <div>
          <Button
            size="sm"
            className="w-full text-xs bg-blue-600 hover:bg-blue-700 text-white"
          >
            <Home className="mr-1.5 h-3.5 w-3.5" />
            Add Property
          </Button>
        </div>

        <div className="flex items-center pt-1 border-t border-blue-200/50 dark:border-blue-800/30 mt-1">
          <Link
            href="/pricing"
            className="flex items-center text-xs text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 transition-colors"
          >
            <Star className="mr-1.5 h-3.5 w-3.5" />
            View Pricing
            <ExternalLink className="ml-1 h-3 w-3" />
          </Link>
        </div>
      </div>
    </div>
  );
}
