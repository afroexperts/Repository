# 🌐 Shared Hosting Deployment Guide - CPanel/WHM

## ⚠️ **Important Notice**

**Shared hosting has significant limitations for full-stack applications.** This guide provides both optimal and alternative deployment strategies.

### 🚫 **Shared Hosting Limitations:**
- No root/sudo access
- Limited Python versions (often only 3.6-3.8)
- No PM2 or process managers
- No MongoDB (usually only MySQL/PostgreSQL)
- No custom service installations
- Limited memory and CPU resources
- No long-running processes

---

## 🎯 **Deployment Strategies**

### **Strategy A: Frontend-Only Deployment** ⭐ *Recommended for Shared Hosting*
Deploy only the React frontend as static files and use external backend services.

### **Strategy B: PHP Backend Alternative** 
Convert key functionality to PHP for better shared hosting compatibility.

### **Strategy C: Hybrid Deployment**
Frontend on shared hosting + backend on external service (Heroku, Railway, etc.)

---

# 📋 **Strategy A: Frontend-Only Deployment**

## 🔧 **Prerequisites**

### Shared Hosting Requirements:
- CPanel with File Manager access
- Node.js support (check with hosting provider)
- Custom domain or subdomain setup
- SSL certificate capability

### External Services Needed:
- **Backend API:** Deploy on Heroku, Railway, or DigitalOcean
- **Database:** MongoDB Atlas (free tier available)
- **File Storage:** AWS S3 or Cloudinary for uploads

## 📂 **Step 1: Prepare Frontend for Static Deployment**

### 1.1 Build Production Frontend
```bash
# On your local machine
cd frontend
npm install
npm run build
```

### 1.2 Create Static Configuration
Create `frontend/public/_redirects` for SPA routing:
```
/*    /index.html   200
```

Create `frontend/public/.htaccess` for Apache servers:
```apache
Options -MultiViews
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^ index.html [QR,L]

# Enable GZIP compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>

# Set cache headers
<IfModule mod_expires.c>
    ExpiresActive on
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
</IfModule>
```

## 📂 **Step 2: CPanel Deployment**

### 2.1 Access CPanel
1. Login to your hosting CPanel
2. Navigate to **File Manager**
3. Go to `public_html` (or your domain folder)

### 2.2 Upload Frontend Files
1. **Compress build folder:** `zip -r frontend-build.zip build/*`
2. **Upload via CPanel File Manager:**
   - Click "Upload" in File Manager
   - Select `frontend-build.zip`
   - Wait for upload completion
3. **Extract files:**
   - Right-click the uploaded zip
   - Select "Extract"
   - Move contents of `build` folder to `public_html`

### 2.3 Configure Domain/Subdomain
```
Domain Structure:
├── public_html/               # Main domain files
│   ├── index.html            # React app entry
│   ├── static/               # JS/CSS assets
│   ├── manifest.json         # PWA manifest
│   └── .htaccess            # Apache configuration
```

## 🔗 **Step 3: External Backend Setup**

### 3.1 Deploy Backend to Cloud Service

#### Option A: Heroku Deployment
```bash
# Install Heroku CLI and login
heroku login

# Create new app
heroku create afroexperts-api

# Set environment variables
heroku config:set MONGO_URL="your_mongodb_atlas_connection_string"
heroku config:set SECRET_KEY="your_jwt_secret"

# Deploy backend
git subtree push --prefix backend heroku main
```

#### Option B: Railway Deployment
1. Connect GitHub repository to Railway
2. Select backend folder for deployment
3. Set environment variables in Railway dashboard
4. Deploy with one click

### 3.2 Update Frontend Configuration
Update frontend `.env` to point to external backend:
```env
REACT_APP_BACKEND_URL=https://your-backend-app.herokuapp.com
```

## 💾 **Step 4: Database Setup (MongoDB Atlas)**

### 4.1 Create MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://cloud.mongodb.com)
2. Create free cluster
3. Create database user
4. Whitelist IP addresses (0.0.0.0/0 for shared hosting)

### 4.2 Get Connection String
```
mongodb+srv://username:password@cluster.mongodb.net/afroexperts_erp
```

### 4.3 Initialize Database
Run initialization scripts on your backend service:
```bash
# After backend deployment
heroku run python seed_demo_data.py
heroku run python add_showcase_clients.py
```

---

# 📋 **Strategy B: PHP Backend Alternative**

## 🔧 **PHP Version Requirements**
- PHP 7.4+ (PHP 8.0+ recommended)
- MySQL/MariaDB access
- JSON extension
- PDO extension
- URL rewrite capability

