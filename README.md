# Job Matching System - University Project

## Overview
This is a **Flask-based Job Matching System** developed as part of a university database management project. It efficiently connects job seekers with employers through advanced matching algorithms, comprehensive profile management, and secure user authentication.

The system leverages modern web technologies and security best practices to provide a robust platform for job recruitment and candidate selection.

## 🚀 Features

### **Core Functionality**
- **Multi-Role Authentication System**
  - **Admin**: Complete system management, user oversight, analytics
  - **Employer**: Job posting, candidate screening, application management
  - **Job Seeker**: Profile creation, job browsing, application tracking

### **Advanced Job Management**
- **Smart Job Posting** with detailed requirements and criteria
- **Skill-based Matching Algorithm** (70+ point scoring system)
- **Advanced Search & Filtering** by location, salary, experience, skills
- **Application Status Tracking** with complete audit trail

### **Assessment & Communication**
- **MCQ Exam System** for candidate evaluation
- **Real-time Messaging** between employers and candidates
- **Notification System** for application updates and system alerts
- **Email Integration** for automated communications

### **Analytics & Reporting**
- **Comprehensive Admin Dashboard** with system statistics
- **Activity Logging** for full audit trail
- **Data Export** capabilities (CSV format)
- **Performance Analytics** and user engagement metrics

### **Security & Performance**
- **CSRF Protection** and secure file uploads
- **Database Query Optimization** with proper indexing
- **Error Handling** with custom error pages
- **Environment-based Configuration** for secure deployment

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.7+ (Flask 3.1.1) |
| **Database** | MySQL 8.0+ with PyMySQL |
| **ORM** | SQLAlchemy 2.0+ |
| **Authentication** | Flask-WTF with CSRF protection |
| **Email** | Flask-Mail with SMTP support |
| **Frontend** | HTML5, CSS3, Bootstrap 5 |
| **Security** | Werkzeug password hashing, secure sessions |

---

## 📦 Quick Installation

### **Method 1: Automated Setup (Recommended)**
```bash
# Clone the repository
git clone <repository-url>
cd job-matching-system

# Run the automated setup script
python setup.py
```

### **Method 2: Manual Setup**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your database and email settings

# 3. Initialize database
cd PROJECT
python main.py
```

---

## ⚙️ Configuration

### **Environment Variables (.env)**
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=job_matching_system

# Security
SECRET_KEY=your-super-secret-key

# Email Configuration (Optional)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### **Database Optimization**
After initial setup, run the optimization script:
```bash
mysql -u root -p job_matching_system < db_optimize.sql
```

---

## 🚀 Usage

### **Starting the Application**
```bash
cd PROJECT
python main.py
```
Access the application at: `http://localhost:5000`

### **Default Admin Account**
Create an admin account through registration, then manually update the database:
```sql
UPDATE users SET user_type='admin' WHERE email='your-admin@email.com';
```

---

## 📊 System Architecture

### **Database Schema**
- **Users & Authentication**: User accounts with role-based access
- **Job Management**: Jobs, applications, and requirements
- **Skills & Matching**: Skill sets and matching algorithms
- **Communication**: Messages, notifications, and email
- **Assessment**: MCQ exams and candidate evaluation
- **Audit**: Activity logs and status history

### **Security Features**
- ✅ Password hashing with Werkzeug
- ✅ CSRF protection on all forms
- ✅ SQL injection prevention with SQLAlchemy ORM
- ✅ Secure file upload validation
- ✅ Session management and timeout
- ✅ Input validation and sanitization

---

## 🔧 Development

### **Project Structure**
```
job-matching-system/
├── PROJECT/
│   ├── main.py              # Main application file
│   ├── templates/           # HTML templates
│   ├── static/             # CSS, JS, uploads
│   └── conversation.html    # Chat interface
├── requirements.txt         # Dependencies
├── setup.py                # Automated setup
├── db_optimize.sql         # Database optimization
├── .env.example            # Configuration template
└── README.md               # Documentation
```

### **Adding New Features**
1. Create database models in `main.py`
2. Add routes with proper authentication decorators
3. Create corresponding HTML templates
4. Update the database with migrations

---

## 🤝 Contributing
This is a university project. For improvements or bug fixes:
1. Fork the repository
2. Create a feature branch
3. Make your changes with proper testing
4. Submit a pull request

---

## 📄 License
This project is developed for educational purposes as part of a university database management course.

---

## 🆘 Support
For issues or questions:
1. Check the logs in the `logs/` directory
2. Verify database connectivity
3. Ensure all environment variables are set correctly
4. Review the error messages in the Flask debug output

