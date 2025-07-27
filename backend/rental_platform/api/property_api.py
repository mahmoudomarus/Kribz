from typing import List, Optional
from datetime import date
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from fastapi.responses import JSONResponse

from ..models.property_models import (
    Property, PropertyCreate, PropertyUpdate,
    ShortTermRental, ShortTermRentalCreate,
    LongTermRental, LongTermRentalCreate,
    PropertySearchFilters, PropertySearchResult,
    PropertyAvailability, PropertyType
)
from ..services.property_service import PropertyService
from dependencies import get_property_service, get_current_user

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("/", response_model=Property, status_code=status.HTTP_201_CREATED, summary="Create a new property")
async def create_property(
    property_data: PropertyCreate,
    property_service: PropertyService = Depends(get_property_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new property listing for short-term or long-term rentals.
    
    - **property_type**: Either 'short_term' for vacation rentals or 'long_term' for real estate
    - **address**: Complete property address with coordinates (optional)
    - **pricing**: price_per_night for short-term or price_per_month for long-term
    - **amenities**: List of property amenities (pool, wifi, parking, etc.)
    - **images**: List of image URLs for the property
    """
    try:
        # Ensure the property belongs to the current user's account
        property_data.account_id = current_user.get("account_id", current_user["id"])
        
        property = await property_service.create_property(property_data)
        return property
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/search", response_model=PropertySearchResult, summary="Search properties with filters")
async def search_properties(
    property_type: Optional[PropertyType] = Query(None, description="Filter by property type"),
    min_price: Optional[float] = Query(None, description="Minimum price (per night for short-term, per month for long-term)"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    bedrooms: Optional[int] = Query(None, description="Number of bedrooms"),
    bathrooms: Optional[int] = Query(None, description="Minimum number of bathrooms"),
    city: Optional[str] = Query(None, description="City name"),
    state: Optional[str] = Query(None, description="State/province"),
    country: Optional[str] = Query(None, description="Country"),
    available_from: Optional[date] = Query(None, description="Available from date"),
    available_to: Optional[date] = Query(None, description="Available to date"),
    min_square_feet: Optional[int] = Query(None, description="Minimum square footage"),
    max_square_feet: Optional[int] = Query(None, description="Maximum square footage"),
    instant_book: Optional[bool] = Query(None, description="Instant booking available (short-term only)"),
    pet_friendly: Optional[bool] = Query(None, description="Pet-friendly properties"),
    amenities: Optional[List[str]] = Query([], description="Required amenities"),
    limit: int = Query(20, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    property_service: PropertyService = Depends(get_property_service)
):
    """
    Search properties with various filters for both short-term and long-term rentals.
    
    Returns paginated results with property details, total count, and filter information.
    """
    try:
        filters = PropertySearchFilters(
            property_type=property_type,
            min_price=min_price,
            max_price=max_price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            city=city,
            state=state,
            country=country,
            available_from=available_from,
            available_to=available_to,
            min_square_feet=min_square_feet,
            max_square_feet=max_square_feet,
            instant_book=instant_book,
            pet_friendly=pet_friendly,
            amenities=amenities,
            limit=limit,
            offset=offset
        )
        
        return await property_service.search_properties(filters)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/my-properties", response_model=List[Property], summary="Get current user's properties")
async def get_my_properties(
    limit: int = Query(20, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    property_service: PropertyService = Depends(get_property_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all properties owned by the current user.
    """
    try:
        account_id = current_user.get("account_id", current_user["id"])
        return await property_service.get_properties_by_account(account_id, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{property_id}", response_model=Property, summary="Get property by ID")
async def get_property(
    property_id: str = Path(..., description="Property ID"),
    property_service: PropertyService = Depends(get_property_service)
):
    """
    Get detailed information about a specific property.
    """
    try:
        property = await property_service.get_property(property_id)
        if not property:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
        return property
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{property_id}", response_model=Property, summary="Update property")
async def update_property(
    property_id: str = Path(..., description="Property ID"),
    property_data: PropertyUpdate = ...,
    property_service: PropertyService = Depends(get_property_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Update property details. Only property owners or listing agents can update properties.
    """
    try:
        # Check if property exists and user has permission
        existing_property = await property_service.get_property(property_id)
        if not existing_property:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
        
        account_id = current_user.get("account_id", current_user["id"])
        user_id = current_user["id"]
        
        # Check permissions
        if (existing_property.account_id != account_id and 
            existing_property.owner_id != user_id and 
            existing_property.listing_agent_id != user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this property")
        
        updated_property = await property_service.update_property(property_id, property_data)
        if not updated_property:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
        
        return updated_property
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete property")
async def delete_property(
    property_id: str = Path(..., description="Property ID"),
    property_service: PropertyService = Depends(get_property_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Soft delete a property (sets is_active to False).
    Only property owners can delete properties.
    """
    try:
        # Check if property exists and user has permission
        existing_property = await property_service.get_property(property_id)
        if not existing_property:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
        
        account_id = current_user.get("account_id", current_user["id"])
        user_id = current_user["id"]
        
        # Check permissions (only owners can delete)
        if existing_property.account_id != account_id and existing_property.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this property")
        
        success = await property_service.delete_property(property_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
        
        return JSONResponse(content={"message": "Property deleted successfully"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Short-term rental endpoints
@router.post("/{property_id}/short-term", response_model=ShortTermRental, status_code=status.HTTP_201_CREATED, summary="Create short-term rental details")
async def create_short_term_rental(
    property_id: str = Path(..., description="Property ID"),
    rental_data: ShortTermRentalCreate = ...,
    property_service: PropertyService = Depends(get_property_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Create detailed short-term rental configuration for vacation rentals.
    
    Includes check-in/out times, house rules, fees, and availability calendar.
    """
    try:
        # Verify property exists and user has permission
        property = await property_service.get_property(property_id)
        if not property:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
        
        if property.property_type != PropertyType.SHORT_TERM:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Property is not a short-term rental")
        
        account_id = current_user.get("account_id", current_user["id"])
        user_id = current_user["id"]
        
        if (property.account_id != account_id and 
            property.owner_id != user_id and 
            property.listing_agent_id != user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to manage this property")
        
        return await property_service.create_short_term_rental(property_id, rental_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{property_id}/short-term", response_model=ShortTermRental, summary="Get short-term rental details")
async def get_short_term_rental(
    property_id: str = Path(..., description="Property ID"),
    property_service: PropertyService = Depends(get_property_service)
):
    """
    Get short-term rental configuration details.
    """
    try:
        rental = await property_service.get_short_term_rental(property_id)
        if not rental:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short-term rental details not found")
        return rental
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Long-term rental endpoints
@router.post("/{property_id}/long-term", response_model=LongTermRental, status_code=status.HTTP_201_CREATED, summary="Create long-term rental details")
async def create_long_term_rental(
    property_id: str = Path(..., description="Property ID"),
    rental_data: LongTermRentalCreate = ...,
    property_service: PropertyService = Depends(get_property_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Create detailed long-term rental configuration for real estate properties.
    
    Includes lease terms, deposit requirements, and tenant screening criteria.
    """
    try:
        # Verify property exists and user has permission
        property = await property_service.get_property(property_id)
        if not property:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
        
        if property.property_type != PropertyType.LONG_TERM:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Property is not a long-term rental")
        
        account_id = current_user.get("account_id", current_user["id"])
        user_id = current_user["id"]
        
        if (property.account_id != account_id and 
            property.owner_id != user_id and 
            property.listing_agent_id != user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to manage this property")
        
        return await property_service.create_long_term_rental(property_id, rental_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{property_id}/long-term", response_model=LongTermRental, summary="Get long-term rental details")
async def get_long_term_rental(
    property_id: str = Path(..., description="Property ID"),
    property_service: PropertyService = Depends(get_property_service)
):
    """
    Get long-term rental configuration details.
    """
    try:
        rental = await property_service.get_long_term_rental(property_id)
        if not rental:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Long-term rental details not found")
        return rental
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Property availability endpoints
@router.post("/{property_id}/availability", response_model=PropertyAvailability, status_code=status.HTTP_201_CREATED, summary="Set property availability")
async def set_property_availability(
    property_id: str = Path(..., description="Property ID"),
    available_from: date = Query(..., description="Available from date"),
    available_to: Optional[date] = Query(None, description="Available to date (optional for ongoing availability)"),
    is_available: bool = Query(True, description="Whether property is available"),
    reason: Optional[str] = Query(None, description="Reason for unavailability"),
    property_service: PropertyService = Depends(get_property_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Set property availability for specific date ranges.
    
    Used for blocking dates for maintenance, owner use, or existing bookings.
    """
    try:
        # Verify property exists and user has permission
        property = await property_service.get_property(property_id)
        if not property:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
        
        account_id = current_user.get("account_id", current_user["id"])
        user_id = current_user["id"]
        
        if (property.account_id != account_id and 
            property.owner_id != user_id and 
            property.listing_agent_id != user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to manage this property")
        
        return await property_service.set_property_availability(
            property_id, available_from, available_to, is_available, reason
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{property_id}/availability", response_model=List[PropertyAvailability], summary="Get property availability")
async def get_property_availability(
    property_id: str = Path(..., description="Property ID"),
    date_from: Optional[date] = Query(None, description="Start date for availability check"),
    date_to: Optional[date] = Query(None, description="End date for availability check"),
    property_service: PropertyService = Depends(get_property_service)
):
    """
    Get property availability for a date range.
    
    Returns all availability records for the property within the specified date range.
    """
    try:
        return await property_service.get_property_availability(property_id, date_from, date_to)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{property_id}/available/{check_date}", response_model=dict, summary="Check property availability on specific date")
async def check_property_availability(
    property_id: str = Path(..., description="Property ID"),
    check_date: date = Path(..., description="Date to check availability"),
    property_service: PropertyService = Depends(get_property_service)
):
    """
    Check if a property is available on a specific date.
    
    Returns a boolean indicating availability status.
    """
    try:
        is_available = await property_service.check_property_available(property_id, check_date)
        return {"property_id": property_id, "date": check_date, "is_available": is_available}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) 