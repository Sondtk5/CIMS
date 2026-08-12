# Deployment Guide - CIMS Production

## Transfer to Another Machine

### Prerequisites
- Docker & Docker Compose installed
- Git installed
- ~500MB disk space

### Step 1: Clone Repository
```bash
git clone https://github.com/Sondtk5/CIMS.git
cd CIMS
```

### Step 2: Restore Production Database
```bash
# Copy the backup database to the correct location
cp cims_production_backup_rev2.db backend/cims.db
```

### Step 3: Start Docker
```bash
docker compose up -d
```

The system will:
- Build the backend (FastAPI)
- Build the frontend (React)
- Load the database from `backend/cims.db`
- Start services on:
  - Frontend: http://localhost
  - Backend API: http://localhost:8000

### Step 4: Login
- URL: http://localhost
- Username: `admin`
- Password: `password123`

## Database Contents
- **Production Mode:** 6 CI projects (with full details)
- **Demo Mode:** 133 sample projects
- **Users:** 6 predefined roles
- **Settings:** KPI targets configured

## 6 Production Projects
1. UTIV-EN-R-26-0001-02-001 - Stain 2 Defect Improvement
2. UTIV-EN-R-26-0001-02-002 - Slit Coater - Takt Time Improvement
3. UTIV-EN-R-26-0001-02-003 - Waviness Defect Improvement
4. UTIV-EN-R-26-0001-02-004 - IOX SYL Improvement - CPM Defect
5. UTIV-EN-R-26-0001-02-005 - IOX SYL Improvement - OP Defect
6. UTIV-EN-R-26-0001-02-006 - Equipment Efficiency Optimization

## Backup Files
- `cims_production_backup_rev2.db` - Full database backup (180 KB)
- `production_6projects_rev2.json` - JSON export of 6 projects (13 KB)

## Verify Installation
```bash
# Check containers running
docker compose ps

# View logs
docker compose logs -f frontend
docker compose logs -f backend

# Check database
docker exec cims_backend python3 << 'EOF'
from app.database import SessionLocal
from app.models.ci_project import CIProject

db = SessionLocal()
count = db.query(CIProject).filter(CIProject.mode == 'PRODUCTION').count()
print(f"Production projects: {count}")
db.close()
EOF
```

## Troubleshooting

### Port Already in Use
```bash
# Change ports in docker-compose.yml
# Or kill existing containers:
docker compose down
```

### Database Issues
```bash
# Rebuild from scratch
rm -f backend/cims.db
docker compose restart
```

### Clear All Data
```bash
docker compose down -v  # Remove volumes too
```

## Notes
- All source code included in repository
- Database file (`backend/cims.db`) is the only changeable file
- Use `cims_production_backup_rev2.db` to restore to this version
- Demo mode has 133 sample projects for testing
