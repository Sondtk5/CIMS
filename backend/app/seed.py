from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.role import Role
from app.models.kpi_target import KPITarget
from app.models.ci_project import CIProject
from app.models.monthly_kpi_snapshot import MonthlyKPISnapshot
from app.models.admin_setting import AdminSetting
from app.core.security import get_password_hash
from datetime import datetime

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Roles if empty
        if db.query(Role).count() == 0:
            roles_data = [
                ("Administrator", "System administrator with full access"),
                ("TPM Manager", "TPM Manager responsible for CI projects"),
                ("Engineer", "Production engineer"),
                ("QA Inspector", "Quality assurance inspector"),
                ("Management", "Management and executive"),
                ("Auditor", "ISO lead auditor")
            ]
            for role_name, description in roles_data:
                r = Role(
                    name=role_name,
                    description=description,
                    is_active=True,
                    updated_by="System"
                )
                db.add(r)
            db.commit()

        # 2. Seed Users if empty
        if db.query(User).count() == 0:
            users_data = [
                ("admin", "admin@uti.com", "Administrator", "System Admin", "TPM"),
                ("manager", "manager@uti.com", "TPM Manager", "TPM Manager", "TPM"),
                ("engineer", "engineer@uti.com", "Engineer", "Senior Engineer", "Production"),
                ("qa", "qa@uti.com", "QA Inspector", "Quality Inspector", "Quality"),
                ("management", "management@uti.com", "Management", "Plant Director", "Executive"),
                ("auditor", "auditor@uti.com", "Auditor", "ISO Lead Auditor", "Quality Audit")
            ]
            for username, email, role, full_name, dept in users_data:
                u = User(
                    username=username,
                    email=email,
                    hashed_password=get_password_hash("password123"),
                    role=role,
                    full_name=full_name,
                    department=dept,
                    is_active=True
                )
                db.add(u)
            db.commit()

        # 3. Seed Admin Settings (CI Numbering) if empty
        if db.query(AdminSetting).count() == 0:
            ci_config = {
                "parts": [
                    {"name": "prefix", "value": "UTIV", "enabled": True, "auto_increment": False},
                    {"name": "department", "value": "EN", "enabled": True, "auto_increment": False},
                    {"name": "category", "value": "R", "enabled": True, "auto_increment": False},
                    {"name": "year", "value": "00", "enabled": True, "auto_increment": False},
                    {"name": "sequence", "value": "0000", "enabled": True, "auto_increment": False},
                    {"name": "version", "value": "00", "enabled": True, "auto_increment": False},
                    {"name": "counter", "value": "000", "enabled": True, "auto_increment": True}
                ],
                "separator": "-",
                "next_counter": 1,
                "last_updated": datetime.utcnow().isoformat()
            }
            admin_setting = AdminSetting(
                setting_key="ci_numbering_config",
                setting_value=ci_config,
                description="CI Project numbering convention configuration"
            )
            db.add(admin_setting)
            db.commit()

        # 4. Seed KPI Targets if empty
        if db.query(KPITarget).count() == 0:
            targets_data = [
                ("on_time_completion", "Improvement Project On-time Completion Rate", 95.0, "%", ">="),
                ("effectiveness_rate", "Improvement Effectiveness Rate", 90.0, "%", ">="),
                ("avg_closing_time", "Average Closing Time", 60.0, "Days", "<="),
                ("cost_saving", "Cost Saving", 50000.0, "USD", ">="),
                ("horizontal_deployment", "Horizontal Deployment", 3.0, "Projects", ">=")
            ]
            for key, name, val, unit, op in targets_data:
                t = KPITarget(
                    kpi_key=key,
                    kpi_name=name,
                    target_value=val,
                    unit=unit,
                    comparison_operator=op,
                    updated_by="System"
                )
                db.add(t)
            db.commit()

        # 5. Seed CI Projects if empty
        if db.query(CIProject).count() == 0:
            seed_projects = [
                {
                    "ci_no": "CI-26-001",
                    "title": "Stain 2 Defect Improvement",
                    "category": "Quality",
                    "department": "Quality",
                    "process_area": "Slit Coater",
                    "start_date": "2026-07-05",
                    "due_date": "2026-07-31",
                    "close_date": "2026-07-28",
                    "status": "Complete",
                    "priority": "High",
                    "owner": "Park Ji-sung",
                    "requester": "Lee Min-ho",
                    "kpi_metric": "Defect Rate (%)",
                    "before_value": 2.50,
                    "target_value": 0.20,
                    "after_value": 0.18,
                    "achievement_rate": 116.0,
                    "result": "PASS",
                    "verified": "Yes",
                    "verified_by": "QA Inspector Kim",
                    "verified_date": "2026-07-29",
                    "closing_days": 23,
                    "cost_saving": 12000.0,
                    "horizontal_deploy": "Yes",
                    "issue_description": "Stain 2 defects occurred intermittently on glass substrate after coating process.",
                    "current_status": "Defect rate at 2.50% causing yield loss.",
                    "target_description": "Reduce stain 2 defect rate to <= 0.20%.",
                    "expected_benefit": "Yield improvement and $12,000 annual saving.",
                    "related_process": "Slit Coater Line 1 & Line 2",
                    "define_stage": {"background": "Customer complaint on coating stain.", "scope": "Slit Coater 1", "team_members": "Park, Lee, Kim"},
                    "analyze_stage": {
                        "five_why": [
                            {"why": "Why is stain 2 defect high?", "answer": "Coating nozzle micro-clogging"},
                            {"why": "Why is nozzle clogging?", "answer": "Chemical residue drying during idle time"},
                            {"why": "Why is residue drying?", "answer": "Nozzle cap purge pressure insufficient"},
                            {"why": "Why is pressure insufficient?", "answer": "Purge line regulator setting decayed"},
                            {"why": "Why did setting decay?", "answer": "Lack of periodic PM calibration checklist"}
                        ],
                        "fishbone": {
                            "Machine": ["Nozzle cap pressure low", "Filter clogging"],
                            "Man": ["Operator cleaning procedure mismatch"],
                            "Material": ["Coating solvent viscosity variation"],
                            "Method": ["Purge frequency insufficient"]
                        }
                    }
                },
                {
                    "ci_no": "CI-26-002",
                    "title": "Takt Time Improvement",
                    "category": "Productivity",
                    "department": "Production",
                    "process_area": "Slit Coater",
                    "start_date": "2026-07-08",
                    "due_date": "2026-08-15",
                    "close_date": None,
                    "status": "Running",
                    "priority": "High",
                    "owner": "Kim Tae-hyung",
                    "requester": "Choi Woo-shik",
                    "kpi_metric": "UPH (pcs/hr)",
                    "before_value": 274.0,
                    "target_value": 443.0,
                    "after_value": 379.0,
                    "achievement_rate": 63.0,
                    "result": "-",
                    "verified": "No",
                    "cost_saving": 18500.0,
                    "horizontal_deploy": "Yes",
                    "issue_description": "Substrate loading cycle time bottlenecking overall line throughput.",
                    "current_status": "Current UPH is 274 pcs/hr.",
                    "target_description": "Increase UPH to >= 443 pcs/hr.",
                    "expected_benefit": "Increase monthly production output by 15%."
                },
                {
                    "ci_no": "CI-26-003",
                    "title": "Waviness Defect Improvement",
                    "category": "Quality",
                    "department": "Quality",
                    "process_area": "Wet Bench",
                    "start_date": "2026-07-10",
                    "due_date": "2026-08-20",
                    "close_date": None,
                    "status": "Running",
                    "priority": "Medium",
                    "owner": "Choi Jin-soo",
                    "requester": "Kang Daniel",
                    "kpi_metric": "Defect Rate (%)",
                    "before_value": 3.10,
                    "target_value": 0.00,
                    "after_value": 0.00,
                    "achievement_rate": 100.0,
                    "result": "PASS",
                    "verified": "Yes",
                    "cost_saving": 8800.0,
                    "horizontal_deploy": "No",
                    "issue_description": "Surface waviness defect observed during wet etching stage.",
                    "current_status": "Defect rate at 3.10%.",
                    "target_description": "Zero waviness defect rate."
                },
                {
                    "ci_no": "CI-26-004",
                    "title": "Reduce CPM Defect in IOX",
                    "category": "Quality",
                    "department": "Quality",
                    "process_area": "IOX",
                    "start_date": "2026-07-15",
                    "due_date": "2026-07-28",
                    "close_date": "2026-07-28",
                    "status": "Complete",
                    "priority": "High",
                    "owner": "Song Hye-kyo",
                    "requester": "Han So-hee",
                    "kpi_metric": "Defect Rate (%)",
                    "before_value": 12.00,
                    "target_value": 1.50,
                    "after_value": 1.85,
                    "achievement_rate": 92.0,
                    "result": "FAIL",
                    "verified": "Yes",
                    "closing_days": 13,
                    "cost_saving": 13000.0,
                    "horizontal_deploy": "Yes",
                    "issue_description": "CPM particle defect after chemical ion exchange process.",
                    "current_status": "Defect rate dropped from 12% to 1.85%.",
                    "target_description": "Reduce CPM defect to <= 1.50%."
                },
                {
                    "ci_no": "CI-26-005",
                    "title": "Chemical Usage Reduction",
                    "category": "Cost Saving",
                    "department": "TPM",
                    "process_area": "Overall",
                    "start_date": "2026-07-18",
                    "due_date": "2026-08-10",
                    "close_date": None,
                    "status": "Running",
                    "priority": "Medium",
                    "owner": "Jung Hae-in",
                    "requester": "Bae Suzy",
                    "kpi_metric": "Chemical Cost (USD/Month)",
                    "before_value": 9500.0,
                    "target_value": 7500.0,
                    "after_value": 7800.0,
                    "achievement_rate": 81.0,
                    "result": "-",
                    "verified": "No",
                    "cost_saving": 2000.0,
                    "horizontal_deploy": "No",
                    "issue_description": "Over-consumption of cleaning solvent during line flush.",
                    "current_status": "Monthly spend $9,500.",
                    "target_description": "Reduce monthly spend to <= $7,500."
                }
            ]

            # Generate 19 more projects for 24 total
            more_categories = ["Quality", "Productivity", "Cost Saving", "Safety / Environment", "Equipment"]
            more_depts = ["Slit Coater", "Wet Bench", "IOX", "Overall", "Maintenance", "Logistics"]
            
            for i in range(6, 25):
                cat = more_categories[i % len(more_categories)]
                dept = more_depts[i % len(more_depts)]
                is_complete = (i <= 18)
                
                seed_projects.append({
                    "ci_no": f"CI-26-{i:03d}",
                    "title": f"{dept} {cat} Optimization Phase {i-5}",
                    "category": cat,
                    "department": dept,
                    "process_area": dept,
                    "start_date": f"2026-06-0{i%9+1}",
                    "due_date": f"2026-07-2{i%9+1}",
                    "close_date": f"2026-07-2{i%9+1}" if is_complete else None,
                    "status": "Complete" if is_complete else "Running",
                    "priority": "High" if i % 2 == 0 else "Medium",
                    "owner": f"Engineer {i}",
                    "requester": f"Manager {i}",
                    "kpi_metric": "Defect Rate (%)" if cat == "Quality" else "Efficiency (%)",
                    "before_value": 5.0 + i,
                    "target_value": 1.0,
                    "after_value": 1.1 if is_complete else 2.5,
                    "achievement_rate": 95.0 if is_complete else 60.0,
                    "result": "PASS" if is_complete else "-",
                    "verified": "Yes" if is_complete else "No",
                    "closing_days": 20 + (i % 15) if is_complete else None,
                    "cost_saving": 1000.0 * (i % 5 + 1),
                    "horizontal_deploy": "Yes" if i % 4 == 0 else "No",
                    "issue_description": f"Operational optimization for {dept} {cat}.",
                    "current_status": "Targeting standard operating procedure alignment."
                })

            for proj_data in seed_projects:
                p = CIProject(**proj_data)
                db.add(p)

            db.commit()

        # 6. Seed Monthly KPI Snapshots for 2026 if empty
        if db.query(MonthlyKPISnapshot).count() == 0:
            snapshot_data = [
                (2026, 1, 92.0, 88.0, 42.0, 45000.0, 1),
                (2026, 2, 90.0, 85.0, 38.0, 48000.0, 2),
                (2026, 3, 95.0, 92.0, 35.0, 55000.0, 2),
                (2026, 4, 98.0, 94.0, 32.0, 58000.0, 3),
                (2026, 5, 94.0, 91.0, 40.0, 52000.0, 3),
                (2026, 6, 96.0, 93.0, 37.0, 61000.0, 4),
            ]
            for year, month, on_time, effectiveness, avg_days, cost_saving, horizontal in snapshot_data:
                snapshot = MonthlyKPISnapshot(
                    year=year,
                    month=month,
                    on_time_completion_rate=on_time,
                    effectiveness_rate=effectiveness,
                    avg_closing_days=avg_days,
                    cost_saving=cost_saving,
                    horizontal_deployment_count=horizontal,
                    total_projects_completed=10 + (month % 5),
                    total_projects_running=5 + (month % 3)
                )
                db.add(snapshot)
            db.commit()

        print("Database seeding completed successfully.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
