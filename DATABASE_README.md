# PlantCare AI - Database Documentation

Complete database setup guide, schema documentation, and troubleshooting for the PlantCare AI application.

## 📋 Table of Contents

1. [Database Overview](#database-overview)
2. [Prerequisites](#prerequisites)
3. [Database Setup](#database-setup)
4. [Complete Database Schema](#complete-database-schema)
5. [Foreign Key Relationships](#foreign-key-relationships)
6. [Database Commands Reference](#database-commands-reference)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#frequently-asked-questions-faq)
9. [Security Best Practices](#security-best-practices)

---

## Database Overview

The PlantCare AI application uses **MySQL 5.7+** or **MySQL 8.0+** as its database system. The database contains **17 tables** with comprehensive foreign key relationships to maintain data integrity.

### Quick Statistics

- **Total Tables**: 17
- **User-dependent Tables**: 13
- **Reference Tables**: 2 (disease_info, weather_data)
- **Cache Tables**: 1 (weather_data)
- **Optional User Link**: 2 (crop_recommendations, crop_yield_predictions)
- **Foreign Key Relationships**: 18
- **Character Set**: UTF8MB4 (full Unicode support)

---

## Prerequisites

Before setting up the database, ensure you have:

- ✅ **MySQL 5.7+** or **MySQL 8.0+** installed and running
- ✅ **Root access** to MySQL or appropriate database privileges
- ✅ **Backend `.env` file** configured with database credentials

---

## Database Setup

### Step 1: Install MySQL

**Windows:**
```powershell
# Download from: https://dev.mysql.com/downloads/installer/
# Follow the installer wizard
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

### Step 2: Create Database

```sql
-- Login to MySQL
mysql -u root -p

-- Create database with proper character set
CREATE DATABASE plantcare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verify creation
SHOW DATABASES;

-- Exit
EXIT;
```

**Quick Command (One-liner):**
```bash
mysql -u root -p -e "CREATE DATABASE plantcare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### Step 3: Create Dedicated Database User (Recommended)

```sql
-- Login as root
mysql -u root -p

-- Create user
CREATE USER 'plantcare_user'@'localhost' IDENTIFIED BY 'YourSecurePassword123!';

-- Grant all privileges on plantcare_db
GRANT ALL PRIVILEGES ON plantcare_db.* TO 'plantcare_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Verify user creation
SELECT User, Host FROM mysql.user WHERE User = 'plantcare_user';

-- Exit
EXIT;
```

### Step 4: Configure Backend Environment

Edit `backend/.env` file:

```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=plantcare_user          # or 'root'
MYSQL_PASSWORD=YourSecurePassword123!
MYSQL_DB=plantcare_db
```

### Step 5: Create All Tables

**Method 1: Using Flask-Migrate (Recommended)**
```bash
cd backend

# Initialize migrations (if first time)
flask db init

# Generate migration
flask db migrate -m "Initial database setup"

# Apply migrations - creates all 17 tables
flask db upgrade
```

**Method 2: Manual Script**
```bash
cd backend
python create_crop_tables.py
```

**Method 3: Verify Setup**
```bash
cd backend
python check_crop_db_status.py
```

### Step 6: Verify Tables Created

```sql
-- Login to database
mysql -u root -p plantcare_db

-- List all tables (should show 17 tables)
SHOW TABLES;

-- Expected tables:
-- users, farms, crops, monitored_crops, farm_notes
-- disease_detections, disease_scans, disease_info
-- forum_posts, forum_replies, forum_votes
-- farm_ledger, calculator_results, calculator_history
-- crop_recommendations, crop_yield_predictions
-- weather_data, alembic_version

-- Check a specific table structure
DESCRIBE users;

-- Exit
EXIT;
```

---

## Complete Database Schema

### Quick Reference: All Database Tables

| # | Table Name | Purpose | Foreign Keys | Records User Data |
|---|------------|---------|--------------|-------------------|
| 1 | **users** | User authentication & profiles | None | ✅ Core |
| 2 | **farms** | Farm management | user_id → users | ✅ Yes |
| 3 | **crops** | Individual crop tracking | farm_id → farms | Via farm |
| 4 | **monitored_crops** | Active crop monitoring | user_id → users, farm_id → farms (optional) | ✅ Yes |
| 5 | **farm_notes** | Farm observations | user_id → users, farm_id → farms | ✅ Yes |
| 6 | **disease_detections** | Legacy disease detection | user_id → users | ✅ Yes |
| 7 | **disease_scans** | Modern disease scanning | user_id → users | ✅ Yes |
| 8 | **disease_info** | Disease reference data | None | ❌ Reference |
| 9 | **forum_posts** | Community discussions | user_id → users | ✅ Yes |
| 10 | **forum_replies** | Post replies | user_id → users, post_id → forum_posts | ✅ Yes |
| 11 | **forum_votes** | Post voting system | user_id → users, post_id → forum_posts | ✅ Yes |
| 12 | **farm_ledger** | Financial transactions | user_id → users | ✅ Yes |
| 13 | **calculator_results** | Calculator outputs | user_id → users | ✅ Yes |
| 14 | **calculator_history** | Calculation history | user_id → users | ✅ Yes |
| 15 | **crop_recommendations** | ML crop suggestions | user_id → users (optional) | 🔄 Optional |
| 16 | **crop_yield_predictions** | ML yield forecasts | user_id → users (optional) | 🔄 Optional |
| 17 | **weather_data** | Weather information | None | ❌ Cache |

---

### Detailed Table Schemas

#### 1. **users** (Core Table)
Primary user authentication and profile table.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `email` - VARCHAR(120), UNIQUE, NOT NULL
- `password_hash` - VARCHAR(255), NOT NULL
- `name` - VARCHAR(64), NOT NULL
- `phone` - VARCHAR(20), NULLABLE
- `date_joined` - DATETIME, DEFAULT: CURRENT_TIMESTAMP
- `role` - VARCHAR(20), DEFAULT: 'user'

**Relationships:**
- → One-to-Many with: farms, disease_detections, disease_scans, forum_posts, forum_replies, forum_votes, farm_ledger, monitored_crops, calculator_results, calculator_history, crop_recommendations, crop_yield_predictions, farm_notes

---

#### 2. **farms**
Stores farm information for each user.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `name` - VARCHAR(90), NOT NULL
- `location` - VARCHAR(128), NULLABLE
- `main_crop` - VARCHAR(64), NOT NULL
- `size_acres` - FLOAT, NOT NULL
- `soil_type` - VARCHAR(64), NULLABLE
- `is_active` - BOOLEAN, DEFAULT: FALSE
- `created_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP
- `user_id` - INT, FOREIGN KEY → users.id, NOT NULL

**Relationships:**
- ← Many-to-One with: users
- → One-to-Many with: crops, farm_notes, monitored_crops (optional)

---

#### 3. **crops**
Individual crop tracking within farms.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `name` - VARCHAR(64), NOT NULL
- `variety` - VARCHAR(64), NULLABLE
- `planted_date` - DATE, NULLABLE
- `expected_harvest` - DATE, NULLABLE
- `status` - VARCHAR(32), NULLABLE
- `health_score` - FLOAT, NULLABLE
- `farm_id` - INT, FOREIGN KEY → farms.id

**Relationships:**
- ← Many-to-One with: farms

---

#### 4. **monitored_crops**
Tracks crops being actively monitored by users.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `name` - VARCHAR(100), NOT NULL
- `farm_name` - VARCHAR(90), NOT NULL
- `farm_id` - INT, FOREIGN KEY → farms.id, NULLABLE
- `planting_date` - DATE, NOT NULL
- `status` - ENUM('Healthy', 'Needs Attention', 'Harvested'), DEFAULT: 'Healthy'
- `variety` - VARCHAR(100), NULLABLE
- `expected_harvest_date` - DATE, NULLABLE
- `health_score` - FLOAT, DEFAULT: 100.0
- `notes` - TEXT, NULLABLE
- `user_id` - INT, FOREIGN KEY → users.id, NOT NULL
- `created_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP
- `updated_at` - DATETIME, ON UPDATE: CURRENT_TIMESTAMP

**Relationships:**
- ← Many-to-One with: users (required)
- ← Many-to-One with: farms (optional)

---

#### 5. **farm_notes**
Notes and observations for farms.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `content` - TEXT, NOT NULL
- `created_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP
- `updated_at` - DATETIME, ON UPDATE: CURRENT_TIMESTAMP
- `farm_id` - INT, FOREIGN KEY → farms.id, NOT NULL
- `user_id` - INT, FOREIGN KEY → users.id, NOT NULL

**Relationships:**
- ← Many-to-One with: farms (CASCADE on delete)
- ← Many-to-One with: users

---

#### 6. **disease_detections**
Legacy disease detection records.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `user_id` - INT, FOREIGN KEY → users.id, NOT NULL
- `plant_type` - VARCHAR(50), NULLABLE
- `image_path` - VARCHAR(200), NULLABLE
- `predicted_disease` - VARCHAR(100), NULLABLE
- `scientific_name` - VARCHAR(100), NULLABLE
- `confidence_score` - FLOAT, NULLABLE
- `severity` - VARCHAR(20), NULLABLE
- `detected_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP
- `details` - JSON, NULLABLE

**Relationships:**
- ← Many-to-One with: users

---

#### 7. **disease_scans**
Modern disease scanning system with enhanced features.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `user_id` - INT, FOREIGN KEY → users.id, NOT NULL
- `image_data` - LONGBLOB, NULLABLE (Binary image storage)
- `image_path` - VARCHAR(255), NULLABLE
- `image_filename` - VARCHAR(100), NOT NULL
- `image_mimetype` - VARCHAR(50), NULLABLE
- `is_confident` - BOOLEAN, DEFAULT: FALSE
- `confidence_threshold` - FLOAT, DEFAULT: 0.8
- `disease_name` - VARCHAR(100), NULLABLE
- `confidence_score` - FLOAT, NULLABLE
- `description` - TEXT, NULLABLE
- `treatment` - TEXT, NULLABLE
- `possible_diseases` - TEXT, NULLABLE (JSON format)
- `plant_type` - VARCHAR(50), NULLABLE
- `scan_timestamp` - DATETIME, DEFAULT: CURRENT_TIMESTAMP
- `processing_time` - FLOAT, NULLABLE
- `model_version` - VARCHAR(20), DEFAULT: 'v1.0'
- `status` - ENUM('pending', 'completed', 'failed'), DEFAULT: 'pending'
- `error_message` - TEXT, NULLABLE

**Relationships:**
- ← Many-to-One with: users

---

#### 8. **disease_info**
Reference table for disease information.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `name` - VARCHAR(100), UNIQUE
- `scientific_name` - VARCHAR(100), NULLABLE
- `description` - TEXT, NULLABLE
- `symptoms` - JSON, NULLABLE
- `treatment` - JSON, NULLABLE
- `prevention` - JSON, NULLABLE
- `affected_plants` - JSON, NULLABLE
- `severity_levels` - JSON, NULLABLE

**Relationships:**
- None (standalone reference table)

---

#### 9. **forum_posts**
Community forum posts.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `user_id` - INT, FOREIGN KEY → users.id, NOT NULL
- `title` - VARCHAR(150), NOT NULL
- `content` - TEXT, NOT NULL
- `category` - VARCHAR(64), NULLABLE
- `is_expert_question` - BOOLEAN, DEFAULT: FALSE
- `created_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP
- `status` - VARCHAR(32), DEFAULT: 'open'
- `views` - INT, DEFAULT: 0
- `is_flagged` - BOOLEAN, DEFAULT: FALSE
- `flagged_reason` - VARCHAR(200), NULLABLE
- `reply_count` - INT, DEFAULT: 0
- `solved` - BOOLEAN, DEFAULT: FALSE
- `upvotes` - INT, DEFAULT: 0
- `downvotes` - INT, DEFAULT: 0
- `edited_at` - DATETIME, NULLABLE
- `edit_count` - INT, DEFAULT: 0

**Relationships:**
- ← Many-to-One with: users
- → One-to-Many with: forum_replies, forum_votes

---

#### 10. **forum_replies**
Replies to forum posts.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `user_id` - INT, FOREIGN KEY → users.id, NOT NULL
- `post_id` - INT, FOREIGN KEY → forum_posts.id, NOT NULL
- `content` - TEXT, NOT NULL
- `is_expert_reply` - BOOLEAN, DEFAULT: FALSE
- `is_accepted` - BOOLEAN, DEFAULT: FALSE
- `created_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP
- `is_flagged` - BOOLEAN, DEFAULT: FALSE
- `flagged_reason` - VARCHAR(200), NULLABLE
- `helpful_count` - INT, DEFAULT: 0
- `edited_at` - DATETIME, NULLABLE
- `edit_count` - INT, DEFAULT: 0

**Relationships:**
- ← Many-to-One with: users
- ← Many-to-One with: forum_posts (CASCADE on delete)

---

#### 11. **forum_votes**
Voting system for forum posts.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `user_id` - INT, FOREIGN KEY → users.id, NOT NULL
- `post_id` - INT, FOREIGN KEY → forum_posts.id, NOT NULL
- `vote_type` - VARCHAR(10), NOT NULL ('upvote' or 'downvote')
- `created_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP

**Constraints:**
- UNIQUE(user_id, post_id) - One vote per user per post

**Relationships:**
- ← Many-to-One with: users
- ← Many-to-One with: forum_posts (CASCADE on delete)

---

#### 12. **farm_ledger**
Financial transactions for farming activities.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `user_id` - INT, FOREIGN KEY → users.id, NOT NULL
- `amount` - FLOAT, NOT NULL
- `category` - VARCHAR(64), NOT NULL
- `note` - VARCHAR(128), NULLABLE
- `transaction_type` - VARCHAR(16), DEFAULT: 'expense' ('expense' or 'income')
- `transaction_date` - DATE, DEFAULT: CURRENT_DATE
- `created_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP

**Relationships:**
- ← Many-to-One with: users

---

#### 13. **calculator_results**
Results from various agricultural calculators.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `user_id` - INT, FOREIGN KEY → users.id, NOT NULL
- `calculator_type` - VARCHAR(32), NOT NULL ('fertilizer', 'pesticide', 'profit')
- `input_data` - JSON, NOT NULL
- `result_data` - JSON, NOT NULL
- `notes` - VARCHAR(256), NULLABLE
- `created_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP

**Relationships:**
- ← Many-to-One with: users

---

#### 14. **calculator_history**
Historical records of calculator usage.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `user_id` - INT, FOREIGN KEY → users.id, NOT NULL
- `calculation_type` - VARCHAR(50), NOT NULL
- `inputs` - JSON, NOT NULL
- `results` - JSON, NOT NULL
- `created_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP

**Relationships:**
- ← Many-to-One with: users

---

#### 15. **crop_recommendations**
ML-based crop recommendations.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `user_id` - INT, FOREIGN KEY → users.id, NULLABLE
- `nitrogen` - FLOAT, NOT NULL
- `phosphorus` - FLOAT, NOT NULL
- `potassium` - FLOAT, NOT NULL
- `temperature` - FLOAT, NOT NULL
- `humidity` - FLOAT, NOT NULL
- `ph` - FLOAT, NOT NULL
- `rainfall` - FLOAT, NOT NULL
- `predicted_crop` - VARCHAR(100), NOT NULL
- `confidence` - FLOAT, NULLABLE
- `created_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP

**Relationships:**
- ← Many-to-One with: users (optional)

---

#### 16. **crop_yield_predictions**
ML-based crop yield predictions.

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `user_id` - INT, FOREIGN KEY → users.id, NULLABLE
- `crop` - VARCHAR(100), NOT NULL
- `season` - VARCHAR(50), NOT NULL
- `state` - VARCHAR(100), NOT NULL
- `annual_rainfall` - FLOAT, NOT NULL
- `fertilizer` - FLOAT, NOT NULL
- `pesticide` - FLOAT, NOT NULL
- `predicted_yield` - FLOAT, NOT NULL
- `unit` - VARCHAR(20), DEFAULT: 'tons/hectare'
- `created_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP

**Relationships:**
- ← Many-to-One with: users (optional)

---

#### 17. **weather_data**
Weather information storage (cache).

**Columns:**
- `id` - INT, PRIMARY KEY, AUTO_INCREMENT
- `location` - VARCHAR(128), NULLABLE
- `temperature` - FLOAT, NULLABLE
- `humidity` - FLOAT, NULLABLE
- `weather_condition` - VARCHAR(64), NULLABLE
- `wind_speed` - FLOAT, NULLABLE
- `rainfall` - FLOAT, NULLABLE
- `forecast_date` - DATE, NULLABLE
- `created_at` - DATETIME, DEFAULT: CURRENT_TIMESTAMP

**Relationships:**
- None (standalone cache table)

---

## Foreign Key Relationships

### Relationship Diagram

```
            ┌─────────┐
            │  users  │ ← Core table (no dependencies)
            └────┬────┘
                 │
    ┌────────────┼────────────┬──────────────┬──────────────┐
    │            │            │              │              │
    ▼            ▼            ▼              ▼              ▼
┌───────┐  ┌────────────┐  ┌────────┐  ┌────────┐  ┌──────────────┐
│ farms │  │ disease_   │  │ forum_ │  │ farm_  │  │ calculator_  │
└───┬───┘  │ scans      │  │ posts  │  │ ledger │  │ results      │
    │      └────────────┘  └───┬────┘  └────────┘  └──────────────┘
    │                          │
    ├────────┬─────────────────┼──────────┐
    │        │                 │          │
    ▼        ▼                 ▼          ▼
┌───────┐  ┌────────────┐  ┌────────┐  ┌────────────┐
│ crops │  │ farm_notes │  │ forum_ │  │ forum_     │
└───────┘  └────────────┘  │ replies│  │ votes      │
                            └────────┘  └────────────┘
```

### Foreign Key Constraints Summary

| Child Table | Foreign Key Column | References | Cascade Delete | Optional |
|-------------|-------------------|------------|----------------|----------|
| farms | user_id | users.id | ❌ | ❌ |
| crops | farm_id | farms.id | ❌ | ❌ |
| monitored_crops | user_id | users.id | ❌ | ❌ |
| monitored_crops | farm_id | farms.id | ❌ | ✅ |
| farm_notes | farm_id | farms.id | ✅ | ❌ |
| farm_notes | user_id | users.id | ❌ | ❌ |
| disease_detections | user_id | users.id | ❌ | ❌ |
| disease_scans | user_id | users.id | ❌ | ❌ |
| forum_posts | user_id | users.id | ❌ | ❌ |
| forum_replies | user_id | users.id | ❌ | ❌ |
| forum_replies | post_id | forum_posts.id | ✅ | ❌ |
| forum_votes | user_id | users.id | ❌ | ❌ |
| forum_votes | post_id | forum_posts.id | ✅ | ❌ |
| farm_ledger | user_id | users.id | ❌ | ❌ |
| calculator_results | user_id | users.id | ❌ | ❌ |
| calculator_history | user_id | users.id | ❌ | ❌ |
| crop_recommendations | user_id | users.id | ❌ | ✅ |
| crop_yield_predictions | user_id | users.id | ❌ | ✅ |

### Table Creation Order

When manually creating tables, follow this order to respect foreign key constraints:

1. **users** (no dependencies)
2. **disease_info** (no dependencies)
3. **weather_data** (no dependencies)
4. **farms** (depends on: users)
5. **crops** (depends on: farms)
6. **monitored_crops** (depends on: users, farms optional)
7. **farm_notes** (depends on: users, farms)
8. **disease_detections** (depends on: users)
9. **disease_scans** (depends on: users)
10. **forum_posts** (depends on: users)
11. **forum_replies** (depends on: users, forum_posts)
12. **forum_votes** (depends on: users, forum_posts)
13. **farm_ledger** (depends on: users)
14. **calculator_results** (depends on: users)
15. **calculator_history** (depends on: users)
16. **crop_recommendations** (depends on: users optional)
17. **crop_yield_predictions** (depends on: users optional)

---

## Database Commands Reference

### Verification Commands

```sql
-- Login to database
mysql -u root -p plantcare_db

-- List all tables
SHOW TABLES;

-- Check table structure
DESCRIBE users;
DESCRIBE farms;
DESCRIBE crops;

-- Verify foreign keys
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE
    REFERENCED_TABLE_SCHEMA = 'plantcare_db'
    AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME, COLUMN_NAME;

-- Count records in all tables
SELECT 'users' AS table_name, COUNT(*) AS row_count FROM users
UNION ALL SELECT 'farms', COUNT(*) FROM farms
UNION ALL SELECT 'crops', COUNT(*) FROM crops
UNION ALL SELECT 'monitored_crops', COUNT(*) FROM monitored_crops
UNION ALL SELECT 'disease_scans', COUNT(*) FROM disease_scans
UNION ALL SELECT 'forum_posts', COUNT(*) FROM forum_posts
UNION ALL SELECT 'calculator_results', COUNT(*) FROM calculator_results;

-- Check indexes
SHOW INDEX FROM users;
SHOW INDEX FROM farms;

-- Exit
EXIT;
```

### Maintenance Commands

```bash
# Backup database
mysqldump -u root -p plantcare_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup specific tables
mysqldump -u root -p plantcare_db users farms crops > backup_core_tables.sql

# Restore database
mysql -u root -p plantcare_db < backup_file.sql

# Check MySQL service status (Linux)
sudo systemctl status mysql

# Check MySQL service status (Windows)
net start | findstr MySQL

# Start MySQL service (Linux)
sudo systemctl start mysql

# Start MySQL service (Windows)
net start MySQL80
```

### Windows PowerShell Commands

```powershell
# Create database
mysql -u root -p -e "CREATE DATABASE plantcare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Backup with timestamp
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
mysqldump -u root -p plantcare_db > "backup_$timestamp.sql"

# Check MySQL service
Get-Service | Where-Object {$_.DisplayName -like "*MySQL*"}

# Start MySQL service
Start-Service MySQL80

# List all tables
mysql -u root -p plantcare_db -e "SHOW TABLES;"
```

### Reset Database (⚠️ CAUTION: Deletes ALL data)

```sql
-- Drop and recreate database
DROP DATABASE IF EXISTS plantcare_db;
CREATE DATABASE plantcare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Then run migrations:
```bash
cd backend
flask db upgrade
```

---

## Troubleshooting

### Issue 1: Can't Connect to MySQL Server

**Symptoms:**
- `ERROR 2002 (HY000): Can't connect to local MySQL server`
- Application fails to start

**Solutions:**

```bash
# Check if MySQL is running (Linux)
sudo systemctl status mysql
sudo systemctl start mysql

# Check if MySQL is running (Windows)
net start | findstr MySQL
net start MySQL80

# Check if MySQL is listening on correct port
netstat -an | findstr 3306

# Test connection
mysql -u root -p -h localhost
```

---

### Issue 2: Access Denied for User

**Symptoms:**
- `ERROR 1045 (28000): Access denied for user 'plantcare_user'@'localhost'`

**Solutions:**

```sql
-- Verify user exists
SELECT User, Host FROM mysql.user WHERE User = 'plantcare_user';

-- Reset password
ALTER USER 'plantcare_user'@'localhost' IDENTIFIED BY 'NewPassword123!';
FLUSH PRIVILEGES;

-- Check privileges
SHOW GRANTS FOR 'plantcare_user'@'localhost';

-- Grant all privileges if needed
GRANT ALL PRIVILEGES ON plantcare_db.* TO 'plantcare_user'@'localhost';
FLUSH PRIVILEGES;
```

Check `.env` file:
```env
MYSQL_USER=plantcare_user
MYSQL_PASSWORD=NewPassword123!
```

---

### Issue 3: Unknown Database

**Symptoms:**
- `ERROR 1049 (42000): Unknown database 'plantcare_db'`

**Solutions:**

```bash
# Create the database
mysql -u root -p -e "CREATE DATABASE plantcare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Verify creation
mysql -u root -p -e "SHOW DATABASES LIKE 'plantcare_db';"
```

---

### Issue 4: Table Doesn't Exist

**Symptoms:**
- `(1146, "Table 'plantcare_db.users' doesn't exist")`
- Application queries fail

**Solutions:**

```bash
# Run migrations
cd backend
flask db upgrade

# OR use manual script
python create_crop_tables.py

# Verify tables created
python check_crop_db_status.py
```

```sql
-- Check existing tables
mysql -u root -p plantcare_db -e "SHOW TABLES;"
```

---

### Issue 5: Foreign Key Constraint Fails

**Symptoms:**
- `Cannot add or update a child row: a foreign key constraint fails`

**Solutions:**

```python
# Check if parent record exists
from app.models.user import User
user = User.query.get(user_id)
if not user:
    print("User does not exist! Create user first.")

# Always create parent before child
user = User(email="test@example.com", name="Test User")
db.session.add(user)
db.session.commit()

# Now create child record
farm = Farm(name="Test Farm", user_id=user.id, main_crop="Wheat", size_acres=10)
db.session.add(farm)
db.session.commit()
```

```sql
-- Check foreign key constraints
SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
WHERE TABLE_NAME = 'farms' AND COLUMN_NAME = 'user_id';

-- Temporarily disable foreign key checks (NOT recommended for production)
SET FOREIGN_KEY_CHECKS = 0;
-- Your operations here
SET FOREIGN_KEY_CHECKS = 1;
```

---

### Issue 6: Migration Errors

**Symptoms:**
- `Target database is not up to date`
- `Table already exists`

**Solutions:**

```bash
cd backend

# Mark current state as up-to-date
flask db stamp head

# Remove old migrations
rm -rf migrations/versions/*  # Linux/Mac
Remove-Item -Recurse -Force migrations/versions/*  # Windows PowerShell

# Create fresh migration
flask db migrate -m "Fresh migration"
flask db upgrade

# OR drop and recreate specific table
mysql -u root -p plantcare_db -e "DROP TABLE IF EXISTS table_name;"
flask db upgrade
```

---

### Issue 7: Character Encoding Issues

**Symptoms:**
- Emojis or special characters display incorrectly
- `Incorrect string value` errors

**Solutions:**

```sql
-- Check database character set
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME 
FROM INFORMATION_SCHEMA.SCHEMATA 
WHERE SCHEMA_NAME = 'plantcare_db';

-- Convert existing database
ALTER DATABASE plantcare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Convert specific table
ALTER TABLE users CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Check table character set
SHOW CREATE TABLE users;
```

---

## Frequently Asked Questions (FAQ)

### Q1: Do I need to create the database manually?

**A:** Yes! Creating the database is mandatory. The application cannot create the database automatically. Run:

```sql
CREATE DATABASE plantcare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

### Q2: What happens if I skip the database setup?

**A:** The application will fail to start with database connection errors like:
- `Unknown database 'plantcare_db'`
- `Can't connect to MySQL server`

---

### Q3: How do I know if all tables are created correctly?

**A:** Run the verification script:

```bash
cd backend
python check_crop_db_status.py
```

Or check manually:

```sql
mysql -u root -p plantcare_db -e "SHOW TABLES;"
```

You should see 17 tables plus `alembic_version`.

---

### Q4: Can I use a different database name?

**A:** Yes! Update your `.env` file:

```env
MYSQL_DB=your_custom_db_name
```

Then create the database with that name:

```sql
CREATE DATABASE your_custom_db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

### Q5: What is the correct order to create tables?

**A:** Always use `flask db upgrade` which handles the correct order automatically. If creating manually, see the [Table Creation Order](#table-creation-order) section.

---

### Q6: Do all tables have foreign keys?

**A:** No. These tables have NO foreign keys:
- `users` (core table)
- `disease_info` (reference data)
- `weather_data` (cache table)

---

### Q7: What tables depend on the users table?

**A:** 13 tables have foreign keys to `users`:
- farms
- disease_detections
- disease_scans
- forum_posts
- forum_replies
- forum_votes
- farm_ledger
- monitored_crops
- calculator_results
- calculator_history
- crop_recommendations (optional)
- crop_yield_predictions (optional)
- farm_notes

---

### Q8: Can I delete a user without breaking the database?

**A:** Deleting a user will affect all related records. Some tables use CASCADE delete (automatically delete related records), others may prevent deletion. Implement a "soft delete" or archive feature instead.

---

### Q9: Why do some foreign keys allow NULL values?

**A:** Optional foreign keys (like `farm_id` in `monitored_crops`) allow records to exist independently. A crop can be monitored without being linked to a specific farm.

---

### Q10: How do I reset the database completely?

**A:** ⚠️ **WARNING**: This deletes ALL data!

```sql
DROP DATABASE IF EXISTS plantcare_db;
CREATE DATABASE plantcare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Then run:

```bash
cd backend
flask db upgrade
```

---

### Q11: What MySQL version is required?

**A:** MySQL 5.7 or higher. MySQL 8.0 is recommended for better performance and native JSON support.

---

### Q12: Can I use MariaDB instead of MySQL?

**A:** Yes! MariaDB 10.2+ is compatible. The connection string remains the same.

---

### Q13: Why UTF8MB4 character set?

**A:** UTF8MB4 supports full Unicode including emojis, special characters, and international text. UTF8 (3-byte) only supports Basic Multilingual Plane characters.

---

### Q14: How are passwords stored?

**A:** Passwords are hashed using Werkzeug's security functions (bcrypt-based) and stored in the `password_hash` column. Plain passwords are never stored.

---

### Q15: What happens if I change the database schema?

**A:** Create a new migration:

```bash
# Modify model files in backend/app/models/
# Then run:
flask db migrate -m "Description of changes"
flask db upgrade
```

---

### Q16: How do I verify foreign key relationships?

**A:** Use this query:

```sql
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE REFERENCED_TABLE_SCHEMA = 'plantcare_db' 
  AND REFERENCED_TABLE_NAME IS NOT NULL;
```

---

### Q17: Can I use this with Docker?

**A:** Yes! Example `docker-compose.yml`:

```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: plantcare_db
      MYSQL_USER: plantcare_user
      MYSQL_PASSWORD: password123
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

Update `.env`:
```env
MYSQL_HOST=mysql
MYSQL_USER=plantcare_user
MYSQL_PASSWORD=password123
MYSQL_DB=plantcare_db
```

---

### Q18: How do I backup the database automatically?

**A:** Create a cron job (Linux) or Task Scheduler task (Windows):

**Linux Cron:**
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * mysqldump -u root -p'password' plantcare_db > /backups/plantcare_$(date +\%Y\%m\%d).sql
```

**Windows Task Scheduler:**
Create a batch file `backup.bat`:
```batch
@echo off
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%
mysqldump -u root -p'password' plantcare_db > C:\backups\plantcare_%timestamp%.sql
```

---

### Q19: What are CASCADE deletes?

**A:** CASCADE means when a parent record is deleted, all child records are automatically deleted:

- Delete `forum_post` → All `forum_replies` and `forum_votes` for that post are deleted
- Delete `farm` → All `farm_notes` for that farm are deleted

---

### Q20: How do I check database size?

**A:** 

```sql
SELECT 
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.TABLES 
WHERE table_schema = 'plantcare_db'
GROUP BY table_schema;
```

---

## Security Best Practices

### 1. Use Dedicated Database User

❌ **Don't:**
```env
MYSQL_USER=root
```

✅ **Do:**
```env
MYSQL_USER=plantcare_user
```

Create dedicated user:
```sql
CREATE USER 'plantcare_user'@'localhost' IDENTIFIED BY 'SecurePassword123!';
GRANT ALL PRIVILEGES ON plantcare_db.* TO 'plantcare_user'@'localhost';
FLUSH PRIVILEGES;
```

---

### 2. Strong Passwords

✅ **Requirements:**
- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- Not dictionary words
- Unique per application

**Generate secure password:**
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(24))"

# OpenSSL
openssl rand -base64 24
```

---

### 3. Regular Backups

✅ **Backup Strategy:**
- Daily automated backups
- Keep 7-30 days of backups
- Test restore procedures regularly
- Store backups in separate location

```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/plantcare"
mkdir -p $BACKUP_DIR

mysqldump -u root -p'password' plantcare_db | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
```

---

### 4. Connection Encryption

✅ **Production Setup:**
```env
# Enable SSL for MySQL connections
MYSQL_SSL_CA=/path/to/ca-cert.pem
MYSQL_SSL_CERT=/path/to/client-cert.pem
MYSQL_SSL_KEY=/path/to/client-key.pem
```

---

### 5. Limit Privileges

```sql
-- Don't grant unnecessary privileges
-- Only grant what's needed

-- ✅ Good: Specific database only
GRANT SELECT, INSERT, UPDATE, DELETE ON plantcare_db.* TO 'plantcare_user'@'localhost';

-- ❌ Bad: All databases
GRANT ALL PRIVILEGES ON *.* TO 'plantcare_user'@'localhost';
```

---

### 6. Parameter Validation

✅ **Always validate user input before database queries**

PlantCare uses SQLAlchemy ORM which provides:
- Parameterized queries (prevents SQL injection)
- Input validation
- Type checking

---

### 7. Audit Logging

Enable MySQL audit logging:

```sql
-- Check if audit log is enabled
SHOW VARIABLES LIKE 'audit_log%';

-- Enable audit logging (MySQL Enterprise)
INSTALL PLUGIN audit_log SONAME 'audit_log.so';
SET GLOBAL audit_log_policy = 'ALL';
```

---

### 8. Monitoring

✅ **Monitor:**
- Failed login attempts
- Unusual query patterns
- Database size growth
- Connection counts
- Slow queries

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow-query.log';
```

---

### 9. Never Commit Credentials

✅ **Add to `.gitignore`:**
```gitignore
.env
.env.local
.env.production
*.sql
backups/
```

---

### 10. Production Hardening

```sql
-- Disable remote root login
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
FLUSH PRIVILEGES;

-- Remove anonymous users
DELETE FROM mysql.user WHERE User='';
FLUSH PRIVILEGES;

-- Remove test database
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
FLUSH PRIVILEGES;
```

---

## Additional Resources

- [MySQL Official Documentation](https://dev.mysql.com/doc/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [MySQL Performance Tuning](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)

---

## Support

For database-related issues:
1. Check this documentation first
2. Review [Troubleshooting](#troubleshooting) section
3. Check [FAQ](#frequently-asked-questions-faq) section
4. Open an issue on GitHub with:
   - Error message
   - MySQL version (`SELECT VERSION();`)
   - Python version (`python --version`)
   - Steps to reproduce

---

**Last Updated**: October 3, 2025  
**Database Version**: MySQL 5.7+ / MySQL 8.0+  
**Tables Count**: 17  
**Foreign Keys**: 18
