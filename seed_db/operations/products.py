from . import *


def insert_pruduct(session, product):
    session.add(DbProduct(
                name=product['name'],
                image=product['image'],
                description=product['description'],
                seller_id=product['seller_id'],
                buyer_id=product['buyer_id'],
                price=product['price'],
                date=product['date'],
                condition=product['condition'],
                category_id=product['category_id'],
                payment_id=product["payment_id"]
            ))
    session.commit()