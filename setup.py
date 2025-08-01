#!/usr/bin/env python3
"""
Setup script for Job Matching System
Handles database initialization, configuration, and dependencies
"""

import os
import sys
import subprocess
import json
import getpass
from pathlib import Path

def install_requirements():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def create_config():
    """Create configuration files"""
    print("\n=== Configuration Setup ===")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("Creating .env configuration file...")
        
        config = {
            'DB_HOST': input("Database host (default: localhost): ") or 'localhost',
            'DB_PORT': input("Database port (default: 3306): ") or '3306',
            'DB_USER': input("Database username (default: root): ") or 'root',
            'DB_PASSWORD': getpass.getpass("Database password: "),
            'DB_NAME': input("Database name (default: job_matching_system): ") or 'job_matching_system',
            'SECRET_KEY': input("Secret key (leave blank to generate): ") or os.urandom(32).hex(),
            'MAIL_USERNAME': input("Email username (optional): "),
            'MAIL_PASSWORD': getpass.getpass("Email password (optional): "),
        }
        
        with open('.env', 'w') as f:
            for key, value in config.items():
                f.write(f"{key}={value}\n")
        
        print("✓ Configuration file created")
    else:
        print("✓ Configuration file already exists")

def create_directories():
    """Create necessary directories"""
    print("\nCreating necessary directories...")
    
    directories = [
        'PROJECT/static/uploads',
        'PROJECT/static/css',
        'PROJECT/static/js',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✓ Directories created")

def check_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    
    try:
        # Import here to avoid dependency issues during setup
        import pymysql
        from dotenv import load_dotenv
        load_dotenv()
        
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            db_name = os.getenv('DB_NAME', 'job_matching_system')
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"✓ Database '{db_name}' ready")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("Please ensure MySQL is running and credentials are correct")
        return False

def initialize_database():
    """Initialize database tables"""
    print("\nInitializing database tables...")
    
    try:
        # Import Flask app to create tables
        sys.path.insert(0, 'PROJECT')
        from main import app, db, init_db
        
        with app.app_context():
            db.create_all()
            print("✓ Database tables created")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating database tables: {e}")
        return False

def run_optimizations():
    """Run database optimizations"""
    print("\nApplying database optimizations...")
    
    if os.path.exists('db_optimize.sql'):
        try:
            import pymysql
            from dotenv import load_dotenv
            load_dotenv()
            
            connection = pymysql.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', 3306)),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'job_matching_system'),
                charset='utf8mb4'
            )
            
            with open('db_optimize.sql', 'r') as f:
                sql_commands = f.read().split(';')
            
            with connection.cursor() as cursor:
                for command in sql_commands:
                    command = command.strip()
                    if command:
                        try:
                            cursor.execute(command)
                        except Exception as e:
                            # Some commands might fail if constraints already exist
                            if "Duplicate key name" not in str(e):
                                print(f"Warning: {e}")
            
            connection.commit()
            connection.close()
            print("✓ Database optimizations applied")
            
        except Exception as e:
            print(f"✗ Error applying optimizations: {e}")

def main():
    """Main setup function"""
    print("=== Job Matching System Setup ===\n")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("✗ Python 3.7+ is required")
        sys.exit(1)
    
    # Install dependencies
    if not install_requirements():
        sys.exit(1)
    
    # Create configuration
    create_config()
    
    # Create directories
    create_directories()
    
    # Test database connection
    if not check_database_connection():
        print("\nPlease fix database configuration and run setup again")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    # Apply optimizations
    run_optimizations()
    
    print("\n=== Setup Complete ===")
    print("To start the application:")
    print("  cd PROJECT")
    print("  python main.py")
    print("\nThe application will be available at: http://localhost:5000")

if __name__ == "__main__":
    main()