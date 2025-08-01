# Deployment Guide - Job Matching System

## 🚀 Production Deployment

### Prerequisites
- Python 3.7+
- MySQL 8.0+
- Web server (Nginx/Apache)
- SSL certificate for HTTPS

### 1. Server Setup

#### Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv mysql-server nginx

# CentOS/RHEL
sudo yum install python3 python3-pip mysql-server nginx
```

#### Create Application User
```bash
sudo useradd -m -s /bin/bash jobmatch
sudo usermod -aG www-data jobmatch
```

### 2. Application Deployment

#### Clone and Setup
```bash
# Switch to application user
sudo su - jobmatch

# Clone repository
git clone <repository-url> /home/jobmatch/job-matching-system
cd /home/jobmatch/job-matching-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

#### Production Configuration
```bash
# Create production environment file
cp .env.example .env.production

# Edit with production settings
nano .env.production
```

**Production .env settings:**
```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=jobmatch_user
DB_PASSWORD=secure_password
DB_NAME=job_matching_system

# Security
SECRET_KEY=very-long-random-string-change-this
FLASK_ENV=production
FLASK_DEBUG=False

# Email
MAIL_SERVER=smtp.your-domain.com
MAIL_PORT=587
MAIL_USERNAME=noreply@your-domain.com
MAIL_PASSWORD=secure_email_password

# Application
UPLOAD_FOLDER=/home/jobmatch/job-matching-system/PROJECT/static/uploads
MAX_CONTENT_LENGTH=16777216
```

### 3. Database Setup

#### Create Production Database
```sql
CREATE DATABASE job_matching_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'jobmatch_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON job_matching_system.* TO 'jobmatch_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Initialize Database
```bash
# Load environment variables
export $(cat .env.production | xargs)

# Initialize database
cd PROJECT
python main.py --init-db-only

# Apply optimizations
mysql -u jobmatch_user -p job_matching_system < ../db_optimize.sql
```

### 4. Gunicorn Configuration

#### Create Gunicorn Config
```bash
# /home/jobmatch/job-matching-system/gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
preload_app = True
user = "jobmatch"
group = "www-data"
```

#### Create Systemd Service
```bash
# /etc/systemd/system/jobmatch.service
[Unit]
Description=Job Matching System
After=network.target

[Service]
User=jobmatch
Group=www-data
WorkingDirectory=/home/jobmatch/job-matching-system/PROJECT
Environment="PATH=/home/jobmatch/job-matching-system/venv/bin"
EnvironmentFile=/home/jobmatch/job-matching-system/.env.production
ExecStart=/home/jobmatch/job-matching-system/venv/bin/gunicorn \
    --config /home/jobmatch/job-matching-system/gunicorn.conf.py \
    main:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable jobmatch
sudo systemctl start jobmatch
sudo systemctl status jobmatch
```

### 5. Nginx Configuration

#### Create Nginx Config
```nginx
# /etc/nginx/sites-available/jobmatch
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /path/to/ssl/certificate.crt;
    ssl_certificate_key /path/to/ssl/private.key;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/jobmatch/job-matching-system/PROJECT/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /uploads/ {
        internal;
        alias /home/jobmatch/job-matching-system/PROJECT/static/uploads/;
    }
}
```

#### Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/jobmatch /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. Security Hardening

#### File Permissions
```bash
# Set proper permissions
sudo chown -R jobmatch:www-data /home/jobmatch/job-matching-system
sudo chmod -R 755 /home/jobmatch/job-matching-system
sudo chmod -R 775 /home/jobmatch/job-matching-system/PROJECT/static/uploads
sudo chmod 600 /home/jobmatch/job-matching-system/.env.production
```

#### Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Firewalld (CentOS)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 7. Monitoring and Logging

#### Setup Log Rotation
```bash
# /etc/logrotate.d/jobmatch
/home/jobmatch/job-matching-system/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 jobmatch www-data
    postrotate
        systemctl reload jobmatch
    endscript
}
```

#### Health Check Script
```bash
#!/bin/bash
# /home/jobmatch/health_check.sh
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ $response != "200" ]; then
    echo "Application health check failed"
    systemctl restart jobmatch
fi
```

### 8. Backup Strategy

#### Database Backup Script
```bash
#!/bin/bash
# /home/jobmatch/backup.sh
BACKUP_DIR="/backups/jobmatch"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database backup
mysqldump -u jobmatch_user -p$DB_PASSWORD job_matching_system > $BACKUP_DIR/db_$DATE.sql

# Application backup
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /home/jobmatch/job-matching-system

# Keep last 30 days
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

#### Cron Job for Backups
```bash
# Add to crontab
0 2 * * * /home/jobmatch/backup.sh
```

### 9. Performance Optimization

#### MySQL Optimization
```sql
-- Add to /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
max_connections = 200
query_cache_size = 64M
thread_cache_size = 8
```

#### Application Caching
```python
# Add Redis for session storage (optional)
pip install redis flask-session

# In main.py
from flask_session import Session
import redis

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
Session(app)
```

### 10. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo crontab -e
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔧 Maintenance

### Regular Tasks
- Monitor system resources
- Check application logs
- Verify backups
- Update dependencies
- Security patches

### Deployment Updates
```bash
# Update application
cd /home/jobmatch/job-matching-system
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart jobmatch
```

## 📞 Support
For production issues:
1. Check systemd logs: `sudo journalctl -u jobmatch -f`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Monitor application logs: `tail -f /home/jobmatch/job-matching-system/logs/app.log`