"""
Seed data service for Demo mode.
Contains sample CI projects for demonstration purposes.
Full 12 months of data for 2024, 2025, 2026 with proper CI numbering.
"""
from sqlalchemy.orm import Session
from app.models.ci_project import CIProject
from datetime import datetime, timedelta
import random

def seed_demo_data(db: Session):
    """
    Load comprehensive sample CI project data for demo mode.
    Creates realistic CI projects for 12 months across 2024-2026 (36+ projects).
    CI numbering format: UTIV-EN-R-YY-0000-00-###
    """
    # Check if demo data already exists
    existing_count = db.query(CIProject).count()
    if existing_count > 0:
        # Already has data, skip seeding
        return {"status": "skipped", "message": "Data already exists"}
    
    demo_projects = []
    counter = 1
    
    # 2024 Projects - 1 per month + more in Q1/Q2
    months_2024 = [
        # Jan 2024
        {"month": 1, "title": "Reduce Slit Coater Defect Rate", "process": "Slit Coater", "metric": "Defect Rate (%)", "before": 8.5, "target": 4.0, "after": 4.2, "cost": 15000, "deploy": "Yes"},
        {"month": 1, "title": "Improve Line Efficiency Q1", "process": "Production Line", "metric": "Efficiency (%)", "before": 78.0, "target": 85.0, "after": 86.5, "cost": 8500, "deploy": "No"},
        # Feb 2024
        {"month": 2, "title": "Reduce Packaging Defects", "process": "Packaging", "metric": "Defect Rate (%)", "before": 5.2, "target": 2.5, "after": 2.8, "cost": 12000, "deploy": "Yes"},
        {"month": 2, "title": "Improve Coating Uniformity Machine A", "process": "Coating Line A", "metric": "Uniformity Score", "before": 75.0, "target": 85.0, "after": 86.5, "cost": 8500, "deploy": "No"},
        # Mar 2024
        {"month": 3, "title": "Optimize Die Cutting Setup", "process": "Die Cutting", "metric": "Setup Time (min)", "before": 35.0, "target": 20.0, "after": 18.5, "cost": 9000, "deploy": "Yes"},
        # Apr 2024
        {"month": 4, "title": "Reduce Packaging Line Downtime", "process": "Packaging", "metric": "Downtime (Hours/Month)", "before": 48.0, "target": 24.0, "after": 22.5, "cost": 45000, "deploy": "Yes"},
        # May 2024
        {"month": 5, "title": "Improve Coating Line B Quality", "process": "Coating Line B", "metric": "Quality Score", "before": 72.0, "target": 82.0, "after": 83.0, "cost": 11000, "deploy": "No"},
        # Jun 2024
        {"month": 6, "title": "Optimize Material Waste", "process": "Die Cutting", "metric": "Waste Rate (%)", "before": 6.8, "target": 3.5, "after": 3.8, "cost": 22000, "deploy": "No"},
        # Jul 2024
        {"month": 7, "title": "Reduce Energy Consumption Q3", "process": "Factory Floor", "metric": "Energy (kWh/Unit)", "before": 8.5, "target": 7.0, "after": 7.2, "cost": 18000, "deploy": "Yes"},
        # Aug 2024
        {"month": 8, "title": "Improve First Pass Yield", "process": "Coating Line B", "metric": "FPY (%)", "before": 80.0, "target": 88.0, "after": 89.0, "cost": 14000, "deploy": "Yes"},
        # Sep 2024
        {"month": 9, "title": "Reduce Maintenance Downtime", "process": "Production Line", "metric": "Downtime (Hours)", "before": 25.0, "target": 12.0, "after": 11.5, "cost": 35000, "deploy": "No"},
        # Oct 2024
        {"month": 10, "title": "Optimize Production Schedule", "process": "Scheduling", "metric": "Efficiency (%)", "before": 75.0, "target": 85.0, "after": 86.0, "cost": 16000, "deploy": "Yes"},
        # Nov 2024
        {"month": 11, "title": "Improve Supplier Quality Q4", "process": "Supplier Management", "metric": "Quality Score", "before": 70.0, "target": 80.0, "after": 81.0, "cost": 7000, "deploy": "No"},
        # Dec 2024
        {"month": 12, "title": "Year-End Quality Initiative", "process": "Quality Control", "metric": "Defect Rate (%)", "before": 4.5, "target": 2.5, "after": 2.6, "cost": 19000, "deploy": "Yes"},
    ]
    
    for item in months_2024:
        ci_no = f"UTIV-EN-R-24-0000-00-{str(counter).zfill(3)}"
        start_day = random.randint(1, 15)
        start_date = f"2024-{str(item['month']).zfill(2)}-{str(start_day).zfill(2)}"
        due_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=random.randint(45, 90))).strftime("%Y-%m-%d")
        close_date = (datetime.strptime(due_date, "%Y-%m-%d") - timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")
        closing_days = (datetime.strptime(close_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
        achievement_rate = round(((item['after'] - item['before']) / (item['target'] - item['before']) * 100), 1) if item['target'] != item['before'] else 100.0
        
        demo_projects.append({
            "ci_no": ci_no,
            "title": item['title'],
            "category": random.choice(["Quality", "Efficiency", "Cost Reduction", "Sustainability"]),
            "department": random.choice(["Engineering", "Operations", "Procurement"]),
            "process_area": item['process'],
            "owner": random.choice(["John Smith", "Mary Johnson", "Robert Lee", "Sarah Davis", "James Wilson", "Emily Brown", "Michael Chen", "David Martinez"]),
            "priority": random.choice(["High", "Medium", "Low"]),
            "start_date": start_date,
            "due_date": due_date,
            "close_date": close_date,
            "status": "Complete",
            "progress": 100,
            "kpi_metric": item['metric'],
            "before_value": item['before'],
            "target_value": item['target'],
            "after_value": item['after'],
            "achievement_rate": achievement_rate,
            "result": "PASS" if achievement_rate >= 90 else "PASS",
            "verified": "Yes",
            "verified_by": "QA Team",
            "verified_date": close_date,
            "cost_saving": item['cost'],
            "horizontal_deploy": item['deploy'],
            "closing_days": closing_days
        })
        counter += 1
    
    # 2025 Projects - 1-2 per month
    months_2025 = [
        {"month": 1, "title": "Improve First Pass Yield", "process": "Coating Line B", "metric": "FPY (%)", "before": 82.0, "target": 90.0, "after": 91.5, "cost": 18000, "deploy": "Yes"},
        {"month": 1, "title": "Quality Initiative 2025", "process": "Quality Control", "metric": "Defect Rate (%)", "before": 3.5, "target": 2.0, "after": 2.1, "cost": 12000, "deploy": "No"},
        {"month": 2, "title": "Reduce Raw Material Cost", "process": "Supplier Management", "metric": "Material Cost ($/Unit)", "before": 12.50, "target": 11.00, "after": 11.20, "cost": 25000, "deploy": "Yes"},
        {"month": 3, "title": "Setup Reduction Q1", "process": "Injection Molding", "metric": "Setup Time (min)", "before": 45.0, "target": 30.0, "after": 31.0, "cost": 14000, "deploy": "No"},
        {"month": 4, "title": "Improve Production Throughput", "process": "Production Line", "metric": "Throughput (Units/hr)", "before": 120.0, "target": 140.0, "after": 142.0, "cost": 22000, "deploy": "Yes"},
        {"month": 5, "title": "Reduce Energy Costs Q2", "process": "Factory Floor", "metric": "Energy (kWh/Unit)", "before": 7.8, "target": 6.5, "after": 6.7, "cost": 16000, "deploy": "Yes"},
        {"month": 6, "title": "Optimize Coating Process", "process": "Coating Line A", "metric": "Uniformity Score", "before": 80.0, "target": 88.0, "after": 89.0, "cost": 19000, "deploy": "No"},
        {"month": 7, "title": "Reduce Scrap Rate", "process": "Quality Control", "metric": "Scrap Rate (%)", "before": 4.2, "target": 2.0, "after": 2.3, "cost": 11000, "deploy": "Yes"},
        {"month": 8, "title": "Improve Maintenance Efficiency", "process": "Maintenance", "metric": "Efficiency (%)", "before": 70.0, "target": 82.0, "after": 83.0, "cost": 28000, "deploy": "Yes"},
        {"month": 9, "title": "Optimize Supplier Deliveries", "process": "Supplier Management", "metric": "On-time Delivery (%)", "before": 75.0, "target": 95.0, "after": 96.0, "cost": 8000, "deploy": "No"},
        {"month": 10, "title": "Reduce Customer Returns Q4", "process": "Quality Control", "metric": "Return Rate (%)", "before": 2.8, "target": 1.5, "after": 1.6, "cost": 15000, "deploy": "Yes"},
        {"month": 11, "title": "Improve Employee Productivity", "process": "Operations", "metric": "Productivity (Units/day)", "before": 950.0, "target": 1100.0, "after": 1105.0, "cost": 12000, "deploy": "No"},
        {"month": 12, "title": "Year-End Process Optimization", "process": "Production Line", "metric": "Efficiency (%)", "before": 82.0, "target": 90.0, "after": 91.0, "cost": 21000, "deploy": "Yes"},
    ]
    
    for item in months_2025:
        ci_no = f"UTIV-EN-R-25-0000-00-{str(counter).zfill(3)}"
        start_day = random.randint(1, 15)
        start_date = f"2025-{str(item['month']).zfill(2)}-{str(start_day).zfill(2)}"
        due_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=random.randint(45, 90))).strftime("%Y-%m-%d")
        close_date = (datetime.strptime(due_date, "%Y-%m-%d") - timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")
        closing_days = (datetime.strptime(close_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
        achievement_rate = round(((item['after'] - item['before']) / (item['target'] - item['before']) * 100), 1) if item['target'] != item['before'] else 100.0
        
        demo_projects.append({
            "ci_no": ci_no,
            "title": item['title'],
            "category": random.choice(["Quality", "Efficiency", "Cost Reduction", "Sustainability"]),
            "department": random.choice(["Engineering", "Operations", "Procurement"]),
            "process_area": item['process'],
            "owner": random.choice(["John Smith", "Mary Johnson", "Robert Lee", "Sarah Davis", "James Wilson", "Emily Brown", "Michael Chen", "David Martinez"]),
            "priority": random.choice(["High", "Medium", "Low"]),
            "start_date": start_date,
            "due_date": due_date,
            "close_date": close_date,
            "status": "Complete",
            "progress": 100,
            "kpi_metric": item['metric'],
            "before_value": item['before'],
            "target_value": item['target'],
            "after_value": item['after'],
            "achievement_rate": achievement_rate,
            "result": "PASS" if achievement_rate >= 90 else "PASS",
            "verified": "Yes",
            "verified_by": "QA Team",
            "verified_date": close_date,
            "cost_saving": item['cost'],
            "horizontal_deploy": item['deploy'],
            "closing_days": closing_days
        })
        counter += 1
    
    # 2026 Projects - Mix of Complete, Running, Pending
    months_2026 = [
        {"month": 1, "title": "Energy Consumption Reduction", "process": "Factory Floor", "metric": "Energy (kWh/Unit)", "before": 8.5, "target": 7.0, "after": 7.2, "cost": 18000, "deploy": "Yes", "status": "Complete"},
        {"month": 1, "title": "Q1 Quality Initiative", "process": "Quality Control", "metric": "Defect Rate (%)", "before": 3.2, "target": 1.8, "after": 1.9, "cost": 14000, "deploy": "No", "status": "Complete"},
        {"month": 2, "title": "Improve Production Capacity", "process": "Production Line", "metric": "Capacity (Units/day)", "before": 1200.0, "target": 1350.0, "after": 1360.0, "cost": 32000, "deploy": "Yes", "status": "Complete"},
        {"month": 3, "title": "Reduce Inventory Cost", "process": "Warehouse", "metric": "Inventory Turn (times/yr)", "before": 8.0, "target": 10.0, "after": 10.2, "cost": 19000, "deploy": "No", "status": "Complete"},
        {"month": 4, "title": "Optimize Supply Chain", "process": "Supplier Management", "metric": "Lead Time (days)", "before": 45.0, "target": 30.0, "after": 31.0, "cost": 12000, "deploy": "Yes", "status": "Complete"},
        {"month": 5, "title": "Improve Maintenance", "process": "Maintenance", "metric": "Mean Time Between Failures", "before": 180.0, "target": 250.0, "after": 260.0, "cost": 25000, "deploy": "No", "status": "Running"},
        {"month": 6, "title": "Quality System 2026", "process": "Quality Control", "metric": "ISO Compliance (%)", "before": 88.0, "target": 95.0, "after": None, "cost": 0, "deploy": "No", "status": "Running"},
        {"month": 7, "title": "Process Automation", "process": "Production Line", "metric": "Automation Level (%)", "before": 45.0, "target": 65.0, "after": None, "cost": 0, "deploy": "Yes", "status": "Running"},
        {"month": 8, "title": "Sustainability Initiative", "process": "Factory Floor", "metric": "Carbon Footprint (tons)", "before": 450.0, "target": 380.0, "after": None, "cost": 0, "deploy": "No", "status": "Pending"},
        {"month": 9, "title": "Digital Transformation", "process": "IT", "metric": "System Uptime (%)", "before": 94.0, "target": 99.0, "after": None, "cost": 0, "deploy": "Yes", "status": "Pending"},
        {"month": 10, "title": "Advanced Analytics Implementation", "process": "Quality Control", "metric": "Prediction Accuracy (%)", "before": 70.0, "target": 85.0, "after": None, "cost": 0, "deploy": "No", "status": "Pending"},
        {"month": 11, "title": "Team Capability Building", "process": "HR", "metric": "Training Hours/Person", "before": 20.0, "target": 40.0, "after": None, "cost": 0, "deploy": "No", "status": "Pending"},
    ]
    
    for item in months_2026:
        ci_no = f"UTIV-EN-R-26-0000-00-{str(counter).zfill(3)}"
        start_day = random.randint(1, 15)
        start_date = f"2026-{str(item['month']).zfill(2)}-{str(start_day).zfill(2)}"
        due_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=random.randint(45, 90))).strftime("%Y-%m-%d")
        
        if item['status'] == 'Complete':
            close_date = (datetime.strptime(due_date, "%Y-%m-%d") - timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")
            closing_days = (datetime.strptime(close_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
            achievement_rate = round(((item['after'] - item['before']) / (item['target'] - item['before']) * 100), 1) if item['target'] != item['before'] else 100.0
            result = "PASS" if achievement_rate >= 90 else "PASS"
        else:
            close_date = None
            closing_days = None
            achievement_rate = None
            result = None
        
        demo_projects.append({
            "ci_no": ci_no,
            "title": item['title'],
            "category": random.choice(["Quality", "Efficiency", "Cost Reduction", "Sustainability"]),
            "department": random.choice(["Engineering", "Operations", "Procurement", "IT", "HR"]),
            "process_area": item['process'],
            "owner": random.choice(["John Smith", "Mary Johnson", "Robert Lee", "Sarah Davis", "James Wilson", "Emily Brown", "Michael Chen", "David Martinez"]),
            "priority": random.choice(["High", "Medium", "Low"]),
            "start_date": start_date,
            "due_date": due_date,
            "close_date": close_date,
            "status": item['status'],
            "progress": 100 if item['status'] == 'Complete' else (75 if item['status'] == 'Running' else 25),
            "kpi_metric": item['metric'],
            "before_value": item['before'],
            "target_value": item['target'],
            "after_value": item['after'],
            "achievement_rate": achievement_rate,
            "result": result,
            "verified": "Yes" if item['status'] == 'Complete' else "No",
            "verified_by": "QA Team" if item['status'] == 'Complete' else None,
            "verified_date": close_date if item['status'] == 'Complete' else None,
            "cost_saving": item['cost'],
            "horizontal_deploy": item['deploy'],
            "closing_days": closing_days
        })
        counter += 1
    
    # Insert all sample projects
    for project_data in demo_projects:
        project = CIProject(**project_data)
        db.add(project)
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Seeded {len(demo_projects)} demo projects for 12 months of 2024-2026",
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
