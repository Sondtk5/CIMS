from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ci_project import CIProject
from app.services.kpi_calculator import calculate_kpis

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/summary")
def get_reports_summary(db: Session = Depends(get_db)):
    kpi_data = calculate_kpis(db)
    projects = db.query(CIProject).all()
    
    # Department breakdown
    dept_map = {}
    for p in projects:
        dept = p.department or "General"
        if dept not in dept_map:
            dept_map[dept] = {"total": 0, "complete": 0, "saving": 0.0}
        dept_map[dept]["total"] += 1
        if p.status == "Complete":
            dept_map[dept]["complete"] += 1
        dept_map[dept]["saving"] += (p.cost_saving or 0.0)

    dept_summary = [
        {
            "department": k,
            "total_projects": v["total"],
            "completed": v["complete"],
            "completion_rate": round((v["complete"] / v["total"] * 100), 1) if v["total"] > 0 else 0,
            "cost_saving": v["saving"]
        }
        for k, v in dept_map.items()
    ]

    return {
        "kpi_data": kpi_data,
        "department_summary": dept_summary,
        "total_projects": len(projects)
    }
