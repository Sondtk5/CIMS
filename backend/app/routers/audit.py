from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.ci_audit import CIAudit
from app.models.user import User
from app.core.rbac import get_current_user

router = APIRouter(prefix="/api/audit", tags=["Log Tracking"])

@router.get("")
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Audit Log accessible to:
    - Administrator: Full access
    - Auditor: Read-only access
    
    Restricted for:
    - All other roles: No access
    """
    if current_user.role not in ["Administrator", "Auditor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{current_user.role} role does not have access to audit logs"
        )
    
    return db.query(CIAudit).order_by(CIAudit.timestamp.desc()).all()
