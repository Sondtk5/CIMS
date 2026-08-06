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
