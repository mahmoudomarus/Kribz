import { SectionHeader } from '@/components/home/section-header';
import { siteConfig } from '@/lib/home';
import { Search, Home, FileText, CreditCard, BarChart3, Users } from 'lucide-react';
import Link from 'next/link';

export function OpenSourceSection() {
  return (
    <section
      id="features"
      className="flex flex-col items-center justify-center w-full relative pb-18"
    >
      <div className="w-full max-w-6xl mx-auto px-6">
        <SectionHeader>
          <h2 className="text-3xl md:text-4xl font-medium tracking-tighter text-center text-balance pb-1">
            Powerful Rental Features
          </h2>
          <p className="text-muted-foreground text-center text-balance font-medium">
            Everything you need to find, manage, and optimize your rental properties with AI.
          </p>
        </SectionHeader>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-12">
          <div className="rounded-xl bg-[#F3F4F6] dark:bg-[#F9FAFB]/[0.02] border border-border p-6">
            <div className="flex flex-col gap-6">
              <div className="flex items-center gap-2 text-primary font-medium">
                <Search className="h-5 w-5" />
                <span>Smart Property Search</span>
              </div>
              <div className="relative">
                <h3 className="text-2xl font-semibold tracking-tight">
                  AI-Powered Property Discovery
                </h3>
                <p className="text-muted-foreground mt-2">
                  Find perfect vacation rentals and long-term properties with intelligent search,
                  personalized recommendations, and real-time availability.
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold bg-secondary/10 border-secondary/20 text-secondary">
                  Smart Filters
                </span>
                <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold bg-secondary/10 border-secondary/20 text-secondary">
                  Price Optimization
                </span>
                <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold bg-secondary/10 border-secondary/20 text-secondary">
                  Real-time Data
                </span>
              </div>
              <Link
                href="/search"
                className="group inline-flex h-10 items-center justify-center gap-2 text-sm font-medium tracking-wide rounded-full text-primary-foreground dark:text-black px-6 shadow-[inset_0_1px_2px_rgba(255,255,255,0.25),0_3px_3px_-1.5px_rgba(16,24,40,0.06),0_1px_1px_rgba(16,24,40,0.08)] bg-primary dark:bg-white hover:bg-primary/90 dark:hover:bg-white/90 transition-all duration-200 w-fit"
              >
                <span>Search Properties</span>
                <span className="inline-flex items-center justify-center size-5 rounded-full bg-white/20 dark:bg-black/10 group-hover:bg-white/30 dark:group-hover:bg-black/20 transition-colors duration-200">
                  <svg
                    width="12"
                    height="12"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    className="text-primary-foreground dark:text-black"
                  >
                    <path
                      d="M7 17L17 7M17 7H8M17 7V16"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </span>
              </Link>
            </div>
          </div>

          <div className="rounded-xl bg-[#F3F4F6] dark:bg-[#F9FAFB]/[0.02] border border-border p-6">
            <div className="flex flex-col gap-6">
              <h3 className="text-xl md:text-2xl font-medium tracking-tight">
                Complete Rental Management
              </h3>
              <p className="text-muted-foreground">
                From property listings to lease signing, manage every aspect of your rental
                business with AI automation and seamless integrations.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-start gap-3">
                  <div className="rounded-full bg-secondary/10 p-2 mt-0.5">
                    <Home className="h-4 w-4 text-secondary" />
                  </div>
                  <div>
                    <h4 className="font-medium">Property Management</h4>
                    <p className="text-muted-foreground text-sm">
                      List and manage properties
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="rounded-full bg-secondary/10 p-2 mt-0.5">
                    <FileText className="h-4 w-4 text-secondary" />
                  </div>
                  <div>
                    <h4 className="font-medium">DocuSign Integration</h4>
                    <p className="text-muted-foreground text-sm">
                      Digital lease signing
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="rounded-full bg-secondary/10 p-2 mt-0.5">
                    <CreditCard className="h-4 w-4 text-secondary" />
                  </div>
                  <div>
                    <h4 className="font-medium">Payment Processing</h4>
                    <p className="text-muted-foreground text-sm">
                      Secure transactions
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="rounded-full bg-secondary/10 p-2 mt-0.5">
                    <BarChart3 className="h-4 w-4 text-secondary" />
                  </div>
                  <div>
                    <h4 className="font-medium">Analytics</h4>
                    <p className="text-muted-foreground text-sm">
                      Performance insights
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
