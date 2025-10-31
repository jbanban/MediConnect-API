from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models

router = APIRouter()

# -------------------------------------------------------------------
# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- DOCTOR ROUTES --------------------

@router.get("/doctor/dashboard")
def doctor_dashboard():
    today_appts = [a for a in models.Appointment if a["status"] == "Pending"]
    return {"message": "Welcome to Doctor Dashboard", "appointments_today": len(today_appts)}

@router.get("/doctor/appointments-today")
def doctor_appointments_today():
    today_appts = [a for a in models.Appointment if a["status"] == "Pending"]
    return {"appointments_today": today_appts}

@router.get("/doctor/set-schedule")
def doctor_set_schedule(doctor_id: int, date: str, time: str):
    new_schedule = {"doctor_id": doctor_id, "date": date, "time": time}
    models.Schedule.append(new_schedule)
    return {"message": "Schedule set successfully", "schedule": new_schedule}

@router.get("/doctor/profile")
def doctor_profile(doctor_id: int):
    for d in models.Doctor:
        if d["id"] == doctor_id:
            return {"profile": d}
    raise HTTPException(status_code=404, detail="Doctor not found")

@router.get("/doctor/create-account")
def doctor_create_account(name: str, specialization: str, email: str, password: str):
    new_doctor = {
        "id": len(models.Doctor) + 1,
        "name": name,
        "specialization": specialization,
        "email": email,
        "password": password
    }
    models.Doctor.append(new_doctor)
    return {"message": "Doctor account created successfully", "doctor": new_doctor}

@router.get("/requests/{doctor_id}")
def get_appointment_requests(doctor_id: int, db: Session = Depends(get_db)):
    requests = db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor_id).all()
    return requests

@router.get("/profile/{doctor_id}")
def get_doctor_profile(doctor_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == doctor_id, models.User.role == "doctor").first()
    if not user:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return user
