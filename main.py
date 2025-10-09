from fastapi import FastAPI
from app.routes import auth, patient, doctor
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    app = FastAPI(
        title="Medicapp Backend API",
        description="FastAPI backend for Clinic Appointment System",
        version="1.0.0",
    )

    # Allow CORS for mobile app access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Change this in production to specific IP/domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize tables
    Base.metadata.create_all(bind=engine)

    # Include all routes
    app.include_router(auth.router)
    app.include_router(patient.router)
    app.include_router(doctor.router)

    return app


app = create_app()
