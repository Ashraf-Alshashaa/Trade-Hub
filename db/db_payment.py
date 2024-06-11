from . import *
from schemas.payments import PaymentStatusUpdate
from db.models import DbPayment


def update_payment(db: Session, id: int, request: PaymentStatusUpdate):
    payment = db.query(DbPayment).filter(DbPayment.id == id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Payment with id {id} not found')
    try:
        payment.status = request.status
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

    return payment