#!/usr/bin/env python3
"""
Add 'mode' column to ci_projects table for separating DEMO and PRODUCTION data.
Handles both fresh DB and existing DB with data.
"""
import os
os.environ['DATABASE_URL'] = 'postgresql://cims_user:cims_password@db:5432/cims_db'

from sqlalchemy import text
from app.database import engine

def add_mode_column():
    """Add mode column if it doesn't exist"""
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='ci_projects' AND column_name='mode'
        """))
        
        if result.fetchone():
            print("✅ Column 'mode' already exists")
            return
        
        # Add column
        conn.execute(text("""
            ALTER TABLE ci_projects 
            ADD COLUMN mode VARCHAR DEFAULT 'PRODUCTION' NOT NULL
        """))
        conn.commit()
        print("✅ Added 'mode' column to ci_projects")

if __name__ == "__main__":
    try:
        add_mode_column()
        print("✅ Migration complete")
    except Exception as e:
        print(f"❌ Error: {e}")
