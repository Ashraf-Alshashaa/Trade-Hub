from . import *


def insert_payments(session, payment):
    session.add(DbPayment(
                id=payment['id'],
                user_id=payment['user_id'],
                amount=payment["amount"],
                status=payment['status'],
                description= payment["description"],
                date=payment['date'],
            ))
    session.commit()