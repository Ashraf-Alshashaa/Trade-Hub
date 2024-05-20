from . import *

def get_product(db: Session, id: int):
    return db.query(DbProduct).filter(DbProduct.id == id).first()