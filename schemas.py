from pydantic import BaseModel, Field
from typing import Optional

##### usuario ######

class UsuarioCreate(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=8, max_length=30)
    activo: bool = True

class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: str
    activo: bool
    model_config = {"from_attributes": True}
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None      
    
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
    

##### Actores #####

class ActorCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    apellido: str = Field(min_length=1, max_length=50)
    pais: str = Field(min_length=2, max_length=20)
    
class ActorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    apellido: Optional[str] = Field(None, min_length=1, max_length=50)
    pais: Optional[str] = Field(None, min_length=2, max_length=20)
    
class ActorSimple(BaseModel):
    id: int
    nombre: str
    apellido: str
    pais: str
    model_config = {"from_attributes": True}    

class ActorResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    pais: str
    peliculas: list["PeliculaSimple"] = []
    
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
    
class PeliculaSimple(BaseModel):
    id: int
    titulo: str
    director: str
    año: int
    duracion_minutos: int
    activa: bool
    model_config = {"from_attributes": True}    

class PeliculaResponse(BaseModel):
    id: int
    titulo: str
    director: str
    año: int
    duracion_minutos: int
    activa: bool
    reseñas: list[ReseñaResponse] = []
    actores: list[ActorSimple] = []
    model_config = {"from_attributes": True}
    
ActorResponse.model_rebuild()