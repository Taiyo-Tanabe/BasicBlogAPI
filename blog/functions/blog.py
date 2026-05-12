from ..  import models
from ..schemas import Blog
from sqlalchemy.orm import Session
from fastapi import status,  HTTPException

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(blog: Blog, db: Session, current_user):
    user_id = [d for d in current_user]
    user_id = user_id[0].id
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id:int, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

def update(id:int, request: Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not found')
    blog.update(request.model_dump())
    db.commit()
    return 'Updated'