## 📂 **Step 1: Create PHP API Structure**

### 1.1 Directory Structure
```
public_html/
├── api/                      # PHP API endpoints
│   ├── index.php            # Main API router
│   ├── config/              # Configuration files
│   │   ├── database.php     # Database connection
│   │   └── cors.php         # CORS headers
│   ├── models/              # Data models
│   │   ├── User.php
│   │   ├── Product.php
│   │   └── Client.php
│   ├── controllers/         # API controllers
│   │   ├── AuthController.php
│   │   ├── ProductController.php
│   │   └── ClientController.php
│   └── .htaccess           # URL rewriting
├── app/                     # React frontend
│   ├── index.html
│   └── static/
└── .htaccess               # Main Apache config
```

### 1.2 Create PHP API Router (`api/index.php`)
```php
<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

require_once 'config/database.php';

// Simple routing
$request_uri = $_SERVER['REQUEST_URI'];
$path = parse_url($request_uri, PHP_URL_PATH);
$path = str_replace('/api', '', $path);
$method = $_SERVER['REQUEST_METHOD'];

// Route handling
switch (true) {
    case $path === '/' && $method === 'GET':
        echo json_encode(['message' => 'Afro Experts API is running', 'timestamp' => date('c')]);
        break;
        
    case preg_match('/^\/clients\/showcase$/', $path) && $method === 'GET':
        require_once 'controllers/ClientController.php';
        $controller = new ClientController();
        $controller->getShowcase();
        break;
        
    case preg_match('/^\/auth\/login$/', $path) && $method === 'POST':
        require_once 'controllers/AuthController.php';
        $controller = new AuthController();
        $controller->login();
        break;
        
    default:
        http_response_code(404);
        echo json_encode(['error' => 'Endpoint not found']);
        break;
}
?>
```

### 1.3 Database Configuration (`api/config/database.php`)
```php
<?php
class Database {
    private $host;
    private $username;
    private $password;
    private $database;
    private $connection;
    
    public function __construct() {
        // Get from CPanel database credentials
        $this->host = 'localhost';
        $this->username = 'your_cpanel_db_user';
        $this->password = 'your_cpanel_db_password';
        $this->database = 'your_cpanel_db_name';
    }
    
    public function connect() {
        $this->connection = null;
        
        try {
            $dsn = "mysql:host=" . $this->host . ";dbname=" . $this->database;
            $this->connection = new PDO($dsn, $this->username, $this->password);
            $this->connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch(PDOException $e) {
            echo "Connection error: " . $e->getMessage();
        }
        
        return $this->connection;
    }
}
?>
```

### 1.4 Client Controller (`api/controllers/ClientController.php`)
```php
<?php
require_once '../config/database.php';

class ClientController {
    private $db;
    
    public function __construct() {
        $database = new Database();
        $this->db = $database->connect();
    }
    
    public function getShowcase() {
        try {
            $query = "SELECT id, name, company_name, logo, website_url, display_order 
                     FROM clients 
                     WHERE showcase_on_website = 1 AND logo IS NOT NULL 
                     ORDER BY display_order ASC, name ASC";
            
            $stmt = $this->db->prepare($query);
            $stmt->execute();
            
            $clients = $stmt->fetchAll(PDO::FETCH_ASSOC);
            
            echo json_encode($clients);
        } catch(Exception $e) {
            http_response_code(500);
            echo json_encode(['error' => 'Failed to fetch client showcase']);
        }
    }
}
?>
```

## 📂 **Step 2: MySQL Database Setup via CPanel**

### 2.1 Create Database
1. **CPanel → MySQL Databases**
2. **Create Database:** `afroexperts_erp`
3. **Create User:** with secure password
4. **Add User to Database:** with full privileges

### 2.2 Create Tables
Use CPanel **phpMyAdmin** to run SQL:

```sql
-- Users table
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'manager', 'cashier') DEFAULT 'cashier',
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clients table with showcase fields
CREATE TABLE clients (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    company_name VARCHAR(200),
    logo TEXT,
    website_url VARCHAR(500),
    showcase_on_website BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    current_stock INT DEFAULT 0,
    minimum_stock INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (id, full_name, email, password_hash, role) VALUES
('1', 'System Admin', 'admin@afroexperts.com', SHA2('AfroExperts2025!', 256), 'admin');

INSERT INTO clients (id, name, company_name, logo, website_url, showcase_on_website, display_order) VALUES
('1', 'Tech Solutions Ltd', 'Tech Solutions Ltd', 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIi4uLg==', 'https://techsolutions.com', TRUE, 1),
('2', 'Build Corp', 'Build Corporation', 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIi4uLg==', 'https://buildcorp.com', TRUE, 2);
```

