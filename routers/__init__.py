from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm.session import Session
from db.database import get_db
from auth.oauth2 import get_current_user
from schemas.users import UserBase