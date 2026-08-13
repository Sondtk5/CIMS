# CIMS Data Sharing & Export Guide

## Quick Summary

**Problem:** When you edit projects locally, other machines running `./update.sh` don't get your edits.

**Solution:** Use `export_data.py` to capture your edits, then commit to Git.

---

## Workflow: Share Your Edits

### Step 1: Make Edits Locally
```
http://localhost → Edit projects → Save
```

### Step 2: Export Your Data
```bash
python3 export_data.py
```

**Output:**
```
✅ EXPORTED SUCCESSFULLY

📊 Summary:
   Production projects: 6
   Demo projects: 133

📋 Production Projects:
   UTIV-EN-R-26-0001-02-001: Stain 2 Defect Improvement
       └─ cost_saving: $99,999.00
   UTIV-EN-R-26-0001-02-002: Slit Coater - Takt Time Improvement
       └─ cost_saving: $18,500.00
   ...

📝 Saved to: backend/seed_production_data.json
```

### Step 3: Verify Data Exported
```bash
# Check the exported data looks right
sqlite3 backend/cims.db "SELECT ci_no, cost_saving FROM ci_projects WHERE mode='PRODUCTION';"
```

### Step 4: Commit & Push to Git
```bash
git add backend/seed_production_data.json
git commit -m "Update: Latest production data with edits"
git push origin main
```

### Step 5: Other Machines Pull & Update
On another machine:
```bash
cd /path/to/CIMS
git pull origin main
./update.sh
# Result: Gets your latest edits!
```

---

## When to Use Each Command

| Situation | Command | Result |
|-----------|---------|--------|
| **First time install** | `./bootstrap.sh` | Fresh install with all 6 prod + 133 demo projects |
| **Update existing running instance** | `./update.sh` | Latest code + data from seed file |
| **After editing projects locally** | `python3 export_data.py` | Exports to seed file (for sharing) |
| **Want to share edits with others** | `git add + git commit + git push` | Other machines can pull & get your edits |
| **Emergency: Recover from backup** | `python3 backend/restore_production_data.py` | Restores from seed file |

---

## Data Flow Explained

### BEFORE (Without Export)
```
Machine A (Edit project → Save)
  ↓
  Saved in: backend/cims.db (LOCAL ONLY)
  ↓
Machine B (git pull + ./update.sh)
  ↓
  Restores from: seed file (OLD data, no edits)
  ❌ Edits not shared!
```

### AFTER (With Export)
```
Machine A (Edit → Save → export_data.py)
  ↓
  Exported to: backend/seed_production_data.json (UPDATED)
  ↓
  Committed: git add + git commit + git push
  ↓
Machine B (git pull + ./update.sh)
  ↓
  Restores from: seed file (CURRENT data with edits)
  ✅ Edits shared successfully!
```

---

## Example: Share Cost Savings Update

### Machine A (Local)
```bash
# 1. Edit project 001, change cost_saving to $99,999
# 2. Click Save (saves to backend/cims.db)

# 3. Export
python3 export_data.py

# Output:
# UTIV-EN-R-26-0001-02-001: Stain 2 Defect Improvement
#     └─ cost_saving: $99,999.00

# 4. Commit
git add backend/seed_production_data.json
git commit -m "Update: Project 001 cost_saving to 99999"
git push origin main
```

### Machine B (Remote)
```bash
# 1. Pull latest
git pull origin main

# 2. Update
./update.sh

# 3. Result: Project 001 now shows cost_saving: $99,999 ✅
```

---

## Important Notes

### Database vs Seed File
- **backend/cims.db** (LOCAL - NOT in Git)
  - Active database where you edit projects
  - Changes are LIVE but LOCAL ONLY
  - Grows as you add projects

- **backend/seed_production_data.json** (IN Git)
  - Snapshot of data
  - When you export, captures all current data
  - Shared across machines via Git
  - Used by restore_production_data.py and update.sh

### Idempotent Restore
`restore_production_data.py` is **idempotent**:
- ✅ Won't delete existing projects
- ✅ Won't overwrite user edits
- ✅ Will add new projects from seed file
- ✅ Safe to run multiple times

Example:
```
Before: 7 projects (6 original + 1 you created)
Export & Restore with seed (6 projects)
After: 7 projects (6 original + 1 you created still there!)
```

### Handling Merge Conflicts
If multiple people edit the same project:

```bash
# You see conflict in seed file
git status
# backend/seed_production_data.json has conflict

# Option 1: Keep yours
git checkout --ours backend/seed_production_data.json
git add backend/seed_production_data.json

# Option 2: Keep theirs
git checkout --theirs backend/seed_production_data.json
git add backend/seed_production_data.json

# Then complete merge
git commit -m "Merge: Resolved data conflict, keeping [yours/theirs]"
```

---

## Troubleshooting

### Problem: "No changes to export"
```bash
python3 export_data.py
# Output: Exported 6 production, same as before
```
**Solution:** You haven't made edits yet, or edits didn't save.
- Verify edits saved: Check http://localhost to see current state
- Try again after editing

### Problem: "Other machine still shows old data"
```bash
# On other machine after git pull + ./update.sh
# Still shows old cost_saving values
```
**Solution:** Restart backend container:
```bash
docker compose restart backend
# Or full restart:
docker compose down && docker compose up -d
```

### Problem: "Database locked - can't export"
```bash
python3 export_data.py
# Error: database is locked
```
**Solution:** Database is being used by running container:
```bash
# Wait a moment and try again, or restart container:
docker compose restart backend
sleep 2
python3 export_data.py
```

---

## Best Practices

1. **Export regularly** after making important edits
   ```bash
   python3 export_data.py
   ```

2. **Commit with descriptive messages**
   ```bash
   git commit -m "Update: Fixed project 001 cost_saving and project 002 DMAIC"
   ```

3. **Test on another machine** before committing to main branch
   ```bash
   git branch test-export
   git push origin test-export
   # Test on another machine
   git merge test-export  # when happy
   ```

4. **Back up before major exports**
   ```bash
   cp backend/cims.db backend/cims_backup_$(date +%Y%m%d).db
   python3 export_data.py
   ```

5. **Pull before editing** to get latest from others
   ```bash
   git pull origin main
   ./update.sh
   # Now edit locally
   ```

---

## Full Workflow Example

```bash
# Machine A (Your machine)
# 1. Make sure you have latest
git pull origin main

# 2. Start/restart containers
docker compose restart backend

# 3. Edit projects at http://localhost

# 4. Export your edits
python3 export_data.py

# 5. Commit and push
git add backend/seed_production_data.json
git commit -m "Update: Completed project 001 with actual cost savings"
git push origin main

# ---

# Machine B (Another user's machine)
# 1. Pull latest
git pull origin main

# 2. Update database with latest data
./update.sh
# Or manually:
# python3 backend/restore_production_data.py
# docker compose restart backend

# 3. Verify: Open http://localhost
#    ✅ Sees project 001 with your cost savings!
```

---

## Summary

| Task | Command | Where |
|------|---------|-------|
| Install on new machine | `./bootstrap.sh` | New machine |
| Update existing machine | `./update.sh` | Running machine |
| Export edits | `python3 export_data.py` | After editing |
| Share edits | `git add + commit + push` | Local machine |
| Restore from backup | `python3 backend/restore_production_data.py` | Any machine |

**Key Point:** Always `export_data.py` before committing to ensure seed file has your latest edits!
