from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.kpi_target import KPITarget
from app.models.user import User
from app.schemas.kpi_target import KPITargetUpdate, KPITargetResponse
from app.core.rbac import get_current_user, require_roles
from app.services.audit_logger import log_audit_event

router = APIRouter(prefix="/api/settings", tags=["Admin Settings"])

@router.get("/kpi-targets", response_model=List[KPITargetResponse])
def get_kpi_targets(db: Session = Depends(get_db)):
    return db.query(KPITarget).all()

@router.put("/kpi-targets/{kpi_key}", response_model=KPITargetResponse)
def update_kpi_target(
    kpi_key: str,
    target_in: KPITargetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    kpi = db.query(KPITarget).filter(KPITarget.kpi_key == kpi_key).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI Target key not found")

    old_val = kpi.target_value
    kpi.target_value = target_in.target_value
    if target_in.comparison_operator:
        kpi.comparison_operator = target_in.comparison_operator
    if target_in.unit:
        kpi.unit = target_in.unit
    
    kpi.updated_by = current_user.full_name
    db.commit()
    db.refresh(kpi)

    log_audit_event(
        db,
        user_name=current_user.full_name,
        user_role=current_user.role,
        action_type="UPDATE_KPI_TARGET",
        field_changed=kpi_key,
        old_value=str(old_val),
        new_value=str(kpi.target_value),
        reason=f"Admin updated target for {kpi.kpi_name}"
    )

    return kpi
