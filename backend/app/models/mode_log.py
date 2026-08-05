from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Create a simple declarative base for this module
DeclarativeBase = declarative_base()

class ModeLog(DeclarativeBase):
    __tablename__ = 'mode_logs'
    
    id = Column(Integer, primary_key=True, index=True)
    mode = Column(String(50), nullable=False)  # DEMO or PRODUCTION
    action = Column(String(100), nullable=False)  # "Switched to DEMO", "Switched to PRODUCTION"
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    user = Column(String(100), nullable=True)  # Username who triggered the change
    details = Column(Text, nullable=True)  # Additional details
    
    def __repr__(self):
        return f"<ModeLog(mode={self.mode}, action={self.action}, timestamp={self.timestamp})>"
