from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models import AphasiaType, AuthMethod

class PatientCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, description="ФИО пациента")
    aphasia_type: AphasiaType
    auth_method: Optional[AuthMethod] = None
    assigned_doctor_id: str

    crm_external_id: Optional[str] = None
    bpms_process_status: Optional[str] = "pending"
    bot_phone: Optional[str] = None

class PatientResponse(BaseModel):
    id: str
    full_name: str
    aphasia_type: AphasiaType
    auth_method: Optional[AuthMethod]
    assigned_doctor_id: str
    created_at: datetime

    class Config:
        from_attributes = True