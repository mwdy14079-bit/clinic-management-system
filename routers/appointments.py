
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Appointment, Doctor, Patient
from schemas import (
    AppointmentCreate,
    AppointmentDetails,
    AppointmentRead,
)
from security import get_current_user


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=AppointmentRead)
def create_appointment(
    appointment_data: AppointmentCreate,
    session: Session = Depends(get_session),
):
    # Check patient
    patient = session.get(
        Patient,
        appointment_data.patient_id,
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    # Check doctor
    doctor = session.get(
        Doctor,
        appointment_data.doctor_id,
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    # Check doctor availability
    existing_appointment = session.exec(
        select(Appointment).where(
            Appointment.doctor_id
            == appointment_data.doctor_id,
            Appointment.appointment_date
            == appointment_data.appointment_date,
            Appointment.appointment_time
            == appointment_data.appointment_time,
        )
    ).first()

    if existing_appointment:
        raise HTTPException(
            status_code=400,
            detail="Doctor is already booked at this time",
        )

    appointment = Appointment(
        patient_id=appointment_data.patient_id,
        doctor_id=appointment_data.doctor_id,
        appointment_date=appointment_data.appointment_date,
        appointment_time=appointment_data.appointment_time,
    )

    session.add(appointment)
    session.commit()
    session.refresh(appointment)

    return appointment


@router.get("/", response_model=list[AppointmentRead])
def get_appointments(
    session: Session = Depends(get_session),
):
    appointments = session.exec(
        select(Appointment)
    ).all()

    return appointments


@router.get(
    "/details",
    response_model=list[AppointmentDetails],
)
def get_appointment_details(
    session: Session = Depends(get_session),
):
    appointments = session.exec(
        select(Appointment)
    ).all()

    result = []

    for appointment in appointments:
        patient = session.get(
            Patient,
            appointment.patient_id,
        )

        doctor = session.get(
            Doctor,
            appointment.doctor_id,
        )

        if patient and doctor:
            result.append(
                AppointmentDetails(
                    id=appointment.id,
                    patient_name=patient.name,
                    doctor_name=doctor.name,
                    appointment_date=appointment.appointment_date,
                    appointment_time=appointment.appointment_time,
                )
            )

    return result


@router.get(
    "/{appointment_id}",
    response_model=AppointmentRead,
)
def get_appointment(
    appointment_id: int,
    session: Session = Depends(get_session),
):
    appointment = session.get(
        Appointment,
        appointment_id,
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found",
        )

    return appointment


@router.put(
    "/{appointment_id}",
    response_model=AppointmentRead,
)
def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentCreate,
    session: Session = Depends(get_session),
):
    appointment = session.get(
        Appointment,
        appointment_id,
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found",
        )

    # Check patient
    patient = session.get(
        Patient,
        appointment_data.patient_id,
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    # Check doctor
    doctor = session.get(
        Doctor,
        appointment_data.doctor_id,
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    # Check if another appointment
    # already uses the same doctor and time
    existing_appointment = session.exec(
        select(Appointment).where(
            Appointment.doctor_id
            == appointment_data.doctor_id,
            Appointment.appointment_date
            == appointment_data.appointment_date,
            Appointment.appointment_time
            == appointment_data.appointment_time,
            Appointment.id != appointment_id,
        )
    ).first()

    if existing_appointment:
        raise HTTPException(
            status_code=400,
            detail="Doctor is already booked at this time",
        )

    appointment.patient_id = appointment_data.patient_id
    appointment.doctor_id = appointment_data.doctor_id
    appointment.appointment_date = (
        appointment_data.appointment_date
    )
    appointment.appointment_time = (
        appointment_data.appointment_time
    )

    session.add(appointment)
    session.commit()
    session.refresh(appointment)

    return appointment


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    session: Session = Depends(get_session),
):
    appointment = session.get(
        Appointment,
        appointment_id,
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found",
        )

    session.delete(appointment)
    session.commit()

    return {
        "message": "Appointment deleted successfully"
    }

