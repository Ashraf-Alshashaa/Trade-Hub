from . import *


class AddressBase(BaseModel):
    street_name: str
    city: str
    country: str
    postcode: str
    house_number: int
    user_id: int
    default: bool


class AddressPrivateDisplay(BaseModel):
    street_name: str
    city: str
    country: str
    postcode: str
    house_number: int

    class Config:
        orm_mode = True


class AddressPublicDisplay(BaseModel):
    postcode: str
    city: str

    class Config:
        orm_mode = True

