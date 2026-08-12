# CIMS Transfer Checklist

## Before Transfer

### On Current Machine (Sao lưu dữ liệu)
- [ ] Backup database: `cims_production_backup_rev2.db` ✅ (180 KB)
- [ ] JSON export: `production_6projects_rev2.json` ✅ (13 KB)
- [ ] Verify 6 production projects
- [ ] Git repo is up to date

### Verify Backup Files
```bash
ls -lh cims_production_backup_rev2.db
ls -lh production_6projects_rev2.json
git status  # Should be clean
```

---

## Transfer to New Machine

### Step 1: Copy Files
Option A - Using USB/Cloud:
```bash
# Copy these files to USB or cloud storage
- CIMS/ (entire folder)
- cims_production_backup_rev2.db
- production_6projects_rev2.json
- DEPLOYMENT_GUIDE.md
- transfer_setup.sh
```

Option B - Using Git (Recommended):
```bash
# On new machine, just clone
git clone https://github.com/Sondtk5/CIMS.git
cd CIMS

# Then copy the backup file
# (Download from secure location or USB)
cp /path/to/cims_production_backup_rev2.db ./
```

### Step 2: Setup on New Machine
```bash
cd CIMS

# Make script executable
chmod +x transfer_setup.sh

# Run automatic setup
./transfer_setup.sh

# OR manual setup:
cp cims_production_backup_rev2.db backend/cims.db
docker compose up -d
```

### Step 3: Verify
```bash
# Check containers
docker compose ps

# Should show:
# - cims_backend (running)
# - cims_frontend (running)

# Test access
curl http://localhost/api/admin/mode
# Should return: {"mode":"PRODUCTION"} or similar

# Check production projects
docker compose exec cims_backend python3 << 'EOF'
from app.database import SessionLocal
from app.models.ci_project import CIProject
db = SessionLocal()
projects = db.query(CIProject).filter(
    CIProject.mode == 'PRODUCTION'
).all()
for p in projects[:3]:
    print(f"{p.ci_no} - {p.title}")
db.close()
EOF
```

### Step 4: Login
- Open: http://localhost
- Username: `admin`
- Password: `password123`
- Should see 6 production projects

---

## Important Files

### Database
- `backend/cims.db` - Active database (auto-created if not present)
- `cims_production_backup_rev2.db` - Backup with 6 production projects

### Configuration
- `docker-compose.yml` - Container definitions
- `backend/` - FastAPI backend source
- `frontend/` - React frontend source

### Guides
- `DEPLOYMENT_GUIDE.md` - Detailed setup instructions
- `PRODUCTION_VERSION_NOTE.md` - Version information
- `transfer_setup.sh` - Automated setup script

---

## Rollback / Recovery

If something goes wrong:
```bash
# Stop everything
docker compose down

# Restore from backup
cp cims_production_backup_rev2.db backend/cims.db

# Restart
docker compose up -d
```

---

## Database Contents

### Production Mode (6 Projects)
1. UTIV-EN-R-26-0001-02-001 - Stain 2 Defect Improvement
2. UTIV-EN-R-26-0001-02-002 - Slit Coater - Takt Time Improvement
3. UTIV-EN-R-26-0001-02-003 - Waviness Defect Improvement
4. UTIV-EN-R-26-0001-02-004 - IOX SYL Improvement - CPM Defect
5. UTIV-EN-R-26-0001-02-005 - IOX SYL Improvement - OP Defect
6. UTIV-EN-R-26-0001-02-006 - Equipment Efficiency Optimization

### Demo Mode (133 Projects)
- 2024: 20 projects
- 2025: 45 projects
- 2026: 68 projects

### Other
- 6 Users with different roles
- 5 KPI Targets configured
- Full audit logs
- Monthly KPI snapshots

---

## Support

If you encounter issues:
1. Check `docker compose logs`
2. Verify Docker is running
3. Check disk space: `df -h`
4. Verify ports 80 and 8000 are available
5. See DEPLOYMENT_GUIDE.md for detailed troubleshooting
