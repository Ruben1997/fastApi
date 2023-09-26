from fastapi import FastAPI, HTTPException, Depends, status
from mangum import Mangum
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
handler = Mangum(app)
models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel): 
    username: str
    document: str
    phoneNumber: str
    email: str 
    password: str 
    state: str 

def get_db(): 
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/')
async def home():
    return {"message": "Example to FastAPI"} 

@app.post('/create_user', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency): 
    db_user = models.User(**user.dict())
    db.add(db_user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save user")

    return {"message": "User created successfully"}


@app.put('/update_user', status_code=status.HTTP_200_OK)
async def update_user(user: UserBase, db: db_dependency): 
    userUpdate = db.query(models.User).filter(models.User.document == user.document).first()
    if user is None: 
        raise HTTPException(status_code=404, detail='User not found')
    for field, value in user.dict(exclude_unset=True).items():
        if value:
            setattr(userUpdate, field, value)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to update user')

    return {"message": 'User updated successfully'}

@app.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency): 
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None: 
        raise HTTPException(status_code=404, detail='User not found')
    return user 

@app.delete('/users/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency): 
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None: 
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to delete user')

    return {"message": 'User deleted successfully'}

@app.get('/users', status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency): 
    users = db.query(models.User).all()
    return users
