from db.models import Base
from db.database import get_db
from db import db_category
from db.models import DbCategory
from seed_db.operations.users import insert_user
from seed_db.operations.addresses import insert_address
from seed_db.operations.products import insert_pruduct
from seed_db.operations.bids import insert_bid
from seed_db.operations.payments import insert_payments
from main import engine
from contextlib import contextmanager
from seed_db.fake_data import addresses_data, bids_data, products_data, users_data, categories_data, payments_data

@contextmanager
def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def seed_db():
    with get_db_session() as session:
        print("---------------------")
        for user in users_data.data():
            insert_user(session, user)
        session.commit()
        print(f"{len(users_data.data())} users has been inserted successfully!")
        

        for address in addresses_data.data():
            insert_address(session, address)
        session.commit()
        print(f"{len(addresses_data.data())} addressess has been inserted successfully!")
        

        for category in categories_data.data():
            db_category.add_category(session, category)
        print(f"{len(categories_data.data())} categories has been inserted successfully!")


        for product in products_data.data():
            insert_pruduct(session, product)
        session.commit()
        print(f"{len(products_data.data())} products has been inserted successfully!")
        

        for bid in bids_data.data():
            insert_bid(session, bid)
        session.commit()
        print(f"{len(bids_data.data())} bids has been inserted successfully!" )

        for payment in payments_data.data():
            insert_payments(session, payment)
        session.commit()
        print(f"{len(payments_data.data())} payments has been inserted successfully!" + "\n" + "---------------------")
        


seed_db()
print("Database seeded successfully!")