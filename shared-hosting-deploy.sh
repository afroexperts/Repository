#!/bin/bash

# Shared Hosting CPanel Deployment Script
# This script prepares the files for manual upload to CPanel

echo "🚀 Preparing Afro Experts ERP for Shared Hosting Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create deployment directory
DEPLOY_DIR="afroexperts-shared-hosting"
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

print_status "Creating shared hosting deployment package..."

# Create directory structure
mkdir -p $DEPLOY_DIR/public_html
mkdir -p $DEPLOY_DIR/api
mkdir -p $DEPLOY_DIR/docs
mkdir -p $DEPLOY_DIR/database

# Copy frontend build
print_status "Preparing frontend for static hosting..."
cd frontend
if [ ! -d "build" ]; then
    print_status "Building React frontend..."
    npm run build
fi

# Copy built frontend to public_html
cp -r build/* ../$DEPLOY_DIR/public_html/
cd ..

# Create .htaccess for frontend SPA routing
cat > $DEPLOY_DIR/public_html/.htaccess << 'EOF'
# React SPA routing
Options -MultiViews
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^ index.html [QR,L]

# Security headers
<IfModule mod_headers.c>
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
</IfModule>

# Enable compression
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
    AddOutputFilterByType DEFLATE application/json
</IfModule>

# Caching
<IfModule mod_expires.c>
    ExpiresActive on
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
</IfModule>
EOF

# Copy PHP API files
print_status "Preparing PHP API for shared hosting..."
cp -r shared-hosting-php-api/* $DEPLOY_DIR/api/

# Copy documentation
print_status "Copying documentation..."
cp SHARED_HOSTING_DEPLOYMENT.md $DEPLOY_DIR/docs/
cp SYSTEM_OVERVIEW.md $DEPLOY_DIR/docs/
cp DEPLOYMENT_GUIDE.md $DEPLOY_DIR/docs/

# Copy database schema
cp shared-hosting-php-api/database_schema.sql $DEPLOY_DIR/database/

# Create configuration templates
print_status "Creating configuration templates..."

# Frontend environment template
cat > $DEPLOY_DIR/public_html/.env.example << 'EOF'
# Update this with your domain
REACT_APP_BACKEND_URL=https://yourdomain.com/api

# App settings
REACT_APP_NAME=Afro Experts ERP
REACT_APP_VERSION=1.0.0
EOF

# Backend database config template
cat > $DEPLOY_DIR/api/config/database_config.php << 'EOF'
<?php
// Update these with your CPanel database credentials
$db_config = [
    'host' => 'localhost',
    'username' => 'cpanel_username_dbname',  // Format: cpanelusername_dbname
    'password' => 'your_database_password',   // Your database password
    'database' => 'cpanel_username_afroexperts',  // Format: cpanelusername_afroexperts
    'charset' => 'utf8mb4'
];

// JWT Secret Key - CHANGE THIS!
$jwt_secret = 'your_super_secret_jwt_key_change_this_in_production';
?>
EOF

# Create deployment instructions
cat > $DEPLOY_DIR/DEPLOYMENT_INSTRUCTIONS.md << 'EOF'
# 📋 CPanel Shared Hosting Deployment Instructions

## 🎯 Quick Start

### 1. Database Setup
1. **CPanel → MySQL Databases**
2. **Create Database:** `afroexperts`
3. **Create User:** with strong password
4. **Add User to Database:** with all privileges
5. **phpMyAdmin:** Import `database/database_schema.sql`

### 2. Upload Files
1. **File Manager:** Navigate to `public_html`
2. **Upload:** Contents of `public_html/` folder
3. **Create API folder:** `public_html/api/`
4. **Upload:** Contents of `api/` folder to `public_html/api/`

### 3. Configuration
1. **Edit:** `public_html/.env` with your domain
2. **Edit:** `api/config/database.php` with your database credentials
3. **Test:** Visit `https://yourdomain.com/api/` - should show API status

### 4. Domain Setup
1. **CPanel → Subdomains** (if using subdomain)
2. **Point to:** `public_html` folder
3. **SSL:** Enable in CPanel SSL section

## 🔧 File Structure After Upload

```
public_html/
├── index.html              # React app
├── static/                 # JS/CSS assets
├── .htaccess              # Apache config
├── api/                   # PHP API
│   ├── index.php          # API router
│   ├── config/            # Configuration
│   ├── controllers/       # API controllers
│   └── .htaccess         # API routing
└── uploads/               # File uploads (create manually)
```

## 🎉 Default Login
- **Email:** admin@afroexperts.com
- **Password:** AfroExperts2025!

## 🆘 Support
- Check CPanel error logs if issues occur
- Verify file permissions (755 for folders, 644 for files)
- Ensure PHP 7.4+ is selected in CPanel
EOF

# Create compressed package
print_status "Creating deployment package..."
tar -czf afroexperts-shared-hosting.tar.gz $DEPLOY_DIR/

# Create zip package for easier upload
if command -v zip &> /dev/null; then
    zip -r afroexperts-shared-hosting.zip $DEPLOY_DIR/
    print_success "✅ Created ZIP package: afroexperts-shared-hosting.zip"
fi

print_success "✅ Created TAR.GZ package: afroexperts-shared-hosting.tar.gz"

# Create file list
print_status "Creating file manifest..."
find $DEPLOY_DIR -type f | sort > $DEPLOY_DIR/FILE_MANIFEST.txt

# Summary
echo ""
print_success "🎉 Shared hosting deployment package ready!"
echo ""
echo "📦 Package Contents:"
echo "   ├── public_html/     - React frontend (static files)"
echo "   ├── api/             - PHP backend API"
echo "   ├── database/        - MySQL schema"
echo "   ├── docs/            - Documentation"
echo "   └── DEPLOYMENT_INSTRUCTIONS.md"
echo ""
echo "📋 Next Steps:"
echo "1. Download: afroexperts-shared-hosting.zip (or .tar.gz)"
echo "2. Follow: DEPLOYMENT_INSTRUCTIONS.md"
echo "3. Upload files to your CPanel hosting"
echo "4. Configure database and domain settings"
echo ""
print_warning "⚠️  Remember to:"
echo "   - Update database credentials in api/config/database.php"
echo "   - Change JWT secret key"
echo "   - Update frontend API URL"
echo "   - Test all functionality after deployment"
echo ""
print_success "🚀 Your ERP system is ready for shared hosting!"