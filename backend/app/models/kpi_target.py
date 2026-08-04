from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class KPITarget(Base):
    __tablename__ = "kpi_targets"

    id = Column(Integer, primary_key=True, index=True)
    kpi_key = Column(String, unique=True, index=True, nullable=False) # on_time_completion, effectiveness_rate, avg_closing_time, cost_saving, horizontal_deployment
    kpi_name = Column(String, nullable=False)
    target_value = Column(Float, nullable=False)
    unit = Column(String, nullable=False) # %, Days, USD, Projects
    comparison_operator = Column(String, nullable=False, default=">=") # >=, <=
    updated_by = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
