-- Krib AI Rental Platform Schema Migration
-- Creates tables for property management, bookings, applications, contracts, and commissions

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create enum types for rental platform
CREATE TYPE property_type AS ENUM ('short_term', 'long_term');
CREATE TYPE booking_status AS ENUM ('pending', 'confirmed', 'cancelled', 'completed');
CREATE TYPE application_status AS ENUM ('submitted', 'under_review', 'approved', 'rejected', 'withdrawn');
CREATE TYPE contract_status AS ENUM ('draft', 'sent', 'partially_signed', 'completed', 'expired');
CREATE TYPE commission_status AS ENUM ('pending', 'processing', 'paid', 'failed');
CREATE TYPE viewing_status AS ENUM ('scheduled', 'completed', 'cancelled', 'rescheduled');

-- ============================================================================
-- CORE PROPERTIES TABLE
-- ============================================================================
CREATE TABLE public.properties (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    property_type property_type NOT NULL,
    address JSONB NOT NULL, -- {street, city, state, country, postal_code, coordinates}
    price_per_night DECIMAL(10,2), -- For short-term rentals
    price_per_month DECIMAL(10,2), -- For long-term rentals
    bedrooms INTEGER,
    bathrooms DECIMAL(3,1),
    square_feet INTEGER,
    amenities JSONB, -- Array of amenity strings
    images JSONB, -- Array of image URLs
    is_active BOOLEAN DEFAULT true,
    listing_agent_id UUID, -- Reference to agent managing this property
    owner_id UUID, -- Property owner (can be different from listing agent)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    
    CONSTRAINT fk_properties_account FOREIGN KEY (account_id) REFERENCES basejump.accounts(id) ON DELETE CASCADE,
    CONSTRAINT fk_properties_listing_agent FOREIGN KEY (listing_agent_id) REFERENCES auth.users(id),
    CONSTRAINT fk_properties_owner FOREIGN KEY (owner_id) REFERENCES auth.users(id)
);

-- ============================================================================
-- SHORT-TERM RENTALS (Vacation/Airbnb-style)
-- ============================================================================
CREATE TABLE public.short_term_rentals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL,
    minimum_nights INTEGER DEFAULT 1,
    maximum_nights INTEGER,
    instant_book BOOLEAN DEFAULT false,
    check_in_time TIME DEFAULT '15:00',
    check_out_time TIME DEFAULT '11:00',
    house_rules TEXT,
    cancellation_policy TEXT,
    cleaning_fee DECIMAL(8,2),
    security_deposit DECIMAL(8,2),
    extra_guest_fee DECIMAL(8,2),
    pet_fee DECIMAL(8,2),
    availability_calendar JSONB, -- Calendar data for available dates
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    
    CONSTRAINT fk_short_term_property FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE
);

-- ============================================================================
-- LONG-TERM RENTALS (Real Estate)
-- ============================================================================
CREATE TABLE public.long_term_rentals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL,
    lease_term_months INTEGER DEFAULT 12,
    security_deposit DECIMAL(10,2),
    pet_deposit DECIMAL(8,2),
    application_fee DECIMAL(6,2),
    income_requirement_multiplier DECIMAL(3,1) DEFAULT 3.0, -- 3x monthly rent
    credit_score_minimum INTEGER,
    background_check_required BOOLEAN DEFAULT true,
    references_required INTEGER DEFAULT 2,
    available_date DATE,
    lease_terms TEXT, -- Additional lease terms
    utilities_included JSONB, -- Array of included utilities
    parking_spots INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    
    CONSTRAINT fk_long_term_property FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE
);

-- ============================================================================
-- BOOKING REQUESTS (Short-term rentals)
-- ============================================================================
CREATE TABLE public.booking_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL,
    guest_id UUID NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    num_guests INTEGER NOT NULL,
    num_pets INTEGER DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    booking_status booking_status DEFAULT 'pending',
    special_requests TEXT,
    guest_information JSONB, -- Contact info, preferences, etc.
    payment_intent_id TEXT, -- Stripe payment intent ID
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    confirmed_at TIMESTAMP WITH TIME ZONE,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT fk_booking_property FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE,
    CONSTRAINT fk_booking_guest FOREIGN KEY (guest_id) REFERENCES auth.users(id) ON DELETE CASCADE,
    CONSTRAINT chk_booking_dates CHECK (check_out_date > check_in_date)
);

