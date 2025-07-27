from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field, validator
from enum import Enum

# Enums for status tracking
class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class ApplicationStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class ViewingStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"

# Booking Request Models (Short-term rentals)
class GuestInformation(BaseModel):
    name: str
    email: str
    phone: str
    special_requests: Optional[str] = None
    arrival_time: Optional[str] = None
    purpose_of_stay: Optional[str] = None

class BookingRequest(BaseModel):
    id: Optional[str] = None
    property_id: str
    guest_id: str
    check_in_date: date
    check_out_date: date
    num_guests: int = Field(..., ge=1, description="Number of guests")
    num_pets: int = Field(0, ge=0, description="Number of pets")
    total_amount: Decimal = Field(..., ge=0, description="Total booking amount")
    booking_status: BookingStatus = BookingStatus.PENDING
    special_requests: Optional[str] = None
    guest_information: Optional[GuestInformation] = None
    payment_intent_id: Optional[str] = None  # Stripe payment intent ID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

    @validator('check_out_date')
    def checkout_after_checkin(cls, v, values):
        if 'check_in_date' in values and v <= values['check_in_date']:
            raise ValueError('Check-out date must be after check-in date')
        return v

    class Config:
        use_enum_values = True
        json_encoders = {
            Decimal: str,
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

class BookingRequestCreate(BaseModel):
    property_id: str
    check_in_date: date
    check_out_date: date
    num_guests: int = Field(..., ge=1)
    num_pets: int = Field(0, ge=0)
    special_requests: Optional[str] = None
    guest_information: Optional[GuestInformation] = None

    @validator('check_out_date')
    def checkout_after_checkin(cls, v, values):
        if 'check_in_date' in values and v <= values['check_in_date']:
            raise ValueError('Check-out date must be after check-in date')
        return v

class BookingRequestUpdate(BaseModel):
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    num_guests: Optional[int] = Field(None, ge=1)
    num_pets: Optional[int] = Field(None, ge=0)
    special_requests: Optional[str] = None
    guest_information: Optional[GuestInformation] = None
    booking_status: Optional[BookingStatus] = None

# Rental Application Models (Long-term rentals)
class PersonalInformation(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    ssn_last_four: str = Field(..., min_length=4, max_length=4, description="Last 4 digits of SSN")
    email: str
    phone: str
    current_address: Dict[str, str]  # Same structure as PropertyAddress
    drivers_license: Optional[str] = None
    marital_status: Optional[str] = None

class EmploymentInformation(BaseModel):
    employer_name: str
    job_title: str
    employment_type: str  # full-time, part-time, contract, self-employed
    monthly_income: Decimal
    employment_start_date: date
    supervisor_name: Optional[str] = None
    supervisor_phone: Optional[str] = None
    hr_contact: Optional[str] = None

class RentalHistory(BaseModel):
    current_landlord_name: Optional[str] = None
    current_landlord_phone: Optional[str] = None
    current_rent_amount: Optional[Decimal] = None
    current_lease_start: Optional[date] = None
    current_lease_end: Optional[date] = None
    reason_for_moving: Optional[str] = None
    previous_addresses: Optional[List[Dict[str, Any]]] = []

class FinancialInformation(BaseModel):
    bank_name: str
    account_type: str  # checking, savings
    monthly_income: Decimal
    other_income: Optional[Decimal] = None
    monthly_debts: Optional[Decimal] = None
    credit_score: Optional[int] = Field(None, ge=300, le=850)
    bankruptcy_history: bool = False
    eviction_history: bool = False

class EmergencyContact(BaseModel):
    name: str
    relationship: str
    phone: str
    email: Optional[str] = None

class PetInformation(BaseModel):
    type: str  # dog, cat, etc.
    breed: str
    age: int
    weight: Optional[int] = None
    vaccinated: bool = True
    spayed_neutered: bool = True

class RentalApplication(BaseModel):
    id: Optional[str] = None
    property_id: str
    applicant_id: str
    application_status: ApplicationStatus = ApplicationStatus.SUBMITTED
    personal_information: PersonalInformation
    employment_information: Optional[EmploymentInformation] = None
    rental_history: Optional[RentalHistory] = None
    financial_information: Optional[FinancialInformation] = None
    additional_occupants: Optional[List[PersonalInformation]] = []
    pets: Optional[List[PetInformation]] = []
    emergency_contacts: Optional[List[EmergencyContact]] = []
    background_check_consent: bool = False
    credit_check_consent: bool = False
    application_fee_paid: bool = False
    move_in_date: Optional[date] = None
    lease_term_requested: Optional[int] = Field(None, description="Requested lease term in months")
    additional_notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    decided_at: Optional[datetime] = None

    class Config:
        use_enum_values = True
        json_encoders = {
            Decimal: str,
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

class RentalApplicationCreate(BaseModel):
    property_id: str
    personal_information: PersonalInformation
    employment_information: Optional[EmploymentInformation] = None
    rental_history: Optional[RentalHistory] = None
    financial_information: Optional[FinancialInformation] = None
    additional_occupants: Optional[List[PersonalInformation]] = []
    pets: Optional[List[PetInformation]] = []
    emergency_contacts: Optional[List[EmergencyContact]] = []
    background_check_consent: bool = False
    credit_check_consent: bool = False
    move_in_date: Optional[date] = None
    lease_term_requested: Optional[int] = None
    additional_notes: Optional[str] = None

class RentalApplicationUpdate(BaseModel):
    personal_information: Optional[PersonalInformation] = None
    employment_information: Optional[EmploymentInformation] = None
    rental_history: Optional[RentalHistory] = None
    financial_information: Optional[FinancialInformation] = None
    additional_occupants: Optional[List[PersonalInformation]] = None
    pets: Optional[List[PetInformation]] = None
    emergency_contacts: Optional[List[EmergencyContact]] = None
    background_check_consent: Optional[bool] = None
    credit_check_consent: Optional[bool] = None
    application_status: Optional[ApplicationStatus] = None
    move_in_date: Optional[date] = None
    lease_term_requested: Optional[int] = None
    additional_notes: Optional[str] = None

# Viewing Schedule Models (Property tours for long-term rentals)
class ViewingSchedule(BaseModel):
    id: Optional[str] = None
    property_id: str
    applicant_id: Optional[str] = None
    agent_id: str
    scheduled_date: datetime
    duration_minutes: int = Field(30, ge=15, le=120, description="Duration in minutes")
    viewing_status: ViewingStatus = ViewingStatus.SCHEDULED
    notes: Optional[str] = None
    feedback: Optional[Dict[str, Any]] = None  # Post-viewing feedback from applicant
    agent_notes: Optional[str] = None
    rescheduled_from: Optional[str] = None  # ID of original viewing if rescheduled
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ViewingScheduleCreate(BaseModel):
    property_id: str
    applicant_id: Optional[str] = None  # Can be public viewing
    agent_id: str
    scheduled_date: datetime
    duration_minutes: int = Field(30, ge=15, le=120)
    notes: Optional[str] = None

class ViewingScheduleUpdate(BaseModel):
    scheduled_date: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=15, le=120)
    viewing_status: Optional[ViewingStatus] = None
    notes: Optional[str] = None
    feedback: Optional[Dict[str, Any]] = None
    agent_notes: Optional[str] = None

# Search and filter models
class BookingSearchFilters(BaseModel):
    property_id: Optional[str] = None
    guest_id: Optional[str] = None
    booking_status: Optional[BookingStatus] = None
    check_in_from: Optional[date] = None
    check_in_to: Optional[date] = None
    check_out_from: Optional[date] = None
    check_out_to: Optional[date] = None
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None
    limit: int = Field(20, le=100)
    offset: int = Field(0, ge=0)

class ApplicationSearchFilters(BaseModel):
    property_id: Optional[str] = None
    applicant_id: Optional[str] = None
    application_status: Optional[ApplicationStatus] = None
    move_in_from: Optional[date] = None
    move_in_to: Optional[date] = None
    min_income: Optional[Decimal] = None
    has_pets: Optional[bool] = None
    background_check_consent: Optional[bool] = None
    credit_check_consent: Optional[bool] = None
    limit: int = Field(20, le=100)
    offset: int = Field(0, ge=0)

class BookingSearchResult(BaseModel):
    bookings: List[BookingRequest]
    total_count: int
    has_more: bool

class ApplicationSearchResult(BaseModel):
    applications: List[RentalApplication]
    total_count: int
    has_more: bool 