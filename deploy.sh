#!/bin/bash

# Afro Experts ERP & POS System Deployment Script
# Usage: ./deploy.sh

set -e

echo "🚀 Starting Afro Experts ERP & POS System Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if running as root
if [ "$EUID" -eq 0 ]; then
  print_error "Please don't run this script as root"
  exit 1
fi

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies
print_status "Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv nodejs npm mongodb nginx curl

# Install PM2 globally
print_status "Installing PM2 process manager..."
sudo npm install -g pm2

# Start and enable MongoDB
print_status "Starting MongoDB service..."
sudo systemctl start mongod
sudo systemctl enable mongod

# Create application directory
APP_DIR="/opt/afroexperts"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Copy application files
print_status "Copying application files..."
cp -r . $APP_DIR/
cd $APP_DIR

# Setup backend
print_status "Setting up backend..."
cd backend

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file from example
if [ ! -f .env ]; then
    cp .env.example .env
    print_warning "Please edit backend/.env with your configuration"
fi

# Initialize database with demo data
print_status "Initializing database..."
python seed_demo_data.py
python add_showcase_clients.py
python seed_rbac_permissions.py
python seed_translations.py

cd ..

# Setup frontend
print_status "Setting up frontend..."
cd frontend

# Install Node.js dependencies
npm install

# Create environment file from example
if [ ! -f .env ]; then
    cp .env.example .env
    print_warning "Please edit frontend/.env with your backend URL"
fi

# Build production version
npm run build

cd ..

# Create logs directory
mkdir -p logs

# Setup PM2 processes
print_status "Setting up PM2 processes..."

# Start backend
cd backend
pm2 start ../ecosystem.backend.json
cd ..

# Start frontend (serve built files)
pm2 serve frontend/build 3000 --name "afroexperts-frontend"

# Save PM2 configuration
pm2 save

# Setup PM2 startup script
pm2 startup

# Configure Nginx
print_status "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/afroexperts > /dev/null <<EOF
server {
    listen 80;
    server_name localhost;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/afroexperts /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Start and enable Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx

# Setup firewall
print_status "Configuring firewall..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
echo "y" | sudo ufw enable

# Create backup script
print_status "Creating backup script..."
tee backup.sh > /dev/null <<EOF
#!/bin/bash
BACKUP_DIR="/opt/backups/afroexperts"
DATE=\$(date +%Y%m%d_%H%M%S)

mkdir -p \$BACKUP_DIR

# Backup MongoDB
mongodump --db afroexperts_erp --out \$BACKUP_DIR/db_\$DATE

# Backup application files
tar -czf \$BACKUP_DIR/app_\$DATE.tar.gz /opt/afroexperts --exclude=/opt/afroexperts/logs --exclude=/opt/afroexperts/node_modules

echo "Backup completed: \$BACKUP_DIR"
EOF

chmod +x backup.sh

# Create systemd service files
print_status "Creating systemd services..."
sudo tee /etc/systemd/system/afroexperts.service > /dev/null <<EOF
[Unit]
Description=Afro Experts ERP & POS System
After=network.target mongod.service

[Service]
Type=forking
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/pm2 resurrect
ExecReload=/usr/bin/pm2 reload all
ExecStop=/usr/bin/pm2 kill
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable afroexperts

print_success "🎉 Deployment completed successfully!"
print_status "📋 Next Steps:"
echo "1. Edit configuration files:"
echo "   - $APP_DIR/backend/.env"
echo "   - $APP_DIR/frontend/.env"
echo ""
echo "2. Update your domain in Nginx config:"
echo "   sudo nano /etc/nginx/sites-available/afroexperts"
echo ""
echo "3. Restart services after configuration:"
echo "   pm2 restart all"
echo "   sudo systemctl restart nginx"
echo ""
echo "4. Default login credentials:"
echo "   Admin: admin@afroexperts.com / AfroExperts2025!"
echo "   Manager: manager@afroexperts.com / Manager2025!"
echo "   Cashier: cashier@afroexperts.com / Cashier2025!"
echo ""
echo "5. Access your application:"
echo "   Frontend: http://your-server-ip"
echo "   API: http://your-server-ip/api"
echo ""
print_success "🚀 Your Afro Experts ERP & POS System is ready to use!"