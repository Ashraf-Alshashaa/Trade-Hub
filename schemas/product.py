from . import *


EXPECTED_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class ConditionEnum(str, Enum):
    NEW = "new"
    USED = "used"
    REFURBISHED = "good as new"


class StateEnum(str, Enum):
    AVAILABLE = "available"
    SOLD = "sold"
    PENDING = "pending"


class ProductBase(BaseModel):
    name: str
    image: str
    description: str
    seller_id: int
    buyer_id: Optional[int]
    price: float
    date: datetime
    condition: ConditionEnum
    state: StateEnum


class ProductDisplay(BaseModel):
    name: str
    image: str
    description: str
    price: float
    date: datetime
    condition: ConditionEnum
    state: StateEnum

    class Config:
        orm_mode = True