from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.ci_project import CIProject
from app.models.user import User
from app.schemas.ci_project import CIProjectCreate, CIProjectUpdate, CIProjectResponse
from app.core.rbac import get_current_user, require_roles
from app.core.config import get_mode
from app.services.audit_logger import log_audit_event
from app.services.ci_numbering_service import generate_ci_number
from datetime import datetime

router = APIRouter(prefix="/api/projects", tags=["CI Projects"])

@router.get("", response_model=List[CIProjectResponse])
def get_projects(
    search: Optional[str] = None,
    category: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get projects - filtered by current app mode (DEMO or PRODUCTION)"""
    current_mode = get_mode()
    query = db.query(CIProject).filter(CIProject.mode == current_mode)
    
    if search:
        s = f"%{search}%"
        query = query.filter(
            (CIProject.ci_no.ilike(s)) |
            (CIProject.title.ilike(s)) |
            (CIProject.owner.ilike(s)) |
            (CIProject.process_area.ilike(s))
        )
    if category and category != "All":
        query = query.filter(CIProject.category == category)
    if department and department != "All":
        query = query.filter(CIProject.department == department)
    if status and status != "All":
        query = query.filter(CIProject.status == status)
    if priority and priority != "All":
        query = query.filter(CIProject.priority == priority)
        
    return query.order_by(CIProject.id.asc()).all()

@router.get("/{project_id}", response_model=CIProjectResponse)
def get_project_by_id(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get single project - checks mode"""
    current_mode = get_mode()
    project = db.query(CIProject).filter(
        (CIProject.id == project_id) & 
        (CIProject.mode == current_mode)
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("", response_model=CIProjectResponse, status_code=201)
def create_project(
    project_in: CIProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "TPM Manager", "Engineer"]))
):
    """
    Create project - only Administrator, TPM Manager, Engineer
    Auto-generates CI No based on current mode (DEMO or PRODUCTION)
    """
    # Auto-generate CI No using new mode-specific config system
    if not project_in.ci_no:
        current_mode = get_mode()
        project_in.ci_no = generate_ci_number(db, mode=current_mode.lower())

    # Calculate achievement rate if metrics present
    ach_rate = project_in.achievement_rate
    if project_in.before_value is not None and project_in.after_value is not None and project_in.target_value is not None:
        try:
            target_diff = abs(project_in.target_value - project_in.before_value)
            actual_diff = abs(project_in.after_value - project_in.before_value)
            if target_diff > 0:
                ach_rate = round((actual_diff / target_diff) * 100, 1)
        except Exception:
            pass

    # Calculate closing days if close date present
    closing_days = project_in.closing_days
    if project_in.close_date and project_in.start_date:
        try:
            d1 = datetime.strptime(project_in.start_date, "%Y-%m-%d")
            d2 = datetime.strptime(project_in.close_date, "%Y-%m-%d")
            closing_days = (d2 - d1).days
        except Exception:
            pass

    db_project = CIProject(
        **project_in.model_dump(exclude_unset=True),
        achievement_rate=ach_rate,
        closing_days=closing_days,
        owner_id=current_user.id,  # Track who created this project
        mode=get_mode()  # Assign to current mode
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    log_audit_event(
        db,
        user_name=current_user.full_name,
        user_role=current_user.role,
        action_type="CREATE",
        project_id=db_project.id,
        ci_no=db_project.ci_no,
        reason=f"Created project: {db_project.title}"
    )

    return db_project

@router.put("/{project_id}", response_model=CIProjectResponse)
def update_project(
    project_id: int,
    project_in: CIProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update project - role-based restrictions:
    - Administrator: can update any project
    - TPM Manager: can update any project
    - Engineer: can update only OWN projects
    - QA: can update project details and mark verified
    - Management, Auditor: cannot update
    """
    project = db.query(CIProject).filter(CIProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check authorization based on role
    if current_user.role == "Management":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Management role cannot edit projects (dashboard view only)"
        )
    elif current_user.role == "Auditor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Auditor role is read-only"
        )
    elif current_user.role == "Engineer":
        # Engineer can only edit their own projects
        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Engineer can only edit their own projects"
            )
    elif current_user.role == "QA Inspector":
        # QA Inspector can only update verified fields
        update_data = project_in.model_dump(exclude_unset=True)
        allowed_fields = {"verified", "verified_by", "verified_date", "result"}
        if not all(field in allowed_fields for field in update_data.keys()):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="QA Inspector can only update verification fields"
            )
    # Administrator and TPM Manager can update anything

    old_status = project.status
    update_data = project_in.model_dump(exclude_unset=True)

    # Recalculate achievement rate if values updated
    before_val = update_data.get("before_value", project.before_value)
    target_val = update_data.get("target_value", project.target_value)
    after_val = update_data.get("after_value", project.after_value)

    if before_val is not None and target_val is not None and after_val is not None:
        try:
            target_diff = abs(target_val - before_val)
            actual_diff = abs(after_val - before_val)
            if target_diff > 0:
                update_data["achievement_rate"] = round((actual_diff / target_diff) * 100, 1)
        except Exception:
            pass

    # Recalculate closing days if status changed to Complete or dates modified
    new_status = update_data.get("status", project.status)
    close_dt = update_data.get("close_date", project.close_date)
    start_dt = update_data.get("start_date", project.start_date)

    if new_status == "Complete" and not close_dt:
        close_dt = datetime.now().strftime("%Y-%m-%d")
        update_data["close_date"] = close_dt

    if close_dt and start_dt:
        try:
            d1 = datetime.strptime(start_dt, "%Y-%m-%d")
            d2 = datetime.strptime(close_dt, "%Y-%m-%d")
            update_data["closing_days"] = (d2 - d1).days
        except Exception:
            pass

    for key, value in update_data.items():
        setattr(project, key, value)

    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)

    log_audit_event(
        db,
        user_name=current_user.full_name,
        user_role=current_user.role,
        action_type="UPDATE",
        project_id=project.id,
        ci_no=project.ci_no,
        field_changed="multiple",
        old_value=old_status,
        new_value=project.status,
        reason="Updated project details"
    )

    return project

@router.delete("/{project_id}", status_code=200)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "TPM Manager"]))
):
    """
    Delete project - only Administrator and TPM Manager
    """
    project = db.query(CIProject).filter(CIProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    ci_no = project.ci_no
    title = project.title

    db.delete(project)
    db.commit()

    log_audit_event(
        db,
        user_name=current_user.full_name,
        user_role=current_user.role,
        action_type="DELETE",
        project_id=project_id,
        ci_no=ci_no,
        reason=f"Deleted project: {title}"
    )

    return {"message": f"Project {ci_no} deleted successfully"}
