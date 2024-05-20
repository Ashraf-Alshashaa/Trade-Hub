from sqlalchemy.orm import Session
from fastapi import status
from schemas.product import ProductBase, StateEnum, ConditionEnum
from db.models import DbProduct