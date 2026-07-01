from fastapi import FastAPI
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "Hola FastAPI"}

class Categoria(str, Enum):
    ropa = "ropa"
    comida = "comida"
    tecnologia = "tecnologia"
    
class Genero(str, Enum):
    ficcion = "ficcion"
    no_ficcion = "no_ficcion"
    poesia = "poesia"
    
class CategoriaProducto(str, Enum):
    electronica = "electronica"
    hogar = "hogar"
    juguetes = "juguetes"
    
class Libro(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    autor: str = Field(min_length=2, max_length=50)
    precio: float = Field(gt=0, le=9999)
    genero: Genero          
    disponible: bool = True
    
    @field_validator("titulo")
    @classmethod
    def titulo_sin_gratis(cls, valor):
        if "gratis" in valor.lower():
            raise ValueError("el título no puede contener la palabra 'gratis'")
        return valor
    
    @model_validator(mode="after")
    def precio_coherente(self):
        if self.disponible and self.precio > 500:
            raise ValueError("libros disponibles no pueden costar más de 500")
        return self
    
class Pelicula(BaseModel):
    titulo: str = Field(min_length=2, max_length=100)
    duracion_minutos: int = Field(gt=0, le=300)
    director: str = Field(min_length=2)
    estreno: int = Field(ge=1888, le=2026)
    
    @field_validator("titulo")
    @classmethod
    def titulo_rechaza_numeros(cls, valor):
        if valor[0].isdigit():
            raise ValueError("el titulo no puede empezar con un numero")
        return valor
    
class PedidoOnline(BaseModel):
    email: str = Field(min_length=5, max_length=50)
    cantidad: int = Field(gt=0, le=100)
    precio_unitario: float = Field(gt=0)
    codigo_descuento: Optional[str] = None
    
    ###### verificacion de email #####
    @field_validator("email")
    @classmethod
    def verificador_correos(cls, valor):
        if "@" not in valor:
            raise ValueError("el email debe tener @")
        posicion = valor.split("@")
        if "." not in posicion[-1]:
            raise ValueError("Despues del @ debe tener un '.'")
        return valor    
        
    @field_validator("codigo_descuento")
    @classmethod
    def verificador_descuentos(cls, valor):
        if valor is None:
            return valor
        if not valor.startswith("DESC-"):
            raise ValueError("Los codigos de descuento empiezan siempre con DESC-")
        return valor
        
    @model_validator(mode="after")
    def precio_coherente(self):
        if self.cantidad > 50 and self.precio_unitario > 10.0:
            raise ValueError("en compras con cantidades mayores a 50 el precio unitario no puede ser mayor a 10.0")
        return self
    
class Departamento(str, Enum):
    rrhh = "rrhh"
    tecnologia = "tecnologia"
    ventas = "ventas"
    finanzas = "finanzas"
    
class Empleado(BaseModel):
    nombre: str = Field(min_length=2, max_length=60)
    edad: int = Field(ge=18, le=65)
    salario: float = Field(gt=0)
    departamento: Departamento
    email_corporativo: str
    salario_bonus: Optional[float] = None 
    
    @field_validator("nombre")
    @classmethod
    def verificacion_de_nombre(cls, valor):
        if any(caracter.isdigit() for caracter in valor):
            raise ValueError("El nombre no puede tener numeros")
        return valor
    
    @field_validator("email_corporativo")
    @classmethod
    def verficacion_de_email(cls, valor):
        if "@" not in valor:
            raise ValueError("el email debe tener @")
        if not valor.endswith("@empresa.com"):
            raise ValueError("el email siempre debe acabar en @empresa.com")
        return valor
    
    @model_validator(mode="after")
    def bonus_coherente(self):
        if self.salario_bonus is None:
            return self
        if not (0 < self.salario_bonus < self.salario):
            raise ValueError("el salario bonus no puede ser 0 o mayor al salario ")
        return self    
    
@app.get("/categorias/{categoria}")
def get_categoria(categoria: Categoria):
    return {"categoria": categoria}

@app.get("/books/{book_id}")
def get_prueba(book_id: int, genre: Genero, available: bool=True, notes: Optional[str] = None):
    return {"book_id": book_id, 
            "genero" : genre, 
            "available" : available, 
            "notes" : notes}
    
@app.get('/productos/{producto_id}')
def get_prueba2(producto_id: int, categoria: CategoriaProducto, 
                en_oferta: Optional[bool]=False, comentario: Optional[str]=None):
    return {"producto_id": producto_id,
            "categoria": categoria,
            "en_oferta": en_oferta,
            "comentario": comentario}

@app.post("/libros")
def crear_libro(libro: Libro):
    return libro

@app.post("/pelicula")
def crear_pelicula(pelicula: Pelicula):
    return pelicula

@app.post("/empleado")
def crear_empleado(empleado: Empleado):
    return empleado