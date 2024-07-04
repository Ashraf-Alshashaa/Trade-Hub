from . import *


def data(): 
    return [
        {'date': datetime(2023, 8, 14, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 10, 'price': 301.00, 'bidder_id': 2},
        {'date': datetime(2023, 9, 15, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 10, 'price': 310.89, 'bidder_id': 3},
        {'date': datetime(2023, 9, 16, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 10, 'price': 314.00, 'bidder_id': 1},
        {'date': datetime(2023, 10, 17, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 7, 'price': 331.00, 'bidder_id': 4},
        {'date': datetime(2024, 1, 18, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 7, 'price': 332.89, 'bidder_id': 3},
        {'date': datetime(2024, 1, 19, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 1, 'price': 122.56, 'bidder_id': 7},
        {'date': datetime(2024, 1, 20, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.ACCEPTED, 'product_id': 13, 'price': 1300.0, 'bidder_id': 5},
        {'date': datetime(2024, 2, 21, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 1, 'price': 166.45, 'bidder_id': 8},
        {'date': datetime(2024, 3, 22, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 1, 'price': 180.78, 'bidder_id': 4},
        {'date': datetime(2024, 4, 23, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 1, 'price': 147.23, 'bidder_id': 10},
        {'date': datetime(2024, 4, 23, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 11, 'price': 899.99, 'bidder_id': 5},
        # New bids, especially from user1 and user2
        {'date': datetime(2024, 5, 5, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 12, 'price': 900.00, 'bidder_id': 1},
        {'date': datetime(2024, 5, 6, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 14, 'price': 550.00, 'bidder_id': 2},
        {'date': datetime(2024, 6, 7, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 15, 'price': 400.00, 'bidder_id': 1},
        {'date': datetime(2024, 6, 9, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 17, 'price': 600.00, 'bidder_id': 1},
        {'date': datetime(2024, 6, 10, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 18, 'price': 700.00, 'bidder_id': 2},
        {'date': datetime(2024, 6, 10, 12, 34, 56, 789012), 'status': schemas.bid.BidStatus.ACCEPTED, 'product_id': 19, 'price': 20000.00, 'bidder_id': 1},
        {'date': datetime(2024, 6, 24, 14, 45, 56, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 11,'price': 905, 'bidder_id': 7},
        {'date': datetime(2024, 6, 25, 17, 21, 33, 789012), 'status': schemas.bid.BidStatus.PENDING, 'product_id': 11, 'price': 910, 'bidder_id': 3},
    ]