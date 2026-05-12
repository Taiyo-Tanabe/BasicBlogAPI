from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from ..schemas import Blog, ShowBlog, User
from ..database import get_db
from .. import models, oauth2
from sqlalchemy.orm import Session
from ..functions import blog

router = APIRouter(prefix='/blog', tags=['blogs'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Blog, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    return blog.create(request, db, current_user)

@router.get('/', response_model=List[ShowBlog])
def all_fetch(db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not available')
    return blog

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    return blog.destroy(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update(request.model_dump())
    db.commit()
    return blog.update(id, request, db)