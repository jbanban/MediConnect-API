from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.model import Appointment, User

router = APIRouter()

@router.get("/requests/{doctor_id}")
def get_appointment_requests(doctor_id: int, db: Session = Depends(get_db)):
    requests = db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()
    return requests

@router.get("/profile/{doctor_id}")
def get_doctor_profile(doctor_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == doctor_id, User.role == "doctor").first()
    if not user:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return user
