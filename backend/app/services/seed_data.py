"""
Seed data service for Demo mode.
Contains sample CI projects for demonstration purposes.
"""
from sqlalchemy.orm import Session
from app.models.ci_project import CIProject
from datetime import datetime, timedelta

def seed_demo_data(db: Session):
    """
    Load sample CI project data for demo mode.
    Creates realistic CI projects across 2024-2026.
    """
    # Check if demo data already exists
    existing_count = db.query(CIProject).count()
    if existing_count > 0:
        # Already has data, skip seeding
        return {"status": "skipped", "message": "Data already exists"}
    
    # Sample CI projects for demo
    demo_projects = [
        {
            "ci_no": "UTIV-EN-R-24-0000-00-001",
            "title": "Reduce Slit Coater Defect Rate by 50%",
            "category": "Quality",
            "department": "Engineering",
            "process_area": "Slit Coater",
            "owner": "John Smith",
            "priority": "High",
            "start_date": "2024-01-15",
            "due_date": "2024-03-15",
            "close_date": "2024-03-10",
            "status": "Complete",
            "progress": 100,
            "kpi_metric": "Defect Rate (%)",
            "before_value": 8.5,
            "target_value": 4.0,
            "after_value": 4.2,
            "achievement_rate": 98.0,
            "result": "PASS",
            "verified": "Yes",
            "verified_by": "QA Team",
            "verified_date": "2024-03-12",
            "cost_saving": 15000.00,
            "horizontal_deploy": "Yes",
            "closing_days": 55
        },
        {
            "ci_no": "UTIV-EN-R-24-0000-00-002",
            "title": "Improve Coating Uniformity Machine A",
            "category": "Quality",
            "department": "Engineering",
            "process_area": "Coating Line A",
            "owner": "Mary Johnson",
            "priority": "Medium",
            "start_date": "2024-02-01",
            "due_date": "2024-04-30",
            "close_date": "2024-04-28",
            "status": "Complete",
            "progress": 100,
            "kpi_metric": "Uniformity Score",
            "before_value": 75.0,
            "target_value": 85.0,
            "after_value": 86.5,
            "achievement_rate": 105.0,
            "result": "PASS",
            "verified": "Yes",
            "verified_by": "QA Team",
            "verified_date": "2024-04-29",
            "cost_saving": 8500.00,
            "horizontal_deploy": "No",
            "closing_days": 87
        },
        {
            "ci_no": "UTIV-EN-R-24-0000-00-003",
            "title": "Reduce Packaging Line Downtime",
            "category": "Efficiency",
            "department": "Operations",
            "process_area": "Packaging",
            "owner": "Robert Lee",
            "priority": "High",
            "start_date": "2024-03-10",
            "due_date": "2024-05-10",
            "close_date": "2024-05-12",
            "status": "Complete",
            "progress": 100,
            "kpi_metric": "Downtime (Hours/Month)",
            "before_value": 48.0,
            "target_value": 24.0,
            "after_value": 22.5,
            "achievement_rate": 110.0,
            "result": "PASS",
            "verified": "Yes",
            "verified_by": "QA Team",
            "verified_date": "2024-05-13",
            "cost_saving": 45000.00,
            "horizontal_deploy": "Yes",
            "closing_days": 63
        },
        {
            "ci_no": "UTIV-EN-R-24-0000-00-004",
            "title": "Optimize Material Waste in Die Cutting",
            "category": "Cost Reduction",
            "department": "Engineering",
            "process_area": "Die Cutting",
            "owner": "Sarah Davis",
            "priority": "Medium",
            "start_date": "2024-04-01",
            "due_date": "2024-06-30",
            "close_date": "2024-06-25",
            "status": "Complete",
            "progress": 100,
            "kpi_metric": "Waste Rate (%)",
            "before_value": 6.8,
            "target_value": 3.5,
            "after_value": 3.8,
            "achievement_rate": 92.0,
            "result": "PASS",
            "verified": "Yes",
            "verified_by": "QA Team",
            "verified_date": "2024-06-26",
            "cost_saving": 22000.00,
            "horizontal_deploy": "No",
            "closing_days": 86
        },
        {
            "ci_no": "UTIV-EN-R-25-0000-00-005",
            "title": "Improve First Pass Yield Rate",
            "category": "Quality",
            "department": "Engineering",
            "process_area": "Coating Line B",
            "owner": "James Wilson",
            "priority": "High",
            "start_date": "2025-01-10",
            "due_date": "2025-03-31",
            "close_date": "2025-03-28",
            "status": "Complete",
            "progress": 100,
            "kpi_metric": "FPY (%)",
            "before_value": 82.0,
            "target_value": 90.0,
            "after_value": 91.5,
            "achievement_rate": 102.0,
            "result": "PASS",
            "verified": "Yes",
            "verified_by": "QA Team",
            "verified_date": "2025-03-29",
            "cost_saving": 18000.00,
            "horizontal_deploy": "Yes",
            "closing_days": 78
        },
        {
            "ci_no": "UTIV-EN-R-25-0000-00-006",
            "title": "Reduce Raw Material Cost",
            "category": "Cost Reduction",
            "department": "Procurement",
            "process_area": "Supplier Management",
            "owner": "Emily Brown",
            "priority": "Medium",
            "start_date": "2025-02-15",
            "due_date": "2025-05-15",
            "close_date": None,
            "status": "Running",
            "progress": 65,
            "kpi_metric": "Material Cost ($/Unit)",
            "before_value": 12.50,
            "target_value": 11.00,
            "after_value": None,
            "achievement_rate": None,
            "result": None,
            "verified": "No",
            "verified_by": None,
            "verified_date": None,
            "cost_saving": 0.00,
            "horizontal_deploy": "No",
            "closing_days": None
        },
        {
            "ci_no": "UTIV-EN-R-25-0000-00-007",
            "title": "Setup Reduction in Injection Molding",
            "category": "Efficiency",
            "department": "Engineering",
            "process_area": "Injection Molding",
            "owner": "Michael Chen",
            "priority": "Low",
            "start_date": "2025-03-01",
            "due_date": "2025-06-30",
            "close_date": None,
            "status": "Pending",
            "progress": 20,
            "kpi_metric": "Setup Time (Minutes)",
            "before_value": 45.0,
            "target_value": 30.0,
            "after_value": None,
            "achievement_rate": None,
            "result": None,
            "verified": "No",
            "verified_by": None,
            "verified_date": None,
            "cost_saving": 0.00,
            "horizontal_deploy": "No",
            "closing_days": None
        },
        {
            "ci_no": "UTIV-EN-R-26-0000-00-008",
            "title": "Energy Consumption Reduction",
            "category": "Sustainability",
            "department": "Facilities",
            "process_area": "Factory Floor",
            "owner": "David Martinez",
            "priority": "Medium",
            "start_date": "2026-01-05",
            "due_date": "2026-03-31",
            "close_date": None,
            "status": "Running",
            "progress": 40,
            "kpi_metric": "Energy (kWh/Unit)",
            "before_value": 8.5,
            "target_value": 7.0,
            "after_value": None,
            "achievement_rate": None,
            "result": None,
            "verified": "No",
            "verified_by": None,
            "verified_date": None,
            "cost_saving": 0.00,
            "horizontal_deploy": "No",
            "closing_days": None
        }
    ]
    
    # Insert sample projects
    for project_data in demo_projects:
        project = CIProject(**project_data)
        db.add(project)
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Seeded {len(demo_projects)} demo projects",
        "count": len(demo_projects)
    }

def clear_all_data(db: Session):
    """
    Clear all CI project data (used when switching to production mode).
    WARNING: This is destructive - all projects will be deleted.
    """
    try:
        # Delete all CI projects
        db.query(CIProject).delete()
        db.commit()
        
        return {
            "status": "success",
            "message": "All CI project data cleared"
        }
    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": f"Failed to clear data: {str(e)}"
        }
