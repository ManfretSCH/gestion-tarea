from fastapi import APIRouter, HTTPException, Depends
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.database import get_db
from app.models import User, Task

router = APIRouter()


@router.get("/", status_code=200, response_model=list[UserResponse])
def get_users(db=Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db=Depends(get_db)):
    existing_user= db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    new_user = User(
        name=user.name,
        email=user.email,
        age=user.age
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", status_code=200, response_model=UserResponse)
def get_user(user_id: int, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", status_code= 200, response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_user = db.query(User).filter(User.email == user_update.email, User.id != user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for task in tasks:
        db.delete(task)
    db.delete(user)
    db.commit()