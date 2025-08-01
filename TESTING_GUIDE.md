# Testing Guide - Job Matching System

## 🧪 How to Test the Application Locally

### **Prerequisites Check**
Before testing, ensure you have:
- Python 3.7+ installed
- MySQL server running
- All dependencies installed

### **Step 1: Quick Setup Verification**

#### **Option A: Automated Setup (Recommended)**
```bash
# Navigate to project directory
cd /workspace

# Run the setup script
python setup.py
```

#### **Option B: Manual Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Create configuration file
cp .env.example .env

# Edit .env file with your settings
nano .env
```

**Minimum .env configuration:**
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=job_matching_system
SECRET_KEY=test-secret-key-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True
```

### **Step 2: Database Setup**

#### **Start MySQL and Create Database**
```bash
# Start MySQL service (Ubuntu/Debian)
sudo systemctl start mysql

# Or for macOS with Homebrew
brew services start mysql

# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE job_matching_system;
EXIT;
```

### **Step 3: Start the Application**

```bash
# Navigate to PROJECT directory
cd PROJECT

# Start the Flask application
python main.py
```

**Expected Output:**
```
INFO - Database tables created successfully
 * Serving Flask app 'main'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

### **Step 4: Basic Functionality Tests**

#### **Test 1: Homepage Access**
1. Open browser and go to: `http://localhost:5000`
2. **Expected Result:** Homepage loads with job statistics
3. **Check for:** No error messages, clean layout

#### **Test 2: User Registration**
1. Click "Register" or go to: `http://localhost:5000/register`
2. Fill out the form:
   - **Email:** test@example.com
   - **Password:** TestPassword123
   - **First Name:** Test
   - **Last Name:** User
   - **User Type:** Job Seeker
3. **Expected Result:** Registration success message, redirect to login

#### **Test 3: User Login**
1. Go to: `http://localhost:5000/login`
2. Login with the credentials you just created
3. **Expected Result:** Redirect to candidate dashboard

#### **Test 4: Database Connection**
Check if data is being saved:
```bash
mysql -u root -p job_matching_system
SELECT * FROM users;
```
**Expected:** Your test user should appear in the results

### **Step 5: Role-Based Testing**

#### **Create Admin User**
```sql
# Connect to MySQL
mysql -u root -p job_matching_system

# Update user type to admin
UPDATE users SET user_type='admin' WHERE email='test@example.com';
```

#### **Create Employer User**
1. Register another user with email: `employer@example.com`
2. Update in database:
```sql
UPDATE users SET user_type='employer' WHERE email='employer@example.com';
```

#### **Test Admin Dashboard**
1. Login as admin user
2. Go to: `http://localhost:5000/admin/dashboard`
3. **Expected:** Access to admin features, user management

#### **Test Employer Dashboard**
1. Login as employer user
2. Go to: `http://localhost:5000/employer/dashboard`
3. **Expected:** Access to job posting features

### **Step 6: Core Feature Testing**

#### **Test Job Posting (Employer)**
1. Login as employer
2. Complete company profile first
3. Go to: `http://localhost:5000/create_job`
4. Create a test job posting
5. **Expected:** Job appears in job listings

#### **Test Job Application (Candidate)**
1. Login as candidate
2. Complete candidate profile
3. Browse jobs and apply to one
4. **Expected:** Application submitted successfully

#### **Test Skills Management (Admin)**
1. Login as admin
2. Go to: `http://localhost:5000/admin/skills`
3. Add some test skills
4. **Expected:** Skills saved and appear in lists

### **Step 7: Advanced Feature Testing**

#### **Test File Upload**
1. Login as candidate
2. Go to profile and try uploading a CV
3. **Expected:** File uploads successfully

#### **Test Messaging System**
1. Have employer send message to candidate
2. Check if candidate receives notification
3. **Expected:** Message appears in inbox

#### **Test MCQ Exam System**
1. Login as employer
2. Create an exam for a job posting
3. Add questions to the exam
4. **Expected:** Exam created successfully

