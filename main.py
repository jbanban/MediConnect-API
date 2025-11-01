from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from security import get_password_hash, verify_password
from database import Base, engine, SessionLocal
from auth import router as auth_router
import models, schemas
import shutil



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

# --- Include authentication router ---
app.include_router(auth_router)

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- PATIENT ROUTES --------------------

@app.get("/patient/dashboard")
def patient_dashboard(db: Session = Depends(get_db)):
    return {"message": "Welcome to your Patient Dashboard", "appointments_count": db.query(models.Appointment).count()}

@app.get("/patient/my-appointments", response_model=list[schemas.AppointmentBase])
def patient_appointments(db: Session = Depends(get_db)):
    return {"message": "List of your appointment requests", "appointments": db.query(models.Appointment).all()}

@app.get("/patient/book-appointment")
def book_appointment(doctor_id: int, date: str, time: str):
    new_appointment = {"doctor_id": doctor_id, "date": date, "time": time, "status": "Pending"}
    models.Appointment.append(new_appointment)
    return {"message": "Appointment booked successfully", "appointment": new_appointment}

@app.get("/patient/profile")
def patient_profile(patient_id: int):
    for p in models.Patient:
        if p["id"] == models.id:
            return {"profile": p}
    raise HTTPException(status_code=404, detail="Patient not found")

@app.post("/patient/login")
def patient_login(email: str, password: str):
    for p in models.Patient:
        if p["email"] == email and p["password"] == password:
            return {"message": "Login successful", "patient": p}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/patient/register")
def patient_register(name: str, email: str, password: str):
    new_patient = {"id": len(models.Patient) + 1, "name": name, "email": email, "password": password}
    models.Patient.append(new_patient)
    return {"message": "Patient registered successfully", "patient": new_patient}

@app.get("/appointments/{patient_id}")
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    appointments = db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).all()
    return appointments

@app.get("/profile/{patient_id}")
def get_patient_profile(patient_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Patient).filter(models.Patient.id == patient_id, models.Patient.role == "patient").first()
    if not user:
        raise HTTPException(status_code=404, detail="Patient not found")
    return user



# -------------------- DOCTOR ROUTES --------------------

@app.get("/doctor/dashboard")
def doctor_dashboard():
    today_appts = [a for a in models.Appointment if a["status"] == "Pending"]
    return {"message": "Welcome to Doctor Dashboard", "appointments_today": len(today_appts)}

@app.get("/doctor/appointments-today")
def doctor_appointments_today():
    today_appts = [a for a in models.Appointment if a["status"] == "Pending"]
    return {"appointments_today": today_appts}

@app.get("/doctor/set-schedule")
def doctor_set_schedule(doctor_id: int, date: str, time: str):
    new_schedule = {"doctor_id": doctor_id, "date": date, "time": time}
    models.Schedule.append(new_schedule)
    return {"message": "Schedule set successfully", "schedule": new_schedule}

@app.get("/doctor/profile")
def doctor_profile(doctor_id: int):
    for d in models.Doctor:
        if d["id"] == doctor_id:
            return {"profile": d}
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.post("/doctor/create-account", response_model=schemas.UserResponse)
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

@app.get("/requests/{doctor_id}")
def get_appointment_requests(doctor_id: int, db: Session = Depends(get_db)):
    requests = db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor_id).all()
    return requests

@app.get("/profile/{doctor_id}")
def get_doctor_profile(doctor_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == doctor_id, models.User.role == "doctor").first()
    if not user:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return user


# -------------------- ADMIN/REPORT ROUTE --------------------

@app.get("/admin/report")
def generate_report():
    report = {
        "total_patients": len(models.Patient),
        "total_doctors": len(models.Doctor),
        "total_appointments": len(models.Appointment),
    }
    return {"message": "System report generated", "report": report}