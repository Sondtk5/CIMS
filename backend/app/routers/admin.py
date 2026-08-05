from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.rbac import require_roles, get_current_user
from app.models.user import User
from app.models.admin_setting import AdminSetting
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
@router.get("/ci-numbering", response_model=CINumberingConfigResponse)
def get_ci_numbering_config(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "TPM Manager", "Engineer", "QA Inspector"]))
):
    """Get current CI numbering configuration (all users can read)"""
    return get_ci_numbering_format(db)

# ===== Admin: Update CI Numbering Configuration =====
@router.put("/ci-numbering", response_model=dict)
def update_ci_numbering(
    config: CINumberingConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator"]))
):
    """Update CI numbering configuration (Admin only)"""
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
            "message": "CI numbering configuration updated",
            "config": get_ci_numbering_format(db)
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
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Administrator", "TPM Manager", "Engineer"]))
):
    """Preview next CI number that will be generated (without incrementing)"""
    try:
        # Get current config
        setting = get_or_create_ci_numbering_config(db)
        config = setting.setting_value
        
        # Temporarily increment counter to generate preview
        original_counter = config.get("next_counter", 1)
        config["next_counter"] = original_counter
        
        next_ci = generate_ci_number(db, dept_code, cat_code)
        
        # Don't save changes - just preview
        return {
            "next_ci_number": next_ci,
            "current_counter": original_counter,
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
