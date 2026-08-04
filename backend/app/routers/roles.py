from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.role import Role
from app.models.user import User
from app.core.rbac import get_current_user, require_roles
from app.services.audit_logger import log_audit_event
from pydantic import BaseModel
from datetime import datetime

class RoleCreate(BaseModel):
    name: str
    description: str = ""
    permissions: str = ""

class RoleUpdate(BaseModel):
    description: str = ""
    permissions: str = ""

class RoleResponse(BaseModel):
    id: int
    name: str
    description: str
    permissions: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    updated_by: str = None
    
    class Config:
        from_attributes = True

class RoleUserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    role: str
    is_active: bool
    
    class Config:
        from_attributes = True

router = APIRouter(prefix="/api/roles", tags=["Role Management"])

@router.get("/", response_model=List[RoleResponse])
def list_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """List all roles"""
    return db.query(Role).all()

@router.post("/", response_model=RoleResponse)
def create_role(
    role_in: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Create a new role"""
    existing = db.query(Role).filter(Role.name == role_in.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role '{role_in.name}' already exists"
        )
    
    role = Role(
        name=role_in.name,
        description=role_in.description,
        permissions=role_in.permissions,
        updated_by=current_user.full_name
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    
    log_audit_event(
        db,
        user_name=current_user.full_name,
        user_role=current_user.role,
        action_type="CREATE_ROLE",
        field_changed=f"Role: {role.name}",
        old_value="",
        new_value=role_in.name,
        reason=f"Admin created new role"
    )
    
    return role

@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Get role details"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    role_in: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Update role details"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    old_desc = role.description
    role.description = role_in.description
    role.permissions = role_in.permissions
    role.updated_at = datetime.utcnow()
    role.updated_by = current_user.full_name
    
    db.commit()
    db.refresh(role)
    
    log_audit_event(
        db,
        user_name=current_user.full_name,
        user_role=current_user.role,
        action_type="UPDATE_ROLE",
        field_changed=f"Role: {role.name}",
        old_value=old_desc,
        new_value=role.description,
        reason=f"Admin updated role"
    )
    
    return role

@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Deactivate a role"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Check if any users have this role
    user_count = db.query(User).filter(User.role == role.name).count()
    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete role with {user_count} assigned user(s)"
        )
    
    role.is_active = False
    db.commit()
    
    log_audit_event(
        db,
        user_name=current_user.full_name,
        user_role=current_user.role,
        action_type="DEACTIVATE_ROLE",
        field_changed=f"Role: {role.name}",
        old_value="active",
        new_value="inactive",
        reason=f"Admin deactivated role"
    )
    
    return {"detail": "Role deactivated successfully"}

@router.get("/{role_id}/users", response_model=List[RoleUserResponse])
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
