from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.model import Appointment, User

router = APIRouter()

@router.get("/appointments/{patient_id}")
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter(Appointment.patient_id == patient_id).all()
    return appointments

@router.get("/profile/{patient_id}")
def get_patient_profile(patient_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == patient_id, User.role == "patient").first()
    if not user:
        raise HTTPException(status_code=404, detail="Patient not found")
    return user
