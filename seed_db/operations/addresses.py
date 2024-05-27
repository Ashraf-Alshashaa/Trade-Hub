from . import *


def insert_address(session, address):
    session.add(DbAddress(
                street_name=address['street_name'],
                city=address['city'],
                country=address['country'],
                postcode=address['postcode'],
                house_number=address['house_number'],
                user_id=address['user_id'],
                default=address['default']
            ))
    session.commit()