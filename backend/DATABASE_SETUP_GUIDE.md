# Database Setup Script Guide

## 📄 File: `create_database_and_tables.py`

This Python script provides a **complete automated setup** for the PlantCare AI database, including:

- ✅ Database creation with UTF8MB4 encoding
- ✅ All 17 tables with proper schemas
- ✅ Foreign key relationships (18 constraints)
- ✅ Indexes for performance optimization
- ✅ Cascade delete rules
- ✅ Verification and validation

## 🚀 Quick Start

### Prerequisites

1. **MySQL 5.7+ or MySQL 8.0+** must be installed and running
2. **Python 3.8+** must be installed
3. **MySQL connector** for Python (will be installed below)

### Installation

```bash
# Navigate to backend directory
cd backend

# Install MySQL connector
pip install mysql-connector-python

# OR add to existing requirements
pip install -r requirements.txt
```

### Usage

**Method 1: Interactive Mode (Recommended for first-time setup)**

```bash
python create_database_and_tables.py
```

The script will prompt you for:
- MySQL username (default: root)
- MySQL password
- Database name (default: plantcare_db)

**Method 2: Using Environment Variables**

```bash
# Set environment variables
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DB=plantcare_db

# Run script (will use environment variables)
python create_database_and_tables.py
```

**Windows PowerShell:**

```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="your_password"
$env:MYSQL_DB="plantcare_db"

python create_database_and_tables.py
```

## 📊 What This Script Does

### Step 1: Database Creation

```sql
CREATE DATABASE plantcare_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci
```

- Creates database with full Unicode support (emojis, international characters)
- Checks if database already exists
- Offers to drop and recreate if needed

### Step 2: Table Creation (17 Tables)

Creates tables in dependency order:

1. **users** - Core authentication table
2. **disease_info** - Reference data
3. **weather_data** - Weather cache
4. **farms** - Farm management
5. **crops** - Crop tracking
6. **monitored_crops** - Active crop monitoring
7. **farm_notes** - Farm observations
8. **disease_detections** - Legacy disease scans
9. **disease_scans** - Modern disease detection
10. **forum_posts** - Community discussions
11. **forum_replies** - Post responses
12. **forum_votes** - Voting system
13. **farm_ledger** - Financial transactions
14. **calculator_results** - Calculator outputs
15. **calculator_history** - Calculation history
16. **crop_recommendations** - ML crop suggestions
17. **crop_yield_predictions** - ML yield forecasts

### Step 3: Verification

- Lists all created tables
- Shows foreign key relationships
- Validates database structure

## 🎨 Features

### ✨ User-Friendly Output

- Color-coded messages:
  - 🟢 **Green** for success
  - 🔴 **Red** for errors
  - 🟡 **Yellow** for warnings
  - 🔵 **Blue** for information

### 🔒 Safe Operations

- Checks if tables exist before creating
- Asks for confirmation before dropping database
- Handles errors gracefully
- Provides detailed error messages

### 📈 Progress Tracking

- Shows real-time progress: "Table 5/17 created"
- Reports success/failure for each operation
- Final summary with statistics

## 📋 Complete Table Schemas

### Core Tables

#### 1. users
```sql
- id (INT, PRIMARY KEY)
- email (VARCHAR(120), UNIQUE)
- password_hash (VARCHAR(255))
- name (VARCHAR(64))
- phone (VARCHAR(20))
- date_joined (DATETIME)
- role (VARCHAR(20))
```

#### 2. farms
```sql
- id (INT, PRIMARY KEY)
- name (VARCHAR(90))
- location (VARCHAR(128))
- main_crop (VARCHAR(64))
- size_acres (FLOAT)
- soil_type (VARCHAR(64))
- is_active (BOOLEAN)
- created_at (DATETIME)
- user_id (INT, FK → users.id)
```

#### 3. crops
```sql
- id (INT, PRIMARY KEY)
- name (VARCHAR(64))
- variety (VARCHAR(64))
- planted_date (DATE)
- expected_harvest (DATE)
- status (VARCHAR(32))
- health_score (FLOAT)
- farm_id (INT, FK → farms.id)
```

### Feature Tables

#### 4. monitored_crops
```sql
- id (INT, PRIMARY KEY)
- name (VARCHAR(100))
- farm_name (VARCHAR(90))
- farm_id (INT, FK → farms.id, NULLABLE)
- planting_date (DATE)
- status (ENUM: Healthy, Needs Attention, Harvested)
- variety (VARCHAR(100))
- expected_harvest_date (DATE)
- health_score (FLOAT)
- notes (TEXT)
- user_id (INT, FK → users.id)
- created_at, updated_at (DATETIME)
```

#### 5. farm_notes
```sql
- id (INT, PRIMARY KEY)
- content (TEXT)
- created_at, updated_at (DATETIME)
- farm_id (INT, FK → farms.id)
- user_id (INT, FK → users.id)
```

### Disease Detection Tables

