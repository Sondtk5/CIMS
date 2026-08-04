from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from app.database import Base

class CIAction(Base):
    __tablename__ = "ci_actions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("ci_projects.id", ondelete="CASCADE"), nullable=False)
    action_text = Column(Text, nullable=False)
    pic = Column(String, nullable=False)
    due_date = Column(String, nullable=False)
    completion_date = Column(String, nullable=True)
    status = Column(String, default="Pending") # Pending, In Progress, Completed
    evidence = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
