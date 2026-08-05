import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = os.getenv("DATABASE_URL", "sqlite:///./cims.db")

engine = create_engine(
    DB_PATH,
    connect_args={"check_same_thread": False} if DB_PATH.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """Initialize database and create all tables"""
    # Import all models to ensure they're registered
    from app.models.user import User
    from app.models.kpi_target import KPITarget
    from app.models.ci_project import CIProject
    from app.models.ci_action import CIAction
    from app.models.ci_audit import CIAudit
    from app.models.admin_setting import AdminSetting
    from app.models.monthly_kpi_snapshot import MonthlyKPISnapshot
    from app.models.mode_log import DeclarativeBase as ModeLogBase, ModeLog
    
    # Create all tables from main Base
    Base.metadata.create_all(bind=engine)
    # Also create ModeLog table from its own base
    ModeLogBase.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
