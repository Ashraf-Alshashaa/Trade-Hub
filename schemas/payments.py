from . import *
from schemas.product import ProductDisplay


class PaymentStatus(str, Enum):
    pending = "requires_payment_method"
    completed = "succeeded"
    failed = "failed"


class PaymentRequest(BaseModel):
    product_ids: Optional[List[int]] = None  # List of item IDs to pay for, or None to pay for the whole cart
    currency: str
    user_id: int  # User ID to identify the cart


class PaymentResponse(BaseModel):
    payment_id: str
    status: PaymentStatus
    amount: float
    description: str
    items: List[ProductDisplay]  # List of items being paid for