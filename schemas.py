from pydantic import BaseModel, Field
from typing import Optional

##### Reseñas ######    
    
class ReseñaCreate(BaseModel):
    texto: str = Field(min_length=10, max_length=500)
    puntuacion: int = Field(ge=1, le=10)
    
class ReseñaUpdate(BaseModel):
    texto: Optional[str] = Field(None, min_length=10, max_length=500)
    puntuacion: Optional[int] = Field(None, ge=1, le=10)
    
class ReseñaResponse(BaseModel):
    id: int
    texto: str
    puntuacion: int
    pelicula_id: int
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
    reseñas: list[ReseñaResponse] = []    
    model_config = {"from_attributes": True}
    