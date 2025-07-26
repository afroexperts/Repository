# 🚀 Afro Experts ERP & POS System - Deployment Guide

## 📋 System Overview

This is a comprehensive ERP & POS system built with:
- **Frontend:** React.js with Tailwind CSS
- **Backend:** FastAPI (Python)
- **Database:** MongoDB
- **Features:** 12 ERP modules, Client showcase, Authentication, Reports, etc.

## 🛠 Prerequisites

### Server Requirements:
- **OS:** Ubuntu 20.04+ / CentOS 8+ / Amazon Linux 2
- **RAM:** Minimum 2GB (Recommended 4GB+)
- **Storage:** Minimum 10GB free space
- **CPU:** 2+ cores recommended

### Software Dependencies:
- **Python 3.8+**
- **Node.js 16+**
- **MongoDB 4.4+**
- **Nginx** (for production)
- **PM2** (for process management)

## 📦 Installation Steps

### 1. System Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and Node.js
sudo apt install python3 python3-pip nodejs npm mongodb -y

# Install PM2 globally
sudo npm install -g pm2

# Install Nginx
sudo apt install nginx -y
```

### 2. MongoDB Setup

```bash
# Start MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod

# Create database and user
mongo
> use afroexperts_erp
> db.createUser({
    user: "erp_user",
    pwd: "your_secure_password",
    roles: [{ role: "readWrite", db: "afroexperts_erp" }]
  })
> exit
```

### 3. Backend Deployment

```bash
# Navigate to backend directory
cd /path/to/your/app/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your settings (see configuration section)

# Start backend with PM2
pm2 start "uvicorn server:app --host 0.0.0.0 --port 8001" --name "afroexperts-backend"
```

### 4. Frontend Deployment

```bash
# Navigate to frontend directory
cd /path/to/your/app/frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
# Edit .env with your backend URL

# Build production version
npm run build

# Serve with PM2
pm2 serve build 3000 --name "afroexperts-frontend"
```

### 5. Nginx Configuration

Create `/etc/nginx/sites-available/afroexperts`:

```nginx
server {
    listen 80;
    server_name your_domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/afroexperts /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## ⚙️ Configuration

### Backend Environment (.env)
```env
# Database
MONGO_URL=mongodb://erp_user:your_secure_password@localhost:27017/afroexperts_erp
DB_NAME=afroexperts_erp

# API Settings
SECRET_KEY=your_jwt_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,https://your_domain.com
```

### Frontend Environment (.env)
```env
REACT_APP_BACKEND_URL=https://your_domain.com
# or for development: http://localhost:8001
```

## 🗄️ Database Setup

### Initialize Default Data
```bash
cd backend
source venv/bin/activate

# Run data initialization scripts
python seed_demo_data.py
python add_showcase_clients.py
python seed_rbac_permissions.py
python seed_translations.py
```

### Default Login Credentials
- **Admin:** admin@afroexperts.com / AfroExperts2025!
- **Manager:** manager@afroexperts.com / Manager2025!
- **Cashier:** cashier@afroexperts.com / Cashier2025!

## 🔒 Security Setup

### 1. SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your_domain.com
```

### 2. Firewall Configuration
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 3. MongoDB Security
```bash
# Edit MongoDB config
sudo nano /etc/mongod.conf

# Add authentication
security:
  authorization: enabled

# Restart MongoDB
sudo systemctl restart mongod
```

## 📊 Process Management

### PM2 Commands
```bash
# View running processes
pm2 list

# View logs
pm2 logs afroexperts-backend
pm2 logs afroexperts-frontend

# Restart services
pm2 restart afroexperts-backend
pm2 restart afroexperts-frontend

# Save PM2 configuration
pm2 save
pm2 startup
```

## 🔧 Maintenance

### Backup Database
```bash
mongodump --db afroexperts_erp --out /backup/$(date +%Y%m%d)
```

### Update Application
```bash
# Backend updates
cd backend
source venv/bin/activate
git pull
pip install -r requirements.txt
pm2 restart afroexperts-backend

# Frontend updates
cd frontend
git pull
npm install
npm run build
pm2 restart afroexperts-frontend
```

## 📈 Monitoring

### System Health Check
```bash
# Check services
pm2 status
sudo systemctl status nginx
sudo systemctl status mongod

# Check logs
pm2 logs --lines 100
sudo tail -f /var/log/nginx/error.log
```

### API Health Endpoint
- GET `/api/` - Returns API status and timestamp

## 🆘 Troubleshooting

### Common Issues:

1. **Backend won't start:**
   - Check MongoDB connection
   - Verify environment variables
   - Check Python dependencies

2. **Frontend shows errors:**
   - Verify REACT_APP_BACKEND_URL
   - Check if backend is running
   - Clear browser cache

3. **Database connection fails:**
   - Check MongoDB service status
   - Verify credentials in .env
   - Check firewall settings

### Log Locations:
- Backend logs: `pm2 logs afroexperts-backend`
- Frontend logs: `pm2 logs afroexperts-frontend`
- Nginx logs: `/var/log/nginx/access.log` & `/var/log/nginx/error.log`
- MongoDB logs: `/var/log/mongodb/mongod.log`

## 📞 Support

For deployment support or issues:
1. Check the troubleshooting section
2. Review log files for specific errors
3. Ensure all prerequisites are met
4. Verify environment configuration

## 🔄 Updates & Maintenance

The system includes:
- Automatic database migrations
- Health check endpoints
- Comprehensive logging
- Error handling and recovery
- Performance monitoring hooks

---

**🎉 Your Afro Experts ERP & POS System is ready for deployment!**