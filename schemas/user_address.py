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
    id: int
    street_name: str
    city: str
    country: str
    postcode: str
    house_number: int
    default: bool

    class Config:
        from_attributes = True


class AddressPublicDisplay(BaseModel):
    id: int
    city: str

    class Config:
        from_attributes = True

