from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Libro(Base):
    __tablename__ = "libros"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(50), nullable=False)
    precio = Column(Float, nullable=False)
    disponible = Column(Boolean, default=True)
    año_publicacion = Column(Integer, nullable=True)