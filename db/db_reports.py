from . import *
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from db.models import DbBid, DbProduct, DbPayment
from schemas.bid import BidStatus
from schemas.payments import PaymentStatus


def get_period_dates(period: str):
    today = datetime.now().date()
    if period == 'lastMonth':
        period_start = today - timedelta(days=30)
        period_end = today
    elif period == 'lastYear':
        period_start = today - timedelta(days=365)
        period_end = today
    else:
        raise HTTPException(status_code=400, detail="Invalid period provided. Supported values are: lastMonth, lastYear")
    
    return period_start, period_end + timedelta(days=1)


def generate_all_periods(period: str, period_start: datetime, period_end: datetime) -> List[str]:
    periods = []
    current = period_start
    while current < period_end:
        if period == 'lastYear':
            periods.append(current.strftime('%Y-%m'))
            current += timedelta(days=30)
        elif period == 'lastMonth':
            periods.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)
    
    return periods


def get_sales_report(period: str, db: Session):
    period_start, period_end = get_period_dates(period)
    
    all_periods = generate_all_periods(period, period_start, period_end)
    
    total_sales = db.query(func.sum(DbPayment.amount)).filter(
        and_(DbPayment.date >= period_start, DbPayment.date < period_end, DbPayment.status == PaymentStatus.completed)
    ).scalar() or 0.0
    
    sales_data_query = []
    if period == 'lastYear':
        sales_data_query = db.query(func.strftime('%Y-%m', DbPayment.date).label('month'), func.sum(DbPayment.amount)).filter(
            and_(DbPayment.date >= period_start, DbPayment.date < period_end, DbPayment.status == PaymentStatus.completed)
        ).group_by('month').all()
    else:
        sales_data_query = db.query(func.strftime('%Y-%m-%d', DbPayment.date).label('day'), func.sum(DbPayment.amount)).filter(
            and_(DbPayment.date >= period_start, DbPayment.date < period_end, DbPayment.status == PaymentStatus.completed)
        ).group_by('day').all()

    sales_data = {entry[0]: entry[1] for entry in sales_data_query}
    
    for period_label in all_periods:
        if period_label not in sales_data:
            sales_data[period_label] = 0
    
    published_products = db.query(DbProduct).filter(DbProduct.date >= period_start, DbProduct.date < period_end).count()
    sold_products = db.query(DbProduct).filter(DbProduct.buyer_id.isnot(None), DbProduct.date >= period_start, DbProduct.date < period_end).count()

    all_published_products = db.query(DbProduct).count()
    all_sold_products = db.query(DbProduct).filter(DbProduct.payment_id.isnot(None)).count()

    return {
        "period": period,
        "total_sales": total_sales,
        "sales_data": [{"label": label, "amount": sales_data[label]} for label in sorted(sales_data.keys())],
        "published_products": published_products,
        "sold_products": sold_products,
        "all_published_products": all_published_products,
        "all_sold_products": all_sold_products
    }


def get_bids_report(period: str, db: Session):
    period_start, period_end = get_period_dates(period)

    all_periods = generate_all_periods(period, period_start, period_end)
    bids_count_query = []
    if period == 'lastYear':
        bids_count_query = db.query(func.strftime('%Y-%m', DbBid.date).label('month'), func.count(DbBid.id)).filter(
            DbBid.date >= period_start, DbBid.date < period_end).group_by('month').all()
    elif period == 'lastMonth':
        bids_count_query = db.query(func.strftime('%Y-%m-%d', DbBid.date).label('day'), func.count(DbBid.id)).filter(
            DbBid.date >= period_start, DbBid.date < period_end).group_by('day').all()

    bids_count = {entry[0]: entry[1] for entry in bids_count_query}

    for period_label in all_periods:
      if period_label not in bids_count:
            bids_count[period_label] = 0

    published_bids = db.query(DbBid).filter(DbBid.date >= period_start, DbBid.date < period_end).count()
    accepted_bids = db.query(DbPayment).filter(DbPayment.status == PaymentStatus.completed, DbPayment.date >= period_start, DbPayment.date <= period_end).count() 
    + db.query(DbBid).filter(DbBid.status == BidStatus.ACCEPTED, DbBid.date >= period_start, DbBid.date < period_end).count()

    all_published_bids = db.query(DbBid).count()
    all_accepted_bids = db.query(DbPayment).filter(DbPayment.status == PaymentStatus.completed).count() + db.query(DbBid).filter(DbBid.status == BidStatus.ACCEPTED).count()

    return {
        "period": period,
        "bids_count": [{"label": label, "count": bids_count[label]} for label in sorted(bids_count.keys())],
        "published_bids": published_bids,
        "accepted_bids": accepted_bids,
        "all_published_bids": all_published_bids,
        "all_accepted_bids": all_accepted_bids
    }