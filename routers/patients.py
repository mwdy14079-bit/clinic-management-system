from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Patient
from schemas import PatientCreate, PatientRead
from security import get_current_user


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=PatientRead)
def create_patient(
    patient_data: PatientCreate,
    session: Session = Depends(get_session),
):
    patient = Patient(
        name=patient_data.name,
        age=patient_data.age,
    )

    session.add(patient)
    session.commit()
    session.refresh(patient)

    return patient


@router.get("/", response_model=list[PatientRead])
def get_patients(
    session: Session = Depends(get_session),
):
    patients = session.exec(
        select(Patient)
    ).all()

    return patients


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(
    patient_id: int,
    session: Session = Depends(get_session),
):
    patient = session.get(
        Patient,
        patient_id,
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return patient


@router.put("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: int,
    patient_data: PatientCreate,
    session: Session = Depends(get_session),
):
    patient = session.get(
        Patient,
        patient_id,
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    patient.name = patient_data.name
    patient.age = patient_data.age

    session.add(patient)
    session.commit()
    session.refresh(patient)

    return patient


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    session: Session = Depends(get_session),
):
    patient = session.get(
        Patient,
        patient_id,
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    session.delete(patient)
    session.commit()

    return {
        "message": "Patient deleted successfully"
    }