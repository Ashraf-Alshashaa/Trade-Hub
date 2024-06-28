from . import *
from schemas.category import CategoryBase
def data(): 
    return[
        CategoryBase(name="Electronics"),
        CategoryBase(name="Furniture"),
        CategoryBase(name="Clothing"),
        CategoryBase(name="Auto and Parts"),
    ]