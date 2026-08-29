from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/resehas")


@router.get("", response_model=list[schemas.ReseñaResponse])
def obtener_reseñas(db:Session = Depends(get_db)):
    reseñas = db.query(models.Reseña).all()
    return reseñas

@router.get("/pelicula/{pelicula_id}", response_model=list[schemas.ReseñaResponse])
def obtener_reseña_pelicula(pelicula_id: int, db:Session = Depends(get_db)):
    pelicula = db.query(models.Pelicula).filter(models.Pelicula.id == pelicula_id).first()
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    
    return pelicula.reseñas
    
@router.get("/{id}", response_model=schemas.ReseñaResponse)
def obtener_reseña(id: int, db:Session = Depends(get_db)):
    reseña = db.query(models.Reseña).filter(models.Reseña.id == id).first()
    
    if reseña is None:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    return reseña

@router.post("/pelicula/{id}" ,response_model=schemas.ReseñaResponse)
def crear_reseña(id: int, reseña: schemas.ReseñaCreate,
                 db:Session = Depends(get_db),
                 usuario_actual: models.Usuario = Depends(auth.get_current_user)):
    pelicula = db.query(models.Pelicula).filter(
        models.Pelicula.id == id
    ).first()
    
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    db_reseña = models.Reseña(
        texto = reseña.texto,
        puntuacion = reseña.puntuacion,
        pelicula_id = id
    )
    
    db.add(db_reseña)
    db.commit()
    db.refresh(db_reseña)
    return db_reseña

@router.delete("/{id}")
def eliminar_reseña(id: int, db:Session = Depends(get_db),
                    usuario_actual: models.Usuario = Depends(auth.get_current_user)):
    reseña = db.query(models.Reseña).filter(models.Reseña.id == id).first()
    
    if reseña is None:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    
    db.delete(reseña)
    db.commit()
    
    return {"mensaje": "Reseña eliminada correctamente"}

@router.patch("/{id}", response_model=schemas.ReseñaResponse)
def editar_reseña(id: int, datos: schemas.ReseñaUpdate, db:Session = Depends(get_db),
                  usuario_actual: models.Usuario = Depends(auth.get_current_user)):
    reseña = db.query(models.Reseña).filter(models.Reseña.id == id).first()
    if reseña is None:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    
    datos_actualizados = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(reseña, campo, valor)
        
    db.commit()
    db.refresh(reseña)
    
    return reseña