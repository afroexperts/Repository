from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from datetime import datetime, timedelta
from typing import List, Optional, Any, Dict
import logging
import uvicorn
import os
import uuid
from contextlib import asynccontextmanager

from database import (
    get_db, create_tables, User, Product, Order, OrderItem, Client,
    InventoryMovement, PosTransaction, ServiceBooking, FinancialTransaction,
    WebsiteSetting, ContactSubmission, UserRole, UserStatus, OrderStatus,
    PaymentMethod, ServiceType, MovementType, TransactionType
)

# Import Pydantic models for validation (keeping the existing ones)
from models import (
    UserCreate, UserLogin, LoginResponse, DashboardStatsResponse,
    ProductCreate, OrderCreate, ClientCreate, InventoryMovementCreate,
    ServiceBookingCreate, FinancialTransactionCreate, ContactSubmissionCreate,
    WebsiteSettingsUpdate
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Creating database tables...")
    create_tables()
    logger.info("Application started successfully")
    yield
    # Shutdown
    logger.info("Application shutting down...")

app = FastAPI(
    title="Afro Experts ERP & POS System",
    description="Complete business management system with MySQL backend",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# Authentication Endpoints
# ===============================

@app.post("/api/auth/login", response_model=LoginResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """User login endpoint"""
    try:
        # Find user by email
        user = db.query(User).filter(User.email == user_data.email).first()
        
        if not user or not user.verify_password(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if user.status != UserStatus.active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is suspended or inactive"
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Create Pydantic User model for response
        user_data = {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "password_hash": user.password_hash,
            "role": user.role,
            "status": user.status,
            "phone": user.phone,
            "department": user.department,
            "last_login": user.last_login,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
        
        return LoginResponse(
            success=True,
            message="Login successful",
            user=user_data,
            token=user.id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@app.get("/api/auth/me")
def get_current_user(token: str = None, db: Session = Depends(get_db)):
    """Get current user information"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token required"
        )
    
    user = db.query(User).filter(User.id == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    return user

# ===============================
# Dashboard Endpoints
# ===============================

@app.get("/api/dashboard/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    try:
        # Calculate stats
        total_sales = db.query(func.sum(PosTransaction.total_amount)).scalar() or 0
        active_orders = db.query(Order).filter(Order.status.in_(['pending', 'processing'])).count()
        total_clients = db.query(Client).count()
        low_stock_items = db.query(Product).filter(Product.current_stock <= Product.minimum_stock).count()
        
        return DashboardStatsResponse(
            total_sales=float(total_sales),
            active_orders=active_orders,
            total_clients=total_clients,
            low_stock_items=low_stock_items,
            pending_quotes=0,  # Add this field
            monthly_growth=15.2
        )
        
    except Exception as e:
        logger.error(f"Dashboard stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard stats")

@app.get("/api/dashboard/recent-transactions")
def get_recent_transactions(limit: int = 10, db: Session = Depends(get_db)):
    """Get recent transactions"""
    try:
        transactions = (
            db.query(PosTransaction)
            .order_by(PosTransaction.created_at.desc())
            .limit(limit)
            .all()
        )
        
        return {"transactions": transactions}
        
    except Exception as e:
        logger.error(f"Recent transactions error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch recent transactions")

# ===============================
# Product Management Endpoints
# ===============================

@app.get("/api/products")
def get_products(db: Session = Depends(get_db)):
    """Get all products"""
    return db.query(Product).all()

@app.post("/api/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create new product"""
    try:
        db_product = Product(
            name=product.name,
            category=product.category,
            description=product.description,
            price=product.price,
            cost_price=product.cost_price,
            sku=product.sku,
            unit=product.unit,
            minimum_stock=product.minimum_stock,
            current_stock=product.current_stock,
            location=product.location
        )
        
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        
        return db_product
        
    except Exception as e:
        logger.error(f"Create product error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create product")

@app.get("/api/products/low-stock")
def get_low_stock_products(db: Session = Depends(get_db)):
    """Get products with low stock"""
    return db.query(Product).filter(Product.current_stock <= Product.minimum_stock).all()

# ===============================
# Client Management Endpoints
# ===============================

@app.get("/api/clients")
def get_clients(db: Session = Depends(get_db)):
    """Get all clients"""
    return db.query(Client).all()

@app.post("/api/clients")
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """Create new client"""
    try:
        db_client = Client(
            name=client.name,
            email=client.email,
            phone=client.phone,
            address=client.address,
            client_type=client.client_type,
            company_name=client.company_name,
            tax_number=client.tax_number,
            credit_limit=client.credit_limit or 0.0
        )
        
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        
        return db_client
        
    except Exception as e:
        logger.error(f"Create client error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create client")

# ===============================
# Order Management Endpoints  
# ===============================

@app.get("/api/orders")
def get_orders(db: Session = Depends(get_db)):
    """Get all orders"""
    return db.query(Order).all()

@app.post("/api/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create new order"""
    try:
        # Calculate totals
        subtotal = sum(item.quantity * item.unit_price for item in order.items)
        tax_amount = subtotal * 0.18  # 18% VAT
        total_amount = subtotal + tax_amount
        
        db_order = Order(
            client_id=order.client_id,
            status=OrderStatus.pending,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,
            payment_method=order.payment_method,
            notes=order.notes
        )
        
        db.add(db_order)
        db.flush()  # Get the ID
        
        # Add order items
        for item in order.items:
            db_item = OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=item.quantity * item.unit_price
            )
            db.add(db_item)
        
        db.commit()
        db.refresh(db_order)
        
        return db_order
        
    except Exception as e:
        logger.error(f"Create order error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create order")

# ===============================
# Settings Management Endpoints
# ===============================

@app.get("/api/settings")
def get_settings(db: Session = Depends(get_db)):
    """Get website settings"""
    try:
        settings = db.query(WebsiteSetting).all()
        return settings
    except Exception as e:
        logger.error(f"Get settings error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch settings")

@app.put("/api/settings")
def update_settings(settings_data: WebsiteSettingsUpdate, db: Session = Depends(get_db)):
    """Update website settings"""
    try:
        # For now, use a default user_id since authentication is simplified
        user_id = "357dbcec-a104-443f-8dec-9e8895417ead"  # Admin user ID
        
        # Check if setting exists
        setting = db.query(WebsiteSetting).filter(WebsiteSetting.section == settings_data.section).first()
        
        if setting:
            # Update existing setting
            setting.data = settings_data.data
            setting.updated_by = user_id
            setting.updated_at = datetime.utcnow()
        else:
            # Create new setting
            setting = WebsiteSetting(
                section=settings_data.section,
                data=settings_data.data,
                updated_by=user_id
            )
            db.add(setting)
        
        db.commit()
        db.refresh(setting)
        
        return {
            "success": True,
            "message": f"Settings updated successfully for section: {settings_data.section}",
            "id": setting.id
        }
        
    except Exception as e:
        logger.error(f"Update settings error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update settings")

# ===============================
# POS Endpoints
# ===============================

@app.get("/api/pos/transactions")
def get_pos_transactions(db: Session = Depends(get_db)):
    """Get POS transactions"""
    return db.query(PosTransaction).order_by(PosTransaction.created_at.desc()).limit(50).all()

# ===============================
# Inventory Endpoints
# ===============================

@app.get("/api/inventory/movements")
def get_inventory_movements(db: Session = Depends(get_db)):
    """Get inventory movements"""
    return db.query(InventoryMovement).order_by(InventoryMovement.created_at.desc()).limit(100).all()

# ===============================
# Finance Endpoints
# ===============================

@app.get("/api/finance/transactions") 
def get_financial_transactions(db: Session = Depends(get_db)):
    """Get financial transactions"""
    return db.query(FinancialTransaction).order_by(FinancialTransaction.created_at.desc()).limit(100).all()

@app.get("/api/finance/summary")
def get_financial_summary(db: Session = Depends(get_db)):
    """Get financial summary"""
    try:
        total_income = db.query(func.sum(FinancialTransaction.amount)).filter(
            FinancialTransaction.transaction_type == TransactionType.income
        ).scalar() or 0
        
        total_expense = db.query(func.sum(FinancialTransaction.amount)).filter(
            FinancialTransaction.transaction_type == TransactionType.expense
        ).scalar() or 0
        
        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "net_profit": float(total_income - total_expense)
        }
        
    except Exception as e:
        logger.error(f"Financial summary error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch financial summary")

# ===============================
# Service Booking Endpoints
# ===============================

@app.get("/api/services/bookings")
def get_service_bookings(db: Session = Depends(get_db)):
    """Get service bookings"""
    return db.query(ServiceBooking).order_by(ServiceBooking.created_at.desc()).all()

# ===============================
# Health Check
# ===============================

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": "mysql", "version": "2.0.0"}

# ===============================
# Legacy Endpoints (for compatibility)
# ===============================

@app.get("/api/content/testimonials")
def get_testimonials():
    """Get testimonials - legacy compatibility"""
    return []

@app.get("/api/stats/impact")
def get_impact_stats():
    """Get impact stats - legacy compatibility"""
    return {"communities_connected": 50, "businesses_served": 1000}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)