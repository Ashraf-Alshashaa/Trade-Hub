from fastapi import APIRouter, Depends
from db import db_product
from schemas import product
from schemas.product import ProductDisplay, ProductBase
from sqlalchemy.orm.session import Session
from db.database import get_db