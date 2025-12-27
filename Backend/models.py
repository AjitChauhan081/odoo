from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database import Base

class User(Base):
    __tablename__ = "user"

    # Mapped and mapped_column provide better type hinting
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(String(255),unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    


class MaintenanceTeam(Base):
    __tablename__="Maintance Team"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)    
    team_name: Mapped[str] = mapped_column(unique=True, index=True)
    team_member_name: Mapped[str] = mapped_column()
    workflow_logic: Mapped[str] = mapped_column()
    
