from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/libros")

@router.post("", response_model=schemas.LibroResponse)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    db_libro = models.Libro(
        titulo=libro.titulo,
        autor=libro.autor,
        precio=libro.precio,
        disponible=libro.disponible
    )
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

@router.get("/libros", response_model=list[schemas.LibroResponse])
def obtener_libros(db: Session = Depends(get_db)):
    libros = db.query(models.Libro).all()
    return libros

@router.get("/libros/{libro_id}", response_model=schemas.LibroResponse)
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.delete("/libros/{libro_id}")
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    db.delete(libro)
    db.commit()
    return {"mensaje": "Libro eliminado correctamente"}

@router.put("/libros/{libro_id}", response_model=schemas.LibroResponse)
def actualizar_libro(libro_id: int, datos: schemas.LibroCreate, db: Session = Depends(get_db)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    libro.titulo = datos.titulo
    libro.autor = datos.autor
    libro.precio = datos.precio
    libro.disponible = datos.disponible
    db.commit()
    db.refresh(libro)
    return libro