from . import *
from schemas.user_address import AddressPrivateDisplay, AddressPublicDisplay


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    address: Optional[AddressPrivateDisplay] = None

    class Config:
        orm_mode = True


class UserPublicDisplay(BaseModel):
    id: int
    username: str
    email: str
    address: Optional[AddressPublicDisplay] = None


class UserUpdateDisplay(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True



class UserAuth(BaseModel):
    id: int
    username: str
    email: str
