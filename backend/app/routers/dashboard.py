from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.kpi_calculator import calculate_kpis

router = APIRouter(prefix="/api/dashboard", tags=["Master Dashboard"])

@router.get("")
def get_dashboard_summary(db: Session = Depends(get_db)):
    return calculate_kpis(db)
