from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from database import engine

from routers.patients import router as patients_router
from routers.doctors import router as doctors_router
from routers.users import router as users_router
from routers.auth import router as auth_router
from routers.appointments import router as appointments_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Clinic Management System",
    description="Professional clinic management system API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {
        "message": "Clinic Management System",
        "status": "running",
    }


app.include_router(
    patients_router,
    prefix="/patients",
    tags=["Patients"],
)

app.include_router(
    doctors_router,
    prefix="/doctors",
    tags=["Doctors"],
)

app.include_router(
    users_router,
    prefix="/users",
    tags=["Users"],
)

app.include_router(
    auth_router,
    tags=["Authentication"],
)

app.include_router(
    appointments_router,
    prefix="/appointments",
    tags=["Appointments"],
)