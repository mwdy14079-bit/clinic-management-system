
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Doctor
from schemas import DoctorCreate, DoctorRead
from security import get_current_user


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=DoctorRead)
def create_doctor(
    doctor_data: DoctorCreate,
    session: Session = Depends(get_session),
):
    doctor = Doctor(
        name=doctor_data.name,
        specialization=doctor_data.specialization,
        phone=doctor_data.phone,
    )

    session.add(doctor)
    session.commit()
    session.refresh(doctor)

    return doctor


@router.get("/", response_model=list[DoctorRead])
def get_doctors(
    session: Session = Depends(get_session),
):
    doctors = session.exec(
        select(Doctor)
    ).all()

    return doctors


@router.get("/{doctor_id}", response_model=DoctorRead)
def get_doctor(
    doctor_id: int,
    session: Session = Depends(get_session),
):
    doctor = session.get(
        Doctor,
        doctor_id,
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    return doctor


@router.put("/{doctor_id}", response_model=DoctorRead)
def update_doctor(
    doctor_id: int,
    doctor_data: DoctorCreate,
    session: Session = Depends(get_session),
):
    doctor = session.get(
        Doctor,
        doctor_id,
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    doctor.name = doctor_data.name
    doctor.specialization = doctor_data.specialization
    doctor.phone = doctor_data.phone

    session.add(doctor)
    session.commit()
    session.refresh(doctor)

    return doctor


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    session: Session = Depends(get_session),
):
    doctor = session.get(
        Doctor,
        doctor_id,
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    session.delete(doctor)
    session.commit()

    return {
        "message": "Doctor deleted successfully"
    }
