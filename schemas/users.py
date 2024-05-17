from . import *
class UserBase(BaseModel):
    username: str
    email: str
    password: str
class UserDisplay(BaseModel):
    username: str
    email: str