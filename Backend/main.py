from fastapi import FastAPI, Path, HTTPException, Query, Depends, status
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,computed_field, Field
from typing import Annotated,Literal,Optional
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import Session
import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app= FastAPI()

@app.post('/signup/')
def create_user(name: str, email: str, pas: str, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(name=name, email=email, password=pas) 
    
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
def fetch_user(email: str, pas: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User does not exist"
        )

    if user.password != pas:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid password"
        )

    return {
        "name": user.name,
        "email": user.email,
        "message": "Login successful"
    }
    
@app.get('/view/')
def view(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user
    
