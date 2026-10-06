from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models
import crud
import schemas
from auth import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    verify_refresh_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from routers_education import router as education_router
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
import uuid

# Créer les tables
Base.metadata.create_all(bind=engine)
if "photo" not in {column["name"] for column in inspect(engine).get_columns("students")}:
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE students ADD COLUMN photo VARCHAR"))

# Créer l'application FastAPI
app = FastAPI(
    title="Education API",
    description="API pour gérer les utilisateurs et le système éducatif",
    version="2.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "*"  # À remplacer par des domaines spécifiques en production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure le router éducatif
app.include_router(education_router)

# Limiteur de taux
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Gestionnaire d'exception pour la limite de taux
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request, exc):
    request_id = str(uuid.uuid4())
    return JSONResponse(
        status_code=429,
        content={"detail": f"Oops, you reached the rate limit. Please try again later. Request ID: {request_id}"}
    )


# Dépendance pour obtenir la session DB
def get_db():
    """Obtenir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Routes
@app.get("/", tags=["Root"])
def root():
    """Route racine"""
    return {
        "message": "Bienvenue à l'API Education",
        "version": "2.0.0"
    }


# ==================== USER ENDPOINTS ====================

@app.post("/auth/register", response_model=schemas.User, tags=["Auth"])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Créer un nouvel utilisateur"""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_user(db=db, user=user)


@app.post("/auth/login", response_model=schemas.Token, tags=["Auth"])
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """Se connecter et obtenir un token"""
    db_user = crud.get_user_by_username(db, username=user.username)
    if not db_user or not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    if not db_user.is_active:
        raise HTTPException(status_code=400, detail="User is inactive")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": db_user.username})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds()),
    }


@app.post("/auth/refresh", response_model=schemas.Token, tags=["Auth"])
def refresh_access_token(
    request: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """Renouveler le token d'accès à partir du token de renouvellement"""
    username = verify_refresh_token(request.refresh_token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None or not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires,
    )
    return {
        "access_token": access_token,
        "refresh_token": request.refresh_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds()),
    }


@app.get("/users/me", response_model=schemas.User, tags=["Users"])
def get_current_user_info(current_user = Depends(get_current_user)):
    """Obtenir les informations de l'utilisateur actuel"""
    return current_user


@app.get("/users/", response_model=list[schemas.User], tags=["Users"])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir la liste de tous les utilisateurs (authentification requise)"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir un utilisateur par ID (authentification requise)"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour un utilisateur (authentification requise)"""
    # Vérifier que l'utilisateur modifie son propre profil
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer un utilisateur (authentification requise)"""
    # Vérifier que l'utilisateur supprime son propre compte
    if current_user.id == user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
