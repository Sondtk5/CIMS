#!/usr/bin/env python3
"""
Export current database state to seed file
Use this after making edits to preserve them for other machines

Usage:
  python3 export_data.py

This will:
1. Export all production projects (with your edits)
2. Export all demo projects
3. Export users, roles, settings
4. Save to backend/seed_production_data.json
5. You can then: git add, commit, push to share with other machines
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
import sys

def export_database():
    db_path = Path("backend/cims.db")
    
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return False
    
    print("📤 Exporting current database...")
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    
    try:
        cursor = conn.cursor()
        
        # Get production projects
        cursor.execute("SELECT * FROM ci_projects WHERE mode='PRODUCTION' ORDER BY ci_no")
        prod_projects = [dict(row) for row in cursor.fetchall()]
        
        # Get demo projects
        cursor.execute("SELECT * FROM ci_projects WHERE mode='DEMO' ORDER BY ci_no")
        demo_projects = [dict(row) for row in cursor.fetchall()]
        
        # Get other tables
        cursor.execute("SELECT * FROM users")
        users = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM roles")
        roles = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM kpi_targets")
        kpi_targets = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM admin_settings")
        admin_settings = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM monthly_kpi_snapshots")
        monthly_kpi_snapshots = [dict(row) for row in cursor.fetchall()]
        
        # Create export
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "production_projects": prod_projects,
            "demo_projects": demo_projects,
            "users": users,
            "roles": roles,
            "kpi_targets": kpi_targets,
            "admin_settings": admin_settings,
            "monthly_kpi_snapshots": monthly_kpi_snapshots
        }
        
        # Save
        seed_path = Path("backend/seed_production_data.json")
        with open(seed_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n✅ EXPORTED SUCCESSFULLY")
        print(f"\n📊 Summary:")
        print(f"   Production projects: {len(prod_projects)}")
        print(f"   Demo projects: {len(demo_projects)}")
        print(f"   Users: {len(users)}")
        print(f"   Roles: {len(roles)}")
        
        print(f"\n📋 Production Projects (with your edits):")
        for proj in prod_projects:
            ci_no = proj.get('ci_no')
            title = proj.get('title')
            cost = proj.get('cost_saving', 0)
            print(f"   {ci_no}: {title}")
            print(f"       └─ cost_saving: ${cost:,.2f}")
        
        print(f"\n📝 Saved to: {seed_path}")
        print(f"   Size: {seed_path.stat().st_size / 1024:.1f} KB")
        
        print(f"\n🚀 Next steps to share:")
        print(f"   1. git add backend/seed_production_data.json")
        print(f"   2. git commit -m 'Update: Latest production data with edits'")
        print(f"   3. git push origin main")
        print(f"   4. Other machines: git pull && ./update.sh")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = export_database()
    sys.exit(0 if success else 1)
