from fastapi import FastAPI, Path, HTTPException, Query, Depends, status,Response
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import Annotated,Literal,Optional
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import Session
import models, database
from datetime import datetime, timedelta,date
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from models import Equipment


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Signup(BaseModel):
    name: Annotated[str,Field(...,description='Name Of User',examples= ['Ajit Chauhan',"Utsav Laheru"])]
    email: Annotated[EmailStr,Field(...,description='Email of User',examples=['Ajit@gmail.com',"Utsav@gmail.com"])]
    password: Annotated[str,Field(...,description='Password Of User',examples=['Ajit@1234'])]

class Login(BaseModel):
    email: Annotated[EmailStr,Field(...,description='Email of User',examples=['Ajit@gmail.com',"Utsav@gmail.com"])]
    password: Annotated[str,Field(...,description='Password Of User',examples=['Ajit@1234'])]

class Equipment_validation(BaseModel):
    equipment_name:Annotated[str,Field(...,description='Name of the Equipment',examples=['MSi laptop','Asus LAptop'])]
    serial_number:Annotated[str,Field(...,description='Serial Number of Equipment',examples=['123WDAD'])]
    company: Annotated[str,Field(...,description='Sub Company name that will handle the euipment',examples=['Odoo Help'])]
    purchase_date: Annotated[date,Field(...,description='Purchase Date of the euipment',examples=['2025-02-05'])]
    assigned_date: Annotated[date, Field(..., description='Date equipment was assigned', examples=['2025-02-06'])]
    warranty_info: Annotated[str,Field(...,description="Warranty Info of Equipment",examples=['How long it has'])]
    location: Annotated[str,Field(...,description='Loaction of office',examples=['Junagadh'])]
    category_id: Annotated[int,Field(...,description='Category of the equipment',examples=['12','2'])]    # Added requirement
    technician_id: Annotated[int,Field(...,description='Id of the technicican that is handling the Euipment',examples=['1','2'])]  # Added requirement
    team_id: Annotated[int, Field(...,description="Id of the team that is handling the equipment",examples=['1','213'])]       # Added requirement
    department: Annotated[str,Field(...,description='Deapartment Name that is handhing the Equipment',examples=['odoo help','oddo warnaty'])]
    is_usable: Annotated[bool,Field(...,description='True of usale or false',examples=['True','Flase'])]
    used_by:Annotated[str,Field(...,description='Employe name that used the equipment',examples=['Mukhesh','Rakesh'])]
    description:Annotated[str,Field(...,description='Full desctiptio of the eqipment received',examples=['Desktop Not showing','Screew Missing '])]
    
class RequestForm(BaseModel):
    created_by:Annotated[str,Field(...,description="Request Creator Name",examples=['Ajit','Utsav'])] 
    maintenance_for:Annotated[str,Field(...,description='Equipment detail',examples=['Asus laptop'])] 
    equipment:Annotated[str,Field(...,description='Equipment Name',examples=['Asus monitor','Msi'])] 
    category:Annotated[str, Field(...,description='Equipment Category',examples=['Monitor','Laptop'])]
    request_date:Annotated[date, Field(...,description='Request Form creation date',examples=['12-02-2200'])]
    maintenance_type:Annotated[Literal['Corrective','Preventive'],Field(..., description="Choose Between two",examples=['Corrective','Preventive'])]
    team:Annotated[str, Field(...,description='Team Name Which will Handel the request',examples=['Team1','team2'])]
    technician:Annotated[str, Field(...,description="Technician name which will handel the operation",examples=['Rushit'])]
    scheduled_date:Annotated[datetime, Field(...,description="The date at which the Equipment will be repair",examples=['12-02-2035'])]
    duration:Annotated[datetime,Field(...,description='Duration it will be take to repair the equipment',examples=['12-02-2025'])]
    priority:Annotated[Literal[1,2,3],Field(..., description="Choose Between two",examples=['1','2','3'])] 
    company:Annotated[str,Field(...,description='The name of the company',examples=['Adani'])]
    
    
    @field_validator('request_date', mode='before')
    @classmethod
    def parse_request_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, "%d-%m-%Y").date()
        return v

    @field_validator('scheduled_date', 'duration', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if isinstance(v, str):
            # Handles "DD-MM-YYYY" or "DD-MM-YYYY HH:MM"
            try:
                return datetime.strptime(v, "%d-%m-%Y %H:%M")
            except ValueError:
                return datetime.strptime(v, "%d-%m-%Y")
        return v
    
    
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
def get_dashboard(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(models.User).filter(models.User.email == email).first()
        return {"message": f"Welcome, {email}!",
                'name':user.name}
    except:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
 
@app.post('/equipment/')
def create_equipment(equipment:Equipment_validation,
    db: Session = Depends(get_db)
):
   
    new_equipment = models.Equipment(
        Equipment_name=equipment.equipment_name,
        Serial_number=equipment.serial_number,
        Company=equipment.company,
        Used_by=equipment.used_by, 
        Purchase_Date=equipment.purchase_date,
        Assigned_Date=equipment.assigned_date, 
        Warranty_Info=equipment.warranty_info,
        Location=equipment.location,
        category_id=equipment.category_id,
        technician_id=equipment.technician_id,
        team_id=equipment.team_id,
        department=equipment.department,
        is_usable=equipment.is_usable,
        Description=equipment.description
    )
    
    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)

    return new_equipment

@app.get('/view_equipment/')
def view_equipment(db: Session = Depends(get_db)):
    user = db.query(models.Equipment).all()
    return user

    
@app.get('/view/')
def view(db: Session = Depends(get_db)):
    user = db.query(models.Equipment).all()
    return user



  
@app.post('/requestform/')
def create_requestform(request: RequestForm, db: Session = Depends(get_db)):
    # Data is already validated by Pydantic here
    
    new_requestform = models.RequestForm(
        Created_By = request.created_by,
        Maintenance_For = request.maintenance_for,
        Equipment = request.equipment,
        Category = request.category,
        Request_Date = request.request_date,
        Maintenance_Type = request.maintenance_type,
        Team = request.team,
        Technician = request.technician,
        Scheduled_Date = request.scheduled_date,
        Duration = request.duration,
        Priority = request.priority,
        Company = request.company,
        Current_Status = "New Request",
        Notes = "",
        Instruction = ""
    )
    
    try:
        db.add(new_requestform)
        db.commit()
        db.refresh(new_requestform)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error during save.")
    
    return new_requestform

    
@app.get('/view_requests/')
def view_requests(db: Session = Depends(get_db)):
    return db.query(models.RequestForm).all()

