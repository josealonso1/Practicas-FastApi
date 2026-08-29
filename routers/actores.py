from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/actores")

@router.post("", response_model=schemas.ActorResponse)
def crear_actores(actor: schemas.ActorCreate, db: Session = Depends(get_db),
                  usuario_actual: models.Usuario = Depends(auth.get_current_user)):
    db_actor = models.Actor(
        nombre = actor.nombre,
        apellido = actor.apellido,
        pais = actor.pais
    )
    
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor

@router.get("", response_model=list[schemas.ActorResponse])
def obtener_actores(db: Session = Depends(get_db)):
    actores = db.query(models.Actor).all()
    return actores

@router.get("/{actor_id}", response_model=schemas.ActorResponse)
def obtener_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor no encontrada")
    return actor

@router.patch("/{actor_id}", response_model=schemas.ActorResponse)
def actualizar_actor(actor_id: int, datos: schemas.ActorUpdate, db: Session = Depends(get_db),
                     usuario_actual: models.Usuario = Depends(auth.get_current_user)):
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor no encontrada")
    
    datos_actualizados= datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(actor, campo, valor)
        
    db.commit()
    db.refresh(actor)
    return actor

@router.delete("/{actor_id}")
def eliminar_actor(actor_id: int, db: Session = Depends(get_db),
                   usuario_actual: models.Usuario = Depends(auth.get_current_user)):
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor no encontrado")
    
    db.delete(actor)
    db.commit()
    return {"mensaje": "Actor eliminado correctamente"}
