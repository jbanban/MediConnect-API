from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "patient"

class DoctorCreate(BaseModel):
    name: str
    email: EmailStr
    specialization: str
    password: str
    contact: Optional[str] = None
    role: str = "doctor"

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserOut(UserBase):
    id: int
    username: str
    email: Optional[str]
    bio: Optional[str]

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None

class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    schedule_id: int
    status: str

    class Config:
        orm_mode = True