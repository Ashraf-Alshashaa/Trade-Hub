from . import *


def data(): 
    return [
        {'date': datetime(2024, 5, 14, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.ACCEPTED, 'product_id': 3, 'price': 350.00, 'bidder_id': 2},
        {'date': datetime(2024, 5, 15, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 7, 'price': 154.89, 'bidder_id': 2},
        {'date': datetime(2024, 5, 16, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.ACCEPTED, 'product_id': 1, 'price': 799.00, 'bidder_id': 1},
        {'date': datetime(2024, 5, 17, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.ACCEPTED, 'product_id': 5, 'price': 399.00, 'bidder_id': 4},
        {'date': datetime(2024, 5, 18, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 7, 'price': 145.89, 'bidder_id': 3},
        {'date': datetime(2024, 5, 19, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 2, 'price': 122.56, 'bidder_id': 7},
        {'date': datetime(2024, 5, 20, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 9, 'price': 175.34, 'bidder_id': 1},
        {'date': datetime(2024, 5, 21, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 4, 'price': 166.45, 'bidder_id': 8},
        {'date': datetime(2024, 5, 22, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 6, 'price': 180.78, 'bidder_id': 5},
        {'date': datetime(2024, 5, 23, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 10, 'price': 147.23, 'bidder_id': 10}
    ]