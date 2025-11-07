from fastapi import APIRouter, FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from security import get_password_hash
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

router = APIRouter(prefix="/doctor", tags=["Doctor"])


# -------------------- DOCTOR ROUTES --------------------

@router.get("/dashboard")
def doctor_dashboard():
    today_appts = [a for a in models.Appointment if a["status"] == "Pending"]
    return {"message": "Welcome to Doctor Dashboard", "appointments_today": len(today_appts)}

@router.get("/appointments-today")
def doctor_appointments_today():
    today_appts = [a for a in models.Appointment if a["status"] == "Pending"]
    return {"appointments_today": today_appts}

@router.get("/set-schedule")
def doctor_set_schedule(doctor_id: int, date: str, time: str):
    new_schedule = {"doctor_id": doctor_id, "date": date, "time": time}
    models.Schedule.append(new_schedule)
    return {"message": "Schedule set successfully", "schedule": new_schedule}

@router.get("/profile")
def doctor_profile(doctor_id: int):
    for d in models.Doctor:
        if d["id"] == doctor_id:
            return {"profile": d}
    raise HTTPException(status_code=404, detail="Doctor not found")

@router.post("/create-account", response_model=schemas.UserResponse)
def doctor_create_account(doctor_data: schemas.DoctorCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == doctor_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = get_password_hash(doctor.password)
    new_user = models.User(
        name=doctor.name,
        email=doctor.email,
        password=hashed_pw,
        role=doctor.role
    )
    doctor = models.Doctor(
        user=new_user,
        specialization=doctor.specialization,
        contact=doctor.contact
    )

    db.add(new_user)
    db.add(doctor)
    db.commit()
    db.refresh(new_user)
    db.refresh(doctor)
    return new_user

@router.get("/requests/{doctor_id}")
def get_appointment_requests(doctor_id: int, db: Session = Depends(get_db)):
    requests = db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor_id).all()
    return requests

@router.get("/profile/{user_id}")
def get_doctor_profile(user_id: int, db: Session = Depends(get_db)):
    doctor = (
        db.query(models.Doctor)
        .join(models.User)
        .filter(models.Doctor.user_id == user_id)
        .first()
    )

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return {
        "doctor_id": doctor.doctor_id,
        "user_id": doctor.user_id,
        "name": doctor.user.name,
        "email": doctor.user.email,
        "role": doctor.user.role,
        "specialization": doctor.specialization,
        "contact": doctor.contact,
    }
