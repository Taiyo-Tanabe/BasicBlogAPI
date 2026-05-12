from fastapi import status, HTTPException
from .. import models
from ..schemas import User
from sqlalchemy.orm import Session
from ..hashing import Hash

def create(request: User, db: Session):
    new_user = models.User(name=request.name, email=request.name, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {id} id not available')
    return user