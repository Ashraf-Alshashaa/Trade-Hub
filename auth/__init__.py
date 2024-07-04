from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from db.database import get_db
from db import models
from auth import oauth2