from typing import List, Optional
from datetime import datetime, date
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from fastapi.responses import JSONResponse

from ..models.booking_models import (
    BookingRequest, BookingRequestCreate, BookingRequestUpdate,
    RentalApplication, RentalApplicationCreate, RentalApplicationUpdate,
    ViewingSchedule, ViewingScheduleCreate, ViewingScheduleUpdate,
    BookingStatus, ApplicationStatus, ViewingStatus,
    BookingSearchFilters, ApplicationSearchFilters,
    BookingSearchResult, ApplicationSearchResult
)
from ..services.booking_service import BookingService
from dependencies import get_booking_service, get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings & Applications"])

# ============================================================================
# BOOKING REQUESTS (Short-term rentals / Vacation bookings)
# ============================================================================

@router.post("/requests", response_model=BookingRequest, status_code=status.HTTP_201_CREATED, summary="Create booking request")
async def create_booking_request(
    booking_data: BookingRequestCreate,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new booking request for a short-term rental (vacation booking).
    
    - **property_id**: ID of the short-term rental property
    - **check_in_date**: Arrival date
    - **check_out_date**: Departure date
    - **num_guests**: Number of guests (affects pricing if extra guest fees apply)
    - **num_pets**: Number of pets (affects pricing if pet fees apply)
    - **guest_information**: Contact details and preferences
    
    The system will automatically:
    - Verify property availability
    - Calculate total pricing including fees
    - Check for booking conflicts
    """
    try:
        guest_id = current_user["id"]
        booking = await booking_service.create_booking_request(booking_data, guest_id)
        return booking
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/requests/search", response_model=BookingSearchResult, summary="Search booking requests")
async def search_booking_requests(
    property_id: Optional[str] = Query(None, description="Filter by property ID"),
    booking_status: Optional[BookingStatus] = Query(None, description="Filter by booking status"),
    check_in_from: Optional[date] = Query(None, description="Check-in date from"),
    check_in_to: Optional[date] = Query(None, description="Check-in date to"),
    check_out_from: Optional[date] = Query(None, description="Check-out date from"),
    check_out_to: Optional[date] = Query(None, description="Check-out date to"),
    min_amount: Optional[float] = Query(None, description="Minimum booking amount"),
    max_amount: Optional[float] = Query(None, description="Maximum booking amount"),
    limit: int = Query(20, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Search booking requests with various filters.
    
    Property owners and agents can search all bookings for their properties.
    Guests can only search their own bookings.
    """
    try:
        # For guests, restrict to their own bookings
        guest_id = current_user["id"] if not current_user.get("is_agent") else None
        
        filters = BookingSearchFilters(
            property_id=property_id,
            guest_id=guest_id,
            booking_status=booking_status,
            check_in_from=check_in_from,
            check_in_to=check_in_to,
            check_out_from=check_out_from,
            check_out_to=check_out_to,
            min_amount=min_amount,
            max_amount=max_amount,
            limit=limit,
            offset=offset
        )
        
        return await booking_service.search_bookings(filters)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/requests/my-bookings", response_model=List[BookingRequest], summary="Get current user's bookings")
async def get_my_bookings(
    limit: int = Query(20, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all booking requests made by the current user.
    """
    try:
        guest_id = current_user["id"]
        return await booking_service.get_bookings_by_guest(guest_id, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/requests/{booking_id}", response_model=BookingRequest, summary="Get booking request by ID")
async def get_booking_request(
    booking_id: str = Path(..., description="Booking request ID"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed information about a specific booking request.
    """
    try:
        booking = await booking_service.get_booking_request(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking request not found")
        
        # Check permissions
        if booking.guest_id != current_user["id"] and not current_user.get("is_agent"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this booking")
        
        return booking
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/requests/{booking_id}", response_model=BookingRequest, summary="Update booking request")
async def update_booking_request(
    booking_id: str = Path(..., description="Booking request ID"),
    booking_data: BookingRequestUpdate = ...,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Update booking request details.
    
    Guests can update their pending bookings.
    Property owners/agents can update booking status.
    """
    try:
        # Check if booking exists and user has permission
        existing_booking = await booking_service.get_booking_request(booking_id)
        if not existing_booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking request not found")
        
        # Permission check
        if existing_booking.guest_id != current_user["id"] and not current_user.get("is_agent"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this booking")
        
        updated_booking = await booking_service.update_booking_request(booking_id, booking_data)
        if not updated_booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking request not found")
        
        return updated_booking
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/requests/{booking_id}/cancel", response_model=dict, summary="Cancel booking request")
async def cancel_booking_request(
    booking_id: str = Path(..., description="Booking request ID"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Cancel a booking request.
    
    Both guests and property owners can cancel bookings with appropriate policies.
    """
    try:
        # Check if booking exists and user has permission
        existing_booking = await booking_service.get_booking_request(booking_id)
        if not existing_booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking request not found")
        
        if existing_booking.guest_id != current_user["id"] and not current_user.get("is_agent"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to cancel this booking")
        
        success = await booking_service.cancel_booking_request(booking_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking request not found")
        
        return {"message": "Booking request cancelled successfully", "booking_id": booking_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/properties/{property_id}/bookings", response_model=List[BookingRequest], summary="Get property bookings")
async def get_property_bookings(
    property_id: str = Path(..., description="Property ID"),
    limit: int = Query(20, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all booking requests for a specific property.
    
    Only property owners and agents can access this endpoint.
    """
    try:
        # TODO: Add property ownership verification
        return await booking_service.get_bookings_by_property(property_id, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# ============================================================================
# RENTAL APPLICATIONS (Long-term rentals)
# ============================================================================

@router.post("/applications", response_model=RentalApplication, status_code=status.HTTP_201_CREATED, summary="Create rental application")
async def create_rental_application(
    application_data: RentalApplicationCreate,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new rental application for a long-term rental property.
    
    - **property_id**: ID of the long-term rental property
    - **personal_information**: Applicant's personal details
    - **employment_information**: Employment and income details
    - **rental_history**: Previous rental history and references
    - **financial_information**: Bank and credit information
    - **pets**: Pet information if applicable
    - **emergency_contacts**: Emergency contact information
    
    Applications require various consents for background and credit checks.
    """
    try:
        applicant_id = current_user["id"]
        application = await booking_service.create_rental_application(application_data, applicant_id)
        return application
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/applications/search", response_model=ApplicationSearchResult, summary="Search rental applications")
async def search_rental_applications(
    property_id: Optional[str] = Query(None, description="Filter by property ID"),
    application_status: Optional[ApplicationStatus] = Query(None, description="Filter by application status"),
    move_in_from: Optional[date] = Query(None, description="Move-in date from"),
    move_in_to: Optional[date] = Query(None, description="Move-in date to"),
    min_income: Optional[float] = Query(None, description="Minimum monthly income"),
    has_pets: Optional[bool] = Query(None, description="Filter by pet ownership"),
    background_check_consent: Optional[bool] = Query(None, description="Filter by background check consent"),
    credit_check_consent: Optional[bool] = Query(None, description="Filter by credit check consent"),
    limit: int = Query(20, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Search rental applications with various filters.
    
    Property owners and agents can search applications for their properties.
    Applicants can only search their own applications.
    """
    try:
        # For regular users, restrict to their own applications
        applicant_id = current_user["id"] if not current_user.get("is_agent") else None
        
        filters = ApplicationSearchFilters(
            property_id=property_id,
            applicant_id=applicant_id,
            application_status=application_status,
            move_in_from=move_in_from,
            move_in_to=move_in_to,
            min_income=min_income,
            has_pets=has_pets,
            background_check_consent=background_check_consent,
            credit_check_consent=credit_check_consent,
            limit=limit,
            offset=offset
        )
        
        return await booking_service.search_applications(filters)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/applications/{application_id}", response_model=RentalApplication, summary="Get rental application by ID")
async def get_rental_application(
    application_id: str = Path(..., description="Rental application ID"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed information about a specific rental application.
    """
    try:
        application = await booking_service.get_rental_application(application_id)
        if not application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rental application not found")
        
        # Check permissions
        if application.applicant_id != current_user["id"] and not current_user.get("is_agent"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this application")
        
        return application
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/applications/{application_id}", response_model=RentalApplication, summary="Update rental application")
async def update_rental_application(
    application_id: str = Path(..., description="Rental application ID"),
    application_data: RentalApplicationUpdate = ...,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Update rental application details.
    
    Applicants can update their submitted applications (before review).
    Property owners/agents can update application status.
    """
    try:
        # Check if application exists and user has permission
        existing_application = await booking_service.get_rental_application(application_id)
        if not existing_application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rental application not found")
        
        # Permission check
        if existing_application.applicant_id != current_user["id"] and not current_user.get("is_agent"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this application")
        
        updated_application = await booking_service.update_rental_application(application_id, application_data)
        if not updated_application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rental application not found")
        
        return updated_application
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# ============================================================================
# VIEWING SCHEDULES (Property tours)
# ============================================================================

@router.post("/viewings", response_model=ViewingSchedule, status_code=status.HTTP_201_CREATED, summary="Schedule property viewing")
async def schedule_property_viewing(
    viewing_data: ViewingScheduleCreate,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Schedule a property viewing/tour for a long-term rental.
    
    - **property_id**: ID of the property to view
    - **agent_id**: ID of the agent conducting the viewing
    - **scheduled_date**: Date and time for the viewing
    - **duration_minutes**: Duration of the viewing (15-120 minutes)
    - **applicant_id**: Optional - specific applicant for the viewing
    
    The system will check agent availability and prevent double-bookings.
    """
    try:
        viewing = await booking_service.create_viewing_schedule(viewing_data)
        return viewing
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/viewings/{viewing_id}", response_model=ViewingSchedule, summary="Get viewing schedule by ID")
async def get_viewing_schedule(
    viewing_id: str = Path(..., description="Viewing schedule ID"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed information about a specific viewing schedule.
    """
    try:
        viewing = await booking_service.get_viewing_schedule(viewing_id)
        if not viewing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viewing schedule not found")
        
        return viewing
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/viewings/{viewing_id}", response_model=ViewingSchedule, summary="Update viewing schedule")
async def update_viewing_schedule(
    viewing_id: str = Path(..., description="Viewing schedule ID"),
    viewing_data: ViewingScheduleUpdate = ...,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Update viewing schedule details.
    
    Agents can update viewing details, notes, and status.
    Applicants can provide feedback after viewings.
    """
    try:
        updated_viewing = await booking_service.update_viewing_schedule(viewing_id, viewing_data)
        if not updated_viewing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viewing schedule not found")
        
        return updated_viewing
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/properties/{property_id}/viewings", response_model=List[ViewingSchedule], summary="Get property viewings")
async def get_property_viewings(
    property_id: str = Path(..., description="Property ID"),
    limit: int = Query(20, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all viewing schedules for a specific property.
    
    Property owners and agents can view all scheduled viewings.
    """
    try:
        return await booking_service.get_viewings_by_property(property_id, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/agents/{agent_id}/viewings", response_model=List[ViewingSchedule], summary="Get agent viewings")
async def get_agent_viewings(
    agent_id: str = Path(..., description="Agent ID"),
    date_from: Optional[date] = Query(None, description="Date from"),
    date_to: Optional[date] = Query(None, description="Date to"),
    limit: int = Query(20, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Get viewing schedules for a specific agent.
    
    Useful for agent calendar management and schedule optimization.
    """
    try:
        return await booking_service.get_viewings_by_agent(agent_id, date_from, date_to, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/agents/{agent_id}/available-slots", response_model=List[datetime], summary="Get available viewing slots")
async def get_available_viewing_slots(
    agent_id: str = Path(..., description="Agent ID"),
    date: date = Query(..., description="Date to check availability"),
    duration_minutes: int = Query(30, ge=15, le=120, description="Duration of viewing in minutes"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Get available time slots for scheduling viewings with an agent on a specific date.
    
    Returns a list of available datetime slots based on agent's existing schedule.
    """
    try:
        return await booking_service.get_available_viewing_slots(agent_id, date, duration_minutes)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) 