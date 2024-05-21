from fastapi import FastAPI
from db.database import engine
from db import models
from routers.product import router as product_router
from routers.users import router as product_users
from auth import authentication
from routers import product_routers

app = FastAPI()
app.include_router(product_router)
app.include_router(product_routers.router)
app.include_router(authentication.router)
app.include_router(product_users)

@app.get('/')
def index():
  return {'message': 'Welcome to Trade Hub app'}

models.Base.metadata.create_all(engine)