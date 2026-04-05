import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, func, Enum as SAEnum
from database import Base

class AphasiaType(str, enum.Enum):
    motor = "motor"
    sensory = "sensory"
    mixed = "mixed"

class AuthMethod(str, enum.Enum):
    biometric = "biometric"
    pin = "pin"
    magic_link = "magic_link"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String, nullable=False)
    aphasia_type = Column(SAEnum(AphasiaType), nullable=False)
    auth_method = Column(SAEnum(AuthMethod), nullable=True)
    assigned_doctor_id = Column(String, nullable=False)

    crm_external_id = Column(String, nullable=True, default=None)
    bpms_process_status = Column(String, default="pending")
    bot_phone = Column(String, nullable=True, default=None)

    created_at = Column(DateTime, server_default=func.now())