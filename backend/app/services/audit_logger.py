from sqlalchemy.orm import Session
from app.models.ci_audit import CIAudit

def log_audit_event(
    db: Session,
    user_name: str,
    user_role: str,
    action_type: str,
    project_id: int = None,
    ci_no: str = None,
    field_changed: str = None,
    old_value: str = None,
    new_value: str = None,
    reason: str = None
):
    audit = CIAudit(
        project_id=project_id,
        ci_no=ci_no,
        user_name=user_name,
        user_role=user_role,
        action_type=action_type,
        field_changed=field_changed,
        old_value=str(old_value) if old_value is not None else None,
        new_value=str(new_value) if new_value is not None else None,
        reason=reason
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit
