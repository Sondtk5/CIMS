from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from datetime import datetime
from app.database import Base

class CIProject(Base):
    __tablename__ = "ci_projects"

    id = Column(Integer, primary_key=True, index=True)
    ci_no = Column(String, unique=True, index=True, nullable=False) # e.g. CI-26-001
    title = Column(String, nullable=False)
    department = Column(String, nullable=False) # Slit Coater, Wet Bench, IOX, Overall, TPM, Quality, etc.
    process_area = Column(String, nullable=True) # Slit Coater, IOX, Line 1, etc.
    category = Column(String, nullable=False) # Quality, Productivity, Cost Saving, Safety / Environment, Equipment, Others
    priority = Column(String, nullable=False, default="Medium") # Low, Medium, High, Critical
    owner = Column(String, nullable=False) # Leader / Owner
    owner_id = Column(Integer, nullable=True, index=True) # User ID who created/owns this project
    requester = Column(String, nullable=True)
    position = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    
    start_date = Column(String, nullable=False) # YYYY-MM-DD
    due_date = Column(String, nullable=False)   # YYYY-MM-DD
    close_date = Column(String, nullable=True)  # YYYY-MM-DD
    
    status = Column(String, nullable=False, default="Running") # Complete, Running, Pending, Draft
    progress = Column(Integer, default=0) # 0-100%
    
    # Section B of CI Request Form & Define Stage
    kpi_metric = Column(String, nullable=True) # Defect Rate (%), UPH (pcs/hr), Chemical Cost (USD/Month), etc.
    before_value = Column(Float, nullable=True)
    target_value = Column(Float, nullable=True)
    after_value = Column(Float, nullable=True)
    achievement_rate = Column(Float, nullable=True) # Calculated %
    
    result = Column(String, nullable=True, default="-") # PASS, FAIL, -
    verified = Column(String, nullable=True, default="No") # Yes, No
    verified_by = Column(String, nullable=True)
    verified_date = Column(String, nullable=True)
    
    closing_days = Column(Integer, nullable=True)
    cost_saving = Column(Float, default=0.0) # USD/Year
    horizontal_deploy = Column(String, default="No") # Yes, No
    
    issue_description = Column(Text, nullable=True)
    current_status = Column(Text, nullable=True)
    target_description = Column(Text, nullable=True)
    expected_benefit = Column(Text, nullable=True)
    related_process = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    
    # TPM Review & Approval
    tpm_reviewed_by = Column(String, nullable=True)
    tpm_review_date = Column(String, nullable=True)
    tpm_review_comment = Column(Text, nullable=True)
    tpm_decision = Column(String, default="Pending") # Approved, Not Approved, Pending
    
    # DMAIC 5-Phase Detailed Content (JSON objects / Text blocks)
    define_stage = Column(JSON, nullable=True)   # { background, scope, team_members, etc. }
    measure_stage = Column(JSON, nullable=True)  # { data_collection_plan, data_source, baseline, etc. }
    analyze_stage = Column(JSON, nullable=True)  # { five_why: [], fishbone: {}, doe: {}, rca_summary: "" }
    improve_stage = Column(JSON, nullable=True)  # { action_items: [], pilot_plan: "", resources: "" }
    control_stage = Column(JSON, nullable=True)  # { sop_update: "", training_plan: "", monitoring_plan: "" }
    
    lessons_learned = Column(JSON, nullable=True) # { what_learned, continue_action, next_action }
    approval_signatures = Column(JSON, nullable=True) # { prepared_by: {name, date}, reviewed_by: {name, date}, approved_by: {name, date} }

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
