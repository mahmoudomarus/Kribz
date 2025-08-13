'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Building, 
  Plus, 
  Edit, 
  Eye, 
  Calendar,
  MapPin,
  Bed,
  Bath,
  Square
} from 'lucide-react';
import Link from 'next/link';

// Mock data - will be replaced with real API calls
const mockProperties = [
  // Will be populated from GET /api/v1/rental/properties/my-properties
];

export default function HostProperties() {
  const [properties, setProperties] = useState(mockProperties);
  const [isLoading, setIsLoading] = useState(true);

  // TODO: Replace with real API call
  useEffect(() => {
    // Fetch user's properties: GET /api/v1/rental/properties/my-properties
    const fetchProperties = async () => {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        setProperties(mockProperties);
      } catch (error) {
        console.error('Error fetching properties:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProperties();
  }, []);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">My Properties</h1>
          <Button asChild>
            <Link href="/property-host/properties/create">
              <Plus className="h-4 w-4 mr-2" />
              Add Property
            </Link>
          </Button>
        </div>
        
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader>
                <div className="h-4 bg-muted rounded w-3/4" />
                <div className="h-3 bg-muted rounded w-1/2" />
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="h-3 bg-muted rounded" />
                  <div className="h-3 bg-muted rounded w-2/3" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">My Properties</h1>
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

      {/* Properties List */}
      {properties.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Building className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No Properties Yet</h3>
            <p className="text-muted-foreground text-center mb-6">
              Start earning by adding your first property to the platform
            </p>
            <Button asChild>
              <Link href="/property-host/properties/create" className="flex items-center gap-2">
                <Plus className="h-4 w-4" />
                Add Your First Property
              </Link>
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {properties.map((property) => (
            <Card key={property.id} className="hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg line-clamp-2">{property.title}</CardTitle>
                    <CardDescription className="flex items-center gap-1 mt-1">
                      <MapPin className="h-3 w-3" />
                      {property.address?.street}, {property.address?.city}
                    </CardDescription>
                  </div>
                  <Badge variant={property.is_active ? "default" : "secondary"}>
                    {property.is_active ? "Active" : "Inactive"}
                  </Badge>
                </div>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {/* Property Details */}
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Bed className="h-4 w-4" />
                    {property.bedrooms} bed
                  </div>
                  <div className="flex items-center gap-1">
                    <Bath className="h-4 w-4" />
                    {property.bathrooms} bath
                  </div>
                  <div className="flex items-center gap-1">
                    <Square className="h-4 w-4" />
                    {property.square_feet} sqft
                  </div>
                </div>

                {/* Pricing */}
                <div className="text-lg font-semibold">
                  {property.property_type === 'short_term' 
                    ? `AED ${property.price_per_night}/night`
                    : `AED ${property.price_per_month}/month`
                  }
                </div>

                {/* Actions */}
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="flex-1">
                    <Eye className="h-4 w-4 mr-2" />
                    View
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1">
                    <Edit className="h-4 w-4 mr-2" />
                    Edit
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1">
                    <Calendar className="h-4 w-4 mr-2" />
                    Calendar
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
