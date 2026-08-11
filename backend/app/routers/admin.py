from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.rbac import require_roles, get_current_user
from app.models.user import User
from app.models.admin_setting import AdminSetting
from app.models.mode_log import ModeLog
from datetime import datetime
from app.services.ci_numbering_service import (
    get_or_create_ci_numbering_config,
    update_ci_numbering_config,
    get_ci_numbering_format,
    generate_ci_number
)
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/admin", tags=["Admin Settings"])

# ===== Pydantic Models =====
class CINumberingPart(BaseModel):
    name: str
    value: str
    enabled: bool
    auto_increment: bool = False

class CINumberingConfigUpdate(BaseModel):
    parts: List[CINumberingPart]
    separator: str = "-"

class CINumberingConfigResponse(BaseModel):
    parts: List[CINumberingPart]
    separator: str
    next_counter: int
    example: str

# ===== Admin: Get CI Numbering Configuration =====
@router.get("/ci-numbering")
def get_ci_numbering_config(
    mode: str = "production",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "TPM Manager", "Engineer", "QA Inspector"]))
):
    """Get current CI numbering configuration for the specified mode (DEMO or PRODUCTION)"""
    return get_ci_numbering_format(db, mode.lower())

# ===== Admin: Update CI Numbering Configuration =====
@router.put("/ci-numbering")
def update_ci_numbering(
    config: CINumberingConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Update CI numbering configuration (affects both DEMO and PRODUCTION - shared structure only)"""
    try:
        # Validate parts
        if not config.parts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one part must be enabled"
            )
        
        # Convert pydantic models to dict
        parts_list = [part.dict() for part in config.parts]
        
        config_data = {
            "parts": parts_list,
            "separator": config.separator
        }
        
        updated_setting = update_ci_numbering_config(db, config_data)
        
        return {
            "status": "success",
            "message": "CI numbering configuration updated (applies to both DEMO and PRODUCTION modes)",
            "config": get_ci_numbering_format(db, "production")
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# ===== Admin: Generate Next CI Number (Preview) =====
@router.post("/ci-numbering/generate")
def preview_next_ci_number(
    dept_code: str = None,
    cat_code: str = None,
    mode: str = "production",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "TPM Manager", "Engineer"]))
):
    """Preview next CI number for the specified mode (without incrementing)"""
    try:
        # Get current config for the mode
        setting = get_or_create_ci_numbering_config(db, mode.lower())
        config = setting.setting_value
        
        # Generate preview without incrementing
        next_ci = generate_ci_number(db, dept_code, cat_code, mode.lower(), commit=False)
        
        return {
            "next_ci_number": next_ci,
            "current_counter": config.get("next_counter", 1),
            "mode": mode.upper(),
            "note": "This is a preview. The counter will increment when project is created."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# ===== Admin: Get All Settings (for future use) =====
@router.get("/settings")
def get_all_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Get all admin settings"""
    settings = db.query(AdminSetting).all()
    return {
        "count": len(settings),
        "settings": [
            {
                "key": s.setting_key,
                "description": s.description,
                "updated_at": s.updated_at
            }
            for s in settings
        ]
    }

# ===== DEMO / PRODUCTION MODE =====
class ModeToggleRequest(BaseModel):
    mode: str  # "demo" or "production"

@router.get("/mode")
def get_current_mode(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Get current application mode (DEMO or PRODUCTION)"""
    from app.core.config import get_mode
    
    current_mode = get_mode()
    
    return {
        "mode": current_mode,
        "description": "Demo mode with 133 sample projects" if current_mode == "DEMO" else "Production mode with real data",
        "demo_count": 133,
        "production_count": 6
    }

@router.put("/mode")
def toggle_app_mode(
    request: ModeToggleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Toggle between demo and production mode (instant, no restart needed)"""
    from app.core.config import set_mode
    
    mode = request.mode.upper()
    if mode not in ["DEMO", "PRODUCTION"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mode must be 'DEMO' or 'PRODUCTION'"
        )
    
    try:
        # Switch mode in memory (no restart needed)
        set_mode(mode)
        
        # Log the mode change
        mode_log = ModeLog(
            mode=mode,
            action=f"Switched to {mode} Mode",
            timestamp=datetime.utcnow(),
            user=current_user.username,
            details=f"User {current_user.full_name} switched mode to {mode}"
        )
        db.add(mode_log)
        db.commit()
        
        message = f"Switched to {mode} mode - Instant mode switching complete"
        return {
            "status": "success",
            "mode": mode,
            "message": message,
            "demo_projects": 133 if mode == "DEMO" else 0,
            "production_projects": 6 if mode == "PRODUCTION" else 0
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to toggle mode: {str(e)}"
        )


# ===== Mode Logs / Tracking =====
@router.get("/mode/logs")
def get_mode_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Get mode change tracking logs (DEMO or PRODUCTION only)"""
    try:
        logs = db.query(ModeLog).order_by(ModeLog.timestamp.desc()).limit(limit).all()
        
        return {
            "status": "success",
            "count": len(logs),
            "logs": [
                {
                    "id": log.id,
                    "mode": log.mode,
                    "action": log.action,
                    "timestamp": log.timestamp.isoformat(),
                    "user": log.user,
                    "details": log.details
                }
                for log in logs
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve logs: {str(e)}"
        )
