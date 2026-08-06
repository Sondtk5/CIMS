from sqlalchemy.orm import Session
from app.models.admin_setting import AdminSetting
from datetime import datetime
import json

DEFAULT_CI_NUMBERING_CONFIG = {
    "parts": [
        {"name": "prefix", "value": "UTIV", "enabled": True, "auto_increment": False},
        {"name": "department", "value": "EN", "enabled": True, "auto_increment": False},
        {"name": "category", "value": "R", "enabled": True, "auto_increment": False},
        {"name": "year", "value": "00", "enabled": True, "auto_increment": False},
        {"name": "sequence", "value": "0001", "enabled": True, "auto_increment": False},
        {"name": "version", "value": "02", "enabled": True, "auto_increment": False},
        {"name": "counter", "value": "001", "enabled": True, "auto_increment": True}  # Auto-increment by default
    ],
    "separator": "-",
    "next_counter": 1,
    "last_updated": datetime.utcnow().isoformat()
}

def get_or_create_ci_numbering_config(db: Session):
    """Get CI numbering config from DB or create default"""
    setting = db.query(AdminSetting).filter(
        AdminSetting.setting_key == "ci_numbering_config"
    ).first()
    
    if not setting:
        # Create default config
        setting = AdminSetting(
            setting_key="ci_numbering_config",
            setting_value=DEFAULT_CI_NUMBERING_CONFIG,
            description="CI Project numbering convention configuration"
        )
        db.add(setting)
        db.commit()
        db.refresh(setting)
    
    return setting

def update_ci_numbering_config(db: Session, config_data: dict):
    """Update CI numbering config"""
    setting = get_or_create_ci_numbering_config(db)
    
    # Merge with existing config, preserve next_counter
    current_value = setting.setting_value.copy() if isinstance(setting.setting_value, dict) else {}
    next_counter = current_value.get("next_counter", 1)
    
    config_data["next_counter"] = next_counter
    config_data["last_updated"] = datetime.utcnow().isoformat()
    
    setting.setting_value = config_data
    setting.updated_at = datetime.utcnow().isoformat()
    db.commit()
    db.refresh(setting)
    
    return setting

def generate_ci_number(db: Session, dept_code: str = None, cat_code: str = None, commit: bool = True) -> str:
    """
    Generate next CI number based on config and existing CI projects.
    
    Strategy:
    1. Query all existing CI projects
    2. Extract counter from last CI no
    3. Auto-increment from there
    4. If no projects exist, use next_counter from config
    
    Example: UTIV-EN-R-26-0000-00-001
    
    Args:
        db: Database session
        dept_code: Override department code (e.g., "EN", "WB")
        cat_code: Override category code (e.g., "R", "Q")
        commit: If True, commit counter increment to DB. If False, just generate without persisting.
    
    Returns:
        Generated CI number string
    """
    from app.models.ci_project import CIProject
    
    setting = get_or_create_ci_numbering_config(db)
    config = setting.setting_value.copy() if isinstance(setting.setting_value, dict) else {}
    parts = config.get("parts", DEFAULT_CI_NUMBERING_CONFIG["parts"])
    separator = config.get("separator", "-")
    
    # Find the counter part to determine padding
    counter_part = next((p for p in parts if p.get("name") == "counter"), None)
    pad_length = len(counter_part.get("value", "000")) if counter_part else 3
    
    # Query existing CI projects and find max counter
    all_projects = db.query(CIProject).all()
    max_counter = 0
    
    if all_projects:
        for project in all_projects:
            try:
                if project.ci_no:
                    # Split by separator and get last part (counter)
                    ci_parts = project.ci_no.split(separator)
                    if ci_parts:
                        counter_str = ci_parts[-1]
                        # Extract number from counter (in case it has letters)
                        counter_num = int(''.join(filter(str.isdigit, counter_str)) or '0')
                        if counter_num > max_counter:
                            max_counter = counter_num
            except Exception as e:
                print(f"Error parsing CI number {project.ci_no}: {e}")
                continue
    
    # Use max_counter + 1 (or next_counter if config is higher)
    next_counter = max(max_counter + 1, config.get("next_counter", 1))
    
    # Build CI number from enabled parts
    parts_list = []
    
    for part in parts:
        if not part.get("enabled", False):
            continue
        
        part_name = part.get("name")
        part_value = part.get("value", "")
        is_auto = part.get("auto_increment", False)
        
        # Override with function parameters if provided
        if part_name == "department" and dept_code:
            part_value = dept_code
        elif part_name == "category" and cat_code:
            part_value = cat_code
        elif part_name == "counter" and is_auto:
            # Use next_counter and pad with zeros
            part_value = str(next_counter).zfill(pad_length)
            
            # Increment counter for next time (and save if commit=True)
            if commit:
                config["next_counter"] = next_counter + 1
                setting.setting_value = config
                setting.updated_at = datetime.utcnow().isoformat()
                db.add(setting)
                db.commit()
                db.refresh(setting)
        elif part_name == "year":
            # Use config value as-is
            # If you want current year, set it in Admin Settings
            # part_value is already set from config
            pass
        
        parts_list.append(str(part_value))
    
    ci_number = separator.join(parts_list)
    
    return ci_number

def generate_ci_number_with_year(db: Session, dept_code: str = None, cat_code: str = None, use_current_year: bool = False, commit: bool = True) -> str:
    """
    Alternative: generate CI with option to use current year
    If you want dynamic current year, use this function with use_current_year=True
    """
    ci = generate_ci_number(db, dept_code, cat_code, commit)
    
    if use_current_year:
        # Replace year part with current year
        # This is for future use if you want dynamic year
        pass
    
    return ci

def get_ci_numbering_format(db: Session) -> dict:
    """Get current CI numbering format for frontend display"""
    setting = get_or_create_ci_numbering_config(db)
    config = setting.setting_value
    
    return {
        "parts": config.get("parts", DEFAULT_CI_NUMBERING_CONFIG["parts"]),
        "separator": config.get("separator", "-"),
        "next_counter": config.get("next_counter", 1),
        "example": generate_ci_number(db, commit=False)  # Preview without incrementing
    }