-- ============================================================================
-- RENTAL APPLICATIONS (Long-term rentals)
-- ============================================================================
CREATE TABLE public.rental_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL,
    applicant_id UUID NOT NULL,
    application_status application_status DEFAULT 'submitted',
    personal_information JSONB NOT NULL, -- Name, contact, SSN (encrypted), etc.
    employment_information JSONB, -- Employer, income, etc.
    rental_history JSONB, -- Previous rentals, references
    financial_information JSONB, -- Bank info, assets, debts
    additional_occupants JSONB, -- Other people who will live there
    pets JSONB, -- Pet information
    emergency_contacts JSONB,
    background_check_consent BOOLEAN DEFAULT false,
    credit_check_consent BOOLEAN DEFAULT false,
    application_fee_paid BOOLEAN DEFAULT false,
    move_in_date DATE,
    lease_term_requested INTEGER, -- Months
    additional_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    decided_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT fk_application_property FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE,
    CONSTRAINT fk_application_applicant FOREIGN KEY (applicant_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

-- ============================================================================
-- VIEWING SCHEDULES (Long-term rentals)
-- ============================================================================
CREATE TABLE public.viewing_schedules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL,
    applicant_id UUID,
    agent_id UUID NOT NULL,
    scheduled_date TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_minutes INTEGER DEFAULT 30,
    viewing_status viewing_status DEFAULT 'scheduled',
    notes TEXT,
    feedback JSONB, -- Post-viewing feedback from applicant
    agent_notes TEXT, -- Agent's notes about the viewing
    rescheduled_from UUID, -- Reference to original viewing if rescheduled
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    completed_at TIMESTAMP WITH TIME ZONE,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT fk_viewing_property FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE,
    CONSTRAINT fk_viewing_applicant FOREIGN KEY (applicant_id) REFERENCES auth.users(id),
    CONSTRAINT fk_viewing_agent FOREIGN KEY (agent_id) REFERENCES auth.users(id) ON DELETE CASCADE,
    CONSTRAINT fk_viewing_rescheduled FOREIGN KEY (rescheduled_from) REFERENCES public.viewing_schedules(id)
);

-- ============================================================================
-- CONTRACTS (DocuSign Integration)
-- ============================================================================
CREATE TABLE public.contracts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL,
    tenant_id UUID NOT NULL,
    landlord_id UUID NOT NULL,
    application_id UUID, -- Link to rental application if applicable
    contract_type TEXT NOT NULL, -- 'lease_agreement', 'rental_contract', etc.
    contract_status contract_status DEFAULT 'draft',
    docusign_envelope_id TEXT, -- DocuSign envelope ID
    contract_terms JSONB NOT NULL, -- Lease terms, rent, deposit, etc.
    monthly_rent DECIMAL(10,2) NOT NULL,
    security_deposit DECIMAL(10,2),
    lease_start_date DATE NOT NULL,
    lease_end_date DATE NOT NULL,
    lease_term_months INTEGER NOT NULL,
    document_url TEXT, -- URL to signed contract
    tenant_signed_at TIMESTAMP WITH TIME ZONE,
    landlord_signed_at TIMESTAMP WITH TIME ZONE,
    fully_executed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    
    CONSTRAINT fk_contract_property FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE,
    CONSTRAINT fk_contract_tenant FOREIGN KEY (tenant_id) REFERENCES auth.users(id) ON DELETE CASCADE,
    CONSTRAINT fk_contract_landlord FOREIGN KEY (landlord_id) REFERENCES auth.users(id) ON DELETE CASCADE,
    CONSTRAINT fk_contract_application FOREIGN KEY (application_id) REFERENCES public.rental_applications(id),
    CONSTRAINT chk_contract_dates CHECK (lease_end_date > lease_start_date)
);

