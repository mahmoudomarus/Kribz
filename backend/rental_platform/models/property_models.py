from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import BaseModel, Field, validator
from enum import Enum

class PropertyType(str, Enum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"

class PropertyAddress(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postal_code: str
    coordinates: Optional[Dict[str, float]] = None  # {"lat": 40.7128, "lng": -74.0060}

class Property(BaseModel):
    id: Optional[str] = None
    account_id: str
    title: str
    description: Optional[str] = None
    property_type: PropertyType
    address: PropertyAddress
    price_per_night: Optional[Decimal] = Field(None, description="For short-term rentals")
    price_per_month: Optional[Decimal] = Field(None, description="For long-term rentals")
    bedrooms: Optional[int] = None
    bathrooms: Optional[Decimal] = None
    square_feet: Optional[int] = None
    amenities: Optional[List[str]] = []
    images: Optional[List[str]] = []  # Array of image URLs
    is_active: bool = True
    listing_agent_id: Optional[str] = None
    owner_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator('price_per_night')
    def validate_short_term_price(cls, v, values):
        if values.get('property_type') == PropertyType.SHORT_TERM and v is None:
            raise ValueError('Short-term rentals must have price_per_night')
        return v

    @validator('price_per_month')
    def validate_long_term_price(cls, v, values):
        if values.get('property_type') == PropertyType.LONG_TERM and v is None:
            raise ValueError('Long-term rentals must have price_per_month')
        return v

    class Config:
        use_enum_values = True
        json_encoders = {
            Decimal: str,
            datetime: lambda v: v.isoformat()
        }

class PropertyCreate(BaseModel):
    account_id: str
    title: str
    description: Optional[str] = None
    property_type: PropertyType
    address: PropertyAddress
    price_per_night: Optional[Decimal] = None
    price_per_month: Optional[Decimal] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[Decimal] = None
    square_feet: Optional[int] = None
    amenities: Optional[List[str]] = []
    images: Optional[List[str]] = []
    listing_agent_id: Optional[str] = None
    owner_id: Optional[str] = None

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    address: Optional[PropertyAddress] = None
    price_per_night: Optional[Decimal] = None
    price_per_month: Optional[Decimal] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[Decimal] = None
    square_feet: Optional[int] = None
    amenities: Optional[List[str]] = None
    images: Optional[List[str]] = None
    is_active: Optional[bool] = None
    listing_agent_id: Optional[str] = None
    owner_id: Optional[str] = None

class ShortTermRental(BaseModel):
    id: Optional[str] = None
    property_id: str
    minimum_nights: int = 1
    maximum_nights: Optional[int] = None
    instant_book: bool = False
    check_in_time: time = time(15, 0)  # 3:00 PM
    check_out_time: time = time(11, 0)  # 11:00 AM
    house_rules: Optional[str] = None
    cancellation_policy: Optional[str] = None
    cleaning_fee: Optional[Decimal] = None
    security_deposit: Optional[Decimal] = None
    extra_guest_fee: Optional[Decimal] = None
    pet_fee: Optional[Decimal] = None
    availability_calendar: Optional[Dict[str, Any]] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            Decimal: str,
            time: lambda v: v.strftime('%H:%M'),
            datetime: lambda v: v.isoformat()
        }

class ShortTermRentalCreate(BaseModel):
    property_id: str
    minimum_nights: int = 1
    maximum_nights: Optional[int] = None
    instant_book: bool = False
    check_in_time: time = time(15, 0)
    check_out_time: time = time(11, 0)
    house_rules: Optional[str] = None
    cancellation_policy: Optional[str] = None
    cleaning_fee: Optional[Decimal] = None
    security_deposit: Optional[Decimal] = None
    extra_guest_fee: Optional[Decimal] = None
    pet_fee: Optional[Decimal] = None
    availability_calendar: Optional[Dict[str, Any]] = {}

class LongTermRental(BaseModel):
    id: Optional[str] = None
    property_id: str
    lease_term_months: int = 12
    security_deposit: Optional[Decimal] = None
    pet_deposit: Optional[Decimal] = None
    application_fee: Optional[Decimal] = None
    income_requirement_multiplier: Decimal = Decimal('3.0')  # 3x monthly rent
    credit_score_minimum: Optional[int] = None
    background_check_required: bool = True
    references_required: int = 2
    available_date: Optional[date] = None
    lease_terms: Optional[str] = None
    utilities_included: Optional[List[str]] = []
    parking_spots: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            Decimal: str,
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

class LongTermRentalCreate(BaseModel):
    property_id: str
    lease_term_months: int = 12
    security_deposit: Optional[Decimal] = None
    pet_deposit: Optional[Decimal] = None
    application_fee: Optional[Decimal] = None
    income_requirement_multiplier: Decimal = Decimal('3.0')
    credit_score_minimum: Optional[int] = None
    background_check_required: bool = True
    references_required: int = 2
    available_date: Optional[date] = None
    lease_terms: Optional[str] = None
    utilities_included: Optional[List[str]] = []
    parking_spots: Optional[int] = None

class PropertySearchFilters(BaseModel):
    property_type: Optional[PropertyType] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    amenities: Optional[List[str]] = []
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    available_from: Optional[date] = None
    available_to: Optional[date] = None
    min_square_feet: Optional[int] = None
    max_square_feet: Optional[int] = None
    instant_book: Optional[bool] = None  # For short-term rentals
    pet_friendly: Optional[bool] = None
    limit: int = Field(20, le=100)
    offset: int = Field(0, ge=0)

class PropertySearchResult(BaseModel):
    properties: List[Property]
    total_count: int
    has_more: bool
    filters_applied: PropertySearchFilters

class PropertyAvailability(BaseModel):
    id: Optional[str] = None
    property_id: str
    available_from: date
    available_to: Optional[date] = None
    is_available: bool = True
    reason_unavailable: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        } 