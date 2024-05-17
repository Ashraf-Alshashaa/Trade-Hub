from . import *


class ConditionEnum(str, Enum):
    new = "new"
    used = "used"
    refurbished = "good as new"


class StateEnum(str, Enum):
    available = "available"
    sold = "sold"
    pending = "pending"


class ProductBase(BaseModel):
    name: str
    image: str
    description: str
    seller_id: int
    price: float
    # datetime requires a certain configuration which stops testing the other properties, therefore for now I changed it to str
    date: str
    condition: ConditionEnum
    state: StateEnum

#Need to add this to the model since Pydentice cannot handle working with complex types such as Datetime
    # class Config:
    #     arbitrary_types_allowed = True

class ProductDisplay(BaseModel):
    name: str
    description: str
    price: float
    # datetime requires a certain configuration which stops testing the other properties, therefore for now I changed it to str
    date: str
    condition: ConditionEnum
    state: StateEnum
    class Config():
        orm_mode = True
        # arbitrary_types_allowed = True