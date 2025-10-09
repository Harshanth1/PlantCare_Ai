# 🔴 MANDATORY: Run This Script First!

## Database Setup Script
**File:** `create_database_and_tables.py`

---

## ⚡ Quick Start (2 Minutes)

```bash
# 1. Navigate to backend
cd backend

# 2. Install MySQL connector
pip install mysql-connector-python

# 3. Run the script
python create_database_and_tables.py

# 4. Enter when prompted:
#    - MySQL Username: root
#    - MySQL Password: (your password)
#    - Database Name: plantcare_db
```

✅ **Done!** Database and all 17 tables created automatically.

---

## 🎯 What This Script Does

Creates everything your application needs:
- ✅ `plantcare_db` database
- ✅ 17 tables (users, farms, crops, etc.)
- ✅ 18 foreign key relationships
- ✅ Performance indexes
- ✅ Proper character encoding (UTF8MB4)

---

## 📺 Example Output

```
============================================================
PlantCare AI - Database Setup Script
============================================================

MySQL User (default: root): root
MySQL Password for root: ********
Database Name (default: plantcare_db): [Enter]

📦 Step 1/3: Creating database...
✅ Database 'plantcare_db' created successfully

📊 Step 2/3: Creating tables...
✅ Table 1/17: users
✅ Table 2/17: disease_info
✅ Table 3/17: weather_data
✅ Table 4/17: farms
✅ Table 5/17: crops
✅ Table 6/17: monitored_crops
✅ Table 7/17: farm_notes
✅ Table 8/17: disease_detections
✅ Table 9/17: disease_scans
✅ Table 10/17: forum_posts
✅ Table 11/17: forum_replies
✅ Table 12/17: forum_votes
✅ Table 13/17: farm_ledger
✅ Table 14/17: calculator_results
✅ Table 15/17: calculator_history
✅ Table 16/17: crop_recommendations
✅ Table 17/17: crop_yield_predictions

✓ Step 3/3: Verifying setup...
📊 Total tables: 17
📊 Total foreign key constraints: 18

============================================================
✅ Database setup completed successfully!
============================================================
```

---

## 🚫 Don't Skip This!

**Without running this script:**
- ❌ Application won't start
- ❌ Backend will crash with database errors
- ❌ No user authentication
- ❌ No data storage

**After running this script:**
- ✅ Application works perfectly
- ✅ All features functional
- ✅ Ready for production

---

## 📚 Need Help?

- **[IMPORTANT_READ_FIRST.md](../IMPORTANT_READ_FIRST.md)** - Why this is required
- **[DATABASE_SETUP_GUIDE.md](DATABASE_SETUP_GUIDE.md)** - Complete guide
- **[DATABASE_README.md](../DATABASE_README.md)** - Full schema docs

---

**Remember:** Run this script BEFORE starting the application!
