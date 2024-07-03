from db import db_reports 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user
from db.database import get_db
from schemas.users import UserBase, UserRole
from schemas.reports import SalesPerformanceReportDisplay, BidsPerformanceReportDisplay


router = APIRouter(
    prefix='/reports',
    tags=['reports']
)


@router.get("/sales", response_model=SalesPerformanceReportDisplay)
def get_sales_performance_report(period: str, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You're not authorized")
    return db_reports.get_sales_report(period, db)

@router.get("/bids", response_model=BidsPerformanceReportDisplay)
def get_bids_performance_report(period: str, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You're not authorized")
    
    return db_reports.get_bids_report(period , db)
