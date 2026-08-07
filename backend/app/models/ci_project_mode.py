from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from datetime import datetime
from app.database import Base

class CIProjectDemo(Base):
    """Demo mode CI projects (sample data)"""
    __tablename__ = "ci_projects_demo"

    id = Column(Integer, primary_key=True, index=True)
    ci_no = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    department = Column(String, nullable=False)
    process_area = Column(String, nullable=True)
    category = Column(String, nullable=False)
    priority = Column(String, nullable=False, default="Medium")
    owner = Column(String, nullable=False)
    owner_id = Column(Integer, nullable=True, index=True)
    requester = Column(String, nullable=True)
    position = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    
    start_date = Column(String, nullable=False)
    due_date = Column(String, nullable=False)
    close_date = Column(String, nullable=True)
    
    status = Column(String, nullable=False, default="Running")
    progress = Column(Integer, default=0)
    
    kpi_metric = Column(String, nullable=True)
    before_value = Column(Float, nullable=True)
    target_value = Column(Float, nullable=True)
    after_value = Column(Float, nullable=True)
    achievement_rate = Column(Float, nullable=True)
    
    result = Column(String, nullable=True, default="-")
    verified = Column(String, nullable=True, default="No")
    verified_by = Column(String, nullable=True)
    verified_date = Column(String, nullable=True)
    
    closing_days = Column(Integer, nullable=True)
    cost_saving = Column(Float, default=0.0)
    horizontal_deploy = Column(String, default="No")
    
    issue_description = Column(Text, nullable=True)
    current_status = Column(Text, nullable=True)
    target_description = Column(Text, nullable=True)
    expected_benefit = Column(Text, nullable=True)
    related_process = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    
    tpm_reviewed_by = Column(String, nullable=True)
    tpm_review_date = Column(String, nullable=True)
    tpm_review_comment = Column(Text, nullable=True)
    tpm_decision = Column(String, default="Pending")
    tpm_approved_by = Column(String, nullable=True)
    tpm_approve_date = Column(String, nullable=True)
    tpm_approve_comment = Column(Text, nullable=True)
    
    define_stage = Column(JSON, nullable=True)
    measure_stage = Column(JSON, nullable=True)
    analyze_stage = Column(JSON, nullable=True)
    improve_stage = Column(JSON, nullable=True)
    control_stage = Column(JSON, nullable=True)
    
    lessons_learned = Column(JSON, nullable=True)
    approval_signatures = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CIProjectProduction(Base):
    """Production mode CI projects (real data)"""
    __tablename__ = "ci_projects_production"

    id = Column(Integer, primary_key=True, index=True)
    ci_no = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    department = Column(String, nullable=False)
    process_area = Column(String, nullable=True)
    category = Column(String, nullable=False)
    priority = Column(String, nullable=False, default="Medium")
    owner = Column(String, nullable=False)
    owner_id = Column(Integer, nullable=True, index=True)
    requester = Column(String, nullable=True)
    position = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    
    start_date = Column(String, nullable=False)
    due_date = Column(String, nullable=False)
    close_date = Column(String, nullable=True)
    
    status = Column(String, nullable=False, default="Running")
    progress = Column(Integer, default=0)
    
    kpi_metric = Column(String, nullable=True)
    before_value = Column(Float, nullable=True)
    target_value = Column(Float, nullable=True)
    after_value = Column(Float, nullable=True)
    achievement_rate = Column(Float, nullable=True)
    
    result = Column(String, nullable=True, default="-")
    verified = Column(String, nullable=True, default="No")
    verified_by = Column(String, nullable=True)
    verified_date = Column(String, nullable=True)
    
    closing_days = Column(Integer, nullable=True)
    cost_saving = Column(Float, default=0.0)
    horizontal_deploy = Column(String, default="No")
    
    issue_description = Column(Text, nullable=True)
    current_status = Column(Text, nullable=True)
    target_description = Column(Text, nullable=True)
    expected_benefit = Column(Text, nullable=True)
    related_process = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    
    tpm_reviewed_by = Column(String, nullable=True)
    tpm_review_date = Column(String, nullable=True)
    tpm_review_comment = Column(Text, nullable=True)
    tpm_decision = Column(String, default="Pending")
    tpm_approved_by = Column(String, nullable=True)
    tpm_approve_date = Column(String, nullable=True)
    tpm_approve_comment = Column(Text, nullable=True)
    
    define_stage = Column(JSON, nullable=True)
    measure_stage = Column(JSON, nullable=True)
    analyze_stage = Column(JSON, nullable=True)
    improve_stage = Column(JSON, nullable=True)
    control_stage = Column(JSON, nullable=True)
    
    lessons_learned = Column(JSON, nullable=True)
    approval_signatures = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
