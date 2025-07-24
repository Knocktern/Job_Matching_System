Job Matching & Recruitment System
Overview
This is a web-based job matching and recruitment system built with Flask and MySQL.
It allows:

Candidates to register, manage profiles, apply for jobs, and take MCQ exams.

Employers to post jobs, manage applications, and create exams.

Admins to monitor the platform, manage users, and generate reports.
It includes smart job recommendations, skill gap analysis, messaging, notifications, and activity logs.

Key Features
Candidate
Register and create detailed profiles with skills and CV upload.

Search and apply for jobs.

Personalized job recommendations.

Skill gap analysis for recommended jobs.

MCQ exam participation with result tracking.

Application tracking and status notifications.

Employer
Company profile management.

Job posting with skill requirements.

Manage applications with status updates.

Create MCQ exams and manage questions.

Analytics on applications and job performance.

Messaging with candidates.

Admin
Dashboard for overall system metrics.

Manage users, skills, and activity logs.

Bulk skill import via CSV.

Export reports (Users, Jobs, Applications, Skills).

Advanced reporting (user growth, job statistics, application trends, skill demand).

Technology Stack
Backend: Flask, Flask-SQLAlchemy

Database: MySQL (via pymysql)

Authentication: Werkzeug security hashing

File Upload: PDF/DOC/DOCX CV upload

Email Service: Flask-Mail (Gmail SMTP)

Frontend: Jinja2 templates (HTML/CSS/Bootstrap)

Other: JSON, CSV export, Notifications system

Installation & Setup
Prerequisites
Python 3.8+

MySQL 5.7+ or MariaDB

