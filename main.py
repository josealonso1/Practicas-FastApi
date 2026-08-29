from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from routers import peliculas, reseñas, actores, usuario


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(peliculas.router)
app.include_router(reseñas.router)
app.include_router(actores.router)
app.include_router(usuario.router)