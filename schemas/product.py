from . import *


class ConditionEnum(str, Enum):
    NEW = "new"
    USED = "used"
    REFURBISHED = "good as new"


class ProductBase(BaseModel):
    name: str
    image: str
    description: str
    seller_id: int
    buyer_id: Optional[int]
    price: float
    date: datetime
    condition: ConditionEnum
    category_id: int



class ProductDisplay(BaseModel):
    id: int
    name: str
    image: str
    description: str
    price: float
    date: datetime
    condition: ConditionEnum
    category_id: int
    seller_id: int
    seller_city: Optional[str] = None
    sold: Optional[bool] = False

    class Config:
        from_attributes = True

