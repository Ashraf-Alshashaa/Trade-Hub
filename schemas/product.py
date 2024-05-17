from . import *


class ConditionEnum(str, Enum):
    new = "new"
    used = "used"
    refurbished = "good as new"


class StateEnum(str, Enum):
    available = "available"
    sold = "sold"
    pending = "pending"


class Product(BaseModel):
    name: str
    image: str
    description: str
    seller_id: int
    price: float
    date: datetime
    condition: ConditionEnum
    state: StateEnum

