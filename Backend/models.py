from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import date
from sqlalchemy import Date
from database import Base
from datetime import date

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(String(255),unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    


class MaintenanceTeam(Base):
    __tablename__ = "maintenance_team" # Fixed typo [cite: 20]
    id: Mapped[int] = mapped_column(primary_key=True, index=True)    
    team_name: Mapped[str] = mapped_column(unique=True, index=True) # e.g., IT, Mechanics [cite: 22]
    # Link specific users (technicians) to teams [cite: 23]
    manager_id: Mapped[int] = mapped_column(ForeignKey("user.id")) 
  
    

class Equipment(Base):
    __tablename__ = "equipment"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    Equipment_name : Mapped[str] = mapped_column()
    Serial_Number : Mapped[str] = mapped_column(unique=True,index=True)
    Company : Mapped[str] = mapped_column(index=True)
    Purchase_Date : Mapped[date] = mapped_column(Date)
    Warranty_Info : Mapped[str] = mapped_column()
    Location : Mapped[str] = mapped_column()
    
