from fastapi import FastAPI
from database import engine
import models
from routers import peliculas, reseñas, actores, usuario


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(peliculas.router)
app.include_router(reseñas.router)
app.include_router(actores.router)
app.include_router(usuario.router)