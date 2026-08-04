from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.ci_audit import CIAudit

router = APIRouter(prefix="/api/audit", tags=["Log Tracking"])

@router.get("")
def get_audit_logs(db: Session = Depends(get_db)):
    return db.query(CIAudit).order_by(CIAudit.timestamp.desc()).all()
