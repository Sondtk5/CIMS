from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.role import Role
from app.models.kpi_target import KPITarget
from app.models.ci_project import CIProject
from app.models.monthly_kpi_snapshot import MonthlyKPISnapshot
from app.models.admin_setting import AdminSetting
from app.core.security import get_password_hash
from app.services.seed_data import seed_demo_data
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
                    {"name": "sequence", "value": "0001", "enabled": True, "auto_increment": False},
                    {"name": "version", "value": "02", "enabled": True, "auto_increment": False},
                    {"name": "counter", "value": "000", "enabled": True, "auto_increment": True}
                ],
                "separator": "-",
                "next_counter": 7,
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

        # 5. Seed CI Projects - Use comprehensive demo data (133 projects)
        seed_demo_data(db)

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
                    total_projects_completed=6,
                    total_projects_running=0
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
