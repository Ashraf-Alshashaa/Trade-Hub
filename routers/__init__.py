from fastapi import APIRouter, Depends, Query
from db import db_product
from sqlalchemy.orm.session import Session
from db.database import get_db