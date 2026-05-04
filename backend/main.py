import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

load_dotenv()

from .database import SessionLocal, engine, Base
from .models import Patient
from .schemas import PatientCreate, PatientResponse
from .bitrix_client import Bitrix24Client

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aphasialess MVP Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bitrix_client = Bitrix24Client()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/patients", response_model=PatientResponse, status_code=201)
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(
        id=str(uuid.uuid4()),
        full_name=patient.full_name,
        aphasia_type=patient.aphasia_type,
        bot_phone=patient.bot_phone,
        assigned_doctor_id=patient.assigned_doctor_id,
        auth_method=patient.auth_method,
        subscription_status=patient.subscription_status,
        crm_external_id=patient.crm_external_id,
        bpms_process_status=patient.bpms_process_status
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    try:
        patient_dict = {
            "full_name": patient.full_name,
            "aphasia_type": patient.aphasia_type,
            "bot_phone": patient.bot_phone,
            "assigned_doctor_id": patient.assigned_doctor_id,
            "auth_method": patient.auth_method,
            "subscription_status": patient.subscription_status,
        }
        crm_result = await bitrix_client.create_contact(patient_dict)
        print(f"CRM Sync Result: {crm_result}")

        if crm_result["status"] == "success":
            pass
    except Exception as e:
        print(f"Ошибка интеграции с CRM: {e}")
        crm_result = {"status": "error", "detail": str(e)}

    return db_patient

@app.get("/patients", response_model=List[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

@app.post("/webhook/crm")
async def crm_sync(data: dict):
    return {"status": "ok", "message": "CRM sync received"}

@app.post("/webhook/bpms")
async def bpms_process_update(data: dict):
    return {"status": "ok", "message": "BPMS process status updated"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "aphasialess-backend"}