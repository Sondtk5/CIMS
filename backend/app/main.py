import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.routers import auth, projects, dashboard, settings, reports, audit, roles
from app.seed import seed_db
from app.models.monthly_kpi_snapshot import MonthlyKPISnapshot  # Import to register model

# Initialize database schema
Base.metadata.create_all(bind=engine)

# Auto seed database on startup
seed_db()

app = FastAPI(
    title="Continual Improvement Management System (CIMS) API",
    description="ISO 9001:2015 & IATF 16949 Compliant Continual Improvement Backend API",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads directory exists
uploads_dir = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Include Routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(dashboard.router)
app.include_router(settings.router)
app.include_router(reports.router)
app.include_router(audit.router)
app.include_router(roles.router)

@app.get("/")
def root():
    return {
        "system": "Continual Improvement Management System (CIMS)",
        "version": "1.0.0",
        "status": "Online",
        "docs": "/docs"
    }
