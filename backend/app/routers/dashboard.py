from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.rbac import get_current_user
from app.services.kpi_calculator import calculate_kpis

router = APIRouter(prefix="/api/dashboard", tags=["Master Dashboard"])

@router.get("")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Dashboard accessible to:
    - Administrator: Full dashboard
    - TPM Manager: CI Project dashboard
    - Management: Executive dashboard (read-only)
    - Auditor: Read-only dashboard
    
    Restricted for:
    - Engineer: No dashboard access
    - QA Inspector: No dashboard access
    """
    # Block Engineer and QA Inspector from dashboard
    if current_user.role in ["Engineer", "QA Inspector"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{current_user.role} role does not have access to the dashboard"
        )
    
    return calculate_kpis(db)
