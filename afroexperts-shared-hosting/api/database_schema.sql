-- MySQL Database Schema for Shared Hosting
-- Run this in CPanel phpMyAdmin after creating your database

-- Users table
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'manager', 'cashier') DEFAULT 'cashier',
    status ENUM('active', 'inactive') DEFAULT 'active',
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_status (status)
);

-- Clients table with showcase functionality
CREATE TABLE clients (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    address TEXT,
    company_name VARCHAR(200),
    tax_number VARCHAR(50),
    client_type ENUM('individual', 'business') DEFAULT 'individual',
    credit_limit DECIMAL(12,2) DEFAULT 0.00,
    current_balance DECIMAL(12,2) DEFAULT 0.00,
    logo TEXT,
    website_url VARCHAR(500),
    showcase_on_website BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_email (email),
    INDEX idx_client_type (client_type),
    INDEX idx_showcase (showcase_on_website),
    INDEX idx_display_order (display_order)
);

-- Products table
CREATE TABLE products (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    cost_price DECIMAL(10,2) DEFAULT 0.00,
    sku VARCHAR(100) UNIQUE,
    unit VARCHAR(20) DEFAULT 'pieces',
    minimum_stock INT DEFAULT 0,
    current_stock INT DEFAULT 0,
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_category (category),
    INDEX idx_sku (sku),
    INDEX idx_stock (current_stock)
);

-- Orders table
CREATE TABLE orders (
    id VARCHAR(36) PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    client_id VARCHAR(36),
    status ENUM('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    subtotal DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    tax_amount DECIMAL(12,2) DEFAULT 0.00,
    discount_amount DECIMAL(12,2) DEFAULT 0.00,
    total_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    payment_status ENUM('pending', 'partial', 'paid', 'refunded') DEFAULT 'pending',
    notes TEXT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_date TIMESTAMP NULL,
    created_by VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_order_number (order_number),
    INDEX idx_client (client_id),
    INDEX idx_status (status),
    INDEX idx_payment_status (payment_status),
    INDEX idx_order_date (order_date)
);

-- Order items table
CREATE TABLE order_items (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36),
    product_name VARCHAR(200) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL,
    INDEX idx_order (order_id),
    INDEX idx_product (product_id)
);

-- Invoices table
CREATE TABLE invoices (
    id VARCHAR(36) PRIMARY KEY,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    client_id VARCHAR(36),
    order_id VARCHAR(36),
    status ENUM('draft', 'sent', 'paid', 'overdue', 'cancelled') DEFAULT 'draft',
    subtotal DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    tax_amount DECIMAL(12,2) DEFAULT 0.00,
    discount_amount DECIMAL(12,2) DEFAULT 0.00,
    total_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    amount_paid DECIMAL(12,2) DEFAULT 0.00,
    amount_due DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    payment_terms VARCHAR(100),
    notes TEXT,
    created_by VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_invoice_number (invoice_number),
    INDEX idx_client (client_id),
    INDEX idx_status (status),
    INDEX idx_due_date (due_date)
);

-- Financial transactions table
CREATE TABLE financial_transactions (
    id VARCHAR(36) PRIMARY KEY,
    transaction_type ENUM('income', 'expense') NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    payment_method ENUM('cash', 'bank_transfer', 'credit_card', 'mobile_money') DEFAULT 'cash',
    reference_id VARCHAR(36),
    reference_type ENUM('invoice', 'order', 'expense', 'other') DEFAULT 'other',
    transaction_date DATE NOT NULL,
    created_by VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_type (transaction_type),
    INDEX idx_category (category),
    INDEX idx_date (transaction_date),
    INDEX idx_reference (reference_id, reference_type)
);

-- Website settings table
CREATE TABLE website_settings (
    id VARCHAR(36) PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value LONGTEXT,
    setting_type ENUM('text', 'json', 'html', 'image') DEFAULT 'text',
    description VARCHAR(255),
    updated_by VARCHAR(36),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_key (setting_key)
);

-- Insert default admin user
INSERT INTO users (id, full_name, email, password_hash, role, status) VALUES 
(
    UUID(), 
    'System Administrator', 
    'admin@afroexperts.com', 
    '$2y$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', -- password: AfroExperts2025!
    'admin', 
    'active'
);

-- Insert sample clients with showcase
INSERT INTO clients (id, name, company_name, email, phone, client_type, logo, website_url, showcase_on_website, display_order) VALUES 
(
    UUID(),
    'RwandaTech Solutions',
    'RwandaTech Solutions Ltd',
    'info@rwandatech.rw',
    '+250788111222',
    'business',
    'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzAwNzNlNiIvPgogIDx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0IiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+VEVDSDwvdGV4dD4KPC9zdmc+',
    'https://rwandatech.rw',
    TRUE,
    1
),
(
    UUID(),
    'BuildRwanda Construction',
    'BuildRwanda Construction Ltd',
    'contact@buildrwanda.com',
    '+250788333444',
    'business',
    'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2ZmNjkwMCIvPgogIDx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEyIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+QlVJTEQ8L3RleHQ+Cjwvc3ZnPg==',
    'https://buildrwanda.com',
    TRUE,
    2
),
(
    UUID(),
    'Kigali Financial Services',
    'Kigali Financial Services Ltd',
    'hello@kigalifinance.rw',
    '+250788555666',
    'business',
    'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzI1OGI2NSIvPgogIDx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEyIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+RklOPC90ZXh0Pgo8L3N2Zz4=',
    'https://kigalifinance.rw',
    TRUE,
    3
);

-- Insert sample products
INSERT INTO products (id, name, category, description, price, cost_price, sku, unit, minimum_stock, current_stock) VALUES 
(UUID(), 'Laptop Computer', 'electronics', 'Business laptop with warranty', 850000.00, 700000.00, 'ELEC001', 'pieces', 5, 12),
(UUID(), 'Office Chair', 'furniture', 'Ergonomic office chair', 125000.00, 95000.00, 'FURN001', 'pieces', 10, 25),
(UUID(), 'Cement Bag', 'construction', '50kg cement bag', 8500.00, 7200.00, 'CONS001', 'bags', 100, 250),
(UUID(), 'Steel Rods', 'construction', '12mm steel construction rods', 25000.00, 22000.00, 'CONS002', 'pieces', 50, 80);

-- Insert default website settings
INSERT INTO website_settings (id, setting_key, setting_value, setting_type, description) VALUES 
(UUID(), 'company_name', 'Afro Experts', 'text', 'Company name'),
(UUID(), 'company_email', 'info@afroexperts.com', 'text', 'Company contact email'),
(UUID(), 'company_phone', '+250788123456', 'text', 'Company phone number'),
(UUID(), 'hero_title', 'Connecting Africa Through Technology', 'text', 'Homepage hero title'),
(UUID(), 'hero_subtitle', 'Empowering businesses with innovative solutions', 'text', 'Homepage hero subtitle');