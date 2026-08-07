
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.rbac import get_current_user
from app.core.config import get_mode
from app.services.kpi_calculator import calculate_kpis, save_current_month_snapshot
from datetime import datetime

router = APIRouter(prefix="/api/dashboard", tags=["Master Dashboard"])

@router.get("")
def get_dashboard_summary(
    year: int = Query(None, description="Year for filtering (None=all years)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Dashboard accessible to all logged-in users.
    Automatically filters by current app mode (DEMO or PRODUCTION).
    Query Parameters:
    - year: Filter by year (2024, 2025, 2026) or None for all years combined
    """
    current_mode = get_mode()
    return calculate_kpis(db, year, current_mode)


@router.post("/snapshot/save-current-month")
def save_month_snapshot(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Manually save current month's KPI snapshot to database.
    Typically called at end of month.
    Only Administrator can call this.
    """
    if current_user.role != "Administrator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Administrator can save KPI snapshots"
        )
    
    result = save_current_month_snapshot(db)
    return result


@router.get("/available-years")
def get_available_years(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of available years from CI projects filtered by current mode.
    Returns sorted list of unique years from CI projects for current mode.
    """
    from sqlalchemy import func, cast, Integer
    from app.models.ci_project import CIProject
    
    current_mode = get_mode()
    
    # Get unique years from CI projects start_date, filtered by mode
    years_result = db.query(
        cast(
            func.substr(CIProject.start_date, 1, 4),
            Integer
        ).distinct()
    ).filter(
        (CIProject.start_date.isnot(None)) &
        (CIProject.mode == current_mode)
    ).all()
    
    # Flatten and sort years
    years = sorted([year[0] for year in years_result if year[0]], reverse=True)
    
    # If no years found, return current year
    if not years:
        years = [datetime.now().year]
    
    # Add current year if not already in list
    current_year = datetime.now().year
    if current_year not in years:
        years.insert(0, current_year)
    
    return {"years": years, "current_year": current_year}
