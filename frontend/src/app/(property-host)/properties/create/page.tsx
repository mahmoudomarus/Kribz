'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { ArrowLeft, Upload } from 'lucide-react';
import Link from 'next/link';
import { toast } from 'sonner';

const DUBAI_AREAS = [
  'Downtown Dubai',
  'Dubai Marina', 
  'Jumeirah Beach Residence (JBR)',
  'Business Bay',
  'DIFC',
  'Jumeirah',
  'Palm Jumeirah',
  'Dubai Hills',
  'Arabian Ranches',
  'Dubai Investment Park',
  'Deira',
  'Bur Dubai'
];

const COMMON_AMENITIES = [
  'WiFi',
  'Air Conditioning', 
  'Swimming Pool',
  'Gym/Fitness Center',
  'Parking',
  'Balcony/Terrace',
  'Kitchen',
  'Washing Machine',
  'Elevator',
  'Security',
  'Concierge',
  'Beach Access',
  'Metro Access',
  'Shopping Mall Nearby'
];

export default function CreateProperty() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [selectedAmenities, setSelectedAmenities] = useState<string[]>([]);
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    property_type: '',
    area: '',
    street_address: '',
    bedrooms: '',
    bathrooms: '',
    square_feet: '',
    price_per_night: '',
    price_per_month: '',
    images: [] as string[]
  });

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleAmenityToggle = (amenity: string) => {
    setSelectedAmenities(prev => 
      prev.includes(amenity) 
        ? prev.filter(a => a !== amenity)
        : [...prev, amenity]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Prepare property data for your existing API
      const propertyData = {
        title: formData.title,
        description: formData.description,
        property_type: formData.property_type,
        address: {
          street: formData.street_address,
          city: 'Dubai',
          state: 'Dubai',
          country: 'UAE',
          postal_code: '00000'
        },
        bedrooms: parseInt(formData.bedrooms) || 0,
        bathrooms: parseFloat(formData.bathrooms) || 0,
        square_feet: parseInt(formData.square_feet) || 0,
        price_per_night: formData.property_type === 'short_term' ? parseFloat(formData.price_per_night) : null,
        price_per_month: formData.property_type === 'long_term' ? parseFloat(formData.price_per_month) : null,
        amenities: selectedAmenities,
        images: formData.images,
        is_active: true
      };

      // TODO: Call your existing property creation API
      // POST /api/v1/rental/properties/
      console.log('Property data to submit:', propertyData);
      
      // For now, simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      toast.success('Property created successfully!');
      router.push('/property-host/properties');
      
    } catch (error) {
      console.error('Error creating property:', error);
      toast.error('Failed to create property. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/property-host/dashboard" className="flex items-center gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Link>
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Add New Property</h1>
          <p className="text-muted-foreground">
            Create a new property listing for your Dubai rental
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <Card>
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
            <CardDescription>
              Enter the basic details about your property
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="title">Property Title *</Label>
              <Input
                id="title"
                placeholder="e.g., Luxury 2BR Apartment in Downtown Dubai"
                value={formData.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Description *</Label>
              <Textarea
                id="description"
                placeholder="Describe your property, its features, and what makes it special..."
                rows={4}
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="property_type">Rental Type *</Label>
                <Select onValueChange={(value) => handleInputChange('property_type', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select rental type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="short_term">Short-term (Vacation Rental)</SelectItem>
                    <SelectItem value="long_term">Long-term (Residential Lease)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="area">Dubai Area *</Label>
                <Select onValueChange={(value) => handleInputChange('area', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select area" />
                  </SelectTrigger>
                  <SelectContent>
                    {DUBAI_AREAS.map((area) => (
                      <SelectItem key={area} value={area}>{area}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="street_address">Street Address</Label>
              <Input
                id="street_address"
                placeholder="e.g., Burj Khalifa Boulevard"
                value={formData.street_address}
                onChange={(e) => handleInputChange('street_address', e.target.value)}
              />
            </div>
          </CardContent>
        </Card>

        {/* Property Details */}
        <Card>
          <CardHeader>
            <CardTitle>Property Details</CardTitle>
            <CardDescription>
              Specify the size and layout of your property
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="bedrooms">Bedrooms</Label>
                <Input
                  id="bedrooms"
                  type="number"
                  min="0"
                  placeholder="0"
                  value={formData.bedrooms}
                  onChange={(e) => handleInputChange('bedrooms', e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="bathrooms">Bathrooms</Label>
                <Input
                  id="bathrooms"
                  type="number"
                  min="0"
                  step="0.5"
                  placeholder="0"
                  value={formData.bathrooms}
                  onChange={(e) => handleInputChange('bathrooms', e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="square_feet">Square Feet</Label>
                <Input
                  id="square_feet"
                  type="number"
                  min="0"
                  placeholder="0"
                  value={formData.square_feet}
                  onChange={(e) => handleInputChange('square_feet', e.target.value)}
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Pricing */}
        <Card>
          <CardHeader>
            <CardTitle>Pricing</CardTitle>
            <CardDescription>
              Set your rental pricing in AED
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {formData.property_type === 'short_term' && (
              <div className="space-y-2">
                <Label htmlFor="price_per_night">Price per Night (AED) *</Label>
                <Input
                  id="price_per_night"
                  type="number"
                  min="0"
                  step="0.01"
                  placeholder="350.00"
                  value={formData.price_per_night}
                  onChange={(e) => handleInputChange('price_per_night', e.target.value)}
                  required={formData.property_type === 'short_term'}
                />
              </div>
            )}

            {formData.property_type === 'long_term' && (
              <div className="space-y-2">
                <Label htmlFor="price_per_month">Price per Month (AED) *</Label>
                <Input
                  id="price_per_month"
                  type="number"
                  min="0"
                  step="0.01"
                  placeholder="8500.00"
                  value={formData.price_per_month}
                  onChange={(e) => handleInputChange('price_per_month', e.target.value)}
                  required={formData.property_type === 'long_term'}
                />
              </div>
            )}
          </CardContent>
        </Card>

        {/* Amenities */}
        <Card>
          <CardHeader>
            <CardTitle>Amenities</CardTitle>
            <CardDescription>
              Select all amenities available at your property
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {COMMON_AMENITIES.map((amenity) => (
                <div key={amenity} className="flex items-center space-x-2">
                  <Checkbox
                    id={amenity}
                    checked={selectedAmenities.includes(amenity)}
                    onCheckedChange={() => handleAmenityToggle(amenity)}
                  />
                  <Label 
                    htmlFor={amenity} 
                    className="text-sm font-normal cursor-pointer"
                  >
                    {amenity}
                  </Label>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Photos */}
        <Card>
          <CardHeader>
            <CardTitle>Photos</CardTitle>
            <CardDescription>
              Upload high-quality photos of your property (coming soon)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8 text-center">
              <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <p className="text-muted-foreground mb-2">Photo upload feature coming soon</p>
              <p className="text-sm text-muted-foreground">
                For now, you can add your property and upload photos later
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Submit */}
        <div className="flex justify-end gap-4">
          <Button type="button" variant="outline" asChild>
            <Link href="/property-host/dashboard">Cancel</Link>
          </Button>
          <Button type="submit" disabled={isLoading}>
            {isLoading ? 'Creating...' : 'Create Property'}
          </Button>
        </div>
      </form>
    </div>
  );
}
