from . import *


class AddressBase(BaseModel):
    street: str
    house_number: int
    city: str
    country: str
    postcode: str
    user_id : int


class AddressPrivateDisplay(BaseModel):
    street: str
    house_number: int
    city: str
    country: str
    postcode: str

    class Config:
        orm_mode = True


class AddressPublicDisplay(BaseModel):
    postcode: str
    city: str

    class Config:
        orm_mode = True

