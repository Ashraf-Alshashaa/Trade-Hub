from . import *

class BidBase(BaseModel):
    product_id: int
    price: float
    bidder_id: int

class BidDisplay(BaseModel):
    product_id: int
    price: float
    bidder_id: int

    class Config:
        orm_mode = True