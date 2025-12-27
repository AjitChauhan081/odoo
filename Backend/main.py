from fastapi import FastAPI, Path, HTTPException, Query, Depends, status
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,computed_field, Field, EmailStr
from typing import Annotated,Literal,Optional
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import Session
import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

class Signup(BaseModel):
    name: Annotated[str,Field(...,description='Name Of User',examples= ['Ajit Chauhan',"Utsav Laheru"])]
    email: Annotated[EmailStr,Field(...,description='Email of User',examples=['Ajit@gmail.com',"Utsav@gmail.com"])]
    password: Annotated[str,Field(...,description='Password Of User',examples=['Ajit@1234'])]

class Login(BaseModel):
    email: Annotated[EmailStr,Field(...,description='Email of User',examples=['Ajit@gmail.com',"Utsav@gmail.com"])]
    password: Annotated[str,Field(...,description='Password Of User',examples=['Ajit@1234'])]


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app= FastAPI()

@app.post('/signup/')
def create_user(sign:Signup, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == sign.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(name=sign.name, email=sign.email, password=sign.password) 
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "message": "User created successfully"
    }


@app.post('/login/')
def fetch_user(login:Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == login.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User does not exist"
        )

    if user.password != login.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid password"
        )

    return JSONResponse(status_code=200,content={
        "name": user.name,
        "email": user.email,
        "message": "Login successful"
    })
    
@app.get('/view/')
def view(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user
    
