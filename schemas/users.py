from . import *
class UserBase(BaseModel):
    username: str
    email: str
    password: str
    address_id: Optional[int] = None

class UserDisplay(BaseModel):
    username: str
    email: str
    class Config():
        orm_mode = True

class UserAuth(BaseModel):
    id: int
    username: str
    email: str