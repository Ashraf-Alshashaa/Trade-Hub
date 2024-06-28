from . import *
from passlib.context import CryptContext
from auth.hash import Hash


def insert_user(session, user):
    session.add(DbUser(
        username=user['username'],
        email=user['email'],
        password=Hash.bcrypt(user['password']),
        role=user["role"]
    ))
    session.commit()