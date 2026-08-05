"""
Seed data service for Demo mode - FULL DEMO DATA
Contains 60 sample CI projects: 20 for each year (2024, 2025, 2026).
All CI numbers follow format: UTIV-EN-R-YY-0000-00-###
"""
from sqlalchemy.orm import Session
from app.models.ci_project import CIProject
from datetime import datetime, timedelta
import random

def seed_demo_data(db: Session):
    """
    Load comprehensive sample CI project data for demo mode.
    Creates 60 realistic CI projects across 2024-2026 with:
    - 2024: 20 projects (all Complete)
    - 2025: 20 projects (all Complete)
    - 2026: 20 projects (14 Complete + 4 Running + 2 Pending)
    CI numbering format: UTIV-EN-R-YY-0000-00-###
    """
    # Check if demo data already exists
    existing_count = db.query(CIProject).count()
    if existing_count > 0:
        return {"status": "skipped", "message": "Data already exists"}
    
    demo_projects = []
    counter = 1
    
    # Helper function to create complete/running/pending projects
    def add_project(title, process, metric, before, target, after, cost, deploy, month, year, status="Complete"):
        ci_no = f"UTIV-EN-R-{str(year)[-2:]}-0000-00-{str(counter).zfill(3)}"
        start_day = random.randint(1, 15)
        start_date = f"{year}-{str(month).zfill(2)}-{str(start_day).zfill(2)}"
        due_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=random.randint(45, 90))).strftime("%Y-%m-%d")
        
        if status == "Complete":
            close_date = (datetime.strptime(due_date, "%Y-%m-%d") - timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")
            closing_days = (datetime.strptime(close_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
            achievement_rate = round(((after - before) / (target - before) * 100), 1) if target != before else 100.0
            result = "PASS"
        else:
            close_date = None
            closing_days = None
            achievement_rate = None
            result = None
        
        return {
            "ci_no": ci_no,
            "title": title,
            "category": random.choice(["Quality", "Efficiency", "Cost Reduction", "Sustainability"]),
            "department": random.choice(["Engineering", "Operations", "Procurement", "IT", "HR", "Facilities"]),
            "process_area": process,
            "owner": random.choice(["John Smith", "Mary Johnson", "Robert Lee", "Sarah Davis", "James Wilson", "Emily Brown", "Michael Chen", "David Martinez", "Lisa Wong", "Tom Anderson"]),
            "priority": random.choice(["High", "Medium", "Low"]),
            "start_date": start_date,
            "due_date": due_date,
            "close_date": close_date,
            "status": status,
            "progress": 100 if status == "Complete" else (75 if status == "Running" else 25),
            "kpi_metric": metric,
            "before_value": before,
            "target_value": target,
            "after_value": after,
            "achievement_rate": achievement_rate,
            "result": result,
            "verified": "Yes" if status == "Complete" else "No",
            "verified_by": "QA Team" if status == "Complete" else None,
            "verified_date": close_date if status == "Complete" else None,
            "cost_saving": cost,
            "horizontal_deploy": deploy,
            "closing_days": closing_days
        }
    
    # 2024: 20 projects
    projects_2024_data = [
        ("Reduce Slit Coater Defect", "Slit Coater", "Defect (%)", 8.5, 4.0, 3.9, 15000, "Yes", 1),
        ("Improve Line Efficiency", "Production Line", "Efficiency (%)", 78.0, 85.0, 85.8, 8500, "No", 1),
        ("Reduce Packaging Defects", "Packaging", "Defect (%)", 5.2, 2.5, 2.4, 12000, "Yes", 2),
        ("Coating Uniformity", "Coating Line A", "Uniformity Score", 75.0, 85.0, 85.5, 8500, "No", 2),
        ("Optimize Die Cutting", "Die Cutting", "Setup Time (min)", 35.0, 20.0, 19.8, 9000, "Yes", 3),
        ("Improve Sorting Speed", "Quality Control", "Speed (Units/min)", 120.0, 140.0, 142.0, 7500, "No", 3),
        ("Reduce Packaging Downtime", "Packaging", "Downtime (Hours)", 48.0, 24.0, 23.5, 45000, "Yes", 4),
        ("Reduce Cycle Time", "Packaging", "Cycle Time (sec)", 28.0, 18.0, 17.5, 9500, "No", 4),
        ("Improve Coating Line B", "Coating Line B", "Quality Score", 72.0, 82.0, 82.5, 11000, "Yes", 5),
        ("Reduce Color Variations", "Coating Line B", "Variation (%)", 4.5, 2.0, 1.95, 10500, "No", 5),
        ("Optimize Material Waste", "Die Cutting", "Waste Rate (%)", 6.8, 3.5, 3.4, 22000, "Yes", 6),
        ("Improve Inventory", "Warehouse", "Turnover (times/yr)", 5.0, 7.0, 7.2, 6500, "No", 6),
        ("Reduce Energy", "Factory Floor", "Energy (kWh/Unit)", 8.5, 7.0, 6.9, 18000, "Yes", 7),
        ("Improve Cooling", "Facilities", "Efficiency (%)", 68.0, 78.0, 78.5, 13000, "No", 7),
        ("First Pass Yield", "Coating Line B", "FPY (%)", 80.0, 88.0, 88.5, 14000, "Yes", 8),
        ("Scrap Rate", "Quality Control", "Scrap Rate (%)", 4.2, 2.0, 1.9, 11000, "No", 8),
        ("Maintenance Downtime", "Production Line", "Downtime (Hours)", 25.0, 12.0, 11.8, 35000, "Yes", 9),
        ("Production Schedule", "Scheduling", "Efficiency (%)", 75.0, 85.0, 85.2, 16000, "Yes", 10),
        ("Supplier Quality", "Supplier Mgmt", "Quality Score", 70.0, 80.0, 80.5, 7000, "No", 11),
        ("Year-End Quality", "Quality Control", "Defect Rate (%)", 4.5, 2.5, 2.4, 19000, "Yes", 12),
    ]
    for title, process, metric, before, target, after, cost, deploy, month in projects_2024_data:
        demo_projects.append(add_project(title, process, metric, before, target, after, cost, deploy, month, 2024))
        counter += 1
    
    # 2025: 20 projects
    projects_2025_data = [
        ("First Pass Yield 2025", "Coating Line B", "FPY (%)", 82.0, 90.0, 90.5, 18000, "Yes", 1),
        ("Q1 Quality", "Quality Control", "Defect Rate (%)", 3.5, 2.0, 1.95, 12000, "No", 1),
        ("Raw Material Cost", "Supplier Mgmt", "Cost Reduction (%)", 12.5, 11.0, 10.95, 25000, "Yes", 2),
        ("Material Optimization", "Warehouse", "Waste (%)", 5.2, 2.8, 2.75, 8500, "No", 2),
        ("Setup Reduction", "Injection Molding", "Setup Time (min)", 45.0, 30.0, 29.5, 14000, "Yes", 3),
        ("Line Speed Improvement", "Production Line", "Speed (Units/min)", 85.0, 95.0, 95.5, 11000, "No", 3),
        ("Production Throughput", "Production Line", "Throughput (Units/hr)", 120.0, 140.0, 141.0, 22000, "Yes", 4),
        ("Reduce Cycle Time Q2", "Packaging", "Cycle Time (sec)", 28.0, 18.0, 17.5, 9500, "No", 4),
        ("Energy Optimization", "Factory Floor", "Energy (kWh/Unit)", 7.8, 6.5, 6.45, 16000, "Yes", 5),
        ("Cooling System", "Facilities", "Efficiency (%)", 68.0, 78.0, 78.5, 13000, "No", 5),
        ("Coating Optimization", "Coating Line A", "Uniformity Score", 80.0, 88.0, 88.2, 19000, "Yes", 6),
        ("Color Variation Q2", "Coating Line B", "Variation (%)", 4.5, 2.0, 1.95, 10500, "No", 6),
        ("Scrap Reduction", "Quality Control", "Scrap Rate (%)", 4.2, 2.0, 1.9, 11000, "Yes", 7),
        ("Sorting Accuracy", "Quality Control", "Accuracy (%)", 92.0, 97.0, 97.2, 7500, "No", 7),
        ("Maintenance Efficiency", "Maintenance", "Efficiency (%)", 70.0, 82.0, 82.5, 28000, "Yes", 8),
        ("Preventive Maintenance", "Maintenance", "MTBF (hours)", 200.0, 280.0, 285.0, 15000, "No", 8),
        ("Supplier Deliveries", "Supplier Mgmt", "On-time (%)", 75.0, 95.0, 95.5, 8000, "Yes", 9),
        ("Return Reduction", "Quality Control", "Return Rate (%)", 2.8, 1.5, 1.45, 15000, "Yes", 10),
        ("Employee Productivity", "Operations", "Productivity (Units/day)", 950.0, 1100.0, 1105.0, 12000, "No", 11),
        ("Year-End Optimization", "Production Line", "Efficiency (%)", 82.0, 90.0, 90.5, 21000, "Yes", 12),
    ]
    for title, process, metric, before, target, after, cost, deploy, month in projects_2025_data:
        demo_projects.append(add_project(title, process, metric, before, target, after, cost, deploy, month, 2025))
        counter += 1
    
    # 2026: 20 projects (14 Complete + 4 Running + 2 Pending)
    projects_2026_data = [
        ("Energy Reduction 2026", "Factory Floor", "Energy (kWh/Unit)", 8.5, 7.0, 6.95, 18000, "Yes", 1, "Complete"),
        ("Q1 Quality 2026", "Quality Control", "Defect Rate (%)", 3.2, 1.8, 1.75, 14000, "No", 1, "Complete"),
        ("Production Capacity", "Production Line", "Capacity (Units/day)", 1200.0, 1350.0, 1360.0, 32000, "Yes", 2, "Complete"),
        ("Inventory Optimization", "Warehouse", "Inventory Turn", 8.0, 10.0, 10.2, 19000, "No", 2, "Complete"),
        ("Supply Chain", "Supplier Mgmt", "Lead Time (days)", 45.0, 30.0, 29.5, 12000, "Yes", 3, "Complete"),
        ("Vendor Quality", "Supplier Mgmt", "Quality Score", 75.0, 85.0, 85.2, 9000, "No", 3, "Complete"),
        ("Process Efficiency", "Production", "Efficiency (%)", 80.0, 90.0, 90.5, 22000, "Yes", 4, "Complete"),
        ("Quality System", "Quality Control", "System Score", 78.0, 88.0, 88.5, 16500, "No", 4, "Complete"),
        ("Maintenance Program", "Maintenance", "MTBF (hours)", 180.0, 250.0, None, 25000, "No", 5, "Running"),
        ("Equipment Upgrade", "Factory Floor", "Uptime (%)", 92.0, 96.0, None, 0, "Yes", 5, "Running"),
        ("Quality System 2026", "Quality Control", "ISO Compliance (%)", 88.0, 95.0, None, 0, "No", 6, "Running"),
        ("Coating Optimization", "Coating Line A", "Uniformity (%)", 85.0, 92.0, None, 0, "Yes", 6, "Running"),
        ("Process Automation", "Production Line", "Automation (%)", 45.0, 65.0, None, 0, "Yes", 7, "Running"),
        ("Control System", "IT", "System Uptime (%)", 94.0, 99.0, None, 0, "No", 7, "Running"),
        ("Sustainability Q3", "Factory Floor", "Carbon (tons)", 450.0, 380.0, None, 0, "No", 8, "Pending"),
        ("Waste Reduction Q3", "Operations", "Waste Reduction (%)", 15.0, 25.0, None, 0, "Yes", 8, "Pending"),
        ("Digital Transform", "IT", "Digital Score (%)", 60.0, 85.0, None, 0, "No", 9, "Pending"),
        ("Analytics Platform", "Quality Control", "Accuracy (%)", 70.0, 85.0, None, 0, "Yes", 9, "Pending"),
        ("Training Program", "HR", "Training Hours/Person", 20.0, 40.0, None, 0, "No", 10, "Pending"),
        ("Skills Development", "HR", "Certification Rate (%)", 45.0, 70.0, None, 0, "Yes", 10, "Pending"),
    ]
    for item in projects_2026_data:
        title, process, metric, before, target, after, cost, deploy, month, status = item
        demo_projects.append(add_project(title, process, metric, before, target, after, cost, deploy, month, 2026, status))
        counter += 1
    
    # Insert all projects
    for project_data in demo_projects:
        project = CIProject(**project_data)
        db.add(project)
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Seeded {len(demo_projects)} comprehensive demo projects (60 total: 20 per year)",
        "count": len(demo_projects)
    }

def clear_all_data(db: Session):
    """Clear all CI project data"""
    try:
        db.query(CIProject).delete()
        db.commit()
        return {"status": "success", "message": "All CI project data cleared"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": f"Failed to clear data: {str(e)}"}
