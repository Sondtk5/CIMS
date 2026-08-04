from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.database import Base

class MonthlyKPISnapshot(Base):
    __tablename__ = "monthly_kpi_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)  # 2024, 2025, 2026, etc.
    month = Column(Integer, nullable=False, index=True)  # 1-12
    
    # KPI Metrics for this month
    on_time_completion_rate = Column(Float, nullable=True)  # %
    effectiveness_rate = Column(Float, nullable=True)  # %
    avg_closing_days = Column(Float, nullable=True)  # Days
    cost_saving = Column(Float, nullable=True)  # USD
    horizontal_deployment_count = Column(Integer, default=0)  # Count
    
    # Metadata
    total_projects_completed = Column(Integer, default=0)
    total_projects_running = Column(Integer, default=0)
    captured_at = Column(DateTime, default=datetime.utcnow)
    
    class Config:
        from_attributes = True
