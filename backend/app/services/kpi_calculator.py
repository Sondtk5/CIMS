from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.ci_project import CIProject
from app.models.kpi_target import KPITarget
from app.models.monthly_kpi_snapshot import MonthlyKPISnapshot
from datetime import datetime

def calculate_kpis(db: Session, year: int = None, mode: str = "PRODUCTION"):
    """
    Calculate KPIs with REAL data from CI projects ONLY.
    Monthly trends calculated from close_date of completed projects.
    If year=None: aggregate ALL projects from all years (All Years mode)
    If year specified: filter to that specific year
    mode: Filter by DEMO or PRODUCTION
    NO sample data, NO snapshots - fully dynamic.
    """
    year_for_display = year if year is not None else datetime.now().year
    
    # Fetch KPI Targets from DB
    targets_db = db.query(KPITarget).all()
    targets_map = {t.kpi_key: t for t in targets_db}

    # Helper target values with fallback defaults
    target_on_time = targets_map.get("on_time_completion").target_value if targets_map.get("on_time_completion") else 95.0
    target_effectiveness = targets_map.get("effectiveness_rate").target_value if targets_map.get("effectiveness_rate") else 90.0
    target_avg_days = targets_map.get("avg_closing_time").target_value if targets_map.get("avg_closing_time") else 60.0
    target_cost_saving = targets_map.get("cost_saving").target_value if targets_map.get("cost_saving") else 50000.0
    target_horizontal = targets_map.get("horizontal_deployment").target_value if targets_map.get("horizontal_deployment") else 3.0

    # Filter projects by mode first
    all_projects_raw = db.query(CIProject).filter(CIProject.mode == mode).all()
    
    # Filter by year for summary cards
    all_projects = []
    for p in all_projects_raw:
        if p.start_date:
            try:
                start_dt = datetime.strptime(p.start_date, "%Y-%m-%d")
                # If year is None, include ALL projects (aggregated)
                # Otherwise filter to specific year
                if year is None or start_dt.year == year:
                    all_projects.append(p)
            except Exception:
                pass
    
    total_projects = len(all_projects)
    
    complete_projects = [p for p in all_projects if p.status == "Complete"]
    running_projects = [p for p in all_projects if p.status == "Running"]
    pending_projects = [p for p in all_projects if p.status == "Pending" or p.status == "Draft"]

    complete_count = len(complete_projects)
    running_count = len(running_projects)
    pending_count = len(pending_projects)

    # 1. On-Time Completion Rate: Completed On Time (close_date <= due_date) / Complete Projects
    on_time_count = 0
    total_closing_days = 0
    closing_days_count = 0

    for p in complete_projects:
        if p.close_date and p.due_date and p.close_date <= p.due_date:
            on_time_count += 1
        
        # Calculate closing days if available
        if p.closing_days is not None:
            total_closing_days += p.closing_days
            closing_days_count += 1
        elif p.start_date and p.close_date:
            try:
                d1 = datetime.strptime(p.start_date, "%Y-%m-%d")
                d2 = datetime.strptime(p.close_date, "%Y-%m-%d")
                days = (d2 - d1).days
                total_closing_days += max(days, 0)
                closing_days_count += 1
            except Exception:
                pass

    on_time_rate = round((on_time_count / complete_count * 100), 1) if complete_count > 0 else 0.0

    # 2. Effectiveness Rate: Verified PASS / Complete Projects
    pass_projects = [p for p in complete_projects if p.result == "PASS"]
    effectiveness_rate = round((len(pass_projects) / complete_count * 100), 1) if complete_count > 0 else 0.0

    # 3. Average Closing Time (Days)
    avg_closing_days = round(total_closing_days / closing_days_count, 1) if closing_days_count > 0 else 0.0

    # 4. Total Cost Saving
    total_cost_saving = sum([p.cost_saving or 0.0 for p in all_projects])

    # 5. Horizontal Deployment Projects
    horizontal_count = sum([1 for p in all_projects if p.horizontal_deploy == "Yes"])

    # Build KPI Performance table list
    kpi_performance_table = [
        {
            "id": 1,
            "kpi_key": "on_time_completion",
            "name": "Improvement Project On-time Completion Rate",
            "target": f"≥ {int(target_on_time)}%",
            "actual": f"{int(on_time_rate)}%" if on_time_rate.is_integer() else f"{on_time_rate}%",
            "status": "Good" if on_time_rate >= target_on_time else ("Close" if on_time_rate >= target_on_time - 5 else "Warning"),
            "raw_actual": on_time_rate,
            "raw_target": target_on_time
        },
        {
            "id": 2,
            "kpi_key": "effectiveness_rate",
            "name": "Improvement Effectiveness Rate",
            "target": f"≥ {int(target_effectiveness)}%",
            "actual": f"{int(effectiveness_rate)}%" if effectiveness_rate.is_integer() else f"{effectiveness_rate}%",
            "status": "Good" if effectiveness_rate >= target_effectiveness else ("Close" if effectiveness_rate >= target_effectiveness - 5 else "Warning"),
            "raw_actual": effectiveness_rate,
            "raw_target": target_effectiveness
        },
        {
            "id": 3,
            "kpi_key": "avg_closing_time",
            "name": "Average Closing Time",
            "target": f"< {int(target_avg_days)} Days",
            "actual": f"{int(avg_closing_days)} Days",
            "status": "Good" if avg_closing_days <= target_avg_days else "Warning",
            "raw_actual": avg_closing_days,
            "raw_target": target_avg_days
        },
        {
            "id": 4,
            "kpi_key": "cost_saving",
            "name": "Cost Saving",
            "target": f"≥ ${target_cost_saving:,.0f}",
            "actual": f"${total_cost_saving:,.0f}",
            "status": "Good" if total_cost_saving >= target_cost_saving else "Warning",
            "raw_actual": total_cost_saving,
            "raw_target": target_cost_saving
        },
        {
            "id": 5,
            "kpi_key": "horizontal_deployment",
            "name": "Horizontal Deployment",
            "target": f"≥ {int(target_horizontal)} Projects",
            "actual": f"{horizontal_count} Projects",
            "status": "Good" if horizontal_count >= target_horizontal else "Warning",
            "raw_actual": horizontal_count,
            "raw_target": target_horizontal
        }
    ]

    # Category distribution for Section 3 donut chart
    category_counts = {}
    for p in all_projects:
        cat = p.category or "Others"
        category_counts[cat] = category_counts.get(cat, 0) + 1

    # ====== MONTHLY TREND: 100% DYNAMIC FROM CI PROJECTS ======
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_on_time = [None] * 12
    monthly_effectiveness = [None] * 12
    monthly_avg_days = [None] * 12
    
    # For each month, calculate KPIs from projects closed in that month/year
    for month_idx in range(12):
        month_num = month_idx + 1  # 1-12
        
        # Find all COMPLETED projects with close_date in this month/year
        month_complete_projects = []
        for p in complete_projects:
            if p.close_date:
                try:
                    close_dt = datetime.strptime(p.close_date, "%Y-%m-%d")
                    # If year is None, include all months from all years
                    # Otherwise filter to specific year/month
                    if (year is None or close_dt.year == year) and close_dt.month == month_num:
                        month_complete_projects.append(p)
                except Exception:
                    pass
        
        # If there are completed projects in this month, calculate KPIs
        if month_complete_projects:
            # On-time rate
            month_on_time_count = sum(1 for p in month_complete_projects 
                                     if p.close_date and p.due_date and p.close_date <= p.due_date)
            monthly_on_time[month_idx] = round((month_on_time_count / len(month_complete_projects) * 100), 1)
            
            # Effectiveness rate (PASS projects)
            month_pass_count = sum(1 for p in month_complete_projects if p.result == "PASS")
            monthly_effectiveness[month_idx] = round((month_pass_count / len(month_complete_projects) * 100), 1)
            
            # Average closing days
            month_closing_days = []
            for p in month_complete_projects:
                if p.closing_days is not None:
                    month_closing_days.append(p.closing_days)
                elif p.start_date and p.close_date:
                    try:
                        d1 = datetime.strptime(p.start_date, "%Y-%m-%d")
                        d2 = datetime.strptime(p.close_date, "%Y-%m-%d")
                        days = (d2 - d1).days
                        month_closing_days.append(max(days, 0))
                    except Exception:
                        pass
            
            if month_closing_days:
                monthly_avg_days[month_idx] = round(sum(month_closing_days) / len(month_closing_days), 1)
            else:
                monthly_avg_days[month_idx] = 0.0

    return {
        "summary_cards": {
            "total": {"count": total_projects, "percent": 100},
            "complete": {"count": complete_count, "percent": round((complete_count / total_projects * 100), 1) if total_projects else 0},
            "running": {"count": running_count, "percent": round((running_count / total_projects * 100), 1) if total_projects else 0},
            "pending": {"count": pending_count, "percent": round((pending_count / total_projects * 100), 1) if total_projects else 0},
            "on_time_rate": {"rate": on_time_rate, "target": target_on_time},
            "effectiveness_rate": {"rate": effectiveness_rate, "target": target_effectiveness},
            "avg_closing_days": {"days": avg_closing_days, "target": target_avg_days},
            "cost_saving": {"amount": total_cost_saving, "target": target_cost_saving},
            "horizontal_deployment": {"count": horizontal_count, "target": target_horizontal}
        },
        "kpi_performance_table": kpi_performance_table,
        "project_status_distribution": [
            {"name": "Complete", "value": complete_count},
            {"name": "Running", "value": running_count},
            {"name": "Pending", "value": pending_count}
        ],
        "project_category_distribution": [
            {"name": k, "value": v} for k, v in category_counts.items()
        ],
        "monthly_kpi_trend": {
            "months": months,
            "on_time_rate": monthly_on_time,
            "effectiveness_rate": monthly_effectiveness,
            "avg_closing_time": monthly_avg_days,
            "year": year_for_display,
            "mode": mode
        }
    }


