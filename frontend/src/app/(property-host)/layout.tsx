'use client';

import { SidebarProvider } from '@/components/ui/sidebar';
import { HostSidebar } from '@/components/host/host-sidebar';
import { BackgroundAALChecker } from '@/components/auth/background-aal-checker';

export default function HostLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <BackgroundAALChecker>
      <SidebarProvider>
        <div className="flex h-screen w-full">
          <HostSidebar />
          <main className="flex-1 overflow-auto">
            <div className="container mx-auto px-4 py-6">
              {children}
            </div>
          </main>
        </div>
      </SidebarProvider>
    </BackgroundAALChecker>
  );
}
