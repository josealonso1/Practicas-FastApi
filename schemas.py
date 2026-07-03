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

    model_config = {"from_attributes": True}