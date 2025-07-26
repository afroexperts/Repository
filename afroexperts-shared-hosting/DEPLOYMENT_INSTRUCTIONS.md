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
