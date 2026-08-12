#!/bin/bash
# Bootstrap script - Run after cloning CIMS repository
# This script sets up the database with production data

set -e

echo "🚀 CIMS Bootstrap - Setting up production data"
echo "================================================"
echo ""

# Check if seed file exists
if [ ! -f "backend/seed_production_data.json" ]; then
    echo "❌ Error: backend/seed_production_data.json not found"
    echo "Make sure you cloned the repository correctly"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required"
    exit 1
fi

echo "📥 Restoring production database from seed file..."
python3 backend/restore_production_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Database restored successfully!"
    echo ""
    echo "🐳 Next steps:"
    echo "  1. docker compose up -d"
    echo "  2. Open http://localhost in your browser"
    echo "  3. Login: admin / password123"
    echo ""
else
    echo ""
    echo "❌ Database restore failed"
    exit 1
fi
