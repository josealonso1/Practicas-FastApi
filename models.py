from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Libro(Base):
    __tablename__ = "libros"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(50), nullable=False)
    precio = Column(Float, nullable=False)
    disponible = Column(Boolean, default=True)
    año_publicacion = Column(Integer, nullable=True)
    
class Pelicula(Base):
    __tablename__ = "peliculas"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    director = Column(String(50), nullable=False)
    año = Column(Integer, nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    activa = Column(Boolean, default=True)
    
    reseñas = relationship("Reseñas", back_populates="pelicula")
    
class Reseña(Base):
    __tablename__ = "reseñas"
    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String(500), nullable=False)
    puntuacion = Column(Integer, nullable=False)
    
    pelicula_id = Column(Integer, ForeignKey("peliculas.id"), nullable=False)
    
    pelicula = relationship("Pelicula", back_populates="reseñas")