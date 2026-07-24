from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/reseñas")


@router.post("/pelicula/{pelicula_id}" ,response_model=schemas.ReseñaResponse)
def crear_reseña(pelicula_id: int, reseña: schemas.ReseñaCreate, db:Session = Depends(get_db)):
    pelicula = db.query(models.Pelicula).filter(
        models.Pelicula.id == pelicula_id
    ).first()
    
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    db_reseña = models.Reseña(
        texto = reseña.texto,
        puntuacion = reseña.puntuacion,
        pelicula_id = pelicula_id
    )
    
    db.add(db_reseña)
    db.commit()
    db.refresh(db_reseña)
    return db_reseña