#### 6. disease_detections (Legacy)
```sql
- id (INT, PRIMARY KEY)
- user_id (INT, FK → users.id)
- plant_type (VARCHAR(50))
- image_path (VARCHAR(200))
- predicted_disease (VARCHAR(100))
- scientific_name (VARCHAR(100))
- confidence_score (FLOAT)
- severity (VARCHAR(20))
- detected_at (DATETIME)
- details (JSON)
```

#### 7. disease_scans (Modern)
```sql
- id (INT, PRIMARY KEY)
- user_id (INT, FK → users.id)
- image_data (LONGBLOB)
- image_path (VARCHAR(255))
- image_filename (VARCHAR(100))
- image_mimetype (VARCHAR(50))
- is_confident (BOOLEAN)
- confidence_threshold (FLOAT)
- disease_name (VARCHAR(100))
- confidence_score (FLOAT)
- description, treatment (TEXT)
- possible_diseases (TEXT/JSON)
- plant_type (VARCHAR(50))
- scan_timestamp (DATETIME)
- processing_time (FLOAT)
- model_version (VARCHAR(20))
- status (ENUM: pending, completed, failed)
- error_message (TEXT)
```

#### 8. disease_info (Reference)
```sql
- id (INT, PRIMARY KEY)
- name (VARCHAR(100), UNIQUE)
- scientific_name (VARCHAR(100))
- description (TEXT)
- symptoms, treatment, prevention (JSON)
- affected_plants, severity_levels (JSON)
```

### Community Tables

#### 9. forum_posts
```sql
- id (INT, PRIMARY KEY)
- user_id (INT, FK → users.id)
- title (VARCHAR(150))
- content (TEXT)
- category (VARCHAR(64))
- is_expert_question (BOOLEAN)
- created_at (DATETIME)
- status (VARCHAR(32))
- views (INT)
- is_flagged (BOOLEAN)
- flagged_reason (VARCHAR(200))
- reply_count (INT)
- solved (BOOLEAN)
- upvotes, downvotes (INT)
- edited_at (DATETIME)
- edit_count (INT)
```

#### 10. forum_replies
```sql
- id (INT, PRIMARY KEY)
- user_id (INT, FK → users.id)
- post_id (INT, FK → forum_posts.id)
- content (TEXT)
- is_expert_reply, is_accepted (BOOLEAN)
- created_at (DATETIME)
- is_flagged (BOOLEAN)
- flagged_reason (VARCHAR(200))
- helpful_count (INT)
- edited_at (DATETIME)
- edit_count (INT)
```

#### 11. forum_votes
```sql
- id (INT, PRIMARY KEY)
- user_id (INT, FK → users.id)
- post_id (INT, FK → forum_posts.id)
- vote_type (VARCHAR(10))
- created_at (DATETIME)
- UNIQUE(user_id, post_id)
```

### Financial Tables

#### 12. farm_ledger
```sql
- id (INT, PRIMARY KEY)
- user_id (INT, FK → users.id)
- amount (FLOAT)
- category (VARCHAR(64))
- note (VARCHAR(128))
- transaction_type (VARCHAR(16))
- transaction_date (DATE)
- created_at (DATETIME)
```

### Calculator Tables

#### 13. calculator_results
```sql
- id (INT, PRIMARY KEY)
- user_id (INT, FK → users.id)
- calculator_type (VARCHAR(32))
- input_data, result_data (JSON)
- notes (VARCHAR(256))
- created_at (DATETIME)
```

#### 14. calculator_history
```sql
- id (INT, PRIMARY KEY)
- user_id (INT, FK → users.id)
- calculation_type (VARCHAR(50))
- inputs, results (JSON)
- created_at (DATETIME)
```

### ML Tables

#### 15. crop_recommendations
```sql
- id (INT, PRIMARY KEY)
- user_id (INT, FK → users.id, NULLABLE)
- nitrogen, phosphorus, potassium (FLOAT)
- temperature, humidity, ph, rainfall (FLOAT)
- predicted_crop (VARCHAR(100))
- confidence (FLOAT)
- created_at (DATETIME)
```

#### 16. crop_yield_predictions
```sql
- id (INT, PRIMARY KEY)
- user_id (INT, FK → users.id, NULLABLE)
- crop (VARCHAR(100))
- season (VARCHAR(50))
- state (VARCHAR(100))
- annual_rainfall, fertilizer, pesticide (FLOAT)
- predicted_yield (FLOAT)
- unit (VARCHAR(20))
- created_at (DATETIME)
```

#### 17. weather_data
```sql
- id (INT, PRIMARY KEY)
- location (VARCHAR(128))
- temperature, humidity (FLOAT)
- weather_condition (VARCHAR(64))
- wind_speed, rainfall (FLOAT)
- forecast_date (DATE)
- created_at (DATETIME)
```

## 🔗 Foreign Key Relationships

