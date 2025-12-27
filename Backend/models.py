from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Boolean, Date, Float
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
  
    
class EquipmentCategory(Base):
    __tablename__ = "equipment_category"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True) # e.g., Computers, Monitors [cite: 9]


class Equipment(Base):
    __tablename__ = "equipment"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column() 
    serial_number: Mapped[str] = mapped_column(unique=True) 
    category_id: Mapped[int] = mapped_column(ForeignKey("equipment_category.id"))
    department: Mapped[str] = mapped_column() 
    location: Mapped[str] = mapped_column() 
    is_usable: Mapped[bool] = mapped_column(default=True) # For Scrap logic [cite: 72]
    
    # Ownership & Responsibility [cite: 9, 15]
    team_id: Mapped[int] = mapped_column(ForeignKey("maintenance_team.id"))
    technician_id: Mapped[int] = mapped_column(ForeignKey("user.id")) # Default technician


class MaintenanceRequest(Base):
    __tablename__ = "maintenance_request"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    subject: Mapped[str] = mapped_column() 
    request_type: Mapped[str] = mapped_column() # Corrective or Preventive [cite: 27]
    
    # Kanban Stages: New | In Progress | Repaired | Scrap [cite: 56]
    stage: Mapped[str] = mapped_column(default="New") 
    
    scheduled_date: Mapped[date] = mapped_column(Date, nullable=True) 
    duration: Mapped[float] = mapped_column(Float, default=0.0) 
    
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id")) 
    team_id: Mapped[int] = mapped_column(ForeignKey("maintenance_team.id"))
    technician_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
