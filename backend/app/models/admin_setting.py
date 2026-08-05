from sqlalchemy import Column, Integer, String, Boolean, JSON
from datetime import datetime
from app.database import Base

class AdminSetting(Base):
    __tablename__ = "admin_settings"

    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String, unique=True, nullable=False, index=True)
    # For CI numbering convention, the key will be "ci_numbering_config"
    
    # Example for ci_numbering_config:
    # {
    #   "parts": [
    #     {"name": "prefix", "value": "UTIV", "enabled": true},
    #     {"name": "department", "value": "EN", "enabled": true},
    #     {"name": "category", "value": "R", "enabled": true},
    #     {"name": "year", "value": "00", "enabled": true},
    #     {"name": "sequence", "value": "0000", "enabled": true},
    #     {"name": "version", "value": "00", "enabled": true},
    #     {"name": "counter", "value": "000", "enabled": true, "auto_increment": true}
    #   ],
    #   "separator": "-",
    #   "next_sequence": 1,  # For counter auto-increment
    #   "last_updated": "2026-08-04T12:00:00"
    # }
    setting_value = Column(JSON, nullable=False)
    
    description = Column(String, nullable=True)
    created_at = Column(String, nullable=False, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, nullable=False, default=lambda: datetime.utcnow().isoformat())
