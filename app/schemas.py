from pydantic import BaseModel, Field, EmailStr, field_validator
from enum import Enum

class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

# ---------- INPUTS (lo que recibe la API) ----------

class UserCreate(BaseModel):
    role: UserRole = UserRole.CUSTOMER
    full_name: str = Field(..., min_length=3, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    balance: float = 0.0  # opcional, por defecto 0
    is_active: bool = True  # opcional, por defecto True

    # Normaliza email a minúsculas
    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

# ---------- OUTPUTS (lo que devuelve la API) ----------

class UserRead(BaseModel):
    id: int
    role: UserRole = UserRole.CUSTOMER
    full_name: str
    email: EmailStr
    balance: float
    is_active: bool

    class Config:
        from_attributes = True  # permite leer desde objetos SQLAlchemy