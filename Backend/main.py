from fastapi import FastAPI, Path, HTTPException, Query, Depends, status,Response
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,computed_field, Field, EmailStr
from typing import Annotated,Literal,Optional
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import Session
import models, database
from models import Equipment
from datetime import datetime

models.Base.metadata.create_all(bind=database.engine)

SECRET_KEY = "SecretCodethatcantbebreak"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

    token = create_access_token(data={"sub": user.email})
    # response.set_cookie(key="access_token", value=token, httponly=True)
    
    return {
        "access_token": token, 
        "token_type": "bearer",
        "name": user.name,
        "email": user.email,
        "message": "Login successful"
    }
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")
@app.get("/dashboard")
def get_dashboard(token: str = Depends(oauth2_scheme)):
    try:
        # Verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"message": f"Welcome, {email}!"}
    except:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
    
@app.get('/view/')
def view(db: Session = Depends(get_db)):
    user = db.query(models.Equipment).all()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Data Not Found"
        )
    return user
    

@app.post('/equipment/')
def create_equipment(equipment_name: str,serial_number: str,company: str,purchase_date: str,
    warranty_info: str,location: str,db: Session = Depends(get_db)):

    #Prasing The DateTime to DD-MM-YYYY
    try:
        parsed_date = datetime.strptime(purchase_date, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="purchase_date must be in DD-MM-YYYY format (e.g. 01-12-2025)"
        )

    new_equipment = Equipment(
        Equipment_name = equipment_name,
        Serial_Number = serial_number,
        Company = company,
        Purchase_Date = parsed_date,
        Warranty_Info = warranty_info,
        Location = location
    )
    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)

    return new_equipment
    
