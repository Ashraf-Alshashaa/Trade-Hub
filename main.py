from fastapi import FastAPI
from db.database import engine
from db import models
from routers import product_post

app = FastAPI()
app.include_router(product_post.router)
@app.get('/')
def index():
  return {'message': 'Welkome to Trade Hub app'}

models.Base.metadata.create_all(engine)