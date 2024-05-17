from fastapi import APIRouter, Depends
from schemas.users import UserDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
from schemas.users import UserBase