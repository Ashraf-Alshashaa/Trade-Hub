from . import *
from schemas.user_address import AddressPrivateDisplay, AddressBase


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str
    address: Optional[AddressPrivateDisplay] = None

    class Config:
        from_attributes = True


class UserAuth(BaseModel):
    id: int
    username: str
    email: str
