import sqlite3
import os

def migrate():
    db_path = "/app/cims.db"
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(ci_projects)")
        columns = [row[1] for row in cursor.fetchall()]
        
        migrations = [
            ("tpm_approved_by", "ALTER TABLE ci_projects ADD COLUMN tpm_approved_by STRING"),
            ("tpm_approve_date", "ALTER TABLE ci_projects ADD COLUMN tpm_approve_date STRING"),
            ("tpm_approve_comment", "ALTER TABLE ci_projects ADD COLUMN tpm_approve_comment TEXT"),
        ]
        
        for col_name, sql in migrations:
            if col_name not in columns:
                print(f"Adding column: {col_name}")
                cursor.execute(sql)
                print(f"✅ Added {col_name}")
            else:
                print(f"Column {col_name} already exists, skipping")
        
        conn.commit()
        print("✅ Migration completed successfully")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
