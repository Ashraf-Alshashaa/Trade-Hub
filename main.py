from fastapi import FastAPI
from db.database import engine
from db import models
from routers import product_routers

app = FastAPI()
app.include_router(product_routers.router)
@app.get('/')
def index():
  return {'message': 'Welkome to Trade Hub app'}

models.Base.metadata.create_all(engine)