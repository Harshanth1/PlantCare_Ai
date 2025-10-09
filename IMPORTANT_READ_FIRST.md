# ⚠️ IMPORTANT - READ BEFORE STARTING THE PROJECT

## 🔴 MANDATORY PREREQUISITE - DATABASE SETUP

**YOU MUST RUN THE DATABASE SETUP SCRIPT BEFORE STARTING THE PROJECT!**

The PlantCare AI application **WILL NOT WORK** without a properly configured MySQL database with all required tables.

---

## ⚡ Quick Setup (5 Minutes)

### Step 1: Ensure MySQL is Running

```bash
# Check if MySQL is running
# Windows
net start | findstr MySQL

# If not running, start it
net start MySQL80  # Replace with your MySQL service name
```

### Step 2: Run the Database Setup Script

```bash
# Navigate to backend directory
cd backend

# Install MySQL connector (one-time only)
pip install mysql-connector-python

# Run the database creation script
python create_database_and_tables.py
```

### Step 3: Follow the Interactive Prompts

The script will ask you:
1. **MySQL Username** (default: `root`)
2. **MySQL Password** (enter your MySQL password)
3. **Database Name** (default: `plantcare_db`)

Example:
```
MySQL User (default: root): root
MySQL Password for root: ********
Database Name (default: plantcare_db): [Press Enter]

✅ Database 'plantcare_db' created successfully
✅ Table 1/17: users
✅ Table 2/17: disease_info
...
✅ Table 17/17: crop_yield_predictions
✅ Successfully created 17/17 tables

📊 Total tables: 17
📊 Total foreign key constraints: 18

✅ Database setup completed successfully!
```

### Step 4: Configure Environment Variables

Edit `backend/.env`:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=plantcare_db

SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 5: Now Start the Project

```bash
# Terminal 1: Start Backend
cd backend
python run.py

# Terminal 2: Start Frontend
cd frontend
npm start
```

---

## 🚫 What Happens If You Skip This Step?

If you try to run the project **WITHOUT** creating the database first, you will get errors like:

❌ **Error 1:** `Unknown database 'plantcare_db'`
```
pymysql.err.OperationalError: (1049, "Unknown database 'plantcare_db'")
```

❌ **Error 2:** `Can't connect to database`
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError)
```

❌ **Error 3:** `Table doesn't exist`
```
(1146, "Table 'plantcare_db.users' doesn't exist")
```

**Solution:** Run the database setup script **FIRST**!

---

## 📊 What the Script Creates

The `create_database_and_tables.py` script automatically creates:

### ✅ Database
- Creates `plantcare_db` database
- Sets UTF8MB4 character encoding (for emoji & international character support)

### ✅ 17 Tables
1. **users** - User authentication & profiles
2. **farms** - Farm management system
3. **crops** - Individual crop tracking
4. **monitored_crops** - Active crop monitoring
5. **farm_notes** - Farm observations & notes
6. **disease_detections** - Legacy disease detection
7. **disease_scans** - Modern AI-powered disease detection
8. **disease_info** - Disease reference database
9. **forum_posts** - Community discussion forum
10. **forum_replies** - Responses to forum posts
11. **forum_votes** - Voting system (upvote/downvote)
12. **farm_ledger** - Financial transaction tracking
13. **calculator_results** - Calculator outputs (fertilizer, pesticide, profit)
14. **calculator_history** - Historical calculation records
15. **crop_recommendations** - AI-based crop suggestions
16. **crop_yield_predictions** - ML-based yield forecasting
17. **weather_data** - Weather information cache

### ✅ 18 Foreign Key Relationships
- Properly linked tables to maintain data integrity
- CASCADE DELETE rules where appropriate
- SET NULL for optional relationships

### ✅ Performance Indexes
- Indexes on frequently queried columns
- Primary keys with AUTO_INCREMENT
- Unique constraints where needed

---

## 🔍 Verify Database Setup

After running the script, verify everything is working:

```bash
cd backend
python check_crop_db_status.py
```

Expected output:
```
=== DATABASE TABLES STATUS ===
Total tables: 17
- crop_recommendations: True
- crop_yield_predictions: True
[... all tables listed ...]
```