-- ============================================================================
-- COMMISSION TRACKING (Payment Processing)
-- ============================================================================
CREATE TABLE public.commission_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_id UUID NOT NULL,
    agent_id UUID NOT NULL,
    commission_type TEXT NOT NULL, -- 'listing', 'selling', 'referral', etc.
    commission_rate DECIMAL(5,4) NOT NULL, -- Percentage (e.g., 0.0300 for 3%)
    commission_amount DECIMAL(10,2) NOT NULL,
    base_amount DECIMAL(10,2) NOT NULL, -- Amount commission is calculated from
    commission_status commission_status DEFAULT 'pending',
    stripe_transfer_id TEXT, -- Stripe transfer ID when paid
    due_date DATE,
    paid_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    
    CONSTRAINT fk_commission_contract FOREIGN KEY (contract_id) REFERENCES public.contracts(id) ON DELETE CASCADE,
    CONSTRAINT fk_commission_agent FOREIGN KEY (agent_id) REFERENCES auth.users(id) ON DELETE CASCADE,
    CONSTRAINT chk_commission_rate CHECK (commission_rate >= 0 AND commission_rate <= 1),
    CONSTRAINT chk_commission_amount CHECK (commission_amount >= 0)
);

-- ============================================================================
-- PROPERTY AVAILABILITY (Real-time availability management)
-- ============================================================================
CREATE TABLE public.property_availability (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL,
    available_from DATE NOT NULL,
    available_to DATE,
    is_available BOOLEAN DEFAULT true,
    reason_unavailable TEXT, -- 'maintenance', 'booked', 'owner_use', etc.
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    
    CONSTRAINT fk_availability_property FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE,
    CONSTRAINT chk_availability_dates CHECK (available_to IS NULL OR available_to >= available_from)
);

-- ============================================================================
-- INDEXES for Performance
-- ============================================================================

-- Properties indexes
CREATE INDEX idx_properties_account_id ON public.properties(account_id);
CREATE INDEX idx_properties_type ON public.properties(property_type);
CREATE INDEX idx_properties_is_active ON public.properties(is_active);
CREATE INDEX idx_properties_location ON public.properties USING GIN (address);
CREATE INDEX idx_properties_listing_agent ON public.properties(listing_agent_id);

-- Booking requests indexes
CREATE INDEX idx_booking_requests_property_id ON public.booking_requests(property_id);
CREATE INDEX idx_booking_requests_guest_id ON public.booking_requests(guest_id);
CREATE INDEX idx_booking_requests_status ON public.booking_requests(booking_status);
CREATE INDEX idx_booking_requests_dates ON public.booking_requests(check_in_date, check_out_date);

-- Rental applications indexes
CREATE INDEX idx_rental_applications_property_id ON public.rental_applications(property_id);
CREATE INDEX idx_rental_applications_applicant_id ON public.rental_applications(applicant_id);
CREATE INDEX idx_rental_applications_status ON public.rental_applications(application_status);

-- Viewing schedules indexes
CREATE INDEX idx_viewing_schedules_property_id ON public.viewing_schedules(property_id);
CREATE INDEX idx_viewing_schedules_agent_id ON public.viewing_schedules(agent_id);
CREATE INDEX idx_viewing_schedules_date ON public.viewing_schedules(scheduled_date);

-- Contracts indexes
CREATE INDEX idx_contracts_property_id ON public.contracts(property_id);
CREATE INDEX idx_contracts_tenant_id ON public.contracts(tenant_id);
CREATE INDEX idx_contracts_status ON public.contracts(contract_status);
CREATE INDEX idx_contracts_docusign ON public.contracts(docusign_envelope_id);

-- Commission tracking indexes
CREATE INDEX idx_commission_tracking_contract_id ON public.commission_tracking(contract_id);
CREATE INDEX idx_commission_tracking_agent_id ON public.commission_tracking(agent_id);
CREATE INDEX idx_commission_tracking_status ON public.commission_tracking(commission_status);

-- Property availability indexes
CREATE INDEX idx_property_availability_property_id ON public.property_availability(property_id);
CREATE INDEX idx_property_availability_dates ON public.property_availability(available_from, available_to);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE public.properties ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.short_term_rentals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.long_term_rentals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.booking_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.rental_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.viewing_schedules ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.contracts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.commission_tracking ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.property_availability ENABLE ROW LEVEL SECURITY;

-- Properties RLS policies
CREATE POLICY "Account members can manage their properties"
    ON public.properties FOR ALL
    USING (basejump.has_role_on_account(account_id));

CREATE POLICY "Public can view active properties"
    ON public.properties FOR SELECT
    USING (is_active = true);

-- Booking requests RLS policies
CREATE POLICY "Guests can manage their own bookings"
    ON public.booking_requests FOR ALL
    USING (guest_id = auth.uid());

