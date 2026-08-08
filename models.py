from datetime import date, time
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int

    appointments: list["Appointment"] = Relationship(
        back_populates="patient"
    )


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str


class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    specialization: str
    phone: str

    appointments: list["Appointment"] = Relationship(
        back_populates="doctor"
    )


class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    patient_id: int = Field(foreign_key="patient.id")
    doctor_id: int = Field(foreign_key="doctor.id")

    appointment_date: date
    appointment_time: time

    patient: Optional["Patient"] = Relationship(
        back_populates="appointments"
    )

    doctor: Optional["Doctor"] = Relationship(
        back_populates="appointments"
    )