from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.helpers import verify_password, create_token, hash_password
from app.schemas import UserCreate, UserResponse
from app.model import User

router = APIRouter()

@router.post("/login")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "role": user.role, "user_id": user.id}

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_pw = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pw,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user