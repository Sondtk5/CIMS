from pydantic import BaseModel
from typing import Optional, Any, Dict, List
from datetime import datetime

class CIProjectBase(BaseModel):
    title: str
    department: str
    process_area: Optional[str] = None
    category: str
    priority: str = "Medium"
    owner: str
    requester: Optional[str] = None
    position: Optional[str] = None
    contact: Optional[str] = None
    
    start_date: str
    due_date: str
    close_date: Optional[str] = None
    status: str = "Running"
    progress: int = 0
    
    kpi_metric: Optional[str] = None
    before_value: Optional[float] = None
    target_value: Optional[float] = None
    after_value: Optional[float] = None
    achievement_rate: Optional[float] = None
    
    result: Optional[str] = "-"
    verified: Optional[str] = "No"
    verified_by: Optional[str] = None
    verified_date: Optional[str] = None
    
    closing_days: Optional[int] = None
    cost_saving: float = 0.0
    horizontal_deploy: str = "No"
    
    issue_description: Optional[str] = None
    current_status: Optional[str] = None
    target_description: Optional[str] = None
    expected_benefit: Optional[str] = None
    related_process: Optional[str] = None
    remarks: Optional[str] = None
    
    tpm_reviewed_by: Optional[str] = None
    tpm_review_date: Optional[str] = None
    tpm_review_comment: Optional[str] = None
    tpm_decision: Optional[str] = "Pending"
    
    define_stage: Optional[Dict[str, Any]] = None
    measure_stage: Optional[Dict[str, Any]] = None
    analyze_stage: Optional[Dict[str, Any]] = None
    improve_stage: Optional[Dict[str, Any]] = None
    control_stage: Optional[Dict[str, Any]] = None
    lessons_learned: Optional[Dict[str, Any]] = None
    approval_signatures: Optional[Dict[str, Any]] = None

class CIProjectCreate(CIProjectBase):
    ci_no: Optional[str] = None # Generated automatically if blank

class CIProjectUpdate(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    process_area: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    owner: Optional[str] = None
    requester: Optional[str] = None
    position: Optional[str] = None
    contact: Optional[str] = None
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    close_date: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = None
    
    kpi_metric: Optional[str] = None
    before_value: Optional[float] = None
    target_value: Optional[float] = None
    after_value: Optional[float] = None
    achievement_rate: Optional[float] = None
    result: Optional[str] = None
    verified: Optional[str] = None
    verified_by: Optional[str] = None
    verified_date: Optional[str] = None
    closing_days: Optional[int] = None
    cost_saving: Optional[float] = None
    horizontal_deploy: Optional[str] = None
    
    issue_description: Optional[str] = None
    current_status: Optional[str] = None
    target_description: Optional[str] = None
    expected_benefit: Optional[str] = None
    related_process: Optional[str] = None
    remarks: Optional[str] = None
    
    tpm_reviewed_by: Optional[str] = None
    tpm_review_date: Optional[str] = None
    tpm_review_comment: Optional[str] = None
    tpm_decision: Optional[str] = None
    
    define_stage: Optional[Dict[str, Any]] = None
    measure_stage: Optional[Dict[str, Any]] = None
    analyze_stage: Optional[Dict[str, Any]] = None
    improve_stage: Optional[Dict[str, Any]] = None
    control_stage: Optional[Dict[str, Any]] = None
    lessons_learned: Optional[Dict[str, Any]] = None
    approval_signatures: Optional[Dict[str, Any]] = None

class CIProjectResponse(CIProjectBase):
    id: int
    ci_no: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
