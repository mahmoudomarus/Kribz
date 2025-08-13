'use client';

import * as React from 'react';
import Link from 'next/link';
import { 
  Home, 
  Building, 
  Calendar, 
  MessageSquare, 
  BarChart3, 
  Settings,
  Plus
} from 'lucide-react';

import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarFooter,
} from '@/components/ui/sidebar';
import { NavUserWithTeams } from '@/components/sidebar/nav-user-with-teams';

const hostNavItems = [
  {
    title: 'Dashboard',
    url: '/property-host/dashboard',
    icon: Home,
  },
  {
    title: 'Properties',
    url: '/property-host/properties',
    icon: Building,
  },
  {
    title: 'Bookings',
    url: '/property-host/bookings',
    icon: Calendar,
  },
  {
    title: 'Messages',
    url: '/property-host/messages',
    icon: MessageSquare,
  },
  {
    title: 'Analytics',
    url: '/property-host/analytics',
    icon: BarChart3,
  },
  {
    title: 'Settings',
    url: '/property-host/settings',
    icon: Settings,
  },
];

export function HostSidebar() {
  return (
    <Sidebar variant="inset">
      <SidebarHeader>
        <div className="flex items-center gap-2 px-4 py-2">
          <Building className="h-6 w-6 text-primary" />
          <div className="flex flex-col">
            <span className="font-semibold text-sm">Property Host</span>
            <span className="text-xs text-muted-foreground">Rental Management</span>
          </div>
        </div>
      </SidebarHeader>
      
      <SidebarContent>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild className="w-full">
              <Link href="/property-host/properties/create" className="flex items-center gap-2">
                <Plus className="h-4 w-4" />
                <span>Add Property</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
          
          {hostNavItems.map((item) => (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton asChild>
                <Link href={item.url} className="flex items-center gap-2">
                  <item.icon className="h-4 w-4" />
                  <span>{item.title}</span>
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarContent>
      
      <SidebarFooter>
        <NavUserWithTeams />
      </SidebarFooter>
    </Sidebar>
  );
}
