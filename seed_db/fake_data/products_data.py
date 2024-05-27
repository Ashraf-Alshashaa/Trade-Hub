from . import *


def data(): 
    return [
    {
        'name': 'Apple iPhone 13',
        'image': 'iphone13.png',
        'description': 'Latest model with A15 Bionic chip',
        'seller_id': 2,
        'buyer_id': 1,
        'price': 799.0,
        'date': datetime(2024, 5, 4, 12, 34, 56, 789012),
        'condition': schemas.product.ConditionEnum.NEW,
        'state': schemas.product.StateEnum.SOLD
    },
    {
        'name': 'Samsung Galaxy S21',
        'image': 'galaxy_s21.png',
        'description': 'High resolution camera with 8K video',
        'seller_id': 1,
        'buyer_id': None,
        'price': 699.0,
        'date': datetime(2024, 5, 5, 12, 34, 56, 789012),
        'condition': schemas.product.ConditionEnum.USED,
        'state': schemas.product.StateEnum.AVAILABLE
    },
    {
        'name': 'Sony WH-1000XM4 Headphones',
        'image': 'sony_wh1000xm4.png',
        'description': 'Industry-leading noise cancellation',
        'seller_id': 4,
        'buyer_id': 2,
        'price': 350.0,
        'date': datetime(2024, 5, 6, 12, 34, 56, 789012),
        'condition': schemas.product.ConditionEnum.NEW,
        'state': schemas.product.StateEnum.SOLD
    },
    {
        'name': 'Dell XPS 13 Laptop',
        'image': 'dell_xps13.png',
        'description': '13.4-inch display with Intel i7 processor',
        'seller_id': 3,
        'buyer_id': None,
        'price': 1200.0,
        'date': datetime(2024, 5, 7, 12, 34, 56, 789012),
        'condition': schemas.product.ConditionEnum.USED,
        'state': schemas.product.StateEnum.AVAILABLE
    },
    {
        'name': 'Apple Watch Series 7',
        'image': 'apple_watch_series7.png',
        'description': 'Advanced health monitoring features',
        'seller_id': 6,
        'buyer_id': None,
        'price': 399.0,
        'date': datetime(2024, 5, 8, 12, 34, 56, 789012),
        'condition': schemas.product.ConditionEnum.NEW,
        'state': schemas.product.StateEnum.PENDING
    },
    {
        'name': 'Canon EOS R5 Camera',
        'image': 'canon_eos_r5.png',
        'description': 'Full-frame mirrorless camera with 45MP sensor',
        'seller_id': 7,
        'buyer_id': None,
        'price': 3899.0,
        'date': datetime(2024, 5, 9, 12, 34, 56, 789012),
        'condition': schemas.product.ConditionEnum.USED,
        'state': schemas.product.StateEnum.AVAILABLE
    },
    {
        'name': 'PlayStation 5',
        'image': 'ps5.png',
        'description': 'Next-gen gaming console with ultra-high-speed SSD',
        'seller_id': 5,
        'buyer_id': None,
        'price': 499.0,
        'date': datetime(2024, 5, 10, 12, 34, 56, 789012),
        'condition': schemas.product.ConditionEnum.NEW,
        'state': schemas.product.StateEnum.AVAILABLE
    },
    {
        'name': 'Nikon Z6 II',
        'image': 'nikon_z6_ii.png',
        'description': 'Mirrorless camera with 24.5MP sensor and 4K video',
        'seller_id': 8,
        'buyer_id': None,
        'price': 1999.0,
        'date': datetime(2024, 5, 11, 12, 34, 56, 789012),
        'condition': schemas.product.ConditionEnum.USED,
        'state': schemas.product.StateEnum.AVAILABLE
    },
    {
        'name': 'Microsoft Surface Pro 7',
        'image': 'surface_pro7.png',
        'description': '2-in-1 laptop with Intel i5 processor',
        'seller_id': 9,
        'buyer_id': None,
        'price': 899.0,
        'date': datetime(2024, 5, 12, 12, 34, 56, 789012),
        'condition': schemas.product.ConditionEnum.NEW,
        'state': schemas.product.StateEnum.AVAILABLE
    },
    {
        'name': 'Bose QuietComfort 35 II',
        'image': 'bose_qc35ii.png',
        'description': 'Wireless noise-cancelling headphones',
        'seller_id': 10,
        'buyer_id': None,
        'price': 299.0,
        'date': datetime(2024, 5, 13, 12, 34, 56, 789012),
        'condition': schemas.product.ConditionEnum.USED,
        'state': schemas.product.StateEnum.AVAILABLE
    }
]