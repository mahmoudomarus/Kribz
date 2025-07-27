from typing import Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field
from enum import Enum

class ContractStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PARTIALLY_SIGNED = "partially_signed"
    COMPLETED = "completed"
    EXPIRED = "expired"

class Contract(BaseModel):
    id: Optional[str] = None
    property_id: str
    tenant_id: str
    landlord_id: str
    application_id: Optional[str] = None  # Link to rental application
    contract_type: str = "lease_agreement"
    contract_status: ContractStatus = ContractStatus.DRAFT
    docusign_envelope_id: Optional[str] = None
    contract_terms: Dict[str, Any] = {}
    monthly_rent: Decimal
    security_deposit: Optional[Decimal] = None
    lease_start_date: date
    lease_end_date: date
    lease_term_months: int
    document_url: Optional[str] = None
    tenant_signed_at: Optional[datetime] = None
    landlord_signed_at: Optional[datetime] = None
    fully_executed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        use_enum_values = True
        json_encoders = {
            Decimal: str,
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

class ContractCreate(BaseModel):
    property_id: str
    tenant_id: str
    landlord_id: str
    application_id: Optional[str] = None
    contract_type: str = "lease_agreement"
    contract_terms: Dict[str, Any] = {}
    monthly_rent: Decimal
    security_deposit: Optional[Decimal] = None
    lease_start_date: date
    lease_end_date: date
    lease_term_months: int

class ContractUpdate(BaseModel):
    contract_status: Optional[ContractStatus] = None
    docusign_envelope_id: Optional[str] = None
    contract_terms: Optional[Dict[str, Any]] = None
    document_url: Optional[str] = None 