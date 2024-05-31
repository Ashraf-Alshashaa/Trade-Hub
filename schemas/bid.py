from . import *


class BidStatus(str, Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'


class BidBase(BaseModel):
    product_id: int
    date: datetime
    price: float
    bidder_id: int
    status: BidStatus


class BidDisplay(BaseModel):
    product_id: int
    date: datetime
    price: float
    bidder_id: int
    status: BidStatus

    class Config:
        from_attributes = True