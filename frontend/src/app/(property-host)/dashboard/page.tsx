'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  Building, 
  Calendar, 
  DollarSign, 
  TrendingUp,
  Plus,
  Eye,
  MessageSquare
} from 'lucide-react';
import Link from 'next/link';

// Mock data - will be replaced with real API calls
const mockStats = {
  totalProperties: 0,
  activeBookings: 0,
  monthlyRevenue: 0,
  viewsThisMonth: 0
};

const mockRecentActivity = [
  // Will be populated with real data
];

export default function HostDashboard() {
  const [stats, setStats] = useState(mockStats);
  const [recentActivity, setRecentActivity] = useState(mockRecentActivity);

  // TODO: Replace with real API calls to your rental platform
  useEffect(() => {
    // Fetch user's properties: GET /api/v1/rental/properties/my-properties
    // Fetch user's bookings: GET /api/v1/rental/bookings/requests/my-bookings  
    // Calculate stats from the data
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Property Dashboard</h1>
          <p className="text-muted-foreground">
            Manage your Dubai rental properties
          </p>
        </div>
        <Button asChild>
          <Link href="/property-host/properties/create" className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            Add Property
          </Link>
        </Button>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Properties</CardTitle>
            <Building className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalProperties}</div>
            <p className="text-xs text-muted-foreground">
              Active listings on the platform
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Bookings</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.activeBookings}</div>
            <p className="text-xs text-muted-foreground">
              Current and upcoming reservations
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">AED {stats.monthlyRevenue.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              Revenue from bookings this month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Property Views</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.viewsThisMonth}</div>
            <p className="text-xs text-muted-foreground">
              Views across all properties this month
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card className="cursor-pointer hover:shadow-md transition-shadow">
          <Link href="/property-host/properties/create">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Plus className="h-5 w-5" />
                List New Property
              </CardTitle>
              <CardDescription>
                Add a new property to your portfolio
              </CardDescription>
            </CardHeader>
          </Link>
        </Card>

        <Card className="cursor-pointer hover:shadow-md transition-shadow">
          <Link href="/property-host/properties">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Building className="h-5 w-5" />
                Manage Properties
              </CardTitle>
              <CardDescription>
                Edit listings, update pricing, and availability
              </CardDescription>
            </CardHeader>
          </Link>
        </Card>

        <Card className="cursor-pointer hover:shadow-md transition-shadow">
          <Link href="/property-host/bookings">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                View Bookings
              </CardTitle>
              <CardDescription>
                Manage reservations and guest requests
              </CardDescription>
            </CardHeader>
          </Link>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
          <CardDescription>
            Latest updates from your properties
          </CardDescription>
        </CardHeader>
        <CardContent>
          {recentActivity.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              <MessageSquare className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No recent activity</p>
              <p className="text-sm">Activity will appear here once you start getting bookings and inquiries</p>
            </div>
          ) : (
            <div className="space-y-4">
              {recentActivity.map((activity, index) => (
                <div key={index} className="flex items-center space-x-4">
                  {/* Activity items will be rendered here */}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Getting Started */}
      <Card>
        <CardHeader>
          <CardTitle>Getting Started</CardTitle>
          <CardDescription>
            Complete these steps to start hosting on our platform
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-muted-foreground rounded-full" />
              <span className="text-sm">Add your first property listing</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-muted-foreground rounded-full" />
              <span className="text-sm">Upload high-quality photos</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-muted-foreground rounded-full" />
              <span className="text-sm">Set competitive pricing</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-muted-foreground rounded-full" />
              <span className="text-sm">Configure availability calendar</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
