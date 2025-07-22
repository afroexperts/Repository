#!/usr/bin/env python3
"""
Seed script to create demo data in MySQL database
"""

from database import SessionLocal, User, Client, Product, UserRole, UserStatus
import uuid
from datetime import datetime

def create_demo_users():
    """Create demo users"""
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin_exists = db.query(User).filter(User.email == "admin@afroexperts.com").first()
        
        if not admin_exists:
            admin_user = User(
                id=str(uuid.uuid4()),
                full_name="System Administrator",
                email="admin@afroexperts.com",
                password_hash=User.hash_password("AfroExperts2025!"),
                role=UserRole.admin,
                status=UserStatus.active,
                phone="+250 788 123 456",
                department="IT"
            )
            db.add(admin_user)
            
        # Create manager user
        manager_exists = db.query(User).filter(User.email == "manager@afroexperts.com").first()
        
        if not manager_exists:
            manager_user = User(
                id=str(uuid.uuid4()),
                full_name="Operations Manager", 
                email="manager@afroexperts.com",
                password_hash=User.hash_password("Manager123!"),
                role=UserRole.manager,
                status=UserStatus.active,
                phone="+250 788 654 321",
                department="Operations"
            )
            db.add(manager_user)
            
        # Create cashier user
        cashier_exists = db.query(User).filter(User.email == "cashier@afroexperts.com").first()
        
        if not cashier_exists:
            cashier_user = User(
                id=str(uuid.uuid4()),
                full_name="John Cashier",
                email="cashier@afroexperts.com", 
                password_hash=User.hash_password("Cashier123!"),
                role=UserRole.cashier,
                status=UserStatus.active,
                phone="+250 788 987 654",
                department="Sales"
            )
            db.add(cashier_user)
            
        db.commit()
        print("✓ Demo users created successfully")
        
    except Exception as e:
        print(f"✗ Error creating demo users: {e}")
        db.rollback()
    finally:
        db.close()

def create_demo_clients():
    """Create demo clients"""
    db = SessionLocal()
    
    try:
        # Check if clients exist
        client_count = db.query(Client).count()
        
        if client_count == 0:
            clients = [
                Client(
                    name="Rwanda Tech Solutions",
                    email="info@rwandatech.rw",
                    phone="+250 788 111 222",
                    address="Kigali, Rwanda",
                    client_type="business",
                    company_name="Rwanda Tech Solutions Ltd",
                    tax_number="1234567890"
                ),
                Client(
                    name="John Mugisha",
                    email="john.mugisha@email.com",
                    phone="+250 788 333 444",
                    address="Nyarugenge, Kigali",
                    client_type="individual"
                ),
                Client(
                    name="Central African Logistics",
                    email="contact@calogistics.cf",
                    phone="+236 70 123 456",
                    address="Bangui, Central African Republic",
                    client_type="business",
                    company_name="CAR Logistics SARL"
                )
            ]
            
            for client in clients:
                db.add(client)
                
            db.commit()
            print("✓ Demo clients created successfully")
            
    except Exception as e:
        print(f"✗ Error creating demo clients: {e}")
        db.rollback()
    finally:
        db.close()

def create_demo_products():
    """Create demo products"""
    db = SessionLocal()
    
    try:
        # Check if products exist
        product_count = db.query(Product).count()
        
        if product_count == 0:
            products = [
                Product(
                    name="Starlink Standard Kit",
                    category="satellite_internet",
                    description="High-speed satellite internet kit with dish and modem",
                    price=599.0,
                    cost_price=450.0,
                    sku="STL-STD-001",
                    unit="kit",
                    minimum_stock=5,
                    current_stock=15,
                    location="Warehouse A"
                ),
                Product(
                    name="Network Switch 24-Port",
                    category="network_hardware", 
                    description="Managed 24-port Gigabit Ethernet switch",
                    price=299.0,
                    cost_price=200.0,
                    sku="NSW-24P-001",
                    unit="piece",
                    minimum_stock=3,
                    current_stock=8,
                    location="Warehouse A"
                ),
                Product(
                    name="Marble Dust - Premium Grade",
                    category="construction_materials",
                    description="High-quality marble dust for construction (Rwanda exclusive)",
                    price=25.0,
                    cost_price=15.0,
                    sku="MRB-DUST-001", 
                    unit="kg",
                    minimum_stock=100,
                    current_stock=500,
                    location="Warehouse B"
                ),
                Product(
                    name="Laptop Dell Inspiron 15",
                    category="computers",
                    description="Business laptop with Intel i5 processor",
                    price=899.0,
                    cost_price=700.0,
                    sku="DELL-INS-15",
                    unit="piece",
                    minimum_stock=2,
                    current_stock=5,
                    location="Warehouse A"
                )
            ]
            
            for product in products:
                db.add(product)
                
            db.commit()
            print("✓ Demo products created successfully")
            
    except Exception as e:
        print(f"✗ Error creating demo products: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main seeding function"""
    print("🌱 Seeding MySQL database with demo data...")
    print("=" * 50)
    
    create_demo_users()
    create_demo_clients() 
    create_demo_products()
    
    print("=" * 50)
    print("🎉 Demo data seeding completed successfully!")

if __name__ == "__main__":
    main()