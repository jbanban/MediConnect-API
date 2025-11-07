from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, SessionLocal
from routes.auth import router as auth_router
from routes.patients import router as patients_router
from routes.doctors import router as doctors_router
import models


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
app.include_router(patients_router)
app.include_router(doctors_router)

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# -------------------- ADMIN/REPORT ROUTE --------------------

@app.get("/admin/report")
def generate_report():
    report = {
        "total_patients": len(models.Patient),
        "total_doctors": len(models.Doctor),
        "total_appointments": len(models.Appointment),
    }
    return {"message": "System report generated", "report": report}