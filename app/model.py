from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# User model (for patients and doctors login)
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(String(20), nullable=False)  # "patient" or "doctor"

    # Relationships
    patient_profile = relationship('Patient', backref='user', uselist=False)
    doctor_profile = relationship('Doctor', backref='user', uselist=False)


# Patient profile (extra info for patients)
class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    contact = Column(String(20), nullable=True)

    appointments = relationship('Appointment', backref='patient', lazy=True)


# Doctor profile (extra info for doctors)
class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    specialization = Column(String(100), nullable=False)
    contact = Column(String(20), nullable=True)

    schedules = relationship('Schedule', backref='doctor', lazy=True)
    appointments = relationship('Appointment', backref='doctor', lazy=True)


# Doctor schedules (available times doctors provide)
class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String(20), default='Available')

    appointments = relationship('Appointment', backref='schedule', lazy=True)


# Appointment booking by patient
class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedules.id'), nullable=False)
    reason = Column(String(200), nullable=True)
    status = Column(String(20), default='Pending')  # Pending / Confirmed / Cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
