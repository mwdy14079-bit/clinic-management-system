from datetime import date, time

from pydantic import BaseModel, Field


# =========================
# Patient Schemas
# =========================

class PatientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0, le=120)


class PatientRead(BaseModel):
    id: int
    name: str
    age: int


# =========================
# User Schemas
# =========================

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=6)


class UserRead(BaseModel):
    id: int
    username: str


class LoginRequest(BaseModel):
    username: str
    password: str


# =========================
# Doctor Schemas
# =========================

class DoctorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    specialization: str = Field(min_length=2, max_length=50)
    phone: str = Field(
        min_length=11,
        max_length=11,
    )


class DoctorRead(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str


# =========================
# Appointment Schemas
# =========================

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time


class AppointmentRead(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time


class AppointmentDetails(BaseModel):
    id: int
    patient_name: str
    doctor_name: str
    appointment_date: date
    appointment_time: time