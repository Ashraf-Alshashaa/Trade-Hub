from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm.session import Session
from db.database import get_db