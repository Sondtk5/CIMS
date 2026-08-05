
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.rbac import get_current_user
from app.services.kpi_calculator import calculate_kpis, save_current_month_snapshot
from datetime import datetime

router = APIRouter(prefix="/api/dashboard", tags=["Master Dashboard"])

@router.get("")
def get_dashboard_summary(
    year: int = Query(None, description="Year for monthly KPI trends (defaults to current year)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Dashboard accessible to all logged-in users:
    - Administrator: Full dashboard
    - TPM Manager: CI Project dashboard
    - Management: Executive dashboard (read-only)
    - Auditor: Read-only dashboard
    - Engineer: CI Project list view
    - QA Inspector: Verification dashboard
    
    Query Parameters:
    - year: Filter monthly KPI trends by year (e.g., 2024, 2025, 2026)
    """
    # All authenticated users have access to dashboard
    # RBAC is handled at component level (some sections may be hidden)
    
    # Use provided year or default to current year
    if year is None:
        year = datetime.now().year
    
    return calculate_kpis(db, year)


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
    Get list of available years from CI projects (based on start_date).
    Returns sorted list of unique years from all CI projects.
    """
    from sqlalchemy import func, cast, Integer
    from app.models.ci_project import CIProject
    
    # Get unique years from CI projects start_date
    years_result = db.query(
        cast(
            func.substr(CIProject.start_date, 1, 4),
            Integer
        ).distinct()
    ).filter(
        CIProject.start_date.isnot(None)
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
