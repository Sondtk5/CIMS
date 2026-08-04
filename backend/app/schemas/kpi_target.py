from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class KPITargetBase(BaseModel):
    kpi_key: str
    kpi_name: str
    target_value: float
    unit: str
    comparison_operator: str = ">="

class KPITargetUpdate(BaseModel):
    target_value: float
    comparison_operator: Optional[str] = None
    unit: Optional[str] = None

class KPITargetResponse(KPITargetBase):
    id: int
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
