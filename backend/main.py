import os
import uuid
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine, Base
from models import Patient
from schemas import PatientCreate, PatientResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aphasialess MVP Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/patients", response_model=PatientResponse, status_code=201)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(id=str(uuid.uuid4()), **patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
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