---

## 🆘 Troubleshooting

### Problem: "Can't connect to MySQL server"

**Solution:**
```bash
# Check MySQL status
net start | findstr MySQL

# Start MySQL if not running
net start MySQL80
```

### Problem: "Access denied for user 'root'"

**Solutions:**
1. Verify you're entering the correct MySQL password
2. Try resetting MySQL root password
3. Create a dedicated database user instead

### Problem: "Module 'mysql.connector' not found"

**Solution:**
```bash
pip install mysql-connector-python
```

### Problem: "Database already exists"

**Solution:**
The script will ask if you want to:
- Drop and recreate (type `yes`) - **⚠️ WARNING: Deletes all data!**
- Use existing database (type `no`)

---

## 📋 Complete Setup Checklist

Before running the project, ensure:

- [ ] **MySQL 5.7+ or 8.0+** installed and running
- [ ] **Python 3.8+** installed
- [ ] **Node.js 16+** and npm installed
- [ ] **Ran** `python create_database_and_tables.py` ✅ **MANDATORY**
- [ ] **Verified** database setup with `python check_crop_db_status.py`
- [ ] **Configured** `backend/.env` with database credentials
- [ ] **Configured** `backend/.env` with Gemini API key
- [ ] **Installed** backend dependencies: `pip install -r requirements.txt`
- [ ] **Installed** frontend dependencies: `npm install`

**Only after completing ALL steps above**, you can:
- [ ] Start backend: `python run.py`
- [ ] Start frontend: `npm start`
- [ ] Access application at `http://localhost:3000`

---

## 🎯 Why This Script is Mandatory

### The Application Architecture:

```
Frontend (React) 
    ↓ API Calls
Backend (Flask)
    ↓ Database Queries
MySQL Database ← YOU ARE HERE (Must setup first!)
    ↓ Contains:
    - 17 Tables
    - 18 Foreign Keys
    - User Data
    - Application Data
```

**Without the database:**
- ❌ Backend cannot start
- ❌ API endpoints will fail
- ❌ User authentication won't work
- ❌ No data storage or retrieval
- ❌ Application is completely non-functional

**With the database:**
- ✅ Backend starts successfully
- ✅ All API endpoints work
- ✅ User authentication functions
- ✅ Data is stored and retrieved
- ✅ Full application functionality

---

## 🚀 One-Command Setup (Advanced)

If you prefer environment variables over interactive prompts:

```bash
# Set environment variables
set MYSQL_USER=root
set MYSQL_PASSWORD=your_password
set MYSQL_DB=plantcare_db

# Run script (no prompts)
cd backend
pip install mysql-connector-python
python create_database_and_tables.py
```

**Linux/Mac:**
```bash
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DB=plantcare_db

cd backend
pip install mysql-connector-python
python create_database_and_tables.py
```

---

## 📚 Additional Documentation

For more detailed information, see:

- **`backend/DATABASE_SETUP_GUIDE.md`** - Complete usage guide
- **`DATABASE_README.md`** - Full database schema documentation
- **`QUICK_START_DATABASE.md`** - Quick reference guide
- **`README.md`** - Main project documentation

---

## ⏱️ Time Estimate

- **Database setup:** 2-5 minutes
- **Backend setup:** 5 minutes
- **Frontend setup:** 3 minutes
- **Total:** ~10-15 minutes

---

## 🎉 Summary

**BEFORE running the project:**
```bash
cd backend
pip install mysql-connector-python
python create_database_and_tables.py
```

**AFTER database is created:**
```bash
# Configure .env files
# Then start the application

# Terminal 1
cd backend
python run.py

# Terminal 2
cd frontend
npm start
```

---

## ⚠️ REMEMBER

**The database setup script (`create_database_and_tables.py`) is NOT optional!**

It is a **MANDATORY PREREQUISITE** that must be completed before the PlantCare AI application can function.

**DO NOT SKIP THIS STEP!**

---

**Created:** October 9, 2025  
**Priority:** 🔴 CRITICAL - MUST READ FIRST  
**Status:** MANDATORY PREREQUISITE
