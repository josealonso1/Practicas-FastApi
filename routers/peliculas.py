from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/peliculas")

@router.post("", response_model=schemas.PeliculaResponse)
def crear_peliculas(pelicula: schemas.PeliculaCreate, db: Session = Depends(get_db)):
    db_pelicula = models.Pelicula(
        titulo = pelicula.titulo,
        director = pelicula.director,
        año = pelicula.año,
        duracion_minutos = pelicula.duracion_minutos,
        activa = pelicula.activa
    )
    db.add(db_pelicula)
    db.commit()
    db.refresh(db_pelicula)
    return db_pelicula

@router.get("", response_model=list[schemas.PeliculaResponse])
def obtener_peliculas(db: Session = Depends(get_db)):
    peliculas = db.query(models.Pelicula).all()
    return peliculas

@router.get("/{pelicula_id}", response_model=schemas.PeliculaResponse)
def obtener_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    pelicula = db.query(models.Pelicula).filter(models.Pelicula.id == pelicula_id).first()
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    return pelicula

@router.delete("/{pelicula_id}")
def eliminar_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    pelicula = db.query(models.Pelicula).filter(models.Pelicula.id == pelicula_id).first()
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    db.delete(pelicula)
    db.commit()
    return {"mensaje": "Pelicula eliminado correctamente"}

@router.patch("/{pelicula_id}", response_model=schemas.PeliculaResponse)
def editar_pelicula(pelicula_id: int, datos: schemas.PeliculaUpdate, db: Session = Depends(get_db)):
    pelicula = db.query(models.Pelicula).filter(models.Pelicula.id == pelicula_id).first()
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    
    datos_actualizados = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(pelicula, campo, valor)
    
    db.commit()
    db.refresh(pelicula)
    return pelicula    

@router.post("/{pelicula_id}/actores/{actor_id}", response_model=schemas.PeliculaResponse)
def agregar_actor_a_pelicula(pelicula_id: int, actor_id: int, db: Session = Depends(get_db)):
    pelicula = db.query(models.Pelicula).filter(models.Pelicula.id == pelicula_id).first()
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor no encontrado")
    
    if actor in pelicula.actores:
        raise HTTPException(status_code=400, detail="El actor ya está asociado a esta película")
    
    pelicula.actores.append(actor)
    db.commit()
    db.refresh(pelicula)
    return pelicula

@router.delete("/{pelicula_id}/actores/{actor_id}")
def quitar_actor_de_pelicula(pelicula_id: int, actor_id: int, db: Session = Depends(get_db)):
    pelicula = db.query(models.Pelicula).filter(models.Pelicula.id == pelicula_id).first()
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if actor is None or actor not in pelicula.actores:
        raise HTTPException(status_code=404, detail="El actor no está asociado a esta película")
    
    pelicula.actores.remove(actor)
    db.commit()
    return {"mensaje": "Actor removido de la película correctamente"}