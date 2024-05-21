from fastapi import FastAPI
from db.database import engine
from db import models
from routers.product import router as product_router
from routers import user_router
from routers import product_routers
from auth import authentication

app = FastAPI()
app.include_router(product_router)
app.include_router(product_routers.router)
app.include_router(authentication.router)
app.include_router(user_router.router)

@app.get('/')
def index():
  return {'message': 'Welcome to Trade Hub app'}

models.Base.metadata.create_all(engine)