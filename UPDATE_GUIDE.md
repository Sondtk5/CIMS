# CIMS Update Guide - For Existing Running Instances

## Quick Update (Recommended)

If you already have CIMS running on your machine and want to update to the latest version:

```bash
cd /path/to/CIMS
./update.sh
```

This script will:
1. ✅ Backup your current database
2. ✅ Pull latest code from Git
3. ✅ Restore production data
4. ✅ Rebuild Docker images
5. ✅ Restart containers
6. ✅ Verify everything works

## Manual Update Process

If you prefer to update step-by-step manually:

### Step 1: Backup Current Database
```bash
# Create a backup of your current database
cp backend/cims.db backend/cims_backup_$(date +%Y%m%d_%H%M%S).db
```

### Step 2: Stop Current Containers
```bash
docker compose down
```

### Step 3: Pull Latest Code
```bash
git pull origin main
```

### Step 4: Restore Production Data
```bash
# This updates the database with latest production snapshot
python3 backend/restore_production_data.py
```

### Step 5: Rebuild Docker Images
```bash
docker compose build
```

### Step 6: Start Containers
```bash
docker compose up -d
```

### Step 7: Verify
```bash
# Check containers
docker compose ps

# Check database
docker compose exec cims_backend python3 << 'EOF'
from app.database import SessionLocal
from app.models.ci_project import CIProject
db = SessionLocal()
prod = db.query(CIProject).filter(CIProject.mode == 'PRODUCTION').count()
demo = db.query(CIProject).filter(CIProject.mode == 'DEMO').count()
print(f"Production: {prod}, Demo: {demo}")
db.close()
EOF
```

## What Gets Updated

### Code Updates (Applied Immediately)
- ✅ Backend source code improvements
- ✅ Frontend source code updates
- ✅ Bug fixes and new features
- ✅ Docker configuration (if changed)

### Database Updates (Via Restore)
The `restore_production_data.py` script is **idempotent**:
- ✅ Adds new projects if they don't exist
- ✅ Does NOT delete your existing edits
- ✅ Does NOT overwrite existing projects
- ✅ Safely merges latest data

### Local-Only Data (Preserved)
- ✅ Your local project edits
- ✅ Custom configurations
- ✅ User credentials
- ⚠️ Only if you didn't delete the database

## Important: User Edits

### Your Local Changes are Preserved
When you run the update:
```
Your edits in backend/cims.db + New projects from seed file
= Merged database with both local changes AND new data
```

### BUT: If You Delete the Database
```bash
# ⚠️ This will LOSE all your local edits
rm backend/cims.db

# ⚠️ Then restore will create ONLY the seed data (no your edits)
python3 backend/restore_production_data.py
```

## Rollback Procedure

If something goes wrong during update:

### Step 1: Stop Containers
```bash
docker compose down
```

### Step 2: Restore Backup
```bash
# Find your backup
ls -lh backend/cims_backup_*.db

# Restore
cp backend/cims_backup_20260812_120000.db backend/cims.db
```

### Step 3: Restart
```bash
docker compose up -d
```

## Troubleshooting

### Problem: Git merge conflicts
**Solution:**
```bash
# Keep your local changes
git pull origin main --no-rebase

# Or if you want latest version
git fetch origin
git reset --hard origin/main
```

### Problem: Docker build fails
**Solution:**
```bash
# Clear cache and rebuild
docker compose build --no-cache
docker compose up -d
```

### Problem: Database restore fails
**Solution:**
```bash
# Check if database is corrupted
sqlite3 backend/cims.db "SELECT COUNT(*) FROM ci_projects;"

# If error, restore from backup
cp backend/cims_backup_*.db backend/cims.db
```

### Problem: Can't connect to http://localhost
**Solution:**
```bash
# Wait longer for containers
sleep 10

# Check container logs
docker compose logs -f backend

# Restart containers
docker compose restart
```

## Comparison: Update vs Fresh Clone

| Scenario | Use |
|----------|-----|
| **Already running CIMS** | `./update.sh` |
| **New machine** | `./bootstrap.sh` |
| **Lost database** | `python3 backend/restore_production_data.py` |
| **Want latest code + new data** | `./update.sh` |
| **Want to reset everything** | `docker compose down -v && ./bootstrap.sh` |

## What if Update Doesn't Work?

If `./update.sh` fails:

```bash
# 1. Check Git status
git status

# 2. Check Docker status
docker compose ps

# 3. Check logs
docker compose logs backend

# 4. Try manual process step-by-step
git pull
python3 backend/restore_production_data.py
docker compose build
docker compose up -d
```

## Before You Update

Make sure:
- ✅ You have a backup of important data
- ✅ Docker is running
- ✅ You're in the CIMS directory
- ✅ You have internet for git pull
- ✅ Port 80 and 8000 are available

## After Update

Verify:
- ✅ http://localhost loads
- ✅ Can login with admin/password123
- ✅ Your edits are still there
- ✅ New projects are visible
- ✅ Database has correct project count

---

**Need help?** Check `DATA_MANAGEMENT.md` for more details on data strategy.