def save_current_month_snapshot(db: Session, mode: str = "PRODUCTION"):
    """[DEPRECATED] Keeping for backwards compatibility but not used."""
    now = datetime.now()
    year = now.year
    month = now.month
    
    kpi_data = calculate_kpis(db, year, mode)
    summary = kpi_data["summary_cards"]
    
    existing = db.query(MonthlyKPISnapshot).filter(
        and_(
            MonthlyKPISnapshot.year == year,
            MonthlyKPISnapshot.month == month
        )
    ).first()
    
    snapshot_data = {
        "on_time_completion_rate": summary["on_time_rate"]["rate"],
        "effectiveness_rate": summary["effectiveness_rate"]["rate"],
        "avg_closing_days": summary["avg_closing_days"]["days"],
        "cost_saving": summary["cost_saving"]["amount"],
        "horizontal_deployment_count": summary["horizontal_deployment"]["count"],
        "total_projects_completed": summary["complete"]["count"],
        "total_projects_running": summary["running"]["count"]
    }
    
    if existing:
        for key, value in snapshot_data.items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return {"action": "updated", "snapshot": existing}
    else:
        new_snapshot = MonthlyKPISnapshot(
            year=year,
            month=month,
            **snapshot_data
        )
        db.add(new_snapshot)
        db.commit()
        db.refresh(new_snapshot)
        return {"action": "created", "snapshot": new_snapshot}
