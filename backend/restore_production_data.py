#!/usr/bin/env python3
"""
Restore production database from seed file.
Run this script after cloning to restore all data.

Usage:
  python3 backend/restore_production_data.py
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

def restore_database():
    """Restore database from seed file"""
    
    db_path = Path("backend/cims.db")
    seed_path = Path("backend/seed_production_data.json")
    
    if not seed_path.exists():
        print(f"❌ Seed file not found: {seed_path}")
        return False
    
    print(f"📥 Loading seed file: {seed_path}")
    
    with open(seed_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Connect to database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        print("\n🔄 Restoring data...")
        
        # Clear existing data (optional - comment out if you want to preserve user changes)
        # cursor.execute("DELETE FROM ci_projects")
        # cursor.execute("DELETE FROM users WHERE id > 6")  # Keep system users
        
        # Restore Production Projects
        prod_count = 0
        for proj in data.get("production_projects", []):
            # Check if project already exists
            cursor.execute("SELECT id FROM ci_projects WHERE ci_no = ?", (proj['ci_no'],))
            if not cursor.fetchone():
                # Insert new project
                cols = list(proj.keys())
                vals = [proj[col] for col in cols]
                placeholders = ','.join(['?' for _ in cols])
                col_names = ','.join(cols)
                
                cursor.execute(
                    f"INSERT INTO ci_projects ({col_names}) VALUES ({placeholders})",
                    vals
                )
                prod_count += 1
        
        # Restore Demo Projects
        demo_count = 0
        for proj in data.get("demo_projects", []):
            cursor.execute("SELECT id FROM ci_projects WHERE ci_no = ?", (proj['ci_no'],))
            if not cursor.fetchone():
                cols = list(proj.keys())
                vals = [proj[col] for col in cols]
                placeholders = ','.join(['?' for _ in cols])
                col_names = ','.join(cols)
                
                cursor.execute(
                    f"INSERT INTO ci_projects ({col_names}) VALUES ({placeholders})",
                    vals
                )
                demo_count += 1
        
        # Restore Users
        user_count = 0
        for user in data.get("users", []):
            cursor.execute("SELECT id FROM users WHERE id = ?", (user['id'],))
            if not cursor.fetchone():
                cols = list(user.keys())
                vals = [user[col] for col in cols]
                placeholders = ','.join(['?' for _ in cols])
                col_names = ','.join(cols)
                
                cursor.execute(
                    f"INSERT INTO users ({col_names}) VALUES ({placeholders})",
                    vals
                )
                user_count += 1
        
        # Restore Roles
        role_count = 0
        for role in data.get("roles", []):
            cursor.execute("SELECT id FROM roles WHERE id = ?", (role['id'],))
            if not cursor.fetchone():
                cols = list(role.keys())
                vals = [role[col] for col in cols]
                placeholders = ','.join(['?' for _ in cols])
                col_names = ','.join(cols)
                
                cursor.execute(
                    f"INSERT INTO roles ({col_names}) VALUES ({placeholders})",
                    vals
                )
                role_count += 1
        
        # Restore KPI Targets
        kpi_count = 0
        for kpi in data.get("kpi_targets", []):
            cursor.execute("SELECT id FROM kpi_targets WHERE id = ?", (kpi['id'],))
            if not cursor.fetchone():
                cols = list(kpi.keys())
                vals = [kpi[col] for col in cols]
                placeholders = ','.join(['?' for _ in cols])
                col_names = ','.join(cols)
                
                cursor.execute(
                    f"INSERT INTO kpi_targets ({col_names}) VALUES ({placeholders})",
                    vals
                )
                kpi_count += 1
        
        # Restore Admin Settings
        admin_count = 0
        for setting in data.get("admin_settings", []):
            cursor.execute("SELECT id FROM admin_settings WHERE id = ?", (setting['id'],))
            if not cursor.fetchone():
                cols = list(setting.keys())
                vals = [setting[col] for col in cols]
                placeholders = ','.join(['?' for _ in cols])
                col_names = ','.join(cols)
                
                cursor.execute(
                    f"INSERT INTO admin_settings ({col_names}) VALUES ({placeholders})",
                    vals
                )
                admin_count += 1
        
        # Restore Monthly KPI Snapshots
        snapshot_count = 0
        for snap in data.get("monthly_kpi_snapshots", []):
            cursor.execute("SELECT id FROM monthly_kpi_snapshots WHERE id = ?", (snap['id'],))
            if not cursor.fetchone():
                cols = list(snap.keys())
                vals = [snap[col] for col in cols]
                placeholders = ','.join(['?' for _ in cols])
                col_names = ','.join(cols)
                
                cursor.execute(
                    f"INSERT INTO monthly_kpi_snapshots ({col_names}) VALUES ({placeholders})",
                    vals
                )
                snapshot_count += 1
        
        conn.commit()
        
        print(f"\n✅ Restored:")
        print(f"  {prod_count} production projects")
        print(f"  {demo_count} demo projects")
        print(f"  {user_count} users")
        print(f"  {role_count} roles")
        print(f"  {kpi_count} KPI targets")
        print(f"  {admin_count} admin settings")
        print(f"  {snapshot_count} monthly snapshots")
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM ci_projects WHERE mode='PRODUCTION'")
        prod_total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ci_projects WHERE mode='DEMO'")
        demo_total = cursor.fetchone()[0]
        
        print(f"\n✅ Database verification:")
        print(f"  Total production projects: {prod_total}")
        print(f"  Total demo projects: {demo_total}")
        print(f"  Total projects: {prod_total + demo_total}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = restore_database()
    exit(0 if success else 1)
