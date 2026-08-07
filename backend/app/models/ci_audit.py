from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base

class CIAudit(Base):
    __tablename__ = "ci_audits"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=True)
    ci_no = Column(String, nullable=True)
    user_name = Column(String, nullable=False)
    user_role = Column(String, nullable=True)
    action_type = Column(String, nullable=False) # CREATE, UPDATE, DELETE, VERIFY, APPROVE
    field_changed = Column(String, nullable=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)
    mode = Column(String, default="PRODUCTION", nullable=False)  # DEMO or PRODUCTION
    timestamp = Column(DateTime, default=datetime.utcnow)
