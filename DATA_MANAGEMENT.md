# CIMS - Continuous Improvement Management System
## Data Management & Deployment Guide

### 📊 Current Status
- **Production Database**: 6 complete CI projects with DMAIC + 5 Why analysis
- **Demo Database**: 133 sample projects for testing
- **Database Storage**: `backend/seed_production_data.json` (tracked in Git)
- **Active Database**: `backend/cims.db` (NOT tracked - generated locally)

---

## 🔄 How Data is Managed

### User Edits (Local Changes)
When users edit projects in the UI:
```
Browser → Frontend API → Backend FastAPI → SQLite Database
                                          ↓
                              backend/cims.db (LOCAL ONLY)
```

**Important**: User edits are saved ONLY in `backend/cims.db` on the LOCAL machine
- Database file is **NOT** committed to Git
- Changes are **NOT** automatically synced to other machines
- Each machine has its own independent database

### Seed File (Production Data Snapshot)
```
backend/seed_production_data.json (266 KB) - TRACKED IN GIT
│
└─ Contains:
   ├─ 6 production projects with complete data
   ├─ 133 demo projects
   ├─ 6 users with credentials
   ├─ 6 roles and KPI targets
   └─ All admin settings
```

---

## 🚀 Deployment on Another Machine

### Step 1: Clone Repository
```bash
git clone https://github.com/Sondtk5/CIMS.git
cd CIMS
```

The repository includes:
- ✅ Source code (frontend + backend)
- ✅ Dockerfile & docker-compose.yml
- ✅ **seed_production_data.json** - Production data snapshot
- ❌ cims.db (NOT included - will be generated fresh)

### Step 2: Restore Production Data
```bash
# Option A: Run bootstrap script (Recommended)
chmod +x bootstrap.sh
./bootstrap.sh

# Option B: Manual restore
python3 backend/restore_production_data.py
```

This creates a fresh `backend/cims.db` with:
- All 6 production projects (with DMAIC + 5 Why data)
- All 133 demo projects
- All users, roles, and settings

### Step 3: Start Docker
```bash
docker compose up -d
```

### Step 4: Access Application
- **URL**: http://localhost
- **Login**: admin / password123

---

## 💾 What Gets Committed to Git?

**TRACKED (IN GIT):**
- ✅ Source code (Python, JavaScript, React)
- ✅ Docker configuration (Dockerfile, docker-compose.yml)
- ✅ seed_production_data.json (production data snapshot)
- ✅ seed scripts (restore_production_data.py)

**NOT TRACKED (LOCAL ONLY):**
- ❌ backend/cims.db (local database file)
- ❌ node_modules/
- ❌ __pycache__/
- ❌ .env files with secrets

---

## 📝 Important: User Changes & Persistence

### Scenario: User Edits a Project
```
Machine A:
├─ User edits project → Saved in local cims.db
└─ Changes ONLY on Machine A

Machine B:
├─ Clone from Git → Gets seed_production_data.json
├─ Bootstrap → Creates fresh cims.db with original data
└─ Machine B does NOT have Machine A's edits
```

**To Share Changes:**
1. **Option 1**: Export data as JSON backup
   ```bash
   # On Machine A - export changes
   python3 backend/backup_database.py
   # Share the backup file with Machine B
   ```

2. **Option 2**: Update seed file in Git
   ```bash
   # On Machine A - update seed file
   python3 backend/export_all_data.py
   # Commit and push
   git add backend/seed_production_data.json
   git commit -m "Update: Production data with latest changes"
   git push
   
   # On Machine B - pull and restore
   git pull
   python3 backend/restore_production_data.py
   docker compose restart backend
   ```

---

## 🔄 Data Flow Diagram

```
┌─ Initial Clone ─────────────────┐
│                                 │
│  git clone CIMS                 │
│  ├─ Gets seed_production_data.json
│  └─ Does NOT get cims.db        │
│                                 │
└──────────────┬──────────────────┘
               │
               ▼
       bootstrap.sh OR
   restore_production_data.py
               │
               ├─ Reads seed_production_data.json
               └─ Creates fresh backend/cims.db
                  (with all production + demo data)
               │
               ▼
    docker compose up -d
               │
               ├─ Mounts ./backend:/app
               ├─ Database accessible
               └─ Users can now edit

    User Edits Project
               │
               ├─ Saved in local cims.db
               ├─ Changes LIVE
               └─ NOT automatically synced to Git
```

---

## 🛠️ For Developers

### Backup Production Data
```bash
# Create a backup of current production data
python3 backend/export_all_data.py
# Creates: production_data_backup_TIMESTAMP.json
```

### Update Seed File with Latest Changes
```bash
# Export current database to seed file
python3 -c "
import shutil
shutil.copy('backend/cims.db', 'backend/cims_temp.db')
# Then export to seed_production_data.json
python3 backend/export_all_data.py --output backend/seed_production_data.json
"

# Commit to Git
git add backend/seed_production_data.json
git commit -m "Update: Production data snapshot"
git push
```

### Reset Database to Original State
```bash
# Delete local database
rm backend/cims.db

# Restore from seed file
python3 backend/restore_production_data.py

# Restart containers
docker compose restart backend
```

---

## 📋 Git Workflow

### When You Want to Share Data Changes

```bash
# Step 1: Update seed file
cp backend/cims.db backend/cims_temp.db
python3 backend/export_all_data.py --output backend/seed_production_data.json

# Step 2: Commit
git add backend/seed_production_data.json
git commit -m "Update: [describe what changed]"
git push origin main

# Step 3: On other machine
git pull origin main
python3 backend/restore_production_data.py
docker compose restart backend
```

---

## 📊 Database Files Reference

| File | Location | Purpose | Tracked in Git? |
|------|----------|---------|-----------------|
| seed_production_data.json | backend/ | Production data snapshot | ✅ YES |
| cims.db | backend/ | Active SQLite database | ❌ NO |
| cims_production_backup_rev2.db | root/ | Manual backup | ❌ NO |

---

## ⚠️ Common Issues

### Problem: Cloned code but no production data
**Solution**: Run bootstrap script
```bash
./bootstrap.sh
```

### Problem: Database missing after git clone
**Solution**: Restore from seed file
```bash
python3 backend/restore_production_data.py
```

### Problem: Want to preserve local changes when pulling updates
**Solution**: Export to backup first
```bash
# Before git pull
cp backend/cims.db backend/cims_local_backup.db

# After git pull
git pull
# Keep your local cims.db (don't restore from seed)
```

### Problem: Machine B doesn't have Machine A's edits
**Solution**: Update seed file in Git (see "For Developers" section above)

---

## ✅ Verification Checklist

After bootstrap or restore, verify:
```bash
# 1. Database exists
ls -lh backend/cims.db

# 2. Can access database
sqlite3 backend/cims.db "SELECT COUNT(*) FROM ci_projects WHERE mode='PRODUCTION';"
# Should return: 6

# 3. Docker containers running
docker compose ps

# 4. Can access web UI
curl http://localhost/api/admin/mode
# Should return something like: {"mode":"PRODUCTION"}

# 5. Can login
# Open http://localhost
# Login: admin / password123
```

---

## Summary

```
🎯 Key Points:
├─ Database file (cims.db) is LOCAL ONLY - not in Git
├─ Production data is in seed_production_data.json - IN Git
├─ User edits saved in cims.db are NOT auto-synced to Git
├─ Each machine has independent database with same initial data
└─ To share changes: Update seed file → Commit → Pull → Restore on other machine
```

---

**Last Updated**: 2026-08-12
**Status**: Production Ready with Data Management Strategy
