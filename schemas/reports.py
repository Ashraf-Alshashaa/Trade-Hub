
from . import *
from typing import Dict, Union

class SalesPerformanceReportDisplay(BaseModel):
    period: str
    total_sales: float
    sales_data: List[Dict[str, Union[str, float]]]
    published_products: int
    sold_products: int
    all_published_products: int
    all_sold_products: int


class BidsPerformanceReportDisplay(BaseModel):
    period: str
    bids_count: List[Dict[str, Union[str, int]]]
    published_bids: int
    accepted_bids: int
    all_published_bids: int
    all_accepted_bids: int