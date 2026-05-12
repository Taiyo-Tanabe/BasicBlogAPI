from fastapi import APIRouter, Depends
from ..schemas import User, ShowUser
from ..database import get_db
from sqlalchemy.orm import Session
from ..functions import user 

router = APIRouter(prefix='/user', tags=['users'])

@router.post('/')
def create_user(request: User, db: Session = Depends(get_db)):
    return user.create(request, db)

@router.get('/{id}', response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)