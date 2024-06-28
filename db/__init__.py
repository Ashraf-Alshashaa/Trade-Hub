from sqlalchemy.orm.session import Session
from db.database import get_db
from fastapi import HTTPException, status
from sqlalchemy.sql.sqltypes import Integer, String, Float, Enum, List
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.exc import IntegrityError