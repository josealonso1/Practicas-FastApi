from fastapi import FastAPI
from enum import Enum
from typing import Optional

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