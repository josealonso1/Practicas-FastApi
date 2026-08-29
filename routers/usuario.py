from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
import models, schemas, auth

router = APIRouter()

@router.post("/usuarios", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.username == usuario.username).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El username ya está registrado")

    hash_generado = auth.get_password_hash(usuario.password)

    db_usuario = models.Usuario(
        username=usuario.username,
        email=usuario.email,
        hashed_password=hash_generado
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.username == form_data.username).first()

    if not usuario or not auth.verify_password(form_data.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    access_token = auth.create_access_token(
        data={"sub": usuario.username},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/usuarios/me", response_model=schemas.UsuarioResponse)
def leer_usuario_actual(usuario_actual: models.Usuario = Depends(auth.get_current_user)):
    return usuario_actual