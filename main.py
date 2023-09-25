from fastapi import FastAPI, HTTPException, Depends, status
from mangum import Mangum
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post('/user/', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency): 
    try:
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

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
    db.commit()

@app.get('/users', status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency): 
    users = db.query(models.User).all()
    return users
