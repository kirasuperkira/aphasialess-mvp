from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .models import AphasiaType, AuthMethod

class PatientCreate(BaseModel):
    full_name: str
    aphasia_type: str
    bot_phone: str = ""
    assigned_doctor_id: str
    auth_method: str = "biometric"
    subscription_status: str = "Trial"
    crm_external_id: Optional[str] = None
    bpms_process_status: Optional[str] = "pending"

class PatientResponse(BaseModel):
    id: str
    full_name: str
    aphasia_type: AphasiaType
    auth_method: Optional[AuthMethod]
    assigned_doctor_id: str
    created_at: datetime

    class Config:
        from_attributes = True