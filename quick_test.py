#!/usr/bin/env python3
"""
Quick Test Script for Job Matching System
Run this script to verify your local setup is working correctly
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def print_header(text):
    print(f"\n{'='*50}")
    print(f" {text}")
    print(f"{'='*50}")

def print_step(step, text):
    print(f"\n[Step {step}] {text}")

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.7+")
        return False

def check_mysql():
    """Check if MySQL is accessible"""
    try:
        import pymysql
        # Try to connect to MySQL
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',  # Try without password first
        )
        connection.close()
        print("✅ MySQL connection - OK")
        return True
    except ImportError:
        print("❌ PyMySQL not installed")
        return False
    except Exception as e:
        print(f"⚠️  MySQL connection issue: {e}")
        print("   Note: You may need to configure database credentials")
        return True  # Don't fail here, user can configure later

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_sqlalchemy
        import werkzeug
        print("✅ Flask dependencies - OK")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def check_project_structure():
    """Check if project files exist"""
    required_files = [
        'PROJECT/main.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ Project structure - OK")
        return True

def check_database_tables():
    """Check if database tables exist"""
    try:
        sys.path.insert(0, 'PROJECT')
        from main import app, db
        
        with app.app_context():
            # Try to query a table
            from main import User
            User.query.count()
        
        print("✅ Database tables - OK")
        return True
    except Exception as e:
        print(f"⚠️  Database tables issue: {e}")
        print("   Note: Tables will be created when you start the application")
        return True

def test_application_startup():
    """Test if application can start"""
    print("🔄 Testing application startup...")
    
    try:
        # Change to PROJECT directory
        os.chdir('PROJECT')
        
        # Start application in background
        process = subprocess.Popen(
            [sys.executable, 'main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for startup
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Application started successfully")
            
            # Test HTTP connection
            try:
                response = requests.get('http://localhost:5000', timeout=5)
                if response.status_code == 200:
                    print("✅ HTTP response - OK")
                    result = True
                else:
                    print(f"⚠️  HTTP response code: {response.status_code}")
                    result = True
            except Exception as e:
                print(f"⚠️  HTTP connection issue: {e}")
                result = True
            
            # Terminate the process
            process.terminate()
            process.wait()
            
            return result
        else:
            # Process terminated, check error
            stdout, stderr = process.communicate()
            print(f"❌ Application failed to start")
            if stderr:
                print(f"Error: {stderr[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Startup test failed: {e}")
        return False
    finally:
        # Go back to original directory
        os.chdir('..')

def main():
    """Main test function"""
    print_header("Job Matching System - Quick Test")
    
    all_tests_passed = True
    
    print_step(1, "Checking Python version")
    if not check_python_version():
        all_tests_passed = False
    
    print_step(2, "Checking project structure")
    if not check_project_structure():
        all_tests_passed = False
        print("\nℹ️  Please ensure you're in the correct project directory")
        return False
    
    print_step(3, "Checking dependencies")
    if not check_dependencies():
        all_tests_passed = False
        print("\nℹ️  Run: pip install -r requirements.txt")
    
    print_step(4, "Checking MySQL connection")
    check_mysql()  # Non-blocking check
    
    print_step(5, "Checking database tables")
    check_database_tables()  # Non-blocking check
    
    print_step(6, "Testing application startup")
    if not test_application_startup():
        all_tests_passed = False
    
    # Summary
    print_header("Test Summary")
    
    if all_tests_passed:
        print("🎉 All critical tests passed!")
        print("\nNext steps:")
        print("1. Configure .env file with your database credentials")
        print("2. Start the application: cd PROJECT && python main.py")
        print("3. Open browser: http://localhost:5000")
        print("4. Register a test user and explore the features")
    else:
        print("⚠️  Some issues were found. Please fix them before proceeding.")
        print("\nCommon solutions:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Configure MySQL and create database")
        print("- Check file permissions")
    
    print(f"\nFor detailed testing instructions, see: TESTING_GUIDE.md")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)