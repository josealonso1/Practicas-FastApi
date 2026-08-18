from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from database import Base
from sqlalchemy.orm import relationship

pelicula_actor = Table(
    "pelicula_actor",
    Base.metadata,          
    Column("pelicula_id", Integer, ForeignKey("peliculas.id")),
    Column("actor_id", Integer, ForeignKey("actores.id"))
)

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True)
    
class Pelicula(Base):
    __tablename__ = "peliculas"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    director = Column(String(50), nullable=False)
    año = Column(Integer, nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    activa = Column(Boolean, default=True)
    
    reseñas = relationship("Reseña", back_populates="pelicula")
    actores = relationship("Actor", secondary=pelicula_actor, back_populates="peliculas")
    
class Reseña(Base):
    __tablename__ = "reseñas"
    
    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String(500), nullable=False)
    puntuacion = Column(Integer, nullable=False)
    
    pelicula_id = Column(Integer, ForeignKey("peliculas.id"), nullable=False)
    
    pelicula = relationship("Pelicula", back_populates="reseñas")
    
class Actor(Base):
    __tablename__ = "actores"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    pais = Column(String(20), nullable=False)
    
    peliculas = relationship("Pelicula", secondary=pelicula_actor, back_populates="actores")