from typing import List, Optional, Dict, Any
from datetime import datetime, date
from supabase import Client
from ..models.property_models import (
    Property, PropertyCreate, PropertyUpdate,
    ShortTermRental, ShortTermRentalCreate,
    LongTermRental, LongTermRentalCreate,
    PropertySearchFilters, PropertySearchResult,
    PropertyAvailability, PropertyType
)

class PropertyService:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client

    async def create_property(self, property_data: PropertyCreate) -> Property:
        """Create a new property listing"""
        try:
            # Insert property
            property_dict = property_data.dict()
            property_dict['address'] = property_dict['address'].dict() if hasattr(property_dict['address'], 'dict') else property_dict['address']
            
            result = self.supabase.table('properties').insert(property_dict).execute()
            
            if not result.data:
                raise Exception("Failed to create property")
            
            property_id = result.data[0]['id']
            
            # Create rental-specific record
            if property_data.property_type == PropertyType.SHORT_TERM:
                await self._create_short_term_rental(property_id)
            elif property_data.property_type == PropertyType.LONG_TERM:
                await self._create_long_term_rental(property_id)
            
            return Property(**result.data[0])
            
        except Exception as e:
            raise Exception(f"Error creating property: {str(e)}")

    async def get_property(self, property_id: str) -> Optional[Property]:
        """Get a property by ID"""
        try:
            result = self.supabase.table('properties').select('*').eq('id', property_id).single().execute()
            
            if result.data:
                return Property(**result.data)
            return None
            
        except Exception as e:
            raise Exception(f"Error fetching property: {str(e)}")

    async def update_property(self, property_id: str, property_data: PropertyUpdate) -> Optional[Property]:
        """Update a property"""
        try:
            update_dict = {k: v for k, v in property_data.dict(exclude_unset=True).items() if v is not None}
            
            if 'address' in update_dict:
                update_dict['address'] = update_dict['address'].dict() if hasattr(update_dict['address'], 'dict') else update_dict['address']
            
            result = self.supabase.table('properties').update(update_dict).eq('id', property_id).execute()
            
            if result.data:
                return Property(**result.data[0])
            return None
            
        except Exception as e:
            raise Exception(f"Error updating property: {str(e)}")

    async def delete_property(self, property_id: str) -> bool:
        """Soft delete a property by setting is_active to False"""
        try:
            result = self.supabase.table('properties').update({'is_active': False}).eq('id', property_id).execute()
            return bool(result.data)
            
        except Exception as e:
            raise Exception(f"Error deleting property: {str(e)}")

    async def search_properties(self, filters: PropertySearchFilters) -> PropertySearchResult:
        """Search properties with filters"""
        try:
            query = self.supabase.table('properties').select('*', count='exact')
            
            # Apply filters
            query = query.eq('is_active', True)
            
            if filters.property_type:
                query = query.eq('property_type', filters.property_type.value)
            
            if filters.min_price and filters.property_type == PropertyType.SHORT_TERM:
                query = query.gte('price_per_night', str(filters.min_price))
            elif filters.min_price and filters.property_type == PropertyType.LONG_TERM:
                query = query.gte('price_per_month', str(filters.min_price))
            
            if filters.max_price and filters.property_type == PropertyType.SHORT_TERM:
                query = query.lte('price_per_night', str(filters.max_price))
            elif filters.max_price and filters.property_type == PropertyType.LONG_TERM:
                query = query.lte('price_per_month', str(filters.max_price))
            
            if filters.bedrooms:
                query = query.eq('bedrooms', filters.bedrooms)
            
            if filters.bathrooms:
                query = query.gte('bathrooms', filters.bathrooms)
            
            if filters.city:
                query = query.ilike('address->>city', f'%{filters.city}%')
            
            if filters.state:
                query = query.ilike('address->>state', f'%{filters.state}%')
            
            if filters.country:
                query = query.ilike('address->>country', f'%{filters.country}%')
            
            if filters.min_square_feet:
                query = query.gte('square_feet', filters.min_square_feet)
            
            if filters.max_square_feet:
                query = query.lte('square_feet', filters.max_square_feet)
            
            # Apply amenities filter
            if filters.amenities:
                for amenity in filters.amenities:
                    query = query.contains('amenities', [amenity])
            
            # Apply pagination
            query = query.range(filters.offset, filters.offset + filters.limit - 1)
            
            result = query.execute()
            
            properties = [Property(**prop) for prop in result.data] if result.data else []
            total_count = result.count or 0
            has_more = (filters.offset + filters.limit) < total_count
            
            return PropertySearchResult(
                properties=properties,
                total_count=total_count,
                has_more=has_more,
                filters_applied=filters
            )
            
        except Exception as e:
            raise Exception(f"Error searching properties: {str(e)}")

    async def get_properties_by_account(self, account_id: str, limit: int = 20, offset: int = 0) -> List[Property]:
        """Get all properties for an account"""
        try:
            result = self.supabase.table('properties').select('*').eq('account_id', account_id).eq('is_active', True).range(offset, offset + limit - 1).execute()
            
            return [Property(**prop) for prop in result.data] if result.data else []
            
        except Exception as e:
            raise Exception(f"Error fetching account properties: {str(e)}")

    # Short-term rental specific methods
    async def create_short_term_rental(self, property_id: str, rental_data: ShortTermRentalCreate) -> ShortTermRental:
        """Create short-term rental details"""
        try:
            rental_dict = rental_data.dict()
            rental_dict['property_id'] = property_id
            
            # Convert time objects to strings
            if 'check_in_time' in rental_dict:
                rental_dict['check_in_time'] = rental_dict['check_in_time'].strftime('%H:%M:%S')
            if 'check_out_time' in rental_dict:
                rental_dict['check_out_time'] = rental_dict['check_out_time'].strftime('%H:%M:%S')
            
            result = self.supabase.table('short_term_rentals').insert(rental_dict).execute()
            
            if result.data:
                return ShortTermRental(**result.data[0])
            raise Exception("Failed to create short-term rental")
            
        except Exception as e:
            raise Exception(f"Error creating short-term rental: {str(e)}")

    async def get_short_term_rental(self, property_id: str) -> Optional[ShortTermRental]:
        """Get short-term rental details by property ID"""
        try:
            result = self.supabase.table('short_term_rentals').select('*').eq('property_id', property_id).single().execute()
            
            if result.data:
                return ShortTermRental(**result.data)
            return None
            
        except Exception as e:
            raise Exception(f"Error fetching short-term rental: {str(e)}")

    # Long-term rental specific methods
    async def create_long_term_rental(self, property_id: str, rental_data: LongTermRentalCreate) -> LongTermRental:
        """Create long-term rental details"""
        try:
            rental_dict = rental_data.dict()
            rental_dict['property_id'] = property_id
            
            result = self.supabase.table('long_term_rentals').insert(rental_dict).execute()
            
            if result.data:
                return LongTermRental(**result.data[0])
            raise Exception("Failed to create long-term rental")
            
        except Exception as e:
            raise Exception(f"Error creating long-term rental: {str(e)}")

    async def get_long_term_rental(self, property_id: str) -> Optional[LongTermRental]:
        """Get long-term rental details by property ID"""
        try:
            result = self.supabase.table('long_term_rentals').select('*').eq('property_id', property_id).single().execute()
            
            if result.data:
                return LongTermRental(**result.data)
            return None
            
        except Exception as e:
            raise Exception(f"Error fetching long-term rental: {str(e)}")

    # Property availability methods
    async def set_property_availability(self, property_id: str, available_from: date, available_to: Optional[date] = None, is_available: bool = True, reason: Optional[str] = None) -> PropertyAvailability:
        """Set property availability"""
        try:
            availability_data = {
                'property_id': property_id,
                'available_from': available_from.isoformat(),
                'available_to': available_to.isoformat() if available_to else None,
                'is_available': is_available,
                'reason_unavailable': reason if not is_available else None
            }
            
            result = self.supabase.table('property_availability').insert(availability_data).execute()
            
            if result.data:
                return PropertyAvailability(**result.data[0])
            raise Exception("Failed to set property availability")
            
        except Exception as e:
            raise Exception(f"Error setting property availability: {str(e)}")

    async def get_property_availability(self, property_id: str, date_from: Optional[date] = None, date_to: Optional[date] = None) -> List[PropertyAvailability]:
        """Get property availability for date range"""
        try:
            query = self.supabase.table('property_availability').select('*').eq('property_id', property_id)
            
            if date_from:
                query = query.gte('available_from', date_from.isoformat())
            if date_to:
                query = query.lte('available_to', date_to.isoformat())
            
            result = query.execute()
            
            return [PropertyAvailability(**avail) for avail in result.data] if result.data else []
            
        except Exception as e:
            raise Exception(f"Error fetching property availability: {str(e)}")

    async def check_property_available(self, property_id: str, check_date: date) -> bool:
        """Check if property is available on a specific date"""
        try:
            result = self.supabase.table('property_availability').select('is_available').eq('property_id', property_id).lte('available_from', check_date.isoformat()).gte('available_to', check_date.isoformat()).execute()
            
            if result.data:
                return all(avail['is_available'] for avail in result.data)
            return True  # No availability records means available by default
            
        except Exception as e:
            raise Exception(f"Error checking property availability: {str(e)}")

    # Helper methods
    async def _create_short_term_rental(self, property_id: str):
        """Create default short-term rental record"""
        default_rental = ShortTermRentalCreate(property_id=property_id)
        await self.create_short_term_rental(property_id, default_rental)

    async def _create_long_term_rental(self, property_id: str):
        """Create default long-term rental record"""
        default_rental = LongTermRentalCreate(property_id=property_id)
        await self.create_long_term_rental(property_id, default_rental) 