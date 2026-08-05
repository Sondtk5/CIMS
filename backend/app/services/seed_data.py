"""
Seed data service for Demo mode - COMPREHENSIVE DEMO DATA
Contains 50+ sample CI projects with full 12 months for 2024-2026.
All CI numbers follow format: UTIV-EN-R-YY-0000-00-###
"""
from sqlalchemy.orm import Session
from app.models.ci_project import CIProject
from datetime import datetime, timedelta
import random

def seed_demo_data(db: Session):
    """
    Load comprehensive sample CI project data for demo mode.
    Creates 50+ realistic CI projects across 2024-2026 with:
    - 2024: 14 projects (all Complete)
    - 2025: 20 projects (all Complete)
    - 2026: 20 projects (mix of Complete/Running/Pending)
    CI numbering format: UTIV-EN-R-YY-0000-00-###
    """
    # Check if demo data already exists
    existing_count = db.query(CIProject).count()
    if existing_count > 0:
        return {"status": "skipped", "message": "Data already exists"}
    
    demo_projects = []
    counter = 1
    
    # 2024: 14 Complete projects
    projects_2024 = [
        {"month": 1, "title": "Reduce Slit Coater Defect Rate", "process": "Slit Coater", "metric": "Defect Rate (%)", "before": 8.5, "target": 4.0, "after": 3.9, "cost": 15000, "deploy": "Yes"},
        {"month": 1, "title": "Improve Line Efficiency Q1", "process": "Production Line", "metric": "Efficiency (%)", "before": 78.0, "target": 85.0, "after": 85.8, "cost": 8500, "deploy": "No"},
        {"month": 2, "title": "Reduce Packaging Defects", "process": "Packaging", "metric": "Defect Rate (%)", "before": 5.2, "target": 2.5, "after": 2.4, "cost": 12000, "deploy": "Yes"},
        {"month": 2, "title": "Improve Coating Uniformity", "process": "Coating Line A", "metric": "Uniformity Score", "before": 75.0, "target": 85.0, "after": 85.5, "cost": 8500, "deploy": "No"},
        {"month": 3, "title": "Optimize Die Cutting Setup", "process": "Die Cutting", "metric": "Setup Time (min)", "before": 35.0, "target": 20.0, "after": 19.8, "cost": 9000, "deploy": "Yes"},
        {"month": 4, "title": "Reduce Packaging Downtime", "process": "Packaging", "metric": "Downtime (Hours)", "before": 48.0, "target": 24.0, "after": 23.5, "cost": 45000, "deploy": "Yes"},
        {"month": 5, "title": "Improve Coating Line B Quality", "process": "Coating Line B", "metric": "Quality Score", "before": 72.0, "target": 82.0, "after": 82.5, "cost": 11000, "deploy": "No"},
        {"month": 6, "title": "Optimize Material Waste", "process": "Die Cutting", "metric": "Waste Rate (%)", "before": 6.8, "target": 3.5, "after": 3.4, "cost": 22000, "deploy": "No"},
        {"month": 7, "title": "Reduce Energy Consumption", "process": "Factory Floor", "metric": "Energy (kWh/Unit)", "before": 8.5, "target": 7.0, "after": 6.9, "cost": 18000, "deploy": "Yes"},
        {"month": 8, "title": "Improve First Pass Yield", "process": "Coating Line B", "metric": "FPY (%)", "before": 80.0, "target": 88.0, "after": 88.5, "cost": 14000, "deploy": "Yes"},
        {"month": 9, "title": "Reduce Maintenance Downtime", "process": "Production Line", "metric": "Downtime (Hours)", "before": 25.0, "target": 12.0, "after": 11.8, "cost": 35000, "deploy": "No"},
        {"month": 10, "title": "Optimize Production Schedule", "process": "Scheduling", "metric": "Efficiency (%)", "before": 75.0, "target": 85.0, "after": 85.2, "cost": 16000, "deploy": "Yes"},
        {"month": 11, "title": "Improve Supplier Quality", "process": "Supplier Management", "metric": "Quality Score", "before": 70.0, "target": 80.0, "after": 80.5, "cost": 7000, "deploy": "No"},
        {"month": 12, "title": "Year-End Quality Initiative", "process": "Quality Control", "metric": "Defect Rate (%)", "before": 4.5, "target": 2.5, "after": 2.4, "cost": 19000, "deploy": "Yes"},
    ]
    
    for item in projects_2024:
        _create_project(item, counter, 2024, demo_projects)
        counter += 1
    
    # 2025: 20 Complete projects
    projects_2025 = [
        {"month": 1, "title": "Improve First Pass Yield", "process": "Coating Line B", "metric": "FPY (%)", "before": 82.0, "target": 90.0, "after": 90.5, "cost": 18000, "deploy": "Yes"},
        {"month": 1, "title": "Q1 Quality Initiative", "process": "Quality Control", "metric": "Defect Rate (%)", "before": 3.5, "target": 2.0, "after": 1.95, "cost": 12000, "deploy": "No"},
        {"month": 2, "title": "Reduce Raw Material Cost", "process": "Supplier Management", "metric": "Cost Reduction (%)", "before": 12.50, "target": 11.00, "after": 10.95, "cost": 25000, "deploy": "Yes"},
        {"month": 2, "title": "Material Optimization", "process": "Warehouse", "metric": "Waste (%)", "before": 5.2, "target": 2.8, "after": 2.75, "cost": 8500, "deploy": "No"},
        {"month": 3, "title": "Setup Reduction Q1", "process": "Injection Molding", "metric": "Setup Time (min)", "before": 45.0, "target": 30.0, "after": 29.5, "cost": 14000, "deploy": "Yes"},
        {"month": 3, "title": "Improve Line Speed", "process": "Production Line", "metric": "Speed (Units/min)", "before": 85.0, "target": 95.0, "after": 95.5, "cost": 11000, "deploy": "No"},
        {"month": 4, "title": "Production Throughput", "process": "Production Line", "metric": "Throughput (Units/hr)", "before": 120.0, "target": 140.0, "after": 141.0, "cost": 22000, "deploy": "Yes"},
        {"month": 4, "title": "Reduce Cycle Time", "process": "Packaging", "metric": "Cycle Time (sec)", "before": 28.0, "target": 18.0, "after": 17.5, "cost": 9500, "deploy": "No"},
        {"month": 5, "title": "Energy Optimization", "process": "Factory Floor", "metric": "Energy (kWh/Unit)", "before": 7.8, "target": 6.5, "after": 6.45, "cost": 16000, "deploy": "Yes"},
        {"month": 5, "title": "Cooling System Efficiency", "process": "Facilities", "metric": "Efficiency (%)", "before": 68.0, "target": 78.0, "after": 78.5, "cost": 13000, "deploy": "No"},
        {"month": 6, "title": "Coating Process Optimization", "process": "Coating Line A", "metric": "Uniformity Score", "before": 80.0, "target": 88.0, "after": 88.2, "cost": 19000, "deploy": "Yes"},
        {"month": 6, "title": "Reduce Color Variations", "process": "Coating Line B", "metric": "Variation (%)", "before": 4.5, "target": 2.0, "after": 1.95, "cost": 10500, "deploy": "No"},
        {"month": 7, "title": "Scrap Rate Reduction", "process": "Quality Control", "metric": "Scrap Rate (%)", "before": 4.2, "target": 2.0, "after": 1.9, "cost": 11000, "deploy": "Yes"},
        {"month": 7, "title": "Improve Sorting Accuracy", "process": "Quality Control", "metric": "Accuracy (%)", "before": 92.0, "target": 97.0, "after": 97.2, "cost": 7500, "deploy": "No"},
        {"month": 8, "title": "Maintenance Efficiency", "process": "Maintenance", "metric": "Efficiency (%)", "before": 70.0, "target": 82.0, "after": 82.5, "cost": 28000, "deploy": "Yes"},
        {"month": 8, "title": "Preventive Maintenance", "process": "Maintenance", "metric": "MTBF (hours)", "before": 200.0, "target": 280.0, "after": 285.0, "cost": 15000, "deploy": "No"},
        {"month": 9, "title": "Supplier Deliveries", "process": "Supplier Management", "metric": "On-time (%)", "before": 75.0, "target": 95.0, "after": 95.5, "cost": 8000, "deploy": "Yes"},
        {"month": 10, "title": "Customer Return Reduction", "process": "Quality Control", "metric": "Return Rate (%)", "before": 2.8, "target": 1.5, "after": 1.45, "cost": 15000, "deploy": "Yes"},
        {"month": 11, "title": "Employee Productivity", "process": "Operations", "metric": "Productivity (Units/day)", "before": 950.0, "target": 1100.0, "after": 1105.0, "cost": 12000, "deploy": "No"},
        {"month": 12, "title": "Year-End Optimization", "process": "Production Line", "metric": "Efficiency (%)", "before": 82.0, "target": 90.0, "after": 90.5, "cost": 21000, "deploy": "Yes"},
    ]
    
    for item in projects_2025:
        _create_project(item, counter, 2025, demo_projects)
        counter += 1
    
    # 2026: 20 projects (12 Complete + 6 Running + 2 Pending)
    projects_2026 = [
        {"month": 1, "title": "Energy Reduction", "process": "Factory Floor", "metric": "Energy (kWh/Unit)", "before": 8.5, "target": 7.0, "after": 6.95, "cost": 18000, "deploy": "Yes", "status": "Complete"},
        {"month": 1, "title": "Q1 Quality", "process": "Quality Control", "metric": "Defect Rate (%)", "before": 3.2, "target": 1.8, "after": 1.75, "cost": 14000, "deploy": "No", "status": "Complete"},
        {"month": 2, "title": "Production Capacity", "process": "Production Line", "metric": "Capacity (Units/day)", "before": 1200.0, "target": 1350.0, "after": 1360.0, "cost": 32000, "deploy": "Yes", "status": "Complete"},
        {"month": 2, "title": "Inventory Optimization", "process": "Warehouse", "metric": "Inventory Turn (times/yr)", "before": 8.0, "target": 10.0, "after": 10.2, "cost": 19000, "deploy": "No", "status": "Complete"},
        {"month": 3, "title": "Supply Chain", "process": "Supplier Management", "metric": "Lead Time (days)", "before": 45.0, "target": 30.0, "after": 29.5, "cost": 12000, "deploy": "Yes", "status": "Complete"},
        {"month": 3, "title": "Vendor Quality", "process": "Supplier Management", "metric": "Quality Score", "before": 75.0, "target": 85.0, "after": 85.2, "cost": 9000, "deploy": "No", "status": "Complete"},
        {"month": 4, "title": "Process Efficiency", "process": "Production", "metric": "Efficiency (%)", "before": 80.0, "target": 90.0, "after": 90.5, "cost": 22000, "deploy": "Yes", "status": "Complete"},
        {"month": 4, "title": "Quality System", "process": "Quality Control", "metric": "System Score", "before": 78.0, "target": 88.0, "after": 88.5, "cost": 16500, "deploy": "No", "status": "Complete"},
        {"month": 5, "title": "Maintenance Program", "process": "Maintenance", "metric": "MTBF (hours)", "before": 180.0, "target": 250.0, "after": None, "cost": 25000, "deploy": "No", "status": "Running"},
        {"month": 5, "title": "Equipment Upgrade", "process": "Factory Floor", "metric": "Uptime (%)", "before": 92.0, "target": 96.0, "after": None, "cost": 0, "deploy": "Yes", "status": "Running"},
        {"month": 6, "title": "Quality System 2026", "process": "Quality Control", "metric": "ISO Compliance (%)", "before": 88.0, "target": 95.0, "after": None, "cost": 0, "deploy": "No", "status": "Running"},
        {"month": 6, "title": "Coating Optimization", "process": "Coating Line A", "metric": "Uniformity (%)", "before": 85.0, "target": 92.0, "after": None, "cost": 0, "deploy": "Yes", "status": "Running"},
        {"month": 7, "title": "Process Automation", "process": "Production Line", "metric": "Automation Level (%)", "before": 45.0, "target": 65.0, "after": None, "cost": 0, "deploy": "Yes", "status": "Running"},
        {"month": 7, "title": "Control System", "process": "IT", "metric": "System Uptime (%)", "before": 94.0, "target": 99.0, "after": None, "cost": 0, "deploy": "No", "status": "Running"},
        {"month": 8, "title": "Sustainability", "process": "Factory Floor", "metric": "Carbon Footprint (tons)", "before": 450.0, "target": 380.0, "after": None, "cost": 0, "deploy": "No", "status": "Pending"},
        {"month": 8, "title": "Waste Reduction", "process": "Operations", "metric": "Waste Reduction (%)", "before": 15.0, "target": 25.0, "after": None, "cost": 0, "deploy": "Yes", "status": "Pending"},
        {"month": 9, "title": "Digital Transformation", "process": "IT", "metric": "Digital Score (%)", "before": 60.0, "target": 85.0, "after": None, "cost": 0, "deploy": "No", "status": "Pending"},
        {"month": 9, "title": "Analytics Platform", "process": "Quality Control", "metric": "Prediction Accuracy (%)", "before": 70.0, "target": 85.0, "after": None, "cost": 0, "deploy": "Yes", "status": "Pending"},
        {"month": 10, "title": "Training Program", "process": "HR", "metric": "Training Hours/Person", "before": 20.0, "target": 40.0, "after": None, "cost": 0, "deploy": "No", "status": "Pending"},
        {"month": 10, "title": "Skills Development", "process": "HR", "metric": "Certification Rate (%)", "before": 45.0, "target": 70.0, "after": None, "cost": 0, "deploy": "Yes", "status": "Pending"},
    ]
    
    for item in projects_2026:
        _create_project(item, counter, 2026, demo_projects, item.get("status", "Complete"))
        counter += 1
    
    # Insert all projects
    for project_data in demo_projects:
        project = CIProject(**project_data)
        db.add(project)
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Seeded {len(demo_projects)} comprehensive demo projects",
        "count": len(demo_projects)
    }

