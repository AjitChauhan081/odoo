from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import date,datetime
from sqlalchemy import Date,DateTime
from database import Base
from datetime import date


class MaintenanceTeam(Base):
    __tablename__ = "maintenance_team" # Fixed typo [cite: 20]
    id: Mapped[int] = mapped_column(primary_key=True, index=True)    
    team_name: Mapped[str] = mapped_column(unique=True, index=True)
    team_member_name: Mapped[str] = mapped_column()
    workflow_logic: Mapped[str] = mapped_column()

#Test
class RequestForm(Base):
    __tablename__="requestform"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    Created_By : Mapped[str] = mapped_column(index=True)
    Maintenance_For : Mapped[str] = mapped_column()      #make it into field so it have only equipment and work center
    Equipment : Mapped[str] = mapped_column()            #Filed for selecting equipment
    Category : Mapped[str] = mapped_column()
    Request_Date : Mapped[date] = mapped_column(Date)
    Maintenance_Type : Mapped[str] = mapped_column()     #Filed For Type like Corrective or Preventive

    #Maintance Info (Which will be Automatically Fetched From Maintance Team Table)
    Team : Mapped[str] = mapped_column()
    Technician : Mapped[str] = mapped_column()
    Scheduled_Date : Mapped[datetime] = mapped_column(DateTime)
    Duration : Mapped[datetime] = mapped_column(DateTime)
    Priority : Mapped[int] = mapped_column()
    Company : Mapped[str] = mapped_column()
    
    Current_Status : Mapped[str] = mapped_column()      #Field For Maintance to change the requester to see That it on "New Request","In progress","Repaired","Scrap"

    #Comment Bar
    Notes : Mapped[str] = mapped_column()
    Instruction : Mapped[str] = mapped_column()
    

class Equipment(Base):
    __tablename__ = "equipment"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    Equipment_name : Mapped[str] = mapped_column()
    Serial_Number : Mapped[str] = mapped_column(unique=True,index=True)
    Company : Mapped[str] = mapped_column(index=True)
    Purchase_Date : Mapped[date] = mapped_column(Date)
    Warranty_Info : Mapped[str] = mapped_column()
    Location : Mapped[str] = mapped_column()
    


