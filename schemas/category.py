from . import *

class CategoryBase(BaseModel):
    name: str


class CategoryDisplay(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True