def _create_project(item, counter, year, projects_list, status="Complete"):
    """Helper to create a project dict"""
    ci_no = f"UTIV-EN-R-{str(year)[-2:]}-0000-00-{str(counter).zfill(3)}"
    start_day = random.randint(1, 15)
    start_date = f"{year}-{str(item['month']).zfill(2)}-{str(start_day).zfill(2)}"
    due_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=random.randint(45, 90))).strftime("%Y-%m-%d")
    
    if status == "Complete":
        close_date = (datetime.strptime(due_date, "%Y-%m-%d") - timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")
        closing_days = (datetime.strptime(close_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
        achievement_rate = round(((item['after'] - item['before']) / (item['target'] - item['before']) * 100), 1) if item['target'] != item['before'] else 100.0
        result = "PASS"
    else:
        close_date = None
        closing_days = None
        achievement_rate = None
        result = None
    
    projects_list.append({
        "ci_no": ci_no,
        "title": item['title'],
        "category": random.choice(["Quality", "Efficiency", "Cost Reduction", "Sustainability"]),
        "department": random.choice(["Engineering", "Operations", "Procurement", "IT", "HR", "Facilities"]),
        "process_area": item['process'],
        "owner": random.choice(["John Smith", "Mary Johnson", "Robert Lee", "Sarah Davis", "James Wilson", "Emily Brown", "Michael Chen", "David Martinez", "Lisa Wong", "Tom Anderson"]),
        "priority": random.choice(["High", "Medium", "Low"]),
        "start_date": start_date,
        "due_date": due_date,
        "close_date": close_date,
        "status": status,
        "progress": 100 if status == "Complete" else (75 if status == "Running" else 25),
        "kpi_metric": item['metric'],
        "before_value": item['before'],
        "target_value": item['target'],
        "after_value": item['after'],
        "achievement_rate": achievement_rate,
        "result": result,
        "verified": "Yes" if status == "Complete" else "No",
        "verified_by": "QA Team" if status == "Complete" else None,
        "verified_date": close_date if status == "Complete" else None,
        "cost_saving": item['cost'],
        "horizontal_deploy": item['deploy'],
        "closing_days": closing_days
    })

def clear_all_data(db: Session):
    """Clear all CI project data"""
    try:
        db.query(CIProject).delete()
        db.commit()
        return {"status": "success", "message": "All CI project data cleared"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": f"Failed to clear data: {str(e)}"}
