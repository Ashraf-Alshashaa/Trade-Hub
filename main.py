from fastapi import FastAPI
from db.database import engine
from db import models
from router import products

app = FastAPI()
app.include_router(products.router)

@app.get('/')
def index():
  return {'message': 'Welkome to Trade Hub app'}

models.Base.metadata.create_all(engine)