#!/usr/bin/env python3
"""
Data migration script from MongoDB to MySQL
Migrates all data from exported JSON files to MySQL database
"""

import json
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from database_mysql import (
    SessionLocal, User, Product, Order, OrderItem, Client, 
    InventoryMovement, PosTransaction, ServiceBooking, 
    FinancialTransaction, WebsiteSetting, ContactSubmission,
    UserRole, UserStatus, OrderStatus, PaymentMethod, 
    ServiceType, MovementType, TransactionType, CountryEnum, ContactStatus
)
import sys
import os

def parse_datetime(date_str):
    """Parse datetime string from MongoDB export"""
    if not date_str:
        return None
    
    if isinstance(date_str, dict) and '$date' in date_str:
        # MongoDB date format
        return datetime.fromisoformat(date_str['$date'].replace('Z', '+00:00'))
    elif isinstance(date_str, str):
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return datetime.utcnow()
    return None

def migrate_users(db: Session):
    """Migrate users from users.json"""
    print("Migrating users...")
    
    try:
        with open('/app/migration_data/users.json', 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                
                user = User(
                    id=data.get('id', str(uuid.uuid4())),
                    full_name=data['full_name'],
                    email=data['email'],
                    password_hash=data['password_hash'],
                    role=UserRole(data['role']),
                    status=UserStatus(data.get('status', 'active')),
                    phone=data.get('phone'),
                    department=data.get('department'),
                    last_login=parse_datetime(data.get('last_login')),
                    created_at=parse_datetime(data.get('created_at')) or datetime.utcnow(),
                    updated_at=parse_datetime(data.get('updated_at'))
                )
                
                db.add(user)
            
        db.commit()
        print("✓ Users migrated successfully")
        
    except Exception as e:
        print(f"✗ Error migrating users: {e}")
        db.rollback()

def migrate_clients(db: Session):
    """Migrate clients from clients.json"""
    print("Migrating clients...")
    
    try:
        with open('/app/migration_data/clients.json', 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                
                client = Client(
                    id=data.get('id', str(uuid.uuid4())),
                    name=data['name'],
                    email=data.get('email'),
                    phone=data.get('phone'),
                    address=data.get('address'),
                    client_type=data.get('type', 'individual'),
                    company_name=data.get('company_name'),
                    tax_number=data.get('tax_number'),
                    credit_limit=data.get('credit_limit', 0.0),
                    current_balance=data.get('current_balance', 0.0),
                    created_at=parse_datetime(data.get('created_at')) or datetime.utcnow(),
                    updated_at=parse_datetime(data.get('updated_at'))
                )
                
                db.add(client)
            
        db.commit()
        print("✓ Clients migrated successfully")
        
    except Exception as e:
        print(f"✗ Error migrating clients: {e}")
        db.rollback()

def migrate_products(db: Session):
    """Migrate products from products.json"""
    print("Migrating products...")
    
    try:
        with open('/app/migration_data/products.json', 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                
                product = Product(
                    id=data.get('id', str(uuid.uuid4())),
                    name=data['name'],
                    category=data['category'],
                    description=data.get('description'),
                    price=float(data['price']),
                    cost_price=float(data.get('cost_price', 0)) if data.get('cost_price') else None,
                    sku=data.get('sku'),
                    unit=data.get('unit', 'pieces'),
                    minimum_stock=int(data.get('minimum_stock', 0)),
                    current_stock=int(data.get('current_stock', 0)),
                    location=data.get('location'),
                    created_at=parse_datetime(data.get('created_at')) or datetime.utcnow(),
                    updated_at=parse_datetime(data.get('updated_at'))
                )
                
                db.add(product)
            
        db.commit()
        print("✓ Products migrated successfully")
        
    except Exception as e:
        print(f"✗ Error migrating products: {e}")
        db.rollback()

def migrate_orders(db: Session):
    """Migrate orders from orders.json"""
    print("Migrating orders...")
    
    try:
        with open('/app/migration_data/orders.json', 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                
                order = Order(
                    id=data.get('id', str(uuid.uuid4())),
                    order_number=data.get('order_number', f"ORD-{str(uuid.uuid4())[:8]}"),
                    client_id=data.get('client_id', ''),  # Handle missing client_id
                    status=OrderStatus(data.get('status', 'pending')),
                    subtotal=float(data.get('subtotal', 0)),
                    tax_amount=float(data.get('tax_amount', 0)),
                    discount_amount=float(data.get('discount_amount', 0)),
                    total_amount=float(data.get('total_amount', 0)),
                    payment_method=PaymentMethod(data['payment_method']) if data.get('payment_method') else None,
                    payment_status=data.get('payment_status', 'pending'),
                    notes=data.get('notes'),
                    created_at=parse_datetime(data.get('created_at')) or datetime.utcnow(),
                    updated_at=parse_datetime(data.get('updated_at'))
                )
                
                db.add(order)
                
                # Migrate order items
                if 'items' in data:
                    for item_data in data['items']:
                        order_item = OrderItem(
                            id=str(uuid.uuid4()),
                            order_id=order.id,
                            product_id=item_data['product_id'],
                            quantity=int(item_data['quantity']),
                            unit_price=float(item_data['unit_price']),
                            line_total=float(item_data['line_total'])
                        )
                        db.add(order_item)
            
        db.commit()
        print("✓ Orders migrated successfully")
        
    except Exception as e:
        print(f"✗ Error migrating orders: {e}")
        db.rollback()

def migrate_inventory_movements(db: Session):
    """Migrate inventory movements from inventory_movements.json"""
    print("Migrating inventory movements...")
    
    try:
        with open('/app/migration_data/inventory_movements.json', 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                
                movement = InventoryMovement(
                    id=data.get('id', str(uuid.uuid4())),
                    product_id=data['product_id'],
                    movement_type=MovementType(data['movement_type']),
                    quantity=int(data['quantity']),
                    unit_cost=float(data.get('unit_cost', 0)) if data.get('unit_cost') else None,
                    total_cost=float(data.get('total_cost', 0)) if data.get('total_cost') else None,
                    reference_number=data.get('reference_number'),
                    notes=data.get('notes'),
                    created_by=data['created_by'],
                    created_at=parse_datetime(data.get('created_at')) or datetime.utcnow()
                )
                
                db.add(movement)
            
        db.commit()
        print("✓ Inventory movements migrated successfully")
        
    except Exception as e:
        print(f"✗ Error migrating inventory movements: {e}")
        db.rollback()

def migrate_pos_transactions(db: Session):
    """Migrate POS transactions from pos_transactions.json"""
    print("Migrating POS transactions...")
    
    try:
        with open('/app/migration_data/pos_transactions.json', 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                
                transaction = PosTransaction(
                    id=data.get('id', str(uuid.uuid4())),
                    receipt_number=data.get('receipt_number', f"RCP-{str(uuid.uuid4())[:8]}"),
                    client_id=data.get('client_id'),
                    items=data.get('items', []),
                    subtotal=float(data.get('subtotal', 0)),
                    discount_percentage=float(data.get('discount_percentage', 0)),
                    discount_amount=float(data.get('discount_amount', 0)),
                    tax_percentage=float(data.get('tax_percentage', 0)),
                    tax_amount=float(data.get('tax_amount', 0)),
                    total_amount=float(data.get('total_amount', 0)),
                    payment_method=PaymentMethod(data['payment_method']),
                    payment_received=float(data.get('payment_received', 0)),
                    change_given=float(data.get('change_given', 0)),
                    cashier_id=data['cashier_id'],
                    created_at=parse_datetime(data.get('created_at')) or datetime.utcnow()
                )
                
                db.add(transaction)
            
        db.commit()
        print("✓ POS transactions migrated successfully")
        
    except Exception as e:
        print(f"✗ Error migrating POS transactions: {e}")
        db.rollback()

def migrate_service_bookings(db: Session):
    """Migrate service bookings from service_bookings.json"""
    print("Migrating service bookings...")
    
    try:
        with open('/app/migration_data/service_bookings.json', 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                
                booking = ServiceBooking(
                    id=data.get('id', str(uuid.uuid4())),
                    booking_number=data.get('booking_number', f"SRV-{str(uuid.uuid4())[:8]}"),
                    client_name=data['client_name'],
                    client_email=data.get('client_email'),
                    client_phone=data['client_phone'],
                    service_type=ServiceType(data['service_type']),
                    description=data['description'],
                    location=data['location'],
                    preferred_date=parse_datetime(data.get('preferred_date')),
                    status=data.get('status', 'pending'),
                    assigned_technician_id=data.get('assigned_technician_id'),
                    estimated_cost=float(data.get('estimated_cost', 0)) if data.get('estimated_cost') else None,
                    actual_cost=float(data.get('actual_cost', 0)) if data.get('actual_cost') else None,
                    notes=data.get('notes'),
                    created_at=parse_datetime(data.get('created_at')) or datetime.utcnow(),
                    updated_at=parse_datetime(data.get('updated_at'))
                )
                
                db.add(booking)
            
        db.commit()
        print("✓ Service bookings migrated successfully")
        
    except Exception as e:
        print(f"✗ Error migrating service bookings: {e}")
        db.rollback()

def migrate_financial_transactions(db: Session):
    """Migrate financial transactions from financial_transactions.json"""
    print("Migrating financial transactions...")
    
    try:
        with open('/app/migration_data/financial_transactions.json', 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                
                transaction = FinancialTransaction(
                    id=data.get('id', str(uuid.uuid4())),
                    transaction_number=data.get('transaction_number', f"TXN-{str(uuid.uuid4())[:8]}"),
                    transaction_type=TransactionType(data['transaction_type']),
                    category=data.get('category', 'general'),  # Default category
                    description=data['description'],
                    amount=float(data['amount']),
                    reference_id=data.get('reference_id'),
                    created_by=data['created_by'],
                    created_at=parse_datetime(data.get('created_at')) or datetime.utcnow()
                )
                
                db.add(transaction)
            
        db.commit()
        print("✓ Financial transactions migrated successfully")
        
    except Exception as e:
        print(f"✗ Error migrating financial transactions: {e}")
        db.rollback()

def migrate_website_settings(db: Session):
    """Migrate website settings from website_settings.json"""
    print("Migrating website settings...")
    
    try:
        with open('/app/migration_data/website_settings.json', 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                
                setting = WebsiteSetting(
                    id=data.get('id', str(uuid.uuid4())),
                    section=data['section'],
                    data=data['data'],
                    updated_by=data['updated_by'],
                    created_at=parse_datetime(data.get('created_at')) or datetime.utcnow(),
                    updated_at=parse_datetime(data.get('updated_at'))
                )
                
                db.add(setting)
            
        db.commit()
        print("✓ Website settings migrated successfully")
        
    except Exception as e:
        print(f"✗ Error migrating website settings: {e}")
        db.rollback()

def migrate_contact_submissions(db: Session):
    """Migrate contact submissions from contact_submissions.json"""
    print("Migrating contact submissions...")
    
    try:
        with open('/app/migration_data/contact_submissions.json', 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                
                submission = ContactSubmission(
                    id=data.get('id', str(uuid.uuid4())),
                    name=data['name'],
                    email=data['email'],
                    phone=data.get('phone'),
                    country=CountryEnum(data['country']),
                    message=data['message'],
                    status=ContactStatus(data.get('status', 'new')),
                    created_at=parse_datetime(data.get('created_at')) or datetime.utcnow()
                )
                
                db.add(submission)
            
        db.commit()
        print("✓ Contact submissions migrated successfully")
        
    except Exception as e:
        print(f"✗ Error migrating contact submissions: {e}")
        db.rollback()

def main():
    """Main migration function"""
    print("🚀 Starting MongoDB to MySQL data migration...")
    print("=" * 50)
    
    # Check if migration data exists
    if not os.path.exists('/app/migration_data'):
        print("✗ Migration data directory not found!")
        return
    
    db = SessionLocal()
    
    try:
        # Run migrations in order (respecting foreign key constraints)
        migrate_users(db)
        migrate_clients(db)
        migrate_products(db)
        migrate_orders(db)
        migrate_inventory_movements(db)
        migrate_pos_transactions(db)
        migrate_service_bookings(db)
        migrate_financial_transactions(db)
        migrate_website_settings(db)
        migrate_contact_submissions(db)
        
        print("=" * 50)
        print("🎉 Data migration completed successfully!")
        
        # Print summary
        print("\n📊 Migration Summary:")
        print(f"Users: {db.query(User).count()}")
        print(f"Clients: {db.query(Client).count()}")
        print(f"Products: {db.query(Product).count()}")
        print(f"Orders: {db.query(Order).count()}")
        print(f"Order Items: {db.query(OrderItem).count()}")
        print(f"Inventory Movements: {db.query(InventoryMovement).count()}")
        print(f"POS Transactions: {db.query(PosTransaction).count()}")
        print(f"Service Bookings: {db.query(ServiceBooking).count()}")
        print(f"Financial Transactions: {db.query(FinancialTransaction).count()}")
        print(f"Website Settings: {db.query(WebsiteSetting).count()}")
        print(f"Contact Submissions: {db.query(ContactSubmission).count()}")
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()