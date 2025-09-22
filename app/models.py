from enum import Enum
from sqlalchemy import Column, Integer, String, Numeric, Boolean, Enum as SAEnum
from .database import Base

class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # Enum en DB (SQLAlchemy crea un CHECK en SQLite)
    role = Column(SAEnum(UserRole, name="user_role"), nullable=False, default=UserRole.CUSTOMER)
    full_name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)  # “username” = email
    hashed_password = Column(String(255), nullable=False)
    balance = Column(Numeric(12, 2), nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)  # nuevo estado