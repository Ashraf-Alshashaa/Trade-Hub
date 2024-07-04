from . import *
from schemas.payments import PaymentStatus

def data(): 
    return [
    {
        "id": "pay99999",
        "user_id": 1,
        "amount": 249.99,
        "status": PaymentStatus.completed,
        "description": "Payment for Leather Jacket",
        "date": datetime(2024, 6, 5, 14, 27, 12, 345678)
    },
    {
        "id": "pay123",
        "user_id": 5,
        "amount": 1300,
        "status": PaymentStatus.completed,
        "description": "Payment for Tesla Model 3",
        "date": datetime(2024, 7, 2, 14, 25, 48, 789012)
    },
    {
        "id": "pay12345678879",
        "user_id": 1,
        "amount": 200.0,
        "status": PaymentStatus.completed,
        "description": "Payment for Luxury Leather Sofa",
        "date": datetime(2024, 3, 11, 14, 22, 35, 123456)
    },
    {
        "id": "pay45678",
        "user_id": 2,
        "amount": 120.0,
        "status": PaymentStatus.completed,
        "description": "Payment for Winter Jacket",
        "date": datetime(2024, 1, 14, 14, 22, 35, 123456)
    },
    {
        "id": "pay123455",
        "user_id": 1,
        "amount": 1500.0,
        "status": PaymentStatus.completed,
        "description": "Payment for Yamaha R1",
        "date": datetime(2024, 6, 17, 14, 22, 35, 123456)
    },
]