| Child Table | Column | References | Cascade Delete |
|-------------|--------|------------|----------------|
| farms | user_id | users.id | ✅ CASCADE |
| crops | farm_id | farms.id | ✅ CASCADE |
| monitored_crops | user_id | users.id | ✅ CASCADE |
| monitored_crops | farm_id | farms.id | ❌ SET NULL |
| farm_notes | farm_id | farms.id | ✅ CASCADE |
| farm_notes | user_id | users.id | ✅ CASCADE |
| disease_detections | user_id | users.id | ✅ CASCADE |
| disease_scans | user_id | users.id | ✅ CASCADE |
| forum_posts | user_id | users.id | ✅ CASCADE |
| forum_replies | user_id | users.id | ✅ CASCADE |
| forum_replies | post_id | forum_posts.id | ✅ CASCADE |
| forum_votes | user_id | users.id | ✅ CASCADE |
| forum_votes | post_id | forum_posts.id | ✅ CASCADE |
| farm_ledger | user_id | users.id | ✅ CASCADE |
| calculator_results | user_id | users.id | ✅ CASCADE |
| calculator_history | user_id | users.id | ✅ CASCADE |
| crop_recommendations | user_id | users.id | ❌ SET NULL |
| crop_yield_predictions | user_id | users.id | ❌ SET NULL |

**Total: 18 Foreign Key Constraints**

## 🛠️ Troubleshooting

### Error: "Can't connect to MySQL server"

**Solution:**
```bash
# Check if MySQL is running
# Windows
net start | findstr MySQL

# Linux
sudo systemctl status mysql
sudo systemctl start mysql
```

### Error: "Access denied for user"

**Solution:**
- Verify MySQL credentials
- Ensure user has CREATE DATABASE privilege
- Try connecting manually: `mysql -u root -p`

### Error: "Module 'mysql.connector' not found"

**Solution:**
```bash
pip install mysql-connector-python
```

### Error: "Database already exists"

**Solution:**
- Script will prompt to drop and recreate
- Or manually: `DROP DATABASE plantcare_db;`
- Or use different database name

### Error: "Table already exists"

**Solution:**
- Script uses `CREATE TABLE IF NOT EXISTS`
- Should skip existing tables automatically
- If issues persist, drop and recreate database

## 📝 Example Output

```
============================================================
PlantCare AI - Database Setup Script
============================================================

ℹ️  MySQL Connection Setup
============================================================
MySQL User (default: root): root
MySQL Password for root: ********
Database Name (default: plantcare_db): plantcare_db

ℹ️  Starting database setup...
============================================================

📦 Step 1/3: Creating database...
✅ Database 'plantcare_db' created successfully with UTF8MB4 encoding

📊 Step 2/3: Creating tables...
ℹ️  Connected to database: plantcare_db
ℹ️  Creating tables...
============================================================
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
============================================================
✅ Successfully created 17/17 tables

✓ Step 3/3: Verifying setup...
============================================================
📊 Total tables: 17

📋 Tables created:
   1. calculator_history
   2. calculator_results
   3. crop_recommendations
   4. crop_yield_predictions
   5. crops
   6. disease_detections
   7. disease_info
   8. disease_scans
   9. farm_ledger
   10. farm_notes
   11. farms
   12. forum_posts
   13. forum_replies
   14. forum_votes
   15. monitored_crops
   16. users
   17. weather_data

🔗 Foreign Key Relationships:
   calculator_history.user_id → users.id
   calculator_results.user_id → users.id
   [... 16 more relationships ...]

📊 Total foreign key constraints: 18

============================================================
✅ Database setup completed successfully!
============================================================
```

## 🆚 Comparison with Other Methods

| Feature | This Script | Flask Migrate | Manual SQL |
|---------|-------------|---------------|------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐ Medium | ⭐⭐ Hard |
| **Interactive** | ✅ Yes | ❌ No | ❌ No |
| **Verification** | ✅ Built-in | ❌ Manual | ❌ Manual |
| **Error Handling** | ✅ Comprehensive | ⭐ Basic | ❌ None |
| **Progress Display** | ✅ Real-time | ❌ Silent | ❌ None |
| **No Flask Required** | ✅ Standalone | ❌ Needs Flask | ✅ Standalone |

## 🎯 When to Use This Script

✅ **Use this script when:**
- Setting up database for the first time
- Flask migrations are failing
- Need to recreate database from scratch
- Want visual confirmation of setup progress
- Need standalone database setup tool

❌ **Use Flask migrations when:**
- Making schema changes to existing database
- Need version control for database changes
- Working in development with frequent model updates

## 📚 Additional Resources

- [DATABASE_README.md](DATABASE_README.md) - Comprehensive database documentation
- [README.md](../README.md) - Main project documentation
- `check_crop_db_status.py` - Verify database status
- `create_crop_tables.py` - Create specific tables

## 🔐 Security Notes

1. **Never commit database passwords** to version control
2. **Use environment variables** for production
3. **Create dedicated database user** (don't use root)
4. **Limit user privileges** to only what's needed
5. **Enable SSL/TLS** for remote database connections
6. **Regular backups** are essential

## 📞 Support

If you encounter issues:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Verify MySQL is running and accessible
3. Check MySQL error logs
4. Ensure proper privileges for database user
5. Review [DATABASE_README.md](DATABASE_README.md) for detailed schema info

---

**Created by:** PlantCare AI Team  
**Last Updated:** 2024  
**License:** MIT
