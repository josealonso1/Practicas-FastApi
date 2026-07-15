from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from routers import peliculas, libros


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(libros.router)
app.include_router(peliculas.router)