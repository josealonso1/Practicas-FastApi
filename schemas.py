from pydantic import BaseModel, Field
from typing import Optional

##### Libros #####

class LibroCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    autor: str = Field(min_length=1, max_length=50)
    precio: float = Field(gt=0)
    disponible: bool = True
    año_publicacion: Optional[int] = None

class LibroResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    precio: float
    disponible: bool
    año_publicacion: Optional[int] = None
    
    model_config = {"from_attributes": True}
    
##### Pelicula #####

class PeliculaCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    director: str = Field(min_length=3, max_length=50)
    año: int = Field(ge=1895, le=2026)
    duracion_minutos: int = Field(gt=0 ,le=600)
    activa: bool = True
    
class PeliculaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=100)
    director: Optional[str] = Field(None, min_length=3, max_length=50)
    año: Optional[int] = Field(None, ge=1895, le=2026)
    duracion_minutos: Optional[int] = Field(None, gt=0 ,le=600)
    activa: Optional[bool] = None

class PeliculaResponse(BaseModel):
    id: int
    titulo: str
    director: str
    año: int
    duracion_minutos: int
    activa: bool
    
    model_config = {"from_attributes": True}
    
class ReseñaCreate(BaseModel):
    texto: str = Field(min_length=10, max_length=500)
    puntuacion: int = Field(ge=1, le=10)
    pelicula_id: int 

class ReseñaResponse(BaseModel):
    id: int
    texto: str
    puntuacion: int
    pelicula_id: int
    model_config = {"from_attributes": True}
    