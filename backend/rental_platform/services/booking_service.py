from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from decimal import Decimal
from supabase import Client

from ..models.booking_models import (
    BookingRequest, BookingRequestCreate, BookingRequestUpdate,
    RentalApplication, RentalApplicationCreate, RentalApplicationUpdate,
    ViewingSchedule, ViewingScheduleCreate, ViewingScheduleUpdate,
    BookingStatus, ApplicationStatus, ViewingStatus,
    BookingSearchFilters, ApplicationSearchFilters,
    BookingSearchResult, ApplicationSearchResult
)
from ..models.property_models import PropertyType

class BookingService:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client

    # ========================================================================
    # BOOKING REQUESTS (Short-term rentals / Vacation bookings)
    # ========================================================================
    
    async def create_booking_request(self, booking_data: BookingRequestCreate, guest_id: str) -> BookingRequest:
        """Create a new booking request for short-term rental"""
        try:
            # Verify property exists and is short-term rental
            property_result = self.supabase.table('properties').select('id, property_type, price_per_night').eq('id', booking_data.property_id).single().execute()
            
            if not property_result.data:
                raise Exception("Property not found")
            
            property = property_result.data
            if property['property_type'] != 'short_term':
                raise Exception("Property is not available for short-term bookings")
            
            # Check property availability for requested dates
            availability_result = self.supabase.table('property_availability').select('is_available').eq('property_id', booking_data.property_id).lte('available_from', booking_data.check_in_date.isoformat()).gte('available_to', booking_data.check_out_date.isoformat()).execute()
            
            if availability_result.data and not all(avail['is_available'] for avail in availability_result.data):
                raise Exception("Property is not available for selected dates")
            
            # Check for existing bookings that conflict
            existing_bookings = self.supabase.table('booking_requests').select('id').eq('property_id', booking_data.property_id).in_('booking_status', ['pending', 'confirmed']).or_(f'check_in_date.lte.{booking_data.check_out_date.isoformat()},check_out_date.gte.{booking_data.check_in_date.isoformat()}').execute()
            
            if existing_bookings.data:
                raise Exception("Property has conflicting bookings for selected dates")
            
            # Calculate total amount
            nights = (booking_data.check_out_date - booking_data.check_in_date).days
            base_amount = Decimal(str(property['price_per_night'])) * nights
            
            # Get short-term rental details for fees
            short_term_result = self.supabase.table('short_term_rentals').select('cleaning_fee, security_deposit, extra_guest_fee, pet_fee').eq('property_id', booking_data.property_id).single().execute()
            
            total_amount = base_amount
            if short_term_result.data:
                fees = short_term_result.data
                if fees.get('cleaning_fee'):
                    total_amount += Decimal(str(fees['cleaning_fee']))
                if fees.get('extra_guest_fee') and booking_data.num_guests > 2:
                    total_amount += Decimal(str(fees['extra_guest_fee'])) * (booking_data.num_guests - 2)
                if fees.get('pet_fee') and booking_data.num_pets > 0:
                    total_amount += Decimal(str(fees['pet_fee'])) * booking_data.num_pets
            
            # Create booking request
            booking_dict = booking_data.dict()
            booking_dict.update({
                'guest_id': guest_id,
                'total_amount': str(total_amount),
                'check_in_date': booking_data.check_in_date.isoformat(),
                'check_out_date': booking_data.check_out_date.isoformat()
            })
            
            result = self.supabase.table('booking_requests').insert(booking_dict).execute()
            
            if result.data:
                return BookingRequest(**result.data[0])
            raise Exception("Failed to create booking request")
            
        except Exception as e:
            raise Exception(f"Error creating booking request: {str(e)}")

    async def get_booking_request(self, booking_id: str) -> Optional[BookingRequest]:
        """Get booking request by ID"""
        try:
            result = self.supabase.table('booking_requests').select('*').eq('id', booking_id).single().execute()
            
            if result.data:
                return BookingRequest(**result.data)
            return None
            
        except Exception as e:
            raise Exception(f"Error fetching booking request: {str(e)}")

    async def update_booking_request(self, booking_id: str, booking_data: BookingRequestUpdate) -> Optional[BookingRequest]:
        """Update booking request"""
        try:
            update_dict = {k: v for k, v in booking_data.dict(exclude_unset=True).items() if v is not None}
            
            # Handle date serialization
            if 'check_in_date' in update_dict:
                update_dict['check_in_date'] = update_dict['check_in_date'].isoformat()
            if 'check_out_date' in update_dict:
                update_dict['check_out_date'] = update_dict['check_out_date'].isoformat()
            
            # Set timestamps based on status changes
            if 'booking_status' in update_dict:
                if update_dict['booking_status'] == BookingStatus.CONFIRMED:
                    update_dict['confirmed_at'] = datetime.utcnow().isoformat()
                elif update_dict['booking_status'] == BookingStatus.CANCELLED:
                    update_dict['cancelled_at'] = datetime.utcnow().isoformat()
            
            result = self.supabase.table('booking_requests').update(update_dict).eq('id', booking_id).execute()
            
            if result.data:
                return BookingRequest(**result.data[0])
            return None
            
        except Exception as e:
            raise Exception(f"Error updating booking request: {str(e)}")

    async def cancel_booking_request(self, booking_id: str) -> bool:
        """Cancel a booking request"""
        try:
            result = self.supabase.table('booking_requests').update({
                'booking_status': BookingStatus.CANCELLED,
                'cancelled_at': datetime.utcnow().isoformat()
            }).eq('id', booking_id).execute()
            
            return bool(result.data)
            
        except Exception as e:
            raise Exception(f"Error cancelling booking request: {str(e)}")

    async def search_bookings(self, filters: BookingSearchFilters) -> BookingSearchResult:
        """Search booking requests with filters"""
        try:
            query = self.supabase.table('booking_requests').select('*', count='exact')
            
            if filters.property_id:
                query = query.eq('property_id', filters.property_id)
            if filters.guest_id:
                query = query.eq('guest_id', filters.guest_id)
            if filters.booking_status:
                query = query.eq('booking_status', filters.booking_status.value)
            if filters.check_in_from:
                query = query.gte('check_in_date', filters.check_in_from.isoformat())
            if filters.check_in_to:
                query = query.lte('check_in_date', filters.check_in_to.isoformat())
            if filters.check_out_from:
                query = query.gte('check_out_date', filters.check_out_from.isoformat())
            if filters.check_out_to:
                query = query.lte('check_out_date', filters.check_out_to.isoformat())
            if filters.min_amount:
                query = query.gte('total_amount', str(filters.min_amount))
            if filters.max_amount:
                query = query.lte('total_amount', str(filters.max_amount))
            
            # Apply pagination
            query = query.range(filters.offset, filters.offset + filters.limit - 1)
            
            result = query.execute()
            
            bookings = [BookingRequest(**booking) for booking in result.data] if result.data else []
            total_count = result.count or 0
            has_more = (filters.offset + filters.limit) < total_count
            
            return BookingSearchResult(
                bookings=bookings,
                total_count=total_count,
                has_more=has_more
            )
            
        except Exception as e:
            raise Exception(f"Error searching bookings: {str(e)}")

    async def get_bookings_by_guest(self, guest_id: str, limit: int = 20, offset: int = 0) -> List[BookingRequest]:
        """Get all bookings for a guest"""
        try:
            result = self.supabase.table('booking_requests').select('*').eq('guest_id', guest_id).range(offset, offset + limit - 1).order('created_at', desc=True).execute()
            
            return [BookingRequest(**booking) for booking in result.data] if result.data else []
            
        except Exception as e:
            raise Exception(f"Error fetching guest bookings: {str(e)}")

    async def get_bookings_by_property(self, property_id: str, limit: int = 20, offset: int = 0) -> List[BookingRequest]:
        """Get all bookings for a property"""
        try:
            result = self.supabase.table('booking_requests').select('*').eq('property_id', property_id).range(offset, offset + limit - 1).order('created_at', desc=True).execute()
            
            return [BookingRequest(**booking) for booking in result.data] if result.data else []
            
        except Exception as e:
            raise Exception(f"Error fetching property bookings: {str(e)}")

    # ========================================================================
    # RENTAL APPLICATIONS (Long-term rentals)
    # ========================================================================

    async def create_rental_application(self, application_data: RentalApplicationCreate, applicant_id: str) -> RentalApplication:
        """Create a new rental application for long-term rental"""
        try:
            # Verify property exists and is long-term rental
            property_result = self.supabase.table('properties').select('id, property_type').eq('id', application_data.property_id).single().execute()
            
            if not property_result.data:
                raise Exception("Property not found")
            
            if property_result.data['property_type'] != 'long_term':
                raise Exception("Property is not available for long-term rentals")
            
            # Check if user already has an active application for this property
            existing_application = self.supabase.table('rental_applications').select('id').eq('property_id', application_data.property_id).eq('applicant_id', applicant_id).in_('application_status', ['submitted', 'under_review']).execute()
            
            if existing_application.data:
                raise Exception("You already have an active application for this property")
            
            # Create application
            application_dict = application_data.dict()
            application_dict['applicant_id'] = applicant_id
            
            # Handle nested model serialization
            if 'personal_information' in application_dict:
                personal_info = application_dict['personal_information']
                if isinstance(personal_info, dict) and 'date_of_birth' in personal_info:
                    personal_info['date_of_birth'] = personal_info['date_of_birth'].isoformat() if hasattr(personal_info['date_of_birth'], 'isoformat') else personal_info['date_of_birth']
            
            if 'employment_information' in application_dict and application_dict['employment_information']:
                emp_info = application_dict['employment_information']
                if isinstance(emp_info, dict) and 'employment_start_date' in emp_info:
                    emp_info['employment_start_date'] = emp_info['employment_start_date'].isoformat() if hasattr(emp_info['employment_start_date'], 'isoformat') else emp_info['employment_start_date']
            
            if 'move_in_date' in application_dict and application_dict['move_in_date']:
                application_dict['move_in_date'] = application_dict['move_in_date'].isoformat()
            
            result = self.supabase.table('rental_applications').insert(application_dict).execute()
            
            if result.data:
                return RentalApplication(**result.data[0])
            raise Exception("Failed to create rental application")
            
        except Exception as e:
            raise Exception(f"Error creating rental application: {str(e)}")

    async def get_rental_application(self, application_id: str) -> Optional[RentalApplication]:
        """Get rental application by ID"""
        try:
            result = self.supabase.table('rental_applications').select('*').eq('id', application_id).single().execute()
            
            if result.data:
                return RentalApplication(**result.data)
            return None
            
        except Exception as e:
            raise Exception(f"Error fetching rental application: {str(e)}")

    async def update_rental_application(self, application_id: str, application_data: RentalApplicationUpdate) -> Optional[RentalApplication]:
        """Update rental application"""
        try:
            update_dict = {k: v for k, v in application_data.dict(exclude_unset=True).items() if v is not None}
            
            # Set timestamps based on status changes
            if 'application_status' in update_dict:
                if update_dict['application_status'] in [ApplicationStatus.APPROVED, ApplicationStatus.REJECTED]:
                    update_dict['decided_at'] = datetime.utcnow().isoformat()
                elif update_dict['application_status'] == ApplicationStatus.UNDER_REVIEW:
                    update_dict['reviewed_at'] = datetime.utcnow().isoformat()
            
            # Handle date serialization
            if 'move_in_date' in update_dict and update_dict['move_in_date']:
                update_dict['move_in_date'] = update_dict['move_in_date'].isoformat()
            
            result = self.supabase.table('rental_applications').update(update_dict).eq('id', application_id).execute()
            
            if result.data:
                return RentalApplication(**result.data[0])
            return None
            
        except Exception as e:
            raise Exception(f"Error updating rental application: {str(e)}")

    async def search_applications(self, filters: ApplicationSearchFilters) -> ApplicationSearchResult:
        """Search rental applications with filters"""
        try:
            query = self.supabase.table('rental_applications').select('*', count='exact')
            
            if filters.property_id:
                query = query.eq('property_id', filters.property_id)
            if filters.applicant_id:
                query = query.eq('applicant_id', filters.applicant_id)
            if filters.application_status:
                query = query.eq('application_status', filters.application_status.value)
            if filters.move_in_from:
                query = query.gte('move_in_date', filters.move_in_from.isoformat())
            if filters.move_in_to:
                query = query.lte('move_in_date', filters.move_in_to.isoformat())
            if filters.background_check_consent is not None:
                query = query.eq('background_check_consent', filters.background_check_consent)
            if filters.credit_check_consent is not None:
                query = query.eq('credit_check_consent', filters.credit_check_consent)
            
            # Apply pagination
            query = query.range(filters.offset, filters.offset + filters.limit - 1)
            
            result = query.execute()
            
            applications = [RentalApplication(**app) for app in result.data] if result.data else []
            total_count = result.count or 0
            has_more = (filters.offset + filters.limit) < total_count
            
            return ApplicationSearchResult(
                applications=applications,
                total_count=total_count,
                has_more=has_more
            )
            
        except Exception as e:
            raise Exception(f"Error searching applications: {str(e)}")

    # ========================================================================
    # VIEWING SCHEDULES (Property tours)
    # ========================================================================

    async def create_viewing_schedule(self, viewing_data: ViewingScheduleCreate) -> ViewingSchedule:
        """Create a new viewing schedule for property tour"""
        try:
            # Verify property exists
            property_result = self.supabase.table('properties').select('id').eq('id', viewing_data.property_id).single().execute()
            
            if not property_result.data:
                raise Exception("Property not found")
            
            # Check if agent is available at the requested time
            agent_conflicts = self.supabase.table('viewing_schedules').select('id').eq('agent_id', viewing_data.agent_id).eq('viewing_status', ViewingStatus.SCHEDULED).lte('scheduled_date', (viewing_data.scheduled_date + timedelta(minutes=viewing_data.duration_minutes)).isoformat()).gte('scheduled_date', (viewing_data.scheduled_date - timedelta(minutes=30)).isoformat()).execute()
            
            if agent_conflicts.data:
                raise Exception("Agent is not available at the requested time")
            
            viewing_dict = viewing_data.dict()
            viewing_dict['scheduled_date'] = viewing_data.scheduled_date.isoformat()
            
            result = self.supabase.table('viewing_schedules').insert(viewing_dict).execute()
            
            if result.data:
                return ViewingSchedule(**result.data[0])
            raise Exception("Failed to create viewing schedule")
            
        except Exception as e:
            raise Exception(f"Error creating viewing schedule: {str(e)}")

    async def get_viewing_schedule(self, viewing_id: str) -> Optional[ViewingSchedule]:
        """Get viewing schedule by ID"""
        try:
            result = self.supabase.table('viewing_schedules').select('*').eq('id', viewing_id).single().execute()
            
            if result.data:
                return ViewingSchedule(**result.data)
            return None
            
        except Exception as e:
            raise Exception(f"Error fetching viewing schedule: {str(e)}")

    async def update_viewing_schedule(self, viewing_id: str, viewing_data: ViewingScheduleUpdate) -> Optional[ViewingSchedule]:
        """Update viewing schedule"""
        try:
            update_dict = {k: v for k, v in viewing_data.dict(exclude_unset=True).items() if v is not None}
            
            # Handle datetime serialization
            if 'scheduled_date' in update_dict:
                update_dict['scheduled_date'] = update_dict['scheduled_date'].isoformat()
            
            # Set timestamps based on status changes
            if 'viewing_status' in update_dict:
                if update_dict['viewing_status'] == ViewingStatus.COMPLETED:
                    update_dict['completed_at'] = datetime.utcnow().isoformat()
                elif update_dict['viewing_status'] == ViewingStatus.CANCELLED:
                    update_dict['cancelled_at'] = datetime.utcnow().isoformat()
            
            result = self.supabase.table('viewing_schedules').update(update_dict).eq('id', viewing_id).execute()
            
            if result.data:
                return ViewingSchedule(**result.data[0])
            return None
            
        except Exception as e:
            raise Exception(f"Error updating viewing schedule: {str(e)}")

    async def get_viewings_by_property(self, property_id: str, limit: int = 20, offset: int = 0) -> List[ViewingSchedule]:
        """Get all viewing schedules for a property"""
        try:
            result = self.supabase.table('viewing_schedules').select('*').eq('property_id', property_id).range(offset, offset + limit - 1).order('scheduled_date', desc=False).execute()
            
            return [ViewingSchedule(**viewing) for viewing in result.data] if result.data else []
            
        except Exception as e:
            raise Exception(f"Error fetching property viewings: {str(e)}")

    async def get_viewings_by_agent(self, agent_id: str, date_from: Optional[date] = None, date_to: Optional[date] = None, limit: int = 20, offset: int = 0) -> List[ViewingSchedule]:
        """Get viewing schedules for an agent"""
        try:
            query = self.supabase.table('viewing_schedules').select('*').eq('agent_id', agent_id)
            
            if date_from:
                query = query.gte('scheduled_date', date_from.isoformat())
            if date_to:
                query = query.lte('scheduled_date', date_to.isoformat())
            
            result = query.range(offset, offset + limit - 1).order('scheduled_date', desc=False).execute()
            
            return [ViewingSchedule(**viewing) for viewing in result.data] if result.data else []
            
        except Exception as e:
            raise Exception(f"Error fetching agent viewings: {str(e)}")

    async def get_available_viewing_slots(self, agent_id: str, date: date, duration_minutes: int = 30) -> List[datetime]:
        """Get available viewing time slots for an agent on a specific date"""
        try:
            # Get existing scheduled viewings for the date
            start_of_day = datetime.combine(date, datetime.min.time())
            end_of_day = datetime.combine(date, datetime.max.time())
            
            existing_viewings = self.supabase.table('viewing_schedules').select('scheduled_date, duration_minutes').eq('agent_id', agent_id).eq('viewing_status', ViewingStatus.SCHEDULED).gte('scheduled_date', start_of_day.isoformat()).lte('scheduled_date', end_of_day.isoformat()).execute()
            
            # Generate available slots (9 AM to 6 PM, excluding existing bookings)
            available_slots = []
            current_time = datetime.combine(date, datetime.strptime('09:00', '%H:%M').time())
            end_time = datetime.combine(date, datetime.strptime('18:00', '%H:%M').time())
            
            while current_time <= end_time:
                slot_end = current_time + timedelta(minutes=duration_minutes)
                
                # Check if this slot conflicts with existing viewings
                conflicts = False
                if existing_viewings.data:
                    for viewing in existing_viewings.data:
                        viewing_start = datetime.fromisoformat(viewing['scheduled_date'].replace('Z', '+00:00'))
                        viewing_end = viewing_start + timedelta(minutes=viewing['duration_minutes'])
                        
                        if (current_time < viewing_end and slot_end > viewing_start):
                            conflicts = True
                            break
                
                if not conflicts:
                    available_slots.append(current_time)
                
                current_time += timedelta(minutes=30)  # 30-minute intervals
            
            return available_slots
            
        except Exception as e:
            raise Exception(f"Error fetching available viewing slots: {str(e)}") 