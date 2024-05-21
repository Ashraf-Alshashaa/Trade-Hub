from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Float, DATETIME, Enum
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from schemas.product import ProductBase, StateEnum, ConditionEnum
from db.models import DbProduct
