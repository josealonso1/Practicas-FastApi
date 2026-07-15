from pydantic import BaseModel, Field
from typing import Optional

class LibroCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    autor: str = Field(min_length=1, max_length=50)
    precio: float = Field(gt=0)
    disponible: bool = True

class LibroResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    precio: float
    disponible: bool
    
class PeliculaCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    director: str = Field(min_length=3, max_length=50)
    año: int = Field(ge=1895, le=2026)
    duracion_minutos: int = Field(gt=0 ,le=360)
    activa: bool = True
    
    model_config = {"from_attributes": True}