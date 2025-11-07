from fastapi import APIRouter, FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models, schemas

# --- Database initialization ---
Base.metadata.create_all(bind=engine)


# --- App setup ---
app = FastAPI(
        title="Medicapp Backend API",
        description="FastAPI backend for Clinic Appointment System"
    )


# --- CORS setup ---
origins = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/patient", tags=["Patient"])

# -------------------- PATIENT ROUTES --------------------

@router.get("/{user_id}/dashboard")
def patient_dashboard(user_id: int, db: Session = Depends(get_db)):
    patient = (
        db.query(models.Patient)
        .join(models.User)
        .filter(models.Patient.user_id == user_id)
        .first()
    )

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "message": f"Welcome, {patient.user.name}",
        "name": patient.user.name,
        "appointments_count": db.query(models.Appointment).filter(models.Appointment.patient_id == patient.patient_id).count(),
    }

@router.get("/my-appointments", response_model=list[schemas.AppointmentBase])
def patient_appointments(db: Session = Depends(get_db)):
    return {"message": "List of your appointment requests", "appointments": db.query(models.Appointment).all()}

@router.get("/book-appointment")
def book_appointment(doctor_id: int, date: str, time: str):
    new_appointment = {"doctor_id": doctor_id, "date": date, "time": time, "status": "Pending"}
    models.Appointment.append(new_appointment)
    return {"message": "Appointment booked successfully", "appointment": new_appointment}

@router.get("/profile")
def patient_profile(patient_id: int):
    for p in models.Patient:
        if p["id"] == models.id:
            return {"profile": p}
    raise HTTPException(status_code=404, detail="Patient not found")

@router.get("/appointments/{patient_id}")
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    appointments = db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).all()
    return appointments

@router.get("/{user_id}")
def get_patient_profile(user_id: int, db: Session = Depends(get_db)):
    # Join User and Patient tables
    patient = (
        db.query(models.Patient)
        .join(models.User)
        .filter(models.Patient.user_id == user_id)
        .first()
    )

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "patient_id": patient.patient_id,
        "user_id": patient.user_id,
        "name": patient.user.name,
        "email": patient.user.email,
        "role": patient.user.role,
        "gender": patient.gender,
        "contact": patient.contact,
    }

@router.put("/{user_id}")
def up_patient_profile(
    user_id: int,
    updated_data: dict = Body(...),
    db: Session = Depends(get_db)
):
    patient = db.query(models.Patient).filter(models.Patient.user_id == user_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    for key, value in updated_data.items():
        if hasattr(patient, key):
            setattr(patient, key, value)

    db.commit()
    db.refresh(patient)
    return {"message": "Profile updated successfully", "patient": patient}

