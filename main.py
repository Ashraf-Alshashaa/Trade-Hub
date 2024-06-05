from fastapi import FastAPI
from db.database import engine
from db import models
from routers import user_router, product_router, bid_router, user_address_router, payments_router, websocket_router
from auth import authentication


app = FastAPI()


app.include_router(bid_router.router)
app.include_router(product_router.router)
app.include_router(authentication.router)
app.include_router(user_router.router)
app.include_router(user_address_router.router)
app.include_router(payments_router.router)
app.include_router(websocket_router.router)


@app.get('/')
def index():
  return {'message': 'Welcome to Trade Hub app'}


models.Base.metadata.create_all(engine)