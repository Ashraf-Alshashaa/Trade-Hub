from fastapi import FastAPI
from db.database import engine
from db import models
from routers import users_router
from auth import authentication

app = FastAPI()

app.include_router(authentication.router)
app.include_router(users_router.router)
@app.get('/')
def index():
  return {'message': 'Welcome to Trade Hub app'}

models.Base.metadata.create_all(engine)