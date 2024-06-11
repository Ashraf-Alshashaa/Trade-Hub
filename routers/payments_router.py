from . import *
from schemas.payments import PaymentResponse, PaymentRequest, PaymentStatus, PaymentStatusUpdate
from db.db_product import get_cart
import os
import stripe
from dotenv import load_dotenv
from fastapi import status
from db.db_bid import change_bid_status_to_pending
from db.models import DbPayment, DbProduct, DbUser
from notifications.notification import NotificationCenter, NotificationType
from db.db_payment import update_payment

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


@router.put("/{id}", response_model=PaymentResponse, summary="Update Payment Status")
def update_payment_status(id: str,
                                request: PaymentStatusUpdate,
                                db: Session = Depends(get_db),
                                current_user: UserBase = Depends(get_current_user)):
    """
           CHange the payment status.

           - **id**: ID of the payment .
           - **db**: Database session.
           """

    updated_payment = update_payment(db, id, request)

    if updated_payment.status == PaymentStatus.completed:
        selected_item_ids = [item.id for item in updated_payment.items]
        change_bid_status_to_pending(db, current_user.id, selected_item_ids)
    #     recipients = {db.query(DbUser).filter(DbUser.id == item.seller_id).first().email
    #                   for item in updated_payment.items}
    #     try:
    #         await notify.notify_user(NotificationType.EMAIL,
    #                        recipient=current_user.email, subject="Payment " + updated_payment.status,
    #                        body=f"The payment has been successful! ")
    #         paid_products = {}
    #         for seller in recipients:
    #         # Perform a single query to get all paid products for the current seller
    #             products = db.query(DbProduct).join(DbUser, DbUser.id == DbProduct.seller_id).filter(
    #                 DbProduct.id.in_(selected_item_ids), DbUser.email == seller
    #                 ).all()
    #             paid_products[seller] = [product.name for product in products]
    #
    #             seller_product = ','.join(paid_products[seller])
    #             await notify.notify_user(NotificationType.EMAIL,
    #                            recipient=seller, subject="Your products are sold!",
    #                            body=f" You sold {seller_product} ! ")
    #     finally:
    #         pass
    # elif updated_payment.status == PaymentStatus.failed:
    #     await notify.notify_user(NotificationType.EMAIL,
    #                        recipient=current_user.email, subject="Payment " + updated_payment.status,
    #                        body=f"The payment has been failed! :( ")

    db.commit()

    return PaymentResponse(
        payment_id=updated_payment.id,
        status=updated_payment.status,
        amount=updated_payment.amount,
        description=updated_payment.description,
        items=updated_payment.items
    )