### **Step 8: Error Handling Tests**

#### **Test 404 Error**
1. Go to: `http://localhost:5000/nonexistent-page`
2. **Expected:** Custom 404 error page

#### **Test Authentication**
1. Try accessing: `http://localhost:5000/admin/dashboard` without login
2. **Expected:** Redirect to login page

#### **Test CSRF Protection**
1. Try submitting forms without CSRF tokens
2. **Expected:** CSRF error prevention

---

## 🔍 **Troubleshooting Common Issues**

### **Issue 1: Application Won't Start**

**Error:** `ImportError: No module named 'flask'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Error:** `Can't connect to MySQL server`
```bash
# Solution: Start MySQL service
sudo systemctl start mysql
# Or check if MySQL is running
sudo systemctl status mysql
```

### **Issue 2: Database Connection Failed**

**Error:** `Access denied for user 'root'@'localhost'`
```bash
# Reset MySQL root password
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'newpassword';
FLUSH PRIVILEGES;
```

### **Issue 3: Database Tables Not Created**

```bash
# Manually create tables
cd PROJECT
python -c "
from main import app, db
with app.app_context():
    db.create_all()
    print('Tables created successfully')
"
```

### **Issue 4: Static Files Not Loading**

**Check file permissions:**
```bash
chmod -R 755 PROJECT/static/
```

### **Issue 5: Email Functionality Not Working**

This is expected in development. Email features are optional and will log warnings if not configured.

---

## ✅ **Quick Health Check Script**

Create a simple test script:

```python
# test_health.py
import requests
import sys

def test_application():
    try:
        # Test homepage
        response = requests.get('http://localhost:5000')
        if response.status_code == 200:
            print("✅ Homepage: OK")
        else:
            print(f"❌ Homepage: Failed ({response.status_code})")
            return False
            
        # Test registration page
        response = requests.get('http://localhost:5000/register')
        if response.status_code == 200:
            print("✅ Registration page: OK")
        else:
            print(f"❌ Registration page: Failed ({response.status_code})")
            
        # Test login page
        response = requests.get('http://localhost:5000/login')
        if response.status_code == 200:
            print("✅ Login page: OK")
        else:
            print(f"❌ Login page: Failed ({response.status_code})")
            
        print("\n🎉 Basic application health check passed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to application. Is it running on port 5000?")
        return False
    except Exception as e:
        print(f"❌ Error during health check: {e}")
        return False

if __name__ == "__main__":
    if test_application():
        sys.exit(0)
    else:
        sys.exit(1)
```

**Run the health check:**
```bash
pip install requests
python test_health.py
```

---

## 📊 **Expected Database Tables**

After successful setup, you should see these tables:
```sql
SHOW TABLES;
```

**Expected tables:**
- `activity_logs`
- `application_status_history`
- `candidate_answers`
- `candidate_profiles`
- `candidate_skills`
- `companies`
- `exam_attempts`
- `job_applications`
- `job_postings`
- `job_required_skills`
- `mcq_exams`
- `mcq_questions`
- `messages`
- `notifications`
- `skills`
- `users`

---

## 🎯 **Success Indicators**

Your application is working correctly if:

1. ✅ Application starts without errors
2. ✅ Homepage loads with statistics
3. ✅ User registration works
4. ✅ Login/logout functions properly
5. ✅ Role-based access works (admin, employer, candidate)
6. ✅ Database tables are created
7. ✅ Forms submit successfully
8. ✅ File uploads work
9. ✅ Error pages display correctly
10. ✅ No console errors in browser

---

## 🆘 **Getting Help**

If you encounter issues:

1. **Check application logs** in the terminal where you started the app
2. **Check browser console** for JavaScript errors
3. **Verify database connection** with the MySQL command line
4. **Ensure all dependencies** are installed correctly
5. **Check file permissions** in the PROJECT directory

**Common log files to check:**
- Terminal output where you ran `python main.py`
- Browser developer console (F12)
- MySQL error logs: `/var/log/mysql/error.log`