from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from typing import Optional
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from jose import jwt, JWTError
from db.database import get_db
from db import models
from auth.hash import Hash
from auth import oauth2
from db.database import get_db
from db import db_user
from passlib.context import CryptContext