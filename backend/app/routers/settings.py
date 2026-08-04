from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.kpi_target import KPITarget
from app.models.user import User
from app.models.role import Role
from app.schemas.kpi_target import KPITargetUpdate, KPITargetResponse
from app.core.rbac import get_current_user, require_roles
from app.core.security import get_password_hash
from app.services.audit_logger import log_audit_event
from pydantic import BaseModel
from datetime import datetime


class ResetPasswordRequest(BaseModel):
    new_password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    department: str
    is_active: bool
    password_changed_at: Optional[datetime] = None
    class Config:
        from_attributes = True


class RolePasswordResetRequest(BaseModel):
    role_name: str
    new_password: str


class RoleUserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    role: str
    class Config:
        from_attributes = True


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


@router.get("/users", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    return db.query(User).all()


@router.post("/users/{user_id}/reset-password")
def reset_user_password(
    user_id: int,
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = get_password_hash(request.new_password)
    user.password_changed_at = datetime.utcnow()
    db.commit()
    
    log_audit_event(
        db,
        user_name=current_user.full_name,
        user_role=current_user.role,
        action_type="RESET_USER_PASSWORD",
        field_changed=f"User {user.username}",
        old_value="***",
        new_value="***",
        reason=f"Admin reset password for {user.username}"
    )
    
    return {"detail": "Password reset successfully"}


@router.get("/roles")
def get_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Get all roles"""
    roles = db.query(Role).filter(Role.is_active == True).all()
    role_list = []
    for role in roles:
        user_count = db.query(User).filter(User.role == role.name).count()
        role_list.append({
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "user_count": user_count,
            "created_at": role.created_at,
            "updated_by": role.updated_by
        })
    return role_list


@router.get("/roles/{role_id}/users", response_model=List[RoleUserResponse])
def get_role_users(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Get all users assigned to a role"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    users = db.query(User).filter(User.role == role.name).all()
    return users


@router.post("/roles/{role_id}/reset-password-for-users")
def reset_password_for_role_users(
    role_id: int,
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Reset password for all users in a role"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    users = db.query(User).filter(User.role == role.name).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found for this role")
    
    hashed_pwd = get_password_hash(request.new_password)
    for user in users:
        user.hashed_password = hashed_pwd
        user.password_changed_at = datetime.utcnow()
    
    db.commit()
    
    log_audit_event(
        db,
        user_name=current_user.full_name,
        user_role=current_user.role,
        action_type="RESET_ROLE_PASSWORD",
        field_changed=f"Role: {role.name}",
        old_value="***",
        new_value="***",
        reason=f"Admin reset password for all users in role {role.name} ({len(users)} users)"
    )
    
    return {
        "detail": f"Password reset successfully for {len(users)} user(s) in role {role.name}"
    }
