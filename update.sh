#!/bin/bash
# Update CIMS from Git on a machine with existing running instance
# This script safely pulls latest changes and restores updated database

set -e

echo "🔄 CIMS Update from Git"
echo "================================"
echo ""

# Check if Docker is running
if ! docker ps &> /dev/null; then
    echo "❌ Error: Docker is not running"
    exit 1
fi

echo "📌 Current Status:"
docker compose ps 2>/dev/null || echo "  ⚠️  Containers not running yet"
echo ""

# Step 1: Backup current database
echo "📦 Step 1: Backing up current database..."
BACKUP_FILE="backend/cims_backup_$(date +%Y%m%d_%H%M%S).db"
if [ -f "backend/cims.db" ]; then
    cp backend/cims.db "$BACKUP_FILE"
    echo "  ✅ Backed up to: $BACKUP_FILE"
else
    echo "  ⚠️  No current database found"
fi

echo ""
echo "🔄 Step 2: Pulling latest from Git..."

# Step 2: Stash local changes (if any)
STASH_RESULT=$(git stash 2>&1 || echo "No changes to stash")
if [[ $STASH_RESULT == *"Saved"* ]]; then
    echo "  ✅ Local changes stashed"
elif [[ $STASH_RESULT == *"No changes"* ]]; then
    echo "  ✅ No local changes"
else
    echo "  ℹ️  $STASH_RESULT"
fi

# Step 3: Pull latest code
git pull origin main
echo "  ✅ Latest code pulled"

echo ""
echo "🔄 Step 3: Restoring production data..."

# Step 4: Restore production data from seed file
if [ -f "backend/seed_production_data.json" ]; then
    python3 backend/restore_production_data.py
    echo "  ✅ Production data restored"
else
    echo "  ❌ Error: seed_production_data.json not found"
    exit 1
fi

echo ""
echo "🐳 Step 4: Restarting Docker containers..."

# Step 5: Rebuild and restart
docker compose down
docker compose build
docker compose up -d

echo "  ✅ Containers restarted"

# Step 6: Wait for containers to start
echo ""
echo "⏳ Waiting for services to start..."
sleep 8

# Step 7: Verify
echo ""
echo "✅ Verification:"
docker compose ps

echo ""
echo "📊 Database Status:"
docker compose exec cims_backend python3 << 'EOF' 2>/dev/null || echo "  (Containers still starting...)"
from app.database import SessionLocal
from app.models.ci_project import CIProject
db = SessionLocal()
prod = db.query(CIProject).filter(CIProject.mode == 'PRODUCTION').count()
demo = db.query(CIProject).filter(CIProject.mode == 'DEMO').count()
print(f"  Production projects: {prod}")
print(f"  Demo projects: {demo}")
db.close()
EOF

echo ""
echo "✅ Update Complete!"
echo ""
echo "📍 Access application:"
echo "  URL: http://localhost"
echo "  Login: admin / password123"
echo ""
echo "🔙 If you need to rollback:"
echo "  cp $BACKUP_FILE backend/cims.db"
echo "  docker compose restart backend"