CREATE POLICY "Property owners can view bookings for their properties"
    ON public.booking_requests FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.properties p 
            WHERE p.id = booking_requests.property_id 
            AND basejump.has_role_on_account(p.account_id)
        )
    );

-- Rental applications RLS policies  
CREATE POLICY "Applicants can manage their own applications"
    ON public.rental_applications FOR ALL
    USING (applicant_id = auth.uid());

CREATE POLICY "Property owners can view applications for their properties"
    ON public.rental_applications FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.properties p 
            WHERE p.id = rental_applications.property_id 
            AND basejump.has_role_on_account(p.account_id)
        )
    );

-- Viewing schedules RLS policies
CREATE POLICY "Applicants can view their own viewings"
    ON public.viewing_schedules FOR SELECT
    USING (applicant_id = auth.uid());

CREATE POLICY "Agents can manage viewings they're assigned to"
    ON public.viewing_schedules FOR ALL
    USING (agent_id = auth.uid());

-- Contracts RLS policies
CREATE POLICY "Contract parties can view their contracts"
    ON public.contracts FOR SELECT
    USING (tenant_id = auth.uid() OR landlord_id = auth.uid());

CREATE POLICY "Property owners can manage contracts for their properties"
    ON public.contracts FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM public.properties p 
            WHERE p.id = contracts.property_id 
            AND basejump.has_role_on_account(p.account_id)
        )
    );

-- Commission tracking RLS policies
CREATE POLICY "Agents can view their own commissions"
    ON public.commission_tracking FOR SELECT
    USING (agent_id = auth.uid());

CREATE POLICY "Account admins can manage commission tracking"
    ON public.commission_tracking FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM public.contracts c
            JOIN public.properties p ON c.property_id = p.id
            WHERE c.id = commission_tracking.contract_id 
            AND basejump.has_role_on_account(p.account_id)
        )
    );

-- Property availability RLS policies
CREATE POLICY "Property owners can manage availability"
    ON public.property_availability FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM public.properties p 
            WHERE p.id = property_availability.property_id 
            AND basejump.has_role_on_account(p.account_id)
        )
    );

CREATE POLICY "Public can view property availability"
    ON public.property_availability FOR SELECT
    USING (is_available = true);

-- ============================================================================
-- FUNCTIONS AND TRIGGERS
-- ============================================================================

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_properties_updated_at BEFORE UPDATE ON public.properties
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_short_term_rentals_updated_at BEFORE UPDATE ON public.short_term_rentals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_long_term_rentals_updated_at BEFORE UPDATE ON public.long_term_rentals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_booking_requests_updated_at BEFORE UPDATE ON public.booking_requests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rental_applications_updated_at BEFORE UPDATE ON public.rental_applications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_viewing_schedules_updated_at BEFORE UPDATE ON public.viewing_schedules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contracts_updated_at BEFORE UPDATE ON public.contracts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_commission_tracking_updated_at BEFORE UPDATE ON public.commission_tracking
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_property_availability_updated_at BEFORE UPDATE ON public.property_availability
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to automatically update property status when contract is fully executed
CREATE OR REPLACE FUNCTION handle_contract_completion()
RETURNS TRIGGER AS $$
BEGIN
    -- When a contract is fully executed (both parties signed), mark property as unavailable
    IF NEW.contract_status = 'completed' AND OLD.contract_status != 'completed' THEN
        INSERT INTO public.property_availability (property_id, available_from, available_to, is_available, reason_unavailable)
        VALUES (NEW.property_id, NEW.lease_start_date, NEW.lease_end_date, false, 'leased')
        ON CONFLICT (property_id, available_from) DO UPDATE SET
            available_to = NEW.lease_end_date,
            is_available = false,
            reason_unavailable = 'leased',
            updated_at = now();
    END IF;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER handle_contract_completion_trigger 
    AFTER UPDATE ON public.contracts
    FOR EACH ROW EXECUTE FUNCTION handle_contract_completion();

-- Function to calculate commission amount automatically
CREATE OR REPLACE FUNCTION calculate_commission_amount()
RETURNS TRIGGER AS $$
BEGIN
    NEW.commission_amount = NEW.base_amount * NEW.commission_rate;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER calculate_commission_amount_trigger 
    BEFORE INSERT OR UPDATE ON public.commission_tracking
    FOR EACH ROW EXECUTE FUNCTION calculate_commission_amount(); 