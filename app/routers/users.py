from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from utils import hash_password

router = APIRouter()
@router.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        role=user.role,
        hashed_password=hashed_pw
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users", response_model=list[schemas.UserResponse])
def get_users(
    email: str = Query(None, description="Filter by email"),
    role: str = Query(None, description="Filter by role"),
    db: Session = Depends(get_db)
):
    # Base query to retrieve users
    query = db.query(models.User)

    if email:
        query = query.filter(models.User.email == email)
    if role:
        query = query.filter(models.User.role == role)
    
    # Execute query
    users = query.all()
    
    if not users:
        raise HTTPException(status_code=404, detail="No users found with the given criteria")
        return users