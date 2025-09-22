from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import User
from .schemas import UserCreate, UserRead
from .security import get_password_hash

app = FastAPI(title="Users API (simple)")

# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)

@app.get("/", tags=["health"])
def health():
    return {"ok": True, "service": "users-api"}

# Registrar usuario
@app.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED, tags=["users"])
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    # Validación simple de username único
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El username ya está registrado."
        )

    user = User(
        role=payload.role,
        full_name=payload.full_name,
        email=payload.email,
        is_active=payload.is_active,
        hashed_password=get_password_hash(payload.password),
        balance=round(payload.balance or 0.0, 2),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Obtener un usuario por ID
@app.get("/users/{user_id}", response_model=UserRead, tags=["users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    return user

# Listar usuarios (simple, sin paginación)
@app.get("/users", response_model=list[UserRead], tags=["users"])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id.asc()).all()