
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import User
from schemas import UserCreate, UserRead
from security import hash_password


router = APIRouter()


@router.post("/", response_model=UserRead)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
):
    username = user_data.username.strip()

    existing_user = session.exec(
        select(User).where(
            User.username == username
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    user = User(
        username=username,
        password=hash_password(user_data.password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get("/", response_model=list[UserRead])
def get_users(
    session: Session = Depends(get_session),
):
    users = session.exec(
        select(User)
    ).all()

    return users


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    user = session.get(
        User,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    user = session.get(
        User,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    session.delete(user)
    session.commit()

    return {
        "message": "User deleted successfully"
    }