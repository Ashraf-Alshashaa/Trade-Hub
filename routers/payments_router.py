from . import *
from schemas.payments import PaymentResponse, PaymentRequest, PaymentStatus
from db.db_product import get_cart
import os
import stripe
from dotenv import load_dotenv
import random
from fastapi import status
from db.db_bid import change_bid_status_to_pending
from db.models import DbPayment, DbProduct
from notifications.notification import NotificationCenter, NotificationType

notify = NotificationCenter()

# Load environment variables from .env file
load_dotenv()
# Set your test secret key obtained from the Stripe dashboard
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix='/payments', tags=['payments'])


@router.post("", response_model=PaymentResponse)
def initiate_payment(payment_request: PaymentRequest,
                     db: Session = Depends(get_db),
                     current_user: UserBase = Depends(get_current_user)):
    """
        Start the payment session.

        - **payment_request**: input selected product ids, user_id.
        - **db**: Database session.
        - **current_user**: Currently authenticated user.
        """
    # Set the seller
    # Retrieve items in the user's cart
    cart_items = get_cart(db, payment_request.user_id)

    if not cart_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is empty")

    if payment_request.user_id != current_user.id:  # and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You're not authorized")

    try:
        if payment_request.product_ids:
            items_to_pay_for = [item for item in cart_items if item.id in payment_request.product_ids]
        else:
            items_to_pay_for = cart_items

        if not items_to_pay_for:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No items to pay for")

        total_amount = sum(item.price for item in items_to_pay_for)

        # Create a payment intent with the calculated total amount
        intent = stripe.PaymentIntent.create(
            amount=int(total_amount * 100),  # Amount in cents
            currency='eur',  # Hardcoded for simplicity, can be passed in request
            payment_method_types=["card"]
        )

        # Create a payment record in the database
        payment = DbPayment(
            id=intent.id,
            user_id=current_user.id,
            amount=total_amount,
            status=PaymentStatus.pending,
            description="Payment for selected items"
        )
        db.add(payment)
        db.commit()

        db.refresh(payment)

    # Update the payment_id field in the products
        for item in items_to_pay_for:
            item.payment_id = payment.id

        db.commit()

        return PaymentResponse(
            payment_id=intent.id,
            status=PaymentStatus.pending,
            amount=total_amount,
            description="Payment for selected items",
            items=items_to_pay_for
        )

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{payment_id}", response_model=PaymentResponse, summary="Update Payment Status")
def update_payment_status(payment_id: str,
                          payment_status: PaymentStatus,
                          db: Session = Depends(get_db),
                          current_user: UserBase = Depends(get_current_user)):
    payment = db.query(DbPayment).filter(DbPayment.id == payment_id, DbPayment.user_id == current_user.id).first()

    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    if payment_status == PaymentStatus.completed:
        payment.status = PaymentStatus.completed
        selected_item_ids = [item.id for item in payment.items]
        change_bid_status_to_pending(db, current_user.id, selected_item_ids)

        notify.notify_user(NotificationType.EMAIL,
                           recipient=current_user.email, subject="Payment " + payment_status,
                           body=f"The payment has been successful! ")

    elif payment_status == PaymentStatus.failed:
        payment.status = PaymentStatus.failed
        notify.notify_user(NotificationType.EMAIL,
                           recipient=current_user.email, subject="Payment " + payment_status,
                           body=f"The payment has been failed! :( ")

    db.commit()

    return PaymentResponse(
        payment_id=payment.id,
        status=payment.status,
        amount=payment.amount,
        description=payment.description,
        items=payment.items # This could be optimized to not query again
    )