---

# 📋 **Strategy C: Hybrid Deployment**

## 🌐 **Architecture Overview**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│  Shared Hosting │    │   Cloud Service │    │  MongoDB Atlas  │
│  (Frontend)     │◄──►│   (Backend)     │◄──►│   (Database)    │
│  React App      │    │   FastAPI       │    │   Cloud DB      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Benefits:
- ✅ Full functionality preserved
- ✅ Leverage shared hosting for frontend
- ✅ Professional backend deployment
- ✅ Scalable database solution

---

# 🛠️ **CPanel-Specific Configurations**

## 📂 **File Manager Best Practices**

### Directory Permissions:
```
public_html/          755
├── api/             755
├── app/             755
├── uploads/         755 (if file uploads needed)
└── .htaccess        644
```

### Security Headers (`.htaccess`):
```apache
# Security headers
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options DENY
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'"

# Hide sensitive files
<Files ~ "\.(env|log|md)$">
    Order allow,deny
    Deny from all
</Files>
```

## 🔧 **CPanel Tools Integration**

### 1. **Cron Jobs Setup**
For automated tasks (backups, reports):
```bash
# CPanel → Cron Jobs
# Daily backup at 2 AM
0 2 * * * /usr/bin/php /home/username/public_html/api/scripts/backup.php

# Weekly report generation
0 6 * * 1 /usr/bin/php /home/username/public_html/api/scripts/weekly_report.php
```

### 2. **Email Setup**
Configure SMTP for notifications:
```php
// api/config/email.php
$mail_config = [
    'host' => 'mail.yourdomain.com',
    'username' => 'noreply@yourdomain.com',
    'password' => 'your_email_password',
    'port' => 587,
    'encryption' => 'tls'
];
```

### 3. **SSL Certificate**
1. **CPanel → SSL/TLS**
2. **Let's Encrypt** (if available)
3. **Force HTTPS Redirect**

---

# 🚨 **Limitations & Workarounds**

## ❌ **Cannot Do on Shared Hosting:**
- Real-time WebSocket connections
- Background processing (PM2, workers)
- Custom server installations
- Long-running processes
- Server-side caching (Redis/Memcached)

## ✅ **Workarounds:**
- **Real-time:** Use polling instead of WebSockets
- **Processing:** Use external services (Zapier, AWS Lambda)
- **Caching:** Use browser cache and CDN
- **File storage:** External services (AWS S3, Cloudinary)

---

# 📋 **Deployment Checklist**

## Pre-Deployment:
- [ ] Verify PHP version compatibility
- [ ] Check MySQL database limits
- [ ] Test file upload sizes
- [ ] Confirm domain/SSL setup

## Deployment:
- [ ] Upload and extract frontend files
- [ ] Configure database connection
- [ ] Test API endpoints
- [ ] Verify CORS settings
- [ ] Check error logs

## Post-Deployment:
- [ ] Test all functionality
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Update DNS if needed
- [ ] Document access credentials

---

# 🆘 **Troubleshooting**

## Common Issues:

### 1. **500 Internal Server Error**
```bash
# Check error logs in CPanel
# Common causes:
- Incorrect file permissions
- PHP syntax errors
- Missing extensions
- .htaccess configuration issues
```

### 2. **CORS Errors**
```php
// Add to all PHP files
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
```

### 3. **Database Connection Issues**
```php
// Verify credentials in CPanel
// Check database user privileges
// Ensure database exists
```

### 4. **File Upload Issues**
```php
// Check PHP limits
ini_set('upload_max_filesize', '10M');
ini_set('post_max_size', '10M');
ini_set('memory_limit', '256M');
```

---

# 📞 **Support Resources**

## Hosting Provider Support:
- Contact hosting support for PHP/MySQL limits
- Request Node.js support if needed
- Ask about SSL certificate options
- Verify backup policies

## Alternative Hosting Recommendations:
If shared hosting proves too limiting:
- **A2 Hosting** - Better PHP/Node.js support
- **SiteGround** - Good performance optimization
- **InMotion** - Developer-friendly features
- **VPS Upgrade** - Full control over environment

---

**🎉 Your shared hosting deployment guide is ready!**

This comprehensive guide provides multiple strategies to deploy your ERP system on shared hosting, from simple static deployment to full PHP conversion. Choose the strategy that best fits your hosting capabilities and requirements.