"""
Seed data service for Demo mode - FULL DEMO DATA
Contains 133 sample CI projects: 20 for 2024, 45 for 2025, 68 for 2026.
All CI numbers follow format: UTIV-EN-R-YY-0000-00-###
"""
from sqlalchemy.orm import Session
from app.models.ci_project import CIProject
from datetime import datetime, timedelta
import random

def seed_demo_data(db: Session):
    """
    Load comprehensive sample CI project data for demo mode.
    Creates 133 realistic CI projects:
    - 2024: 20 projects (all Complete)
    - 2025: 45 projects (all Complete)
    - 2026: 68 projects (48 Complete + 15 Running + 5 Pending)
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
    
    # 2024: 20 projects (all Complete)
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
    
    # 2025: 45 projects (all Complete)
    projects_2025_data = [
        ("First Pass Yield Q1", "Coating Line B", "FPY (%)", 82.0, 90.0, 90.5, 18000, "Yes", 1),
        ("Q1 Quality", "Quality Control", "Defect Rate (%)", 3.5, 2.0, 1.95, 12000, "No", 1),
        ("Raw Material Cost Q1", "Supplier Mgmt", "Cost Reduction (%)", 12.5, 11.0, 10.95, 25000, "Yes", 1),
        ("Material Optimization Q1", "Warehouse", "Waste (%)", 5.2, 2.8, 2.75, 8500, "No", 1),
        ("Setup Reduction Q1", "Injection Molding", "Setup Time (min)", 45.0, 30.0, 29.5, 14000, "Yes", 1),
        ("Line Speed Q1", "Production Line", "Speed (Units/min)", 85.0, 95.0, 95.5, 11000, "No", 2),
        ("Production Throughput Q1", "Production Line", "Throughput (Units/hr)", 120.0, 140.0, 141.0, 22000, "Yes", 2),
        ("Cycle Time Q1", "Packaging", "Cycle Time (sec)", 28.0, 18.0, 17.5, 9500, "No", 2),
        ("Energy Q1", "Factory Floor", "Energy (kWh/Unit)", 7.8, 6.5, 6.45, 16000, "Yes", 2),
        ("Cooling System Q1", "Facilities", "Efficiency (%)", 68.0, 78.0, 78.5, 13000, "No", 2),
        ("Coating Q1", "Coating Line A", "Uniformity Score", 80.0, 88.0, 88.2, 19000, "Yes", 3),
        ("Color Variation Q1", "Coating Line B", "Variation (%)", 4.5, 2.0, 1.95, 10500, "No", 3),
        ("Scrap Reduction Q1", "Quality Control", "Scrap Rate (%)", 4.2, 2.0, 1.9, 11000, "Yes", 3),
        ("Sorting Accuracy Q1", "Quality Control", "Accuracy (%)", 92.0, 97.0, 97.2, 7500, "No", 3),
        ("Maintenance Q1", "Maintenance", "Efficiency (%)", 70.0, 82.0, 82.5, 28000, "Yes", 3),
        ("Preventive Maintenance Q1", "Maintenance", "MTBF (hours)", 200.0, 280.0, 285.0, 15000, "No", 4),
        ("Supplier Deliveries Q1", "Supplier Mgmt", "On-time (%)", 75.0, 95.0, 95.5, 8000, "Yes", 4),
        ("Return Reduction Q1", "Quality Control", "Return Rate (%)", 2.8, 1.5, 1.45, 15000, "Yes", 4),
        ("Employee Productivity Q1", "Operations", "Productivity (Units/day)", 950.0, 1100.0, 1105.0, 12000, "No", 4),
        ("Optimization Q1", "Production Line", "Efficiency (%)", 82.0, 90.0, 90.5, 21000, "Yes", 4),
        ("Defect Reduction Q2", "Quality Control", "Defect (%)", 3.8, 2.2, 2.15, 13000, "No", 5),
        ("Process Improvement Q2", "Production", "Cycle Time (min)", 32.0, 22.0, 21.5, 17000, "Yes", 5),
        ("Equipment Efficiency Q2", "Factory Floor", "Uptime (%)", 88.0, 95.0, 95.2, 19000, "No", 5),
        ("Waste Reduction Q2", "Operations", "Waste Rate (%)", 6.5, 3.0, 2.9, 24000, "Yes", 6),
        ("Safety Improvement Q2", "Safety", "Safety Score", 75.0, 88.0, 88.5, 5000, "No", 6),
        ("Cost Control Q2", "Finance", "Cost Per Unit", 125.0, 105.0, 104.5, 32000, "Yes", 6),
        ("Quality Audit Q2", "Quality Control", "Audit Score (%)", 82.0, 90.0, 90.2, 8000, "No", 6),
        ("Supplier Performance Q2", "Supplier Mgmt", "Performance Score", 78.0, 88.0, 88.5, 11000, "Yes", 7),
        ("Inventory Q2", "Warehouse", "Turnover", 6.5, 8.5, 8.7, 14000, "No", 7),
        ("Production Planning Q2", "Planning", "Efficiency (%)", 80.0, 90.0, 90.5, 16000, "Yes", 7),
        ("Quality System Q3", "Quality Control", "System Score", 85.0, 92.0, 92.5, 9000, "No", 8),
        ("Coating Process Q3", "Coating Line A", "Quality (%)", 86.0, 94.0, 94.5, 20000, "Yes", 8),
        ("Packaging Line Q3", "Packaging", "Efficiency (%)", 82.0, 92.0, 92.5, 15000, "No", 8),
        ("Material Cost Q3", "Supplier Mgmt", "Cost Reduction (%)", 10.0, 15.0, 15.5, 28000, "Yes", 9),
        ("Production Capacity Q3", "Production", "Capacity (Units/day)", 1250.0, 1400.0, 1420.0, 35000, "No", 9),
        ("Equipment Maintenance Q3", "Maintenance", "MTBF (hours)", 220.0, 300.0, 310.0, 18000, "Yes", 9),
        ("Quality Control Q3", "Quality Control", "Pass Rate (%)", 94.0, 97.0, 97.5, 12000, "No", 10),
        ("Process Optimization Q3", "Production", "Throughput (%)", 88.0, 95.0, 95.5, 22000, "Yes", 10),
        ("Supply Chain Q3", "Logistics", "Lead Time (days)", 35.0, 25.0, 24.5, 16000, "No", 10),
        ("Final Quality Q4", "Quality Control", "Final Score", 89.0, 95.0, 95.5, 14000, "Yes", 11),
        ("Year-End Efficiency", "Operations", "Overall Efficiency (%)", 85.0, 92.0, 92.5, 25000, "No", 12),
        ("Annual Cost Saving", "Finance", "Cost Saving ($)", 150000.0, 200000.0, 210000.0, 45000, "Yes", 12),
        ("Supplier Agreement", "Supplier Mgmt", "Agreement Rate (%)", 80.0, 95.0, 95.5, 10000, "No", 12),
        ("Customer Satisfaction", "Sales", "Satisfaction (%)", 87.0, 94.0, 94.5, 8000, "Yes", 12),
        ("Employee Training", "HR", "Training Hours", 800.0, 1200.0, 1250.0, 5000, "No", 12),
    ]
    for title, process, metric, before, target, after, cost, deploy, month in projects_2025_data:
        demo_projects.append(add_project(title, process, metric, before, target, after, cost, deploy, month, 2025))
        counter += 1
    
    # 2026: 68 projects (48 Complete + 15 Running + 5 Pending)
    projects_2026_complete = [
        ("Q1 Energy Reduction", "Factory Floor", "Energy (kWh/Unit)", 8.5, 7.0, 6.95, 18000, "Yes", 1, "Complete"),
        ("Q1 Quality Start", "Quality Control", "Defect Rate (%)", 3.2, 1.8, 1.75, 14000, "No", 1, "Complete"),
        ("Q1 Production Capacity", "Production Line", "Capacity (Units/day)", 1200.0, 1350.0, 1360.0, 32000, "Yes", 1, "Complete"),
        ("Q1 Inventory Opt", "Warehouse", "Inventory Turn", 8.0, 10.0, 10.2, 19000, "No", 1, "Complete"),
        ("Q1 Supply Chain", "Supplier Mgmt", "Lead Time (days)", 45.0, 30.0, 29.5, 12000, "Yes", 1, "Complete"),
        ("Q1 Vendor Quality", "Supplier Mgmt", "Quality Score", 75.0, 85.0, 85.2, 9000, "No", 2, "Complete"),
        ("Q1 Process Eff", "Production", "Efficiency (%)", 80.0, 90.0, 90.5, 22000, "Yes", 2, "Complete"),
        ("Q1 Quality System", "Quality Control", "System Score", 78.0, 88.0, 88.5, 16500, "No", 2, "Complete"),
        ("Q2 Maintenance", "Maintenance", "MTBF (hours)", 200.0, 280.0, 285.0, 25000, "Yes", 4, "Complete"),
        ("Q2 Equipment", "Factory Floor", "Uptime (%)", 92.0, 96.0, 96.2, 20000, "No", 4, "Complete"),
        ("Q2 Quality Audit", "Quality Control", "Audit Score (%)", 88.0, 95.0, 95.5, 11000, "Yes", 4, "Complete"),
        ("Q2 Coating Line", "Coating Line A", "Uniformity (%)", 85.0, 92.0, 92.5, 18000, "No", 4, "Complete"),
        ("Q2 Process Auto", "Production Line", "Automation (%)", 45.0, 65.0, 65.5, 28000, "Yes", 4, "Complete"),
        ("Q2 Control System", "IT", "System Uptime (%)", 94.0, 99.0, 99.2, 15000, "No", 5, "Complete"),
        ("Q2 Material Cost", "Supplier Mgmt", "Cost Per Unit", 120.0, 100.0, 99.5, 26000, "Yes", 5, "Complete"),
        ("Q2 Safety", "Safety", "Incident Rate", 5.0, 2.0, 1.8, 8000, "No", 5, "Complete"),
        ("Q2 Compliance", "Compliance", "Compliance Score (%)", 85.0, 95.0, 95.5, 12000, "Yes", 5, "Complete"),
        ("Q3 Efficiency", "Operations", "Overall Efficiency (%)", 82.0, 90.0, 90.5, 22000, "No", 7, "Complete"),
        ("Q3 Cost Saving", "Finance", "Cost Saving ($)", 180000.0, 220000.0, 230000.0, 50000, "Yes", 7, "Complete"),
        ("Q3 Production", "Production", "Throughput (Units/hr)", 140.0, 160.0, 165.0, 32000, "No", 7, "Complete"),
        ("Q3 Supplier", "Supplier Mgmt", "On-time Delivery (%)", 90.0, 98.0, 98.2, 14000, "Yes", 7, "Complete"),
        ("Q3 Customer", "Sales", "Satisfaction (%)", 88.0, 95.0, 95.5, 10000, "No", 8, "Complete"),
        ("Q3 HR Training", "HR", "Training Hours", 900.0, 1300.0, 1350.0, 6000, "Yes", 8, "Complete"),
        ("Q3 IT System", "IT", "System Availability (%)", 96.0, 99.0, 99.1, 9000, "No", 8, "Complete"),
        ("Q3 Waste", "Operations", "Waste Reduction (%)", 18.0, 28.0, 28.5, 31000, "Yes", 8, "Complete"),
        ("Q4 Planning", "Planning", "Planning Accuracy (%)", 82.0, 92.0, 92.5, 11000, "No", 10, "Complete"),
        ("Q4 Quality Final", "Quality Control", "Final Pass Rate (%)", 96.0, 98.0, 98.2, 13000, "Yes", 10, "Complete"),
        ("Q4 Cost Control", "Finance", "Cost Per Unit", 105.0, 90.0, 89.5, 35000, "No", 10, "Complete"),
        ("Q4 Supplier Perf", "Supplier Mgmt", "Performance Score", 88.0, 95.0, 95.5, 17000, "Yes", 10, "Complete"),
        ("Q4 Maintenance", "Maintenance", "Uptime (%)", 98.0, 99.0, 99.1, 16000, "No", 10, "Complete"),
        ("Q4 Safety Final", "Safety", "Safety Score", 95.0, 98.0, 98.2, 7000, "Yes", 11, "Complete"),
        ("Year-End Review", "Quality Control", "Overall Score (%)", 91.0, 96.0, 96.5, 21000, "No", 11, "Complete"),
        ("Final Efficiency", "Operations", "Efficiency (%)", 89.0, 96.0, 96.5, 28000, "Yes", 11, "Complete"),
        ("Year-End Cost", "Finance", "Cumulative Saving ($)", 250000.0, 300000.0, 320000.0, 60000, "No", 12, "Complete"),
        ("Sustainability", "Environment", "Carbon Reduction (tons)", 45.0, 35.0, 34.5, 22000, "Yes", 12, "Complete"),
        ("Digital Score", "IT", "Digital Maturity (%)", 70.0, 85.0, 85.5, 15000, "No", 12, "Complete"),
        ("Employee Dev", "HR", "Development Score", 78.0, 88.0, 88.5, 9000, "Yes", 12, "Complete"),
        ("Customer Retention", "Sales", "Retention Rate (%)", 92.0, 98.0, 98.2, 18000, "No", 12, "Complete"),
        ("Supply Chain Resilience", "Logistics", "Resilience Score", 75.0, 88.0, 88.5, 14000, "Yes", 12, "Complete"),
        ("Process Innovation", "R&D", "Innovation Index", 65.0, 80.0, 80.5, 19000, "No", 12, "Complete"),
        ("Quality Excellence", "Quality Control", "Excellence Score", 93.0, 98.0, 98.5, 16000, "Yes", 12, "Complete"),
        ("Operational Excellence", "Operations", "OE Score", 87.0, 95.0, 95.5, 25000, "No", 12, "Complete"),
        ("Financial Performance", "Finance", "ROI (%)", 18.0, 25.0, 25.5, 45000, "Yes", 12, "Complete"),
        ("Market Position", "Strategy", "Market Share (%)", 12.0, 15.0, 15.2, 32000, "No", 12, "Complete"),
        ("Compliance Final", "Compliance", "Compliance (%)", 98.0, 99.0, 99.2, 11000, "Yes", 12, "Complete"),
        ("Team Development", "HR", "Team Score", 82.0, 92.0, 92.5, 8000, "No", 12, "Complete"),
        ("Risk Management", "Risk", "Risk Score", 88.0, 95.0, 95.5, 12000, "Yes", 12, "Complete"),
        ("Strategic Goals", "Strategy", "Goal Achievement (%)", 92.0, 98.0, 98.2, 38000, "No", 12, "Complete"),
    ]
    for item in projects_2026_complete:
        title, process, metric, before, target, after, cost, deploy, month, status = item
        demo_projects.append(add_project(title, process, metric, before, target, after, cost, deploy, month, 2026, status))
        counter += 1
    
    # 2026: 15 Running projects
    projects_2026_running = [
        ("Maintenance Program Q1", "Maintenance", "MTBF (hours)", 180.0, 250.0, None, 0, "No", 1, "Running"),
        ("Equipment Upgrade Q1", "Factory Floor", "Uptime (%)", 92.0, 96.0, None, 0, "Yes", 1, "Running"),
        ("Quality System 2026", "Quality Control", "ISO Compliance (%)", 88.0, 95.0, None, 0, "No", 2, "Running"),
        ("Coating Optimization Q2", "Coating Line A", "Uniformity (%)", 85.0, 92.0, None, 0, "Yes", 2, "Running"),
        ("Process Automation Q2", "Production Line", "Automation (%)", 45.0, 65.0, None, 0, "Yes", 3, "Running"),
        ("Control System Q2", "IT", "System Uptime (%)", 94.0, 99.0, None, 0, "No", 3, "Running"),
        ("Supply Chain Q3", "Logistics", "Efficiency (%)", 75.0, 88.0, None, 0, "Yes", 5, "Running"),
        ("Manufacturing Q3", "Production", "Output (Units)", 1300.0, 1500.0, None, 0, "No", 5, "Running"),
        ("Quality Assurance Q3", "Quality Control", "Pass Rate (%)", 94.0, 98.0, None, 0, "Yes", 6, "Running"),
        ("HR Development Q3", "HR", "Training Score", 80.0, 92.0, None, 0, "No", 6, "Running"),
        ("IT Modernization Q4", "IT", "Digital Score (%)", 72.0, 88.0, None, 0, "Yes", 8, "Running"),
        ("Safety Enhancement Q4", "Safety", "Safety Index", 85.0, 95.0, None, 0, "No", 8, "Running"),
        ("Financial Planning Q4", "Finance", "Budget Efficiency (%)", 78.0, 90.0, None, 0, "Yes", 9, "Running"),
        ("Customer Focus Q4", "Sales", "Customer Index", 86.0, 95.0, None, 0, "No", 9, "Running"),
        ("Strategic Initiative Q4", "Strategy", "Initiative Score", 80.0, 92.0, None, 0, "Yes", 10, "Running"),
    ]
    for item in projects_2026_running:
        title, process, metric, before, target, after, cost, deploy, month, status = item
        demo_projects.append(add_project(title, process, metric, before, target, after, cost, deploy, month, 2026, status))
        counter += 1
    
    # 2026: 5 Pending projects
    projects_2026_pending = [
        ("Advanced Analytics Q2", "IT", "Analytics Score", 60.0, 85.0, None, 0, "No", 3, "Pending"),
        ("Innovation Lab Q3", "R&D", "Innovation Index", 65.0, 85.0, None, 0, "Yes", 6, "Pending"),
        ("Sustainability Initiative Q4", "Environment", "Sustainability Score", 70.0, 88.0, None, 0, "No", 9, "Pending"),
        ("Digital Transformation Q4", "IT", "Digital Maturity (%)", 65.0, 88.0, None, 0, "Yes", 9, "Pending"),
        ("Next Gen Process Q4", "Production", "Process Score", 72.0, 90.0, None, 0, "No", 10, "Pending"),
    ]
    for item in projects_2026_pending:
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
        "message": f"Seeded {len(demo_projects)} comprehensive demo projects (133 total: 2024=20, 2025=45, 2026=68)",
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
