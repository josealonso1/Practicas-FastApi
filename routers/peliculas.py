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

@router.put("/{pelicula_id}", response_model=schemas.PeliculaResponse)
def editar_pelicula(pelicula_id: int, datos: schemas.PeliculaCreate, db: Session = Depends(get_db)):
    pelicula = db.query(models.Pelicula).filter(models.Pelicula.id == pelicula_id).first()
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    pelicula.titulo = datos.titulo
    pelicula.director = datos.director
    pelicula.año = datos.año
    pelicula.duracion_minutos = datos.duracion_minutos
    pelicula.activa = datos.activa
    db.commit()
    db.refresh(pelicula)
    return pelicula    