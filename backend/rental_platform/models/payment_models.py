from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field
from enum import Enum

class CommissionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PAID = "paid"
    FAILED = "failed"

class CommissionTracking(BaseModel):
    id: Optional[str] = None
    contract_id: str
    agent_id: str
    commission_type: str = "listing"  # listing, selling, referral
    commission_rate: Decimal = Field(..., ge=0, le=1, description="Commission rate as decimal (e.g., 0.03 for 3%)")
    commission_amount: Decimal = Field(..., ge=0, description="Calculated commission amount")
    base_amount: Decimal = Field(..., ge=0, description="Amount commission is calculated from")
    commission_status: CommissionStatus = CommissionStatus.PENDING
    stripe_transfer_id: Optional[str] = None
    due_date: Optional[date] = None
    paid_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        use_enum_values = True
        json_encoders = {
            Decimal: str,
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

class CommissionTrackingCreate(BaseModel):
    contract_id: str
    agent_id: str
    commission_type: str = "listing"
    commission_rate: Decimal = Field(..., ge=0, le=1)
    base_amount: Decimal = Field(..., ge=0)
    due_date: Optional[date] = None

class CommissionTrackingUpdate(BaseModel):
    commission_status: Optional[CommissionStatus] = None
    stripe_transfer_id: Optional[str] = None
    paid_at: Optional[datetime] = None 