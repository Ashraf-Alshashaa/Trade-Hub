from fastapi import FastAPI
from db.database import engine
from db import models
from routers import users
from auth import authentication
from routers import product_routers

app = FastAPI()

app.include_router(product_routers.router)
app.include_router(authentication.router)
app.include_router(users.router)

@app.get('/')
def index():
  return {'message': 'Welcome to Trade Hub app'}

models.Base.metadata.create_all(engine)