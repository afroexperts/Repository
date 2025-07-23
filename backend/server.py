from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import io
from datetime import datetime, timedelta
from fastapi.responses import StreamingResponse
import tempfile
import os
from typing import List, Optional, Any, Dict
import logging
import uvicorn
import uuid
from contextlib import asynccontextmanager

from database import (
    get_db, create_tables, User, Product, Order, OrderItem, Client,
    InventoryMovement, PosTransaction, ServiceBooking, FinancialTransaction,
    WebsiteSetting, ContactSubmission, UserRole, UserStatus, OrderStatus,
    PaymentMethod, ServiceType, MovementType, TransactionType,
    Invoice, InvoiceItem, InvoicePayment, InvoiceLog, InvoiceTemplate,
    InvoiceStatus, InvoiceType, PaymentStatus, Currency,
    PortfolioItem, PortfolioCategory, PortfolioStatus,
    SecondHandItem, SecondHandCategory, SecondHandCondition,
    MarbleDustBatch, MarbleDustQuality, MarbleDustStatus,
    StarlinkInstallation, StarlinkKitType, StarlinkInstallationStatus, StarlinkServiceStatus,
    Permission, Language, RolePermission, UserPermission, Translation, UserPreference,
    RecurringInvoice, RecurringInvoiceItem, RecurringInvoiceFrequency
)

# Import Pydantic models for validation (keeping the existing ones)
from models import (
    UserCreate, UserLogin, LoginResponse, DashboardStatsResponse,
    ProductCreate, OrderCreate, ClientCreate, InventoryMovementCreate,
    ServiceBookingCreate, FinancialTransactionCreate, ContactSubmissionCreate,
    WebsiteSettingsUpdate, InvoiceCreate, InvoiceUpdate, InvoiceItemCreate,
    InvoicePaymentCreate, InvoicePaymentUpdate, InvoiceTemplateCreate,
    PortfolioItemCreate, PortfolioItemUpdate, PortfolioItem as PortfolioItemResponse,
    SecondHandItemCreate, SecondHandItemUpdate, SecondHandItem as SecondHandItemResponse,
    MarbleDustBatchCreate, MarbleDustBatchUpdate, MarbleDustBatch as MarbleDustBatchResponse,
    StarlinkInstallationCreate, StarlinkInstallationUpdate, StarlinkInstallation as StarlinkInstallationResponse,
    PermissionCheck, RolePermissionsUpdate, UserPermissionCreate, UserPermissionUpdate,
    TranslationCreate, TranslationUpdate, Translation as TranslationResponse,
    UserPreferenceUpdate, UserPreference as UserPreferenceResponse,
    RecurringInvoiceCreate, RecurringInvoiceUpdate, RecurringInvoice as RecurringInvoiceResponse
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
    """Get all orders with client and item details"""
    try:
        orders = db.query(Order).all()
        
        # Format response with client details
        formatted_orders = []
        for order in orders:
            formatted_order = {
                "id": order.id,
                "order_number": order.order_number,
                "client_id": order.client_id,
                "client_name": order.client.name if order.client else "Unknown",
                "status": order.status.value,
                "subtotal": order.subtotal,
                "tax_amount": order.tax_amount,
                "total_amount": order.total_amount,
                "payment_method": order.payment_method.value if order.payment_method else None,
                "payment_status": order.payment_status,
                "notes": order.notes,
                "created_at": order.created_at.isoformat() if order.created_at else None,
                "updated_at": order.updated_at.isoformat() if order.updated_at else None,
                "items": [
                    {
                        "id": item.id,
                        "product_id": item.product_id,
                        "product_name": item.product.name if item.product else "Unknown",
                        "quantity": item.quantity,
                        "unit_price": item.unit_price,
                        "line_total": item.line_total
                    } for item in order.items
                ]
            }
            formatted_orders.append(formatted_order)
        
        return formatted_orders
    except Exception as e:
        logger.error(f"Get orders error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve orders")

@app.post("/api/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create new order"""
    try:
        # Find or create client based on provided information
        client = None
        if order.client_email:
            # Try to find existing client by email
            client = db.query(Client).filter(Client.email == order.client_email).first()
        
        if not client and order.client_phone:
            # Try to find existing client by phone
            client = db.query(Client).filter(Client.phone == order.client_phone).first()
        
        if not client:
            # Create new client
            client = Client(
                name=order.client_name,
                email=order.client_email,
                phone=order.client_phone,
                client_type="individual"
            )
            db.add(client)
            db.flush()  # Get the client ID
        
        # Generate order number
        order_count = db.query(Order).count()
        order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{order_count + 1:04d}"
        
        # Calculate totals
        subtotal = sum(item.quantity * item.unit_price for item in order.items)
        tax_amount = subtotal * 0.18  # 18% VAT
        total_amount = subtotal + tax_amount
        
        db_order = Order(
            order_number=order_number,
            client_id=client.id,
            status=OrderStatus.pending,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,
            payment_method=order.payment_method,
            payment_status="pending",
            notes=order.notes
        )
        
        db.add(db_order)
        db.flush()  # Get the ID
        
        # Add order items and update product stock
        for item in order.items:
            # Check product availability
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=400, detail=f"Product not found: {item.product_id}")
            
            if product.current_stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
            
            # Create order item
            db_item = OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=item.quantity * item.unit_price
            )
            db.add(db_item)
            
            # Update product stock
            product.current_stock -= item.quantity
        
        db.commit()
        db.refresh(db_order)
        
        return db_order
        
    except Exception as e:
        logger.error(f"Create order error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create order")

@app.get("/api/orders/{order_id}")
def get_order(order_id: str, db: Session = Depends(get_db)):
    """Get single order with details"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        logger.error(f"Get order error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve order")

@app.put("/api/orders/{order_id}")
def update_order(order_id: str, order_update: dict, db: Session = Depends(get_db)):
    """Update order details"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Update allowed fields
        if 'status' in order_update:
            order.status = OrderStatus(order_update['status'])
        if 'payment_method' in order_update:
            order.payment_method = PaymentMethod(order_update['payment_method'])
        if 'payment_status' in order_update:
            order.payment_status = order_update['payment_status']
        if 'notes' in order_update:
            order.notes = order_update['notes']
        
        order.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(order)
        
        return order
    except Exception as e:
        logger.error(f"Update order error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update order")

@app.delete("/api/orders/{order_id}")
def delete_order(order_id: str, db: Session = Depends(get_db)):
    """Delete an order"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Check if order can be deleted (not delivered)
        if order.status == OrderStatus.delivered:
            raise HTTPException(status_code=400, detail="Cannot delete delivered orders")
        
        # Delete order items first
        db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
        
        # Delete the order
        db.delete(order)
        db.commit()
        
        return {"message": "Order deleted successfully"}
    except Exception as e:
        logger.error(f"Delete order error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete order")

@app.get("/api/orders/status/{status}")
def get_orders_by_status(status: str, db: Session = Depends(get_db)):
    """Get orders by status"""
    try:
        orders = db.query(Order).filter(Order.status == OrderStatus(status)).all()
        return orders
    except Exception as e:
        logger.error(f"Get orders by status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve orders")

@app.put("/api/orders/{order_id}/status")
def update_order_status(order_id: str, status_update: dict, db: Session = Depends(get_db)):
    """Update order status"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        new_status = OrderStatus(status_update['status'])
        order.status = new_status
        order.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(order)
        
        return {"message": f"Order status updated to {new_status.value}", "order": order}
    except Exception as e:
        logger.error(f"Update order status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update order status")

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
    """Get inventory movements with product details"""
    try:
        movements = db.query(InventoryMovement).order_by(InventoryMovement.created_at.desc()).limit(100).all()
        
        # Format response with product details
        formatted_movements = []
        for movement in movements:
            formatted_movement = {
                "id": movement.id,
                "product_id": movement.product_id,
                "product_name": movement.product.name if movement.product else "Unknown",
                "movement_type": movement.movement_type.value,
                "quantity": movement.quantity,
                "unit_cost": movement.unit_cost,
                "total_cost": movement.total_cost,
                "reference_number": movement.reference_number,
                "notes": movement.notes,
                "created_at": movement.created_at.isoformat() if movement.created_at else None,
                "created_by": movement.created_by
            }
            formatted_movements.append(formatted_movement)
        
        return formatted_movements
    except Exception as e:
        logger.error(f"Get inventory movements error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve inventory movements")

@app.get("/api/inventory/movements/{movement_id}")
def get_inventory_movement(movement_id: str, db: Session = Depends(get_db)):
    """Get single inventory movement"""
    try:
        movement = db.query(InventoryMovement).filter(InventoryMovement.id == movement_id).first()
        if not movement:
            raise HTTPException(status_code=404, detail="Movement not found")
        return movement
    except Exception as e:
        logger.error(f"Get inventory movement error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve inventory movement")

@app.put("/api/inventory/movements/{movement_id}")
def update_inventory_movement(movement_id: str, movement_update: dict, db: Session = Depends(get_db)):
    """Update inventory movement"""
    try:
        movement = db.query(InventoryMovement).filter(InventoryMovement.id == movement_id).first()
        if not movement:
            raise HTTPException(status_code=404, detail="Movement not found")
        
        # Update allowed fields
        if 'notes' in movement_update:
            movement.notes = movement_update['notes']
        if 'reference_number' in movement_update:
            movement.reference_number = movement_update['reference_number']
        
        movement.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(movement)
        
        return movement
    except Exception as e:
        logger.error(f"Update inventory movement error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update inventory movement")

@app.delete("/api/inventory/movements/{movement_id}")
def delete_inventory_movement(movement_id: str, db: Session = Depends(get_db)):
    """Delete inventory movement"""
    try:
        movement = db.query(InventoryMovement).filter(InventoryMovement.id == movement_id).first()
        if not movement:
            raise HTTPException(status_code=404, detail="Movement not found")
        
        # Reverse the stock movement before deletion
        product = db.query(Product).filter(Product.id == movement.product_id).first()
        if product:
            if movement.movement_type in [MovementType.stock_in, MovementType.returned]:
                product.current_stock = max(0, product.current_stock - movement.quantity)
            elif movement.movement_type in [MovementType.stock_out, MovementType.damaged]:
                product.current_stock += movement.quantity
        
        db.delete(movement)
        db.commit()
        
        return {"message": "Movement deleted successfully"}
    except Exception as e:
        logger.error(f"Delete inventory movement error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete inventory movement")

@app.get("/api/inventory/movements/product/{product_id}")
def get_product_movements(product_id: str, db: Session = Depends(get_db)):
    """Get movements for a specific product"""
    try:
        movements = db.query(InventoryMovement).filter(
            InventoryMovement.product_id == product_id
        ).order_by(InventoryMovement.created_at.desc()).all()
        return movements
    except Exception as e:
        logger.error(f"Get product movements error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve product movements")

@app.get("/api/inventory/movements/type/{movement_type}")
def get_movements_by_type(movement_type: str, db: Session = Depends(get_db)):
    """Get movements by type"""
    try:
        movements = db.query(InventoryMovement).filter(
            InventoryMovement.movement_type == MovementType(movement_type)
        ).order_by(InventoryMovement.created_at.desc()).all()
        return movements
    except Exception as e:
        logger.error(f"Get movements by type error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve movements by type")

@app.get("/api/inventory/summary")
def get_inventory_summary(db: Session = Depends(get_db)):
    """Get inventory summary statistics"""
    try:
        # Get total stock value
        total_stock_value = db.query(func.sum(Product.price * Product.current_stock)).scalar() or 0
        
        # Get low stock items
        low_stock_items = db.query(Product).filter(Product.current_stock <= Product.minimum_stock).count()
        
        # Get total products
        total_products = db.query(Product).count()
        
        # Get recent movements
        recent_movements = db.query(InventoryMovement).order_by(InventoryMovement.created_at.desc()).limit(10).all()
        
        # Get movement counts by type
        movement_counts = {}
        for movement_type in MovementType:
            count = db.query(InventoryMovement).filter(
                InventoryMovement.movement_type == movement_type
            ).count()
            movement_counts[movement_type.value] = count
        
        return {
            "total_stock_value": total_stock_value,
            "low_stock_items": low_stock_items,
            "total_products": total_products,
            "recent_movements": len(recent_movements),
            "movement_counts": movement_counts
        }
    except Exception as e:
        logger.error(f"Get inventory summary error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve inventory summary")

@app.post("/api/inventory/movements")
def create_inventory_movement(movement_data: InventoryMovementCreate, db: Session = Depends(get_db)):
    """Create inventory movement"""
    try:
        # Get user ID from token (simplified for demo)
        user_id = "56846977-f345-439c-b019-3330f3d16b7e"  # Use the actual admin user ID
        
        # Check if product exists
        product = db.query(Product).filter(Product.id == movement_data.product_id).first()
        if not product:
            raise HTTPException(status_code=400, detail="Product not found")
        
        # Validate stock out movements
        if movement_data.movement_type in ['stock_out', 'damaged'] and product.current_stock < movement_data.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock for this movement")
        
        # Calculate total cost
        total_cost = None
        if movement_data.unit_cost:
            total_cost = movement_data.unit_cost * movement_data.quantity
        
        db_movement = InventoryMovement(
            product_id=movement_data.product_id,
            movement_type=MovementType(movement_data.movement_type),
            quantity=movement_data.quantity,
            unit_cost=movement_data.unit_cost,
            total_cost=total_cost,
            reference_number=movement_data.reference,
            notes=movement_data.reason,
            created_by=user_id
        )
        
        db.add(db_movement)
        db.flush()  # Get the ID
        
        # Update product stock
        if movement_data.movement_type in ['stock_in', 'returned']:
            product.current_stock += movement_data.quantity
        elif movement_data.movement_type in ['stock_out', 'damaged']:
            product.current_stock = max(0, product.current_stock - movement_data.quantity)
        elif movement_data.movement_type == 'adjustment':
            # For adjustment, the quantity represents the new stock level
            product.current_stock = movement_data.quantity
        
        db.commit()
        db.refresh(db_movement)
        
        return db_movement
        
    except HTTPException:
        raise  # Re-raise HTTPExceptions to preserve status codes
    except Exception as e:
        logger.error(f"Create inventory movement error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create inventory movement")

# ===============================
# Finance Endpoints  
# ===============================

@app.post("/api/finance/transactions")
def create_financial_transaction(transaction_data: FinancialTransactionCreate, db: Session = Depends(get_db)):
    """Create financial transaction with enhanced validation"""
    try:
        # Get user ID from token (simplified for demo)
        user_id = "56846977-f345-439c-b019-3330f3d16b7e"
        
        # Generate transaction number
        transaction_count = db.query(FinancialTransaction).count()
        transaction_number = f"TXN-{datetime.utcnow().strftime('%Y%m%d')}-{transaction_count + 1:04d}"
        
        db_transaction = FinancialTransaction(
            transaction_number=transaction_number,
            transaction_type=TransactionType(transaction_data.transaction_type),
            category=transaction_data.category,
            description=transaction_data.description,
            amount=transaction_data.amount,
            reference_id=transaction_data.reference,
            created_by=user_id
        )
        
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        return db_transaction
        
    except Exception as e:
        logger.error(f"Create financial transaction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create financial transaction")

# ===============================
# POS Transaction Endpoints
# ===============================

@app.post("/api/pos/transactions")
def create_pos_transaction(transaction_data: dict, db: Session = Depends(get_db)):
    """Create POS transaction"""
    try:
        # Default cashier_id for now
        cashier_id = "357dbcec-a104-443f-8dec-9e8895417ead"
        
        db_transaction = PosTransaction(
            receipt_number=f"RCP-{str(uuid.uuid4())[:8]}",
            client_id=transaction_data.get('client_id'),
            items=transaction_data['items'],
            subtotal=float(transaction_data['subtotal']),
            discount_percentage=float(transaction_data.get('discount_percentage', 0)),
            discount_amount=float(transaction_data.get('discount_amount', 0)),
            tax_percentage=float(transaction_data.get('tax_percentage', 0)),
            tax_amount=float(transaction_data['tax_amount']),
            total_amount=float(transaction_data['total_amount']),
            payment_method=PaymentMethod(transaction_data.get('payment_method', 'cash')),
            payment_received=float(transaction_data['payment_received']),
            change_given=float(transaction_data.get('change_given', 0)),
            cashier_id=cashier_id
        )
        
        db.add(db_transaction)
        
        # Update product stock for each item
        for item in transaction_data['items']:
            product = db.query(Product).filter(Product.id == item['id']).first()
            if product:
                product.current_stock = max(0, product.current_stock - item['quantity'])
        
        db.commit()
        db.refresh(db_transaction)
        
        return db_transaction
        
    except Exception as e:
        logger.error(f"Create POS transaction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create POS transaction")

# ===============================
# Service Booking Endpoints (Enhanced)
# ===============================

@app.post("/api/services/bookings")  
def create_service_booking(booking_data: ServiceBookingCreate, db: Session = Depends(get_db)):
    """Create service booking with enhanced validation"""
    try:
        # Generate booking number
        booking_count = db.query(ServiceBooking).count()
        booking_number = f"SRV-{datetime.utcnow().strftime('%Y%m%d')}-{booking_count + 1:04d}"
        
        db_booking = ServiceBooking(
            booking_number=booking_number,
            client_name=booking_data.client_name,
            client_email=booking_data.client_email,
            client_phone=booking_data.client_phone,
            service_type=ServiceType(booking_data.service_type),
            description=booking_data.description,
            location=booking_data.location,
            preferred_date=booking_data.preferred_date,
            status='pending',
            estimated_cost=booking_data.cost_estimate,
            notes=booking_data.notes
        )
        
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        
        return db_booking
        
    except Exception as e:
        logger.error(f"Create service booking error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create service booking")

# ===============================
# Finance Endpoints
# ===============================

@app.get("/api/finance/transactions")
def get_financial_transactions(db: Session = Depends(get_db)):
    """Get financial transactions with enhanced details"""
    try:
        transactions = db.query(FinancialTransaction).order_by(FinancialTransaction.created_at.desc()).limit(100).all()
        
        # Format response with additional details
        formatted_transactions = []
        for transaction in transactions:
            formatted_transaction = {
                "id": transaction.id,
                "transaction_number": transaction.transaction_number,
                "transaction_type": transaction.transaction_type.value,
                "category": transaction.category,
                "description": transaction.description,
                "amount": transaction.amount,
                "reference_id": transaction.reference_id,
                "created_at": transaction.created_at.isoformat() if transaction.created_at else None,
                "created_by": transaction.created_by
            }
            formatted_transactions.append(formatted_transaction)
        
        return formatted_transactions
    except Exception as e:
        logger.error(f"Get financial transactions error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve financial transactions")

@app.get("/api/finance/transactions/{transaction_id}")
def get_financial_transaction(transaction_id: str, db: Session = Depends(get_db)):
    """Get single financial transaction"""
    try:
        transaction = db.query(FinancialTransaction).filter(FinancialTransaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    except Exception as e:
        logger.error(f"Get financial transaction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve financial transaction")

@app.put("/api/finance/transactions/{transaction_id}")
def update_financial_transaction(transaction_id: str, transaction_update: dict, db: Session = Depends(get_db)):
    """Update financial transaction"""
    try:
        transaction = db.query(FinancialTransaction).filter(FinancialTransaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Update allowed fields
        if 'category' in transaction_update:
            transaction.category = transaction_update['category']
        if 'description' in transaction_update:
            transaction.description = transaction_update['description']
        if 'amount' in transaction_update:
            transaction.amount = float(transaction_update['amount'])
        if 'reference_id' in transaction_update:
            transaction.reference_id = transaction_update['reference_id']
        
        db.commit()
        db.refresh(transaction)
        
        return transaction
    except Exception as e:
        logger.error(f"Update financial transaction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update financial transaction")

@app.delete("/api/finance/transactions/{transaction_id}")
def delete_financial_transaction(transaction_id: str, db: Session = Depends(get_db)):
    """Delete financial transaction"""
    try:
        transaction = db.query(FinancialTransaction).filter(FinancialTransaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        db.delete(transaction)
        db.commit()
        
        return {"message": "Transaction deleted successfully"}
    except Exception as e:
        logger.error(f"Delete financial transaction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete financial transaction")

@app.get("/api/finance/transactions/type/{transaction_type}")
def get_transactions_by_type(transaction_type: str, db: Session = Depends(get_db)):
    """Get transactions by type (income/expense)"""
    try:
        transactions = db.query(FinancialTransaction).filter(
            FinancialTransaction.transaction_type == TransactionType(transaction_type)
        ).order_by(FinancialTransaction.created_at.desc()).all()
        return transactions
    except Exception as e:
        logger.error(f"Get transactions by type error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve transactions by type")

@app.get("/api/finance/transactions/category/{category}")
def get_transactions_by_category(category: str, db: Session = Depends(get_db)):
    """Get transactions by category"""
    try:
        transactions = db.query(FinancialTransaction).filter(
            FinancialTransaction.category == category
        ).order_by(FinancialTransaction.created_at.desc()).all()
        return transactions
    except Exception as e:
        logger.error(f"Get transactions by category error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve transactions by category")

@app.get("/api/finance/analytics")
def get_financial_analytics(db: Session = Depends(get_db)):
    """Get comprehensive financial analytics"""
    try:
        # Monthly income/expense trends using MySQL DATE_FORMAT
        monthly_income = db.query(
            func.date_format(FinancialTransaction.created_at, '%Y-%m').label('month'),
            func.sum(FinancialTransaction.amount).label('total')
        ).filter(
            FinancialTransaction.transaction_type == TransactionType.income
        ).group_by(
            func.date_format(FinancialTransaction.created_at, '%Y-%m')
        ).order_by('month').all()
        
        monthly_expense = db.query(
            func.date_format(FinancialTransaction.created_at, '%Y-%m').label('month'),
            func.sum(FinancialTransaction.amount).label('total')
        ).filter(
            FinancialTransaction.transaction_type == TransactionType.expense
        ).group_by(
            func.date_format(FinancialTransaction.created_at, '%Y-%m')
        ).order_by('month').all()
        
        # Category breakdown
        category_breakdown = db.query(
            FinancialTransaction.category,
            FinancialTransaction.transaction_type,
            func.sum(FinancialTransaction.amount).label('total')
        ).group_by(
            FinancialTransaction.category,
            FinancialTransaction.transaction_type
        ).all()
        
        # Recent transactions
        recent_transactions = db.query(FinancialTransaction).order_by(
            FinancialTransaction.created_at.desc()
        ).limit(10).all()
        
        return {
            "monthly_income": [{"month": str(item.month), "total": float(item.total)} for item in monthly_income],
            "monthly_expense": [{"month": str(item.month), "total": float(item.total)} for item in monthly_expense],
            "category_breakdown": [
                {
                    "category": item.category,
                    "type": item.transaction_type.value,
                    "total": float(item.total)
                } for item in category_breakdown
            ],
            "recent_transactions": len(recent_transactions)
        }
    except Exception as e:
        logger.error(f"Financial analytics error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve financial analytics")

@app.get("/api/finance/summary")
def get_financial_summary(db: Session = Depends(get_db)):
    """Get enhanced financial summary"""
    try:
        # Total income and expense
        total_income = db.query(func.sum(FinancialTransaction.amount)).filter(
            FinancialTransaction.transaction_type == TransactionType.income
        ).scalar() or 0
        
        total_expense = db.query(func.sum(FinancialTransaction.amount)).filter(
            FinancialTransaction.transaction_type == TransactionType.expense
        ).scalar() or 0
        
        # Monthly income and expense (current month)
        current_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        monthly_income = db.query(func.sum(FinancialTransaction.amount)).filter(
            FinancialTransaction.transaction_type == TransactionType.income,
            FinancialTransaction.created_at >= current_month_start
        ).scalar() or 0
        
        monthly_expense = db.query(func.sum(FinancialTransaction.amount)).filter(
            FinancialTransaction.transaction_type == TransactionType.expense,
            FinancialTransaction.created_at >= current_month_start
        ).scalar() or 0
        
        # Transaction counts
        income_count = db.query(FinancialTransaction).filter(
            FinancialTransaction.transaction_type == TransactionType.income
        ).count()
        
        expense_count = db.query(FinancialTransaction).filter(
            FinancialTransaction.transaction_type == TransactionType.expense
        ).count()
        
        # Top categories
        top_income_categories = db.query(
            FinancialTransaction.category,
            func.sum(FinancialTransaction.amount).label('total')
        ).filter(
            FinancialTransaction.transaction_type == TransactionType.income
        ).group_by(FinancialTransaction.category).order_by(func.sum(FinancialTransaction.amount).desc()).limit(5).all()
        
        top_expense_categories = db.query(
            FinancialTransaction.category,
            func.sum(FinancialTransaction.amount).label('total')
        ).filter(
            FinancialTransaction.transaction_type == TransactionType.expense
        ).group_by(FinancialTransaction.category).order_by(func.sum(FinancialTransaction.amount).desc()).limit(5).all()
        
        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "net_profit": float(total_income - total_expense),
            "monthly_income": float(monthly_income),
            "monthly_expense": float(monthly_expense),
            "monthly_net": float(monthly_income - monthly_expense),
            "income_count": income_count,
            "expense_count": expense_count,
            "total_transactions": income_count + expense_count,
            "top_income_categories": [{"category": cat.category, "total": float(cat.total)} for cat in top_income_categories],
            "top_expense_categories": [{"category": cat.category, "total": float(cat.total)} for cat in top_expense_categories]
        }
        
    except Exception as e:
        logger.error(f"Financial summary error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch financial summary")

# ===============================
# Service Booking Endpoints
# ===============================

@app.get("/api/services/bookings")
def get_service_bookings(db: Session = Depends(get_db)):
    """Get service bookings with enhanced details"""
    try:
        bookings = db.query(ServiceBooking).order_by(ServiceBooking.created_at.desc()).all()
        
        # Format response with additional details
        formatted_bookings = []
        for booking in bookings:
            formatted_booking = {
                "id": booking.id,
                "booking_number": booking.booking_number,
                "client_name": booking.client_name,
                "client_email": booking.client_email,
                "client_phone": booking.client_phone,
                "service_type": booking.service_type.value,
                "description": booking.description,
                "location": booking.location,
                "preferred_date": booking.preferred_date.isoformat() if booking.preferred_date else None,
                "status": booking.status,
                "assigned_technician_id": booking.assigned_technician_id,
                "estimated_cost": booking.estimated_cost,
                "actual_cost": booking.actual_cost,
                "notes": booking.notes,
                "created_at": booking.created_at.isoformat() if booking.created_at else None,
                "updated_at": booking.updated_at.isoformat() if booking.updated_at else None
            }
            formatted_bookings.append(formatted_booking)
        
        return formatted_bookings
    except Exception as e:
        logger.error(f"Get service bookings error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve service bookings")

@app.get("/api/services/bookings/{booking_id}")
def get_service_booking(booking_id: str, db: Session = Depends(get_db)):
    """Get single service booking"""
    try:
        booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking
    except Exception as e:
        logger.error(f"Get service booking error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve service booking")

@app.put("/api/services/bookings/{booking_id}")
def update_service_booking(booking_id: str, booking_update: dict, db: Session = Depends(get_db)):
    """Update service booking"""
    try:
        booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Update allowed fields
        if 'status' in booking_update:
            booking.status = booking_update['status']
        if 'assigned_technician_id' in booking_update:
            booking.assigned_technician_id = booking_update['assigned_technician_id']
        if 'estimated_cost' in booking_update:
            booking.estimated_cost = float(booking_update['estimated_cost'])
        if 'actual_cost' in booking_update:
            booking.actual_cost = float(booking_update['actual_cost'])
        if 'notes' in booking_update:
            booking.notes = booking_update['notes']
        if 'preferred_date' in booking_update:
            booking.preferred_date = datetime.fromisoformat(booking_update['preferred_date'].replace('Z', '+00:00'))
        
        booking.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(booking)
        
        return booking
    except Exception as e:
        logger.error(f"Update service booking error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update service booking")

@app.delete("/api/services/bookings/{booking_id}")
def delete_service_booking(booking_id: str, db: Session = Depends(get_db)):
    """Delete service booking"""
    try:
        booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Check if booking can be deleted (not in progress or completed)
        if booking.status in ['in_progress', 'completed']:
            raise HTTPException(status_code=400, detail="Cannot delete booking that is in progress or completed")
        
        db.delete(booking)
        db.commit()
        
        return {"message": "Booking deleted successfully"}
    except HTTPException:
        raise  # Re-raise HTTPExceptions to preserve status codes
    except Exception as e:
        logger.error(f"Delete service booking error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete service booking")

@app.get("/api/services/bookings/status/{status}")
def get_bookings_by_status(status: str, db: Session = Depends(get_db)):
    """Get bookings by status"""
    try:
        bookings = db.query(ServiceBooking).filter(ServiceBooking.status == status).order_by(ServiceBooking.created_at.desc()).all()
        return bookings
    except Exception as e:
        logger.error(f"Get bookings by status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve bookings by status")

@app.get("/api/services/bookings/type/{service_type}")
def get_bookings_by_type(service_type: str, db: Session = Depends(get_db)):
    """Get bookings by service type"""
    try:
        bookings = db.query(ServiceBooking).filter(ServiceBooking.service_type == ServiceType(service_type)).order_by(ServiceBooking.created_at.desc()).all()
        return bookings
    except Exception as e:
        logger.error(f"Get bookings by type error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve bookings by type")

@app.put("/api/services/bookings/{booking_id}/status")
def update_booking_status(booking_id: str, status_update: dict, db: Session = Depends(get_db)):
    """Update booking status"""
    try:
        booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        new_status = status_update['status']
        booking.status = new_status
        booking.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(booking)
        
        return {"message": f"Booking status updated to {new_status}", "booking": booking}
    except Exception as e:
        logger.error(f"Update booking status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update booking status")

@app.get("/api/services/summary")
def get_services_summary(db: Session = Depends(get_db)):
    """Get service booking summary statistics"""
    try:
        # Total bookings
        total_bookings = db.query(ServiceBooking).count()
        
        # Bookings by status
        status_counts = {}
        for status in ['pending', 'confirmed', 'in_progress', 'completed', 'cancelled']:
            count = db.query(ServiceBooking).filter(ServiceBooking.status == status).count()
            status_counts[status] = count
        
        # Bookings by service type
        service_type_counts = {}
        for service_type in ServiceType:
            count = db.query(ServiceBooking).filter(ServiceBooking.service_type == service_type).count()
            service_type_counts[service_type.value] = count
        
        # Revenue calculations
        total_revenue = db.query(func.sum(ServiceBooking.actual_cost)).filter(
            ServiceBooking.status == 'completed'
        ).scalar() or 0
        
        estimated_revenue = db.query(func.sum(ServiceBooking.estimated_cost)).filter(
            ServiceBooking.status.in_(['confirmed', 'in_progress'])
        ).scalar() or 0
        
        # Recent bookings
        recent_bookings = db.query(ServiceBooking).order_by(ServiceBooking.created_at.desc()).limit(5).all()
        
        # This month's bookings
        current_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_bookings = db.query(ServiceBooking).filter(
            ServiceBooking.created_at >= current_month_start
        ).count()
        
        return {
            "total_bookings": total_bookings,
            "status_counts": status_counts,
            "service_type_counts": service_type_counts,
            "total_revenue": float(total_revenue),
            "estimated_revenue": float(estimated_revenue),
            "recent_bookings": len(recent_bookings),
            "monthly_bookings": monthly_bookings
        }
    except Exception as e:
        logger.error(f"Get services summary error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve services summary")

# ===============================
# Health Check
# ===============================

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": "mysql", "version": "2.0.0"}

# ===============================
# Reports Module Endpoints
# ===============================

def generate_report_header(doc, report_title, company_name="Afro Experts"):
    """Generate standardized report header"""
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0c4864')
    )
    
    company_style = ParagraphStyle(
        'CompanyStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#666666')
    )
    
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#666666')
    )
    
    # Add header content
    header_content = [
        Paragraph(company_name, company_style),
        Paragraph(report_title, header_style),
        Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", date_style),
        Spacer(1, 0.2*inch)
    ]
    
    return header_content

def create_excel_header(ws, report_title, company_name="Afro Experts"):
    """Create standardized Excel header"""
    # Company name
    ws['A1'] = company_name
    ws['A1'].font = Font(size=14, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')
    
    # Report title
    ws['A2'] = report_title
    ws['A2'].font = Font(size=12, bold=True)
    ws['A2'].alignment = Alignment(horizontal='center')
    
    # Date
    ws['A3'] = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ws['A3'].font = Font(size=10)
    ws['A3'].alignment = Alignment(horizontal='center')
    
    return 5  # Return starting row for data

@app.get("/api/reports/orders/pdf")
def generate_orders_pdf_report(db: Session = Depends(get_db)):
    """Generate PDF report for orders"""
    try:
        # Get orders data
        orders = db.query(Order).order_by(Order.created_at.desc()).all()
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
        
        # Build document content
        content = []
        content.extend(generate_report_header(doc, "Orders Report"))
        
        # Summary section
        styles = getSampleStyleSheet()
        summary_data = [
            ['Total Orders', str(len(orders))],
            ['Pending Orders', str(len([o for o in orders if o.status == OrderStatus.pending]))],
            ['Completed Orders', str(len([o for o in orders if o.status == OrderStatus.delivered]))],
            ['Total Revenue', f"RWF {sum(o.total_amount for o in orders if o.status == OrderStatus.delivered):,.2f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(Paragraph("Summary", styles['Heading2']))
        content.append(summary_table)
        content.append(Spacer(1, 0.3*inch))
        
        # Orders table
        content.append(Paragraph("Orders Details", styles['Heading2']))
        
        # Prepare orders data for table
        orders_data = [['Order Number', 'Client', 'Date', 'Status', 'Total Amount']]
        for order in orders[:50]:  # Limit to 50 orders for PDF
            orders_data.append([
                order.order_number,
                order.client.name if order.client else 'N/A',
                order.created_at.strftime('%Y-%m-%d') if order.created_at else 'N/A',
                order.status.value,
                f"RWF {order.total_amount:,.2f}"
            ])
        
        orders_table = Table(orders_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1*inch, 1.2*inch])
        orders_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0c4864')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(orders_table)
        
        # Build PDF
        doc.build(content)
        buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(buffer.read()),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=orders_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"}
        )
        
    except Exception as e:
        logger.error(f"Generate orders PDF report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate orders PDF report")

@app.get("/api/reports/orders/excel")
def generate_orders_excel_report(db: Session = Depends(get_db)):
    """Generate Excel report for orders"""
    try:
        # Get orders data
        orders = db.query(Order).order_by(Order.created_at.desc()).all()
        
        # Create workbook and worksheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Orders Report"
        
        # Create header
        start_row = create_excel_header(ws, "Orders Report")
        
        # Summary section
        ws[f'A{start_row}'] = "SUMMARY"
        ws[f'A{start_row}'].font = Font(size=12, bold=True)
        start_row += 1
        
        summary_data = [
            ['Total Orders', len(orders)],
            ['Pending Orders', len([o for o in orders if o.status == OrderStatus.pending])],
            ['Completed Orders', len([o for o in orders if o.status == OrderStatus.delivered])],
            ['Total Revenue', f"RWF {sum(o.total_amount for o in orders if o.status == OrderStatus.delivered):,.2f}"]
        ]
        
        for row_data in summary_data:
            ws[f'A{start_row}'] = row_data[0]
            ws[f'B{start_row}'] = row_data[1]
            ws[f'A{start_row}'].font = Font(bold=True)
            start_row += 1
        
        start_row += 2
        
        # Orders details section
        ws[f'A{start_row}'] = "ORDERS DETAILS"
        ws[f'A{start_row}'].font = Font(size=12, bold=True)
        start_row += 1
        
        # Headers
        headers = ['Order Number', 'Client Name', 'Date', 'Status', 'Items', 'Total Amount']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=start_row, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color='0c4864', end_color='0c4864', fill_type='solid')
            cell.font = Font(bold=True, color='FFFFFF')
            cell.alignment = Alignment(horizontal='center')
        
        start_row += 1
        
        # Orders data
        for order in orders:
            ws.cell(row=start_row, column=1, value=order.order_number)
            ws.cell(row=start_row, column=2, value=order.client.name if order.client else 'N/A')
            ws.cell(row=start_row, column=3, value=order.created_at.strftime('%Y-%m-%d') if order.created_at else 'N/A')
            ws.cell(row=start_row, column=4, value=order.status.value)
            ws.cell(row=start_row, column=5, value=len(order.items))
            ws.cell(row=start_row, column=6, value=f"RWF {order.total_amount:,.2f}")
            start_row += 1
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Create buffer and save
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(buffer.read()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=orders_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"}
        )
        
    except Exception as e:
        logger.error(f"Generate orders Excel report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate orders Excel report")

@app.get("/api/reports/inventory/pdf")
def generate_inventory_pdf_report(db: Session = Depends(get_db)):
    """Generate PDF report for inventory"""
    try:
        # Get inventory data
        products = db.query(Product).order_by(Product.name).all()
        movements = db.query(InventoryMovement).order_by(InventoryMovement.created_at.desc()).limit(100).all()
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
        
        # Build document content
        content = []
        content.extend(generate_report_header(doc, "Inventory Report"))
        
        # Summary section
        styles = getSampleStyleSheet()
        total_products = len(products)
        total_stock_value = sum(p.price * p.current_stock for p in products)
        low_stock_items = len([p for p in products if p.current_stock <= p.minimum_stock])
        
        summary_data = [
            ['Total Products', str(total_products)],
            ['Low Stock Items', str(low_stock_items)],
            ['Recent Movements', str(len(movements))],
            ['Total Stock Value', f"RWF {total_stock_value:,.2f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(Paragraph("Summary", styles['Heading2']))
        content.append(summary_table)
        content.append(Spacer(1, 0.3*inch))
        
        # Products table
        content.append(Paragraph("Products Inventory", styles['Heading2']))
        
        products_data = [['Product Name', 'SKU', 'Current Stock', 'Min Stock', 'Price', 'Stock Value']]
        for product in products[:50]:  # Limit to 50 products for PDF
            stock_value = product.price * product.current_stock
            products_data.append([
                product.name,
                product.sku,
                str(product.current_stock),
                str(product.minimum_stock),
                f"RWF {product.price:,.2f}",
                f"RWF {stock_value:,.2f}"
            ])
        
        products_table = Table(products_data, colWidths=[1.5*inch, 1*inch, 0.8*inch, 0.8*inch, 1*inch, 1*inch])
        products_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0c4864')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(products_table)
        
        # Build PDF
        doc.build(content)
        buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(buffer.read()),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=inventory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"}
        )
        
    except Exception as e:
        logger.error(f"Generate inventory PDF report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate inventory PDF report")

@app.get("/api/reports/inventory/excel")
def generate_inventory_excel_report(db: Session = Depends(get_db)):
    """Generate Excel report for inventory"""
    try:
        # Get inventory data
        products = db.query(Product).order_by(Product.name).all()
        movements = db.query(InventoryMovement).order_by(InventoryMovement.created_at.desc()).limit(100).all()
        
        # Create workbook with multiple sheets
        wb = openpyxl.Workbook()
        
        # Products sheet
        ws_products = wb.active
        ws_products.title = "Products Inventory"
        
        # Create header for products
        start_row = create_excel_header(ws_products, "Products Inventory Report")
        
        # Summary section
        ws_products[f'A{start_row}'] = "SUMMARY"
        ws_products[f'A{start_row}'].font = Font(size=12, bold=True)
        start_row += 1
        
        total_products = len(products)
        total_stock_value = sum(p.price * p.current_stock for p in products)
        low_stock_items = len([p for p in products if p.current_stock <= p.minimum_stock])
        
        summary_data = [
            ['Total Products', total_products],
            ['Low Stock Items', low_stock_items],
            ['Total Stock Value', f"RWF {total_stock_value:,.2f}"]
        ]
        
        for row_data in summary_data:
            ws_products[f'A{start_row}'] = row_data[0]
            ws_products[f'B{start_row}'] = row_data[1]
            ws_products[f'A{start_row}'].font = Font(bold=True)
            start_row += 1
        
        start_row += 2
        
        # Products details
        ws_products[f'A{start_row}'] = "PRODUCTS DETAILS"
        ws_products[f'A{start_row}'].font = Font(size=12, bold=True)
        start_row += 1
        
        # Headers
        headers = ['Product Name', 'SKU', 'Category', 'Current Stock', 'Min Stock', 'Unit Price', 'Stock Value']
        for col, header in enumerate(headers, 1):
            cell = ws_products.cell(row=start_row, column=col, value=header)
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='0c4864', end_color='0c4864', fill_type='solid')
            cell.alignment = Alignment(horizontal='center')
        
        start_row += 1
        
        # Products data
        for product in products:
            stock_value = product.price * product.current_stock
            ws_products.cell(row=start_row, column=1, value=product.name)
            ws_products.cell(row=start_row, column=2, value=product.sku)
            ws_products.cell(row=start_row, column=3, value=product.category)
            ws_products.cell(row=start_row, column=4, value=product.current_stock)
            ws_products.cell(row=start_row, column=5, value=product.minimum_stock)
            ws_products.cell(row=start_row, column=6, value=f"RWF {product.price:,.2f}")
            ws_products.cell(row=start_row, column=7, value=f"RWF {stock_value:,.2f}")
            
            # Highlight low stock items
            if product.current_stock <= product.minimum_stock:
                for col in range(1, 8):
                    ws_products.cell(row=start_row, column=col).fill = PatternFill(start_color='ffcccc', end_color='ffcccc', fill_type='solid')
            
            start_row += 1
        
        # Auto-adjust column widths
        for column in ws_products.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws_products.column_dimensions[column_letter].width = adjusted_width
        
        # Create buffer and save
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(buffer.read()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=inventory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"}
        )
        
    except Exception as e:
        logger.error(f"Generate inventory Excel report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate inventory Excel report")

@app.get("/api/reports/finance/pdf")
def generate_finance_pdf_report(db: Session = Depends(get_db)):
    """Generate PDF report for financial transactions"""
    try:
        # Get financial data
        transactions = db.query(FinancialTransaction).order_by(FinancialTransaction.created_at.desc()).limit(100).all()
        
        # Calculate summary
        total_income = sum(t.amount for t in transactions if t.transaction_type == TransactionType.income)
        total_expense = sum(t.amount for t in transactions if t.transaction_type == TransactionType.expense)
        net_profit = total_income - total_expense
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
        
        # Build document content
        content = []
        content.extend(generate_report_header(doc, "Financial Report"))
        
        # Summary section
        styles = getSampleStyleSheet()
        summary_data = [
            ['Total Income', f"RWF {total_income:,.2f}"],
            ['Total Expenses', f"RWF {total_expense:,.2f}"],
            ['Net Profit', f"RWF {net_profit:,.2f}"],
            ['Total Transactions', str(len(transactions))]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(Paragraph("Financial Summary", styles['Heading2']))
        content.append(summary_table)
        content.append(Spacer(1, 0.3*inch))
        
        # Transactions table
        content.append(Paragraph("Recent Transactions", styles['Heading2']))
        
        transactions_data = [['Date', 'Description', 'Category', 'Type', 'Amount']]
        for transaction in transactions[:50]:  # Limit to 50 transactions for PDF
            transactions_data.append([
                transaction.created_at.strftime('%Y-%m-%d') if transaction.created_at else 'N/A',
                transaction.description,
                transaction.category,
                transaction.transaction_type.value,
                f"RWF {transaction.amount:,.2f}"
            ])
        
        transactions_table = Table(transactions_data, colWidths=[1*inch, 2*inch, 1*inch, 1*inch, 1.2*inch])
        transactions_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0c4864')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(transactions_table)
        
        # Build PDF
        doc.build(content)
        buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(buffer.read()),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=finance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"}
        )
        
    except Exception as e:
        logger.error(f"Generate finance PDF report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate finance PDF report")

@app.get("/api/reports/finance/excel")
def generate_finance_excel_report(db: Session = Depends(get_db)):
    """Generate Excel report for financial transactions"""
    try:
        # Get financial data
        transactions = db.query(FinancialTransaction).order_by(FinancialTransaction.created_at.desc()).all()
        
        # Calculate summary
        total_income = sum(t.amount for t in transactions if t.transaction_type == TransactionType.income)
        total_expense = sum(t.amount for t in transactions if t.transaction_type == TransactionType.expense)
        net_profit = total_income - total_expense
        
        # Create workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Financial Report"
        
        # Create header
        start_row = create_excel_header(ws, "Financial Report")
        
        # Summary section
        ws[f'A{start_row}'] = "FINANCIAL SUMMARY"
        ws[f'A{start_row}'].font = Font(size=12, bold=True)
        start_row += 1
        
        summary_data = [
            ['Total Income', f"RWF {total_income:,.2f}"],
            ['Total Expenses', f"RWF {total_expense:,.2f}"],
            ['Net Profit', f"RWF {net_profit:,.2f}"],
            ['Total Transactions', len(transactions)]
        ]
        
        for row_data in summary_data:
            ws[f'A{start_row}'] = row_data[0]
            ws[f'B{start_row}'] = row_data[1]
            ws[f'A{start_row}'].font = Font(bold=True)
            start_row += 1
        
        start_row += 2
        
        # Transactions details
        ws[f'A{start_row}'] = "TRANSACTIONS DETAILS"
        ws[f'A{start_row}'].font = Font(size=12, bold=True)
        start_row += 1
        
        # Headers
        headers = ['Date', 'Transaction Number', 'Description', 'Category', 'Type', 'Amount']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=start_row, column=col, value=header)
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='0c4864', end_color='0c4864', fill_type='solid')
            cell.alignment = Alignment(horizontal='center')
        
        start_row += 1
        
        # Transactions data
        for transaction in transactions:
            ws.cell(row=start_row, column=1, value=transaction.created_at.strftime('%Y-%m-%d') if transaction.created_at else 'N/A')
            ws.cell(row=start_row, column=2, value=transaction.transaction_number)
            ws.cell(row=start_row, column=3, value=transaction.description)
            ws.cell(row=start_row, column=4, value=transaction.category)
            ws.cell(row=start_row, column=5, value=transaction.transaction_type.value)
            ws.cell(row=start_row, column=6, value=f"RWF {transaction.amount:,.2f}")
            
            # Color code by transaction type
            if transaction.transaction_type == TransactionType.income:
                ws.cell(row=start_row, column=6).fill = PatternFill(start_color='ccffcc', end_color='ccffcc', fill_type='solid')
            else:
                ws.cell(row=start_row, column=6).fill = PatternFill(start_color='ffcccc', end_color='ffcccc', fill_type='solid')
            
            start_row += 1
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Create buffer and save
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(buffer.read()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=finance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"}
        )
        
    except Exception as e:
        logger.error(f"Generate finance Excel report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate finance Excel report")

@app.get("/api/reports/services/pdf")
def generate_services_pdf_report(db: Session = Depends(get_db)):
    """Generate PDF report for service bookings"""
    try:
        # Get service bookings data
        bookings = db.query(ServiceBooking).order_by(ServiceBooking.created_at.desc()).all()
        
        # Calculate summary
        total_bookings = len(bookings)
        completed_bookings = len([b for b in bookings if b.status == 'completed'])
        pending_bookings = len([b for b in bookings if b.status == 'pending'])
        total_revenue = sum(b.actual_cost for b in bookings if b.actual_cost and b.status == 'completed')
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
        
        # Build document content
        content = []
        content.extend(generate_report_header(doc, "Service Bookings Report"))
        
        # Summary section
        styles = getSampleStyleSheet()
        summary_data = [
            ['Total Bookings', str(total_bookings)],
            ['Completed Bookings', str(completed_bookings)],
            ['Pending Bookings', str(pending_bookings)],
            ['Total Revenue', f"RWF {total_revenue:,.2f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(Paragraph("Service Bookings Summary", styles['Heading2']))
        content.append(summary_table)
        content.append(Spacer(1, 0.3*inch))
        
        # Bookings table
        content.append(Paragraph("Service Bookings Details", styles['Heading2']))
        
        bookings_data = [['Booking Number', 'Client', 'Service Type', 'Date', 'Status']]
        for booking in bookings[:50]:  # Limit to 50 bookings for PDF
            bookings_data.append([
                booking.booking_number,
                booking.client_name,
                booking.service_type.value.replace('_', ' ').title(),
                booking.created_at.strftime('%Y-%m-%d') if booking.created_at else 'N/A',
                booking.status.title()
            ])
        
        bookings_table = Table(bookings_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch, 1*inch])
        bookings_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0c4864')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(bookings_table)
        
        # Build PDF
        doc.build(content)
        buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(buffer.read()),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=services_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"}
        )
        
    except Exception as e:
        logger.error(f"Generate services PDF report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate services PDF report")

@app.get("/api/reports/services/excel")
def generate_services_excel_report(db: Session = Depends(get_db)):
    """Generate Excel report for service bookings"""
    try:
        # Get service bookings data
        bookings = db.query(ServiceBooking).order_by(ServiceBooking.created_at.desc()).all()
        
        # Calculate summary
        total_bookings = len(bookings)
        completed_bookings = len([b for b in bookings if b.status == 'completed'])
        pending_bookings = len([b for b in bookings if b.status == 'pending'])
        total_revenue = sum(b.actual_cost for b in bookings if b.actual_cost and b.status == 'completed')
        
        # Create workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Service Bookings Report"
        
        # Create header
        start_row = create_excel_header(ws, "Service Bookings Report")
        
        # Summary section
        ws[f'A{start_row}'] = "SERVICE BOOKINGS SUMMARY"
        ws[f'A{start_row}'].font = Font(size=12, bold=True)
        start_row += 1
        
        summary_data = [
            ['Total Bookings', total_bookings],
            ['Completed Bookings', completed_bookings],
            ['Pending Bookings', pending_bookings],
            ['Total Revenue', f"RWF {total_revenue:,.2f}"]
        ]
        
        for row_data in summary_data:
            ws[f'A{start_row}'] = row_data[0]
            ws[f'B{start_row}'] = row_data[1]
            ws[f'A{start_row}'].font = Font(bold=True)
            start_row += 1
        
        start_row += 2
        
        # Bookings details
        ws[f'A{start_row}'] = "SERVICE BOOKINGS DETAILS"
        ws[f'A{start_row}'].font = Font(size=12, bold=True)
        start_row += 1
        
        # Headers
        headers = ['Booking Number', 'Client Name', 'Service Type', 'Date', 'Status', 'Location', 'Estimated Cost', 'Actual Cost']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=start_row, column=col, value=header)
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='0c4864', end_color='0c4864', fill_type='solid')
            cell.alignment = Alignment(horizontal='center')
        
        start_row += 1
        
        # Bookings data
        for booking in bookings:
            ws.cell(row=start_row, column=1, value=booking.booking_number)
            ws.cell(row=start_row, column=2, value=booking.client_name)
            ws.cell(row=start_row, column=3, value=booking.service_type.value.replace('_', ' ').title())
            ws.cell(row=start_row, column=4, value=booking.created_at.strftime('%Y-%m-%d') if booking.created_at else 'N/A')
            ws.cell(row=start_row, column=5, value=booking.status.title())
            ws.cell(row=start_row, column=6, value=booking.location)
            ws.cell(row=start_row, column=7, value=f"RWF {booking.estimated_cost:,.2f}" if booking.estimated_cost else 'N/A')
            ws.cell(row=start_row, column=8, value=f"RWF {booking.actual_cost:,.2f}" if booking.actual_cost else 'N/A')
            
            # Color code by status
            if booking.status == 'completed':
                for col in range(1, 9):
                    ws.cell(row=start_row, column=col).fill = PatternFill(start_color='ccffcc', end_color='ccffcc', fill_type='solid')
            elif booking.status == 'pending':
                for col in range(1, 9):
                    ws.cell(row=start_row, column=col).fill = PatternFill(start_color='ffffcc', end_color='ffffcc', fill_type='solid')
            
            start_row += 1
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Create buffer and save
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(buffer.read()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=services_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"}
        )
        
    except Exception as e:
        logger.error(f"Generate services Excel report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate services Excel report")

@app.get("/api/reports/comprehensive/pdf")
def generate_comprehensive_pdf_report(db: Session = Depends(get_db)):
    """Generate comprehensive PDF report for all modules"""
    try:
        # Get data from all modules
        orders = db.query(Order).all()
        products = db.query(Product).all()
        transactions = db.query(FinancialTransaction).all()
        bookings = db.query(ServiceBooking).all()
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
        
        # Build document content
        content = []
        content.extend(generate_report_header(doc, "Comprehensive Business Report"))
        
        # Executive Summary
        styles = getSampleStyleSheet()
        content.append(Paragraph("Executive Summary", styles['Heading2']))
        
        # Key metrics
        total_orders = len(orders)
        total_products = len(products)
        total_revenue = sum(o.total_amount for o in orders if o.status == OrderStatus.delivered)
        total_bookings = len(bookings)
        
        summary_data = [
            ['Total Orders', str(total_orders)],
            ['Total Products', str(total_products)],
            ['Total Revenue', f"RWF {total_revenue:,.2f}"],
            ['Service Bookings', str(total_bookings)]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(summary_table)
        content.append(Spacer(1, 0.3*inch))
        
        # Financial Summary
        content.append(Paragraph("Financial Overview", styles['Heading2']))
        
        total_income = sum(t.amount for t in transactions if t.transaction_type == TransactionType.income)
        total_expense = sum(t.amount for t in transactions if t.transaction_type == TransactionType.expense)
        net_profit = total_income - total_expense
        
        financial_data = [
            ['Total Income', f"RWF {total_income:,.2f}"],
            ['Total Expenses', f"RWF {total_expense:,.2f}"],
            ['Net Profit', f"RWF {net_profit:,.2f}"]
        ]
        
        financial_table = Table(financial_data, colWidths=[2*inch, 2*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(financial_table)
        content.append(Spacer(1, 0.3*inch))
        
        # Recent Orders
        content.append(Paragraph("Recent Orders", styles['Heading2']))
        
        recent_orders = sorted(orders, key=lambda x: x.created_at, reverse=True)[:10]
        orders_data = [['Order Number', 'Client', 'Date', 'Status', 'Amount']]
        for order in recent_orders:
            orders_data.append([
                order.order_number,
                order.client.name if order.client else 'N/A',
                order.created_at.strftime('%Y-%m-%d') if order.created_at else 'N/A',
                order.status.value,
                f"RWF {order.total_amount:,.2f}"
            ])
        
        orders_table = Table(orders_data, colWidths=[1.2*inch, 1.2*inch, 1*inch, 1*inch, 1.2*inch])
        orders_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0c4864')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(orders_table)
        
        # Build PDF
        doc.build(content)
        buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(buffer.read()),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"}
        )
        
    except Exception as e:
        logger.error(f"Generate comprehensive PDF report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate comprehensive PDF report")

@app.get("/api/reports/list")
def get_available_reports():
    """Get list of available reports"""
    return {
        "reports": [
            {
                "id": "orders",
                "name": "Orders Report",
                "description": "Detailed orders report with client information and order status",
                "formats": ["pdf", "excel"]
            },
            {
                "id": "inventory",
                "name": "Inventory Report",
                "description": "Complete inventory report with stock levels and values",
                "formats": ["pdf", "excel"]
            },
            {
                "id": "finance",
                "name": "Financial Report",
                "description": "Financial transactions report with income and expense analysis",
                "formats": ["pdf", "excel"]
            },
            {
                "id": "services",
                "name": "Service Bookings Report",
                "description": "Service bookings report with client details and booking status",
                "formats": ["pdf", "excel"]
            },
            {
                "id": "comprehensive",
                "name": "Comprehensive Business Report",
                "description": "Complete business overview with all modules summary",
                "formats": ["pdf"]
            }
        ]
    }

# ===============================
# Invoice Management Endpoints
# ===============================

@app.get("/api/invoices")
def get_invoices(db: Session = Depends(get_db)):
    """Get all invoices with enhanced details"""
    try:
        invoices = db.query(Invoice).order_by(Invoice.created_at.desc()).all()
        
        # Format response with client and payment details
        formatted_invoices = []
        for invoice in invoices:
            formatted_invoice = {
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "invoice_type": invoice.invoice_type.value,
                "client_id": invoice.client_id,
                "client_name": invoice.client_name,
                "client_email": invoice.client_email,
                "client_phone": invoice.client_phone,
                "client_address": invoice.client_address,
                "issue_date": invoice.issue_date.isoformat() if invoice.issue_date else None,
                "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
                "subtotal": invoice.subtotal,
                "tax_rate": invoice.tax_rate,
                "tax_amount": invoice.tax_amount,
                "discount_amount": invoice.discount_amount,
                "total_amount": invoice.total_amount,
                "currency": invoice.currency.value,
                "status": invoice.status.value,
                "notes": invoice.notes,
                "terms": invoice.terms,
                "order_id": invoice.order_id,
                "service_booking_id": invoice.service_booking_id,
                "is_recurring": invoice.is_recurring,
                "recurring_frequency": invoice.recurring_frequency,
                "next_invoice_date": invoice.next_invoice_date.isoformat() if invoice.next_invoice_date else None,
                "paid_amount": invoice.paid_amount,
                "balance_due": invoice.balance_due,
                "created_by": invoice.created_by,
                "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
                "updated_at": invoice.updated_at.isoformat() if invoice.updated_at else None,
                "email_sent": invoice.email_sent,
                "email_sent_at": invoice.email_sent_at.isoformat() if invoice.email_sent_at else None,
                "sms_sent": invoice.sms_sent,
                "sms_sent_at": invoice.sms_sent_at.isoformat() if invoice.sms_sent_at else None,
                "reminder_count": invoice.reminder_count,
                "last_reminder_sent": invoice.last_reminder_sent.isoformat() if invoice.last_reminder_sent else None,
                "items_count": len(invoice.items),
                "payments_count": len(invoice.payments)
            }
            formatted_invoices.append(formatted_invoice)
        
        return formatted_invoices
    except Exception as e:
        logger.error(f"Get invoices error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve invoices")

@app.get("/api/invoices/summary")
def get_invoices_summary(db: Session = Depends(get_db)):
    """Get invoice summary statistics"""
    try:
        # Total invoices
        total_invoices = db.query(Invoice).count()
        
        # Invoices by status
        status_counts = {}
        for status in InvoiceStatus:
            count = db.query(Invoice).filter(Invoice.status == status).count()
            status_counts[status.value] = count
        
        # Financial summary
        total_invoiced = db.query(func.sum(Invoice.total_amount)).scalar() or 0
        total_paid = db.query(func.sum(Invoice.paid_amount)).scalar() or 0
        total_outstanding = total_invoiced - total_paid
        
        # Overdue invoices
        current_date = datetime.utcnow()
        overdue_count = db.query(Invoice).filter(
            Invoice.due_date < current_date,
            Invoice.status.in_([InvoiceStatus.sent, InvoiceStatus.partially_paid, InvoiceStatus.overdue])
        ).count()
        
        overdue_amount = db.query(func.sum(Invoice.balance_due)).filter(
            Invoice.due_date < current_date,
            Invoice.status.in_([InvoiceStatus.sent, InvoiceStatus.partially_paid, InvoiceStatus.overdue])
        ).scalar() or 0
        
        # Monthly statistics
        current_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_invoices = db.query(Invoice).filter(Invoice.created_at >= current_month_start).count()
        monthly_amount = db.query(func.sum(Invoice.total_amount)).filter(Invoice.created_at >= current_month_start).scalar() or 0
        
        # Recent invoices
        recent_invoices = db.query(Invoice).order_by(Invoice.created_at.desc()).limit(5).all()
        
        return {
            "total_invoices": total_invoices,
            "status_counts": status_counts,
            "total_invoiced": float(total_invoiced),
            "total_paid": float(total_paid),
            "total_outstanding": float(total_outstanding),
            "overdue_count": overdue_count,
            "overdue_amount": float(overdue_amount),
            "monthly_invoices": monthly_invoices,
            "monthly_amount": float(monthly_amount),
            "recent_invoices": len(recent_invoices)
        }
    except Exception as e:
        logger.error(f"Get invoices summary error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve invoices summary: {str(e)}")

@app.get("/api/invoices/overdue")
def get_overdue_invoices(db: Session = Depends(get_db)):
    """Get overdue invoices"""
    try:
        # Update overdue status for invoices past due date
        current_date = datetime.utcnow()
        overdue_invoices = db.query(Invoice).filter(
            Invoice.due_date < current_date,
            Invoice.status.in_([InvoiceStatus.sent, InvoiceStatus.partially_paid])
        ).all()
        
        # Update status to overdue
        for invoice in overdue_invoices:
            if invoice.status != InvoiceStatus.overdue:
                invoice.status = InvoiceStatus.overdue
                invoice.updated_at = datetime.utcnow()
        
        db.commit()
        
        # Get all overdue invoices
        overdue_invoices = db.query(Invoice).filter(Invoice.status == InvoiceStatus.overdue).order_by(Invoice.due_date.asc()).all()
        
        # Format response
        formatted_invoices = []
        for invoice in overdue_invoices:
            days_overdue = (current_date - invoice.due_date).days
            formatted_invoice = {
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "client_name": invoice.client_name,
                "client_email": invoice.client_email,
                "client_phone": invoice.client_phone,
                "total_amount": invoice.total_amount,
                "balance_due": invoice.balance_due,
                "currency": invoice.currency.value,
                "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
                "days_overdue": days_overdue,
                "reminder_count": invoice.reminder_count,
                "last_reminder_sent": invoice.last_reminder_sent.isoformat() if invoice.last_reminder_sent else None
            }
            formatted_invoices.append(formatted_invoice)
        
        return formatted_invoices
    except Exception as e:
        logger.error(f"Get overdue invoices error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve overdue invoices: {str(e)}")

@app.get("/api/invoices/status/{status}")
def get_invoices_by_status(status: str, db: Session = Depends(get_db)):
    """Get invoices by status"""
    try:
        invoices = db.query(Invoice).filter(Invoice.status == InvoiceStatus(status)).order_by(Invoice.created_at.desc()).all()
        
        # Format response
        formatted_invoices = []
        for invoice in invoices:
            formatted_invoice = {
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "client_name": invoice.client_name,
                "total_amount": invoice.total_amount,
                "currency": invoice.currency.value,
                "status": invoice.status.value,
                "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
                "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
                "balance_due": invoice.balance_due
            }
            formatted_invoices.append(formatted_invoice)
        
        return formatted_invoices
    except Exception as e:
        logger.error(f"Get invoices by status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve invoices by status")

@app.get("/api/invoices/{invoice_id}")
def get_invoice(invoice_id: str, db: Session = Depends(get_db)):
    """Get single invoice with full details"""
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        # Format response with items and payments
        formatted_invoice = {
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "invoice_type": invoice.invoice_type.value,
            "client_id": invoice.client_id,
            "client_name": invoice.client_name,
            "client_email": invoice.client_email,
            "client_phone": invoice.client_phone,
            "client_address": invoice.client_address,
            "issue_date": invoice.issue_date.isoformat() if invoice.issue_date else None,
            "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
            "subtotal": invoice.subtotal,
            "tax_rate": invoice.tax_rate,
            "tax_amount": invoice.tax_amount,
            "discount_amount": invoice.discount_amount,
            "total_amount": invoice.total_amount,
            "currency": invoice.currency.value,
            "status": invoice.status.value,
            "notes": invoice.notes,
            "terms": invoice.terms,
            "order_id": invoice.order_id,
            "service_booking_id": invoice.service_booking_id,
            "is_recurring": invoice.is_recurring,
            "recurring_frequency": invoice.recurring_frequency,
            "next_invoice_date": invoice.next_invoice_date.isoformat() if invoice.next_invoice_date else None,
            "paid_amount": invoice.paid_amount,
            "balance_due": invoice.balance_due,
            "created_by": invoice.created_by,
            "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
            "updated_at": invoice.updated_at.isoformat() if invoice.updated_at else None,
            "email_sent": invoice.email_sent,
            "email_sent_at": invoice.email_sent_at.isoformat() if invoice.email_sent_at else None,
            "sms_sent": invoice.sms_sent,
            "sms_sent_at": invoice.sms_sent_at.isoformat() if invoice.sms_sent_at else None,
            "reminder_count": invoice.reminder_count,
            "last_reminder_sent": invoice.last_reminder_sent.isoformat() if invoice.last_reminder_sent else None,
            "items": [
                {
                    "id": item.id,
                    "item_type": item.item_type,
                    "product_id": item.product_id,
                    "product_name": item.product.name if item.product else None,
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "line_total": item.line_total,
                    "weight": item.weight,
                    "weight_unit": item.weight_unit,
                    "hours": item.hours,
                    "hourly_rate": item.hourly_rate,
                    "discount_percentage": item.discount_percentage,
                    "discount_amount": item.discount_amount
                } for item in invoice.items
            ],
            "payments": [
                {
                    "id": payment.id,
                    "payment_method": payment.payment_method.value,
                    "amount": payment.amount,
                    "payment_date": payment.payment_date.isoformat() if payment.payment_date else None,
                    "payment_status": payment.payment_status.value,
                    "reference_number": payment.reference_number,
                    "transaction_id": payment.transaction_id,
                    "afropay_transaction_id": payment.afropay_transaction_id,
                    "afropay_status": payment.afropay_status,
                    "notes": payment.notes
                } for payment in invoice.payments
            ]
        }
        
        return formatted_invoice
    except Exception as e:
        logger.error(f"Get invoice error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve invoice")

@app.get("/api/invoices/{invoice_id}/payments")
def get_invoice_payments(invoice_id: str, db: Session = Depends(get_db)):
    """Get payments for an invoice"""
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        payments = db.query(InvoicePayment).filter(InvoicePayment.invoice_id == invoice_id).order_by(InvoicePayment.created_at.desc()).all()
        
        # Format response
        formatted_payments = []
        for payment in payments:
            formatted_payment = {
                "id": payment.id,
                "payment_method": payment.payment_method.value,
                "amount": payment.amount,
                "payment_date": payment.payment_date.isoformat() if payment.payment_date else None,
                "payment_status": payment.payment_status.value,
                "reference_number": payment.reference_number,
                "transaction_id": payment.transaction_id,
                "afropay_transaction_id": payment.afropay_transaction_id,
                "afropay_status": payment.afropay_status,
                "notes": payment.notes,
                "created_at": payment.created_at.isoformat() if payment.created_at else None
            }
            formatted_payments.append(formatted_payment)
        
        return formatted_payments
    except Exception as e:
        logger.error(f"Get invoice payments error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve invoice payments")

@app.get("/api/invoices/{invoice_id}/logs")
def get_invoice_logs(invoice_id: str, db: Session = Depends(get_db)):
    """Get audit logs for an invoice"""
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        logs = db.query(InvoiceLog).filter(InvoiceLog.invoice_id == invoice_id).order_by(InvoiceLog.performed_at.desc()).all()
        
        # Format response
        formatted_logs = []
        for log in logs:
            formatted_log = {
                "id": log.id,
                "action": log.action,
                "description": log.description,
                "performed_by": log.performed_by,
                "performed_by_name": log.performed_by_user.full_name if log.performed_by_user else "Unknown",
                "performed_at": log.performed_at.isoformat() if log.performed_at else None,
                "metadata": log.log_metadata
            }
            formatted_logs.append(formatted_log)
        
        return formatted_logs
    except Exception as e:
        logger.error(f"Get invoice logs error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve invoice logs")

@app.post("/api/invoices/generate-from-order/{order_id}")
def generate_invoice_from_order(order_id: str, db: Session = Depends(get_db)):
    """Generate invoice from order"""
    try:
        user_id = "56846977-f345-439c-b019-3330f3d16b7e"
        
        # Get order
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Check if invoice already exists for this order
        existing_invoice = db.query(Invoice).filter(Invoice.order_id == order_id).first()
        if existing_invoice:
            raise HTTPException(status_code=400, detail="Invoice already exists for this order")
        
        # Generate invoice number
        invoice_count = db.query(Invoice).count()
        invoice_number = f"INV-{datetime.utcnow().strftime('%Y')}-{invoice_count + 1:04d}"
        
        # Create invoice
        db_invoice = Invoice(
            invoice_number=invoice_number,
            invoice_type=InvoiceType.pos_sale,
            client_id=order.client_id,
            client_name=order.client.name if order.client else "Walk-in Customer",
            client_email=order.client.email if order.client else None,
            client_phone=order.client.phone if order.client else None,
            issue_date=datetime.utcnow(),
            due_date=datetime.utcnow() + timedelta(days=30),  # 30 days from now
            subtotal=order.subtotal,
            tax_rate=0.18,
            tax_amount=order.tax_amount,
            total_amount=order.total_amount,
            currency=Currency.rwf,
            status=InvoiceStatus.draft,
            order_id=order_id,
            balance_due=order.total_amount,
            created_by=user_id
        )
        
        db.add(db_invoice)
        db.flush()
        
        # Create invoice items from order items
        for order_item in order.items:
            db_item = InvoiceItem(
                invoice_id=db_invoice.id,
                item_type="product",
                product_id=order_item.product_id,
                description=order_item.product.name if order_item.product else "Product",
                quantity=order_item.quantity,
                unit_price=order_item.unit_price,
                line_total=order_item.line_total
            )
            db.add(db_item)
        
        # Create audit log
        log_entry = InvoiceLog(
            invoice_id=db_invoice.id,
            action="created",
            description=f"Invoice {invoice_number} generated from order {order.order_number}",
            performed_by=user_id,
            log_metadata={"order_id": order_id, "order_number": order.order_number}
        )
        db.add(log_entry)
        
        db.commit()
        db.refresh(db_invoice)
        
        return db_invoice
        
    except Exception as e:
        logger.error(f"Generate invoice from order error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate invoice from order")

@app.post("/api/invoices/generate-from-service/{service_booking_id}")
def generate_invoice_from_service(service_booking_id: str, db: Session = Depends(get_db)):
    """Generate invoice from service booking"""
    try:
        user_id = "56846977-f345-439c-b019-3330f3d16b7e"
        
        # Get service booking
        service_booking = db.query(ServiceBooking).filter(ServiceBooking.id == service_booking_id).first()
        if not service_booking:
            raise HTTPException(status_code=404, detail="Service booking not found")
        
        # Check if invoice already exists for this service booking
        existing_invoice = db.query(Invoice).filter(Invoice.service_booking_id == service_booking_id).first()
        if existing_invoice:
            raise HTTPException(status_code=400, detail="Invoice already exists for this service booking")
        
        # Generate invoice number
        invoice_count = db.query(Invoice).count()
        invoice_number = f"INV-{datetime.utcnow().strftime('%Y')}-{invoice_count + 1:04d}"
        
        # Calculate amounts
        service_amount = service_booking.actual_cost or service_booking.estimated_cost or 0.0
        tax_amount = service_amount * 0.18
        total_amount = service_amount + tax_amount
        
        # Create invoice
        db_invoice = Invoice(
            invoice_number=invoice_number,
            invoice_type=InvoiceType.service_booking,
            client_name=service_booking.client_name,
            client_email=service_booking.client_email,
            client_phone=service_booking.client_phone,
            issue_date=datetime.utcnow(),
            due_date=datetime.utcnow() + timedelta(days=30),  # 30 days from now
            subtotal=service_amount,
            tax_rate=0.18,
            tax_amount=tax_amount,
            total_amount=total_amount,
            currency=Currency.rwf,
            status=InvoiceStatus.draft,
            service_booking_id=service_booking_id,
            balance_due=total_amount,
            created_by=user_id
        )
        
        db.add(db_invoice)
        db.flush()
        
        # Create invoice item for service
        db_item = InvoiceItem(
            invoice_id=db_invoice.id,
            item_type="service",
            description=f"{service_booking.service_type.value.replace('_', ' ').title()} - {service_booking.description}",
            quantity=1,
            unit_price=service_amount,
            line_total=service_amount
        )
        db.add(db_item)
        
        # Create audit log
        log_entry = InvoiceLog(
            invoice_id=db_invoice.id,
            action="created",
            description=f"Invoice {invoice_number} generated from service booking {service_booking.booking_number}",
            performed_by=user_id,
            log_metadata={"service_booking_id": service_booking_id, "booking_number": service_booking.booking_number}
        )
        db.add(log_entry)
        
        db.commit()
        db.refresh(db_invoice)
        
        return db_invoice
        
    except Exception as e:
        logger.error(f"Generate invoice from service booking error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate invoice from service booking")

# ===============================
# Missing Invoice CRUD Endpoints
# ===============================

@app.post("/api/invoices")
def create_invoice(invoice_data: InvoiceCreate, db: Session = Depends(get_db)):
    """Create new invoice"""
    try:
        user_id = "56846977-f345-439c-b019-3330f3d16b7e"  # Demo admin user
        
        # Generate invoice number
        invoice_count = db.query(Invoice).count()
        invoice_number = f"INV-{datetime.utcnow().strftime('%Y')}-{invoice_count + 1:04d}"
        
        # Calculate totals
        subtotal = sum(item.quantity * item.unit_price for item in invoice_data.items)
        tax_amount = subtotal * invoice_data.tax_rate
        total_amount = subtotal + tax_amount - invoice_data.discount_amount
        
        # Handle client creation/update
        client_id = invoice_data.client_id
        if not client_id and invoice_data.client_name:
            # Check if client exists by name/email/phone
            existing_client = None
            if invoice_data.client_email:
                existing_client = db.query(Client).filter(Client.email == invoice_data.client_email).first()
            if not existing_client and invoice_data.client_phone:
                existing_client = db.query(Client).filter(Client.phone == invoice_data.client_phone).first()
            
            if existing_client:
                client_id = existing_client.id
            else:
                # Create new client
                new_client = Client(
                    name=invoice_data.client_name,
                    email=invoice_data.client_email,
                    phone=invoice_data.client_phone,
                    address=invoice_data.client_address
                )
                db.add(new_client)
                db.flush()
                client_id = new_client.id
        
        # Create invoice
        db_invoice = Invoice(
            invoice_number=invoice_number,
            invoice_type=invoice_data.invoice_type,
            client_id=client_id,
            client_name=invoice_data.client_name,
            client_email=invoice_data.client_email,
            client_phone=invoice_data.client_phone,
            client_address=invoice_data.client_address,
            issue_date=datetime.utcnow(),
            due_date=invoice_data.due_date,
            subtotal=subtotal,
            tax_rate=invoice_data.tax_rate,
            tax_amount=tax_amount,
            discount_amount=invoice_data.discount_amount,
            total_amount=total_amount,
            currency=invoice_data.currency,
            status=InvoiceStatus.draft,
            notes=invoice_data.notes,
            terms=invoice_data.terms,
            order_id=invoice_data.order_id,
            service_booking_id=invoice_data.service_booking_id,
            is_recurring=invoice_data.is_recurring,
            recurring_frequency=invoice_data.recurring_frequency,
            balance_due=total_amount,
            created_by=user_id
        )
        
        db.add(db_invoice)
        db.flush()
        
        # Create invoice items
        for item_data in invoice_data.items:
            line_total = item_data.quantity * item_data.unit_price
            if item_data.discount_amount:
                line_total -= item_data.discount_amount
            elif item_data.discount_percentage:
                line_total -= (line_total * item_data.discount_percentage / 100)
            
            db_item = InvoiceItem(
                invoice_id=db_invoice.id,
                item_type=item_data.item_type,
                product_id=item_data.product_id,
                description=item_data.description,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                line_total=line_total,
                weight=item_data.weight,
                weight_unit=item_data.weight_unit,
                hours=item_data.hours,
                hourly_rate=item_data.hourly_rate,
                discount_percentage=item_data.discount_percentage,
                discount_amount=item_data.discount_amount
            )
            db.add(db_item)
        
        # Create audit log
        log_entry = InvoiceLog(
            invoice_id=db_invoice.id,
            action="created",
            description=f"Invoice {invoice_number} created manually",
            performed_by=user_id,
            log_metadata={"invoice_type": invoice_data.invoice_type.value}
        )
        db.add(log_entry)
        
        db.commit()
        db.refresh(db_invoice)
        
        return {
            "success": True,
            "message": "Invoice created successfully",
            "id": db_invoice.id,
            "invoice_number": db_invoice.invoice_number
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Create invoice error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create invoice: {str(e)}")

@app.put("/api/invoices/{invoice_id}")
def update_invoice(invoice_id: str, invoice_update: InvoiceUpdate, db: Session = Depends(get_db)):
    """Update existing invoice"""
    try:
        user_id = "56846977-f345-439c-b019-3330f3d16b7e"  # Demo admin user
        
        # Get existing invoice
        db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not db_invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        # Check if invoice can be updated (not paid or cancelled)
        if db_invoice.status in [InvoiceStatus.paid, InvoiceStatus.cancelled]:
            raise HTTPException(status_code=400, detail="Cannot update paid or cancelled invoice")
        
        # Update fields
        update_data = invoice_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_invoice, field, value)
        
        db_invoice.updated_at = datetime.utcnow()
        
        # Recalculate balance if status changed
        if invoice_update.status and invoice_update.status != db_invoice.status:
            if invoice_update.status == InvoiceStatus.paid:
                db_invoice.paid_amount = db_invoice.total_amount
                db_invoice.balance_due = 0.0
            elif invoice_update.status in [InvoiceStatus.draft, InvoiceStatus.sent]:
                db_invoice.balance_due = db_invoice.total_amount - db_invoice.paid_amount
        
        # Create audit log
        log_entry = InvoiceLog(
            invoice_id=db_invoice.id,
            action="updated",
            description=f"Invoice {db_invoice.invoice_number} updated",
            performed_by=user_id,
            log_metadata={"updated_fields": list(update_data.keys())}
        )
        db.add(log_entry)
        
        db.commit()
        
        return {
            "success": True,
            "message": "Invoice updated successfully",
            "id": db_invoice.id
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Update invoice error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update invoice: {str(e)}")

@app.delete("/api/invoices/{invoice_id}")
def delete_invoice(invoice_id: str, db: Session = Depends(get_db)):
    """Delete invoice"""
    try:
        user_id = "56846977-f345-439c-b019-3330f3d16b7e"  # Demo admin user
        
        # Get existing invoice
        db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not db_invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        # Check if invoice can be deleted (only draft invoices)
        if db_invoice.status != InvoiceStatus.draft:
            raise HTTPException(status_code=400, detail="Can only delete draft invoices")
        
        # Create audit log before deletion
        log_entry = InvoiceLog(
            invoice_id=db_invoice.id,
            action="deleted",
            description=f"Invoice {db_invoice.invoice_number} deleted",
            performed_by=user_id,
            log_metadata={"invoice_number": db_invoice.invoice_number}
        )
        db.add(log_entry)
        db.commit()
        
        # Delete invoice (cascade will handle items, payments, logs)
        db.delete(db_invoice)
        db.commit()
        
        return {
            "success": True,
            "message": "Invoice deleted successfully"
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Delete invoice error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete invoice: {str(e)}")

@app.post("/api/invoices/{invoice_id}/payments")
def add_invoice_payment(invoice_id: str, payment_data: InvoicePaymentCreate, db: Session = Depends(get_db)):
    """Add payment to invoice"""
    try:
        user_id = "56846977-f345-439c-b019-3330f3d16b7e"  # Demo admin user
        
        # Get existing invoice
        db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not db_invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        # Check if invoice can receive payments
        if db_invoice.status in [InvoiceStatus.cancelled, InvoiceStatus.paid]:
            raise HTTPException(status_code=400, detail="Cannot add payment to cancelled or fully paid invoice")
        
        # Validate payment amount
        if payment_data.amount <= 0:
            raise HTTPException(status_code=400, detail="Payment amount must be greater than 0")
        
        if payment_data.amount > db_invoice.balance_due:
            raise HTTPException(status_code=400, detail="Payment amount cannot exceed balance due")
        
        # Create payment record
        db_payment = InvoicePayment(
            invoice_id=invoice_id,
            payment_method=payment_data.payment_method,
            amount=payment_data.amount,
            payment_date=payment_data.payment_date or datetime.utcnow(),
            payment_status=PaymentStatus.completed,
            reference_number=payment_data.reference_number,
            transaction_id=payment_data.transaction_id,
            notes=payment_data.notes,
            created_by=user_id
        )
        
        db.add(db_payment)
        
        # Update invoice payment status
        db_invoice.paid_amount += payment_data.amount
        db_invoice.balance_due = db_invoice.total_amount - db_invoice.paid_amount
        db_invoice.updated_at = datetime.utcnow()
        
        # Update invoice status based on payment
        if db_invoice.balance_due <= 0:
            db_invoice.status = InvoiceStatus.paid
            db_invoice.balance_due = 0.0  # Ensure it's exactly 0
        else:
            db_invoice.status = InvoiceStatus.partially_paid
        
        # Create audit log
        log_entry = InvoiceLog(
            invoice_id=invoice_id,
            action="payment_added",
            description=f"Payment of {payment_data.amount} {db_invoice.currency.value} added to invoice {db_invoice.invoice_number}",
            performed_by=user_id,
            log_metadata={
                "payment_amount": payment_data.amount,
                "payment_method": payment_data.payment_method.value,
                "new_balance": float(db_invoice.balance_due)
            }
        )
        db.add(log_entry)
        
        db.commit()
        db.refresh(db_payment)
        
        return {
            "success": True,
            "message": "Payment added successfully",
            "payment_id": db_payment.id,
            "new_balance": db_invoice.balance_due,
            "invoice_status": db_invoice.status.value
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Add invoice payment error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add payment: {str(e)}")

@app.get("/api/invoices/client/{client_id}")
def get_invoices_by_client(client_id: str, db: Session = Depends(get_db)):
    """Get all invoices for a specific client"""
    try:
        # Verify client exists
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Get invoices for client
        invoices = db.query(Invoice).filter(Invoice.client_id == client_id).order_by(Invoice.created_at.desc()).all()
        
        # Format response
        formatted_invoices = []
        for invoice in invoices:
            formatted_invoice = {
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "invoice_type": invoice.invoice_type.value,
                "issue_date": invoice.issue_date.isoformat() if invoice.issue_date else None,
                "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
                "total_amount": invoice.total_amount,
                "paid_amount": invoice.paid_amount,
                "balance_due": invoice.balance_due,
                "currency": invoice.currency.value,
                "status": invoice.status.value,
                "created_at": invoice.created_at.isoformat() if invoice.created_at else None
            }
            formatted_invoices.append(formatted_invoice)
        
        return {
            "client_name": client.name,
            "client_email": client.email,
            "total_invoices": len(invoices),
            "invoices": formatted_invoices
        }
        
    except Exception as e:
        logger.error(f"Get invoices by client error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve client invoices: {str(e)}")

# ===============================
# Portfolio Management Endpoints
# ===============================

@app.get("/api/portfolio")
def get_portfolio_items(db: Session = Depends(get_db)):
    """Get all portfolio items with enhanced details"""
    try:
        portfolio_items = db.query(PortfolioItem).order_by(PortfolioItem.created_at.desc()).all()
        
        # Format response
        formatted_items = []
        for item in portfolio_items:
            formatted_item = {
                "id": item.id,
                "title": item.title,
                "category": item.category,
                "description": item.description,
                "image": item.image,
                "technologies": item.technologies,
                "client": item.client,
                "date": item.date,
                "status": item.status,
                "link": item.link,
                "results": item.results,
                "created_by": item.created_by,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None
            }
            formatted_items.append(formatted_item)
        
        return formatted_items
    except Exception as e:
        logger.error(f"Get portfolio items error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve portfolio items")

@app.post("/api/portfolio")
def create_portfolio_item(item_data: PortfolioItemCreate, db: Session = Depends(get_db)):
    """Create new portfolio item"""
    try:
        user_id = "56846977-f345-439c-b019-3330f3d16b7e"  # Demo admin user
        
        # Create portfolio item
        db_item = PortfolioItem(
            title=item_data.title,
            category=item_data.category.value if hasattr(item_data.category, 'value') else item_data.category,
            description=item_data.description,
            image=item_data.image,
            technologies=item_data.technologies,
            client=item_data.client,
            date=item_data.date,
            status=item_data.status.value if hasattr(item_data.status, 'value') else item_data.status,
            link=item_data.link,
            results=item_data.results,
            created_by=user_id
        )
        
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        
        return {
            "success": True,
            "message": "Portfolio item created successfully",
            "id": db_item.id
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Create portfolio item error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create portfolio item: {str(e)}")

@app.get("/api/portfolio/summary")
def get_portfolio_summary(db: Session = Depends(get_db)):
    """Get portfolio statistics and summary"""
    try:
        # Total items
        total_items = db.query(PortfolioItem).count()
        
        # Items by category
        category_counts = {}
        for category in PortfolioCategory:
            count = db.query(PortfolioItem).filter(PortfolioItem.category == category.value).count()
            category_counts[category.value] = count
        
        # Items by status
        status_counts = {}
        for status in PortfolioStatus:
            count = db.query(PortfolioItem).filter(PortfolioItem.status == status.value).count()
            status_counts[status.value] = count
        
        # Recent items
        recent_items = db.query(PortfolioItem).order_by(PortfolioItem.created_at.desc()).limit(5).all()
        
        # Technologies usage (get most used technologies)
        technology_usage = {}
        all_items = db.query(PortfolioItem).all()
        for item in all_items:
            if item.technologies and isinstance(item.technologies, list):
                for tech in item.technologies:
                    technology_usage[tech] = technology_usage.get(tech, 0) + 1
        
        # Sort technologies by usage
        top_technologies = sorted(technology_usage.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_items": total_items,
            "category_counts": category_counts,
            "status_counts": status_counts,
            "recent_items": len(recent_items),
            "top_technologies": dict(top_technologies)
        }
    except Exception as e:
        logger.error(f"Get portfolio summary error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve portfolio summary: {str(e)}")

@app.get("/api/portfolio/{item_id}")
def get_portfolio_item(item_id: str, db: Session = Depends(get_db)):
    """Get single portfolio item with full details"""
    try:
        item = db.query(PortfolioItem).filter(PortfolioItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Portfolio item not found")
        
        # Format response
        formatted_item = {
            "id": item.id,
            "title": item.title,
            "category": item.category,
            "description": item.description,
            "image": item.image,
            "technologies": item.technologies,
            "client": item.client,
            "date": item.date,
            "status": item.status,
            "link": item.link,
            "results": item.results,
            "created_by": item.created_by,
            "created_by_name": item.created_by_user.full_name if item.created_by_user else "Unknown",
            "created_at": item.created_at.isoformat() if item.created_at else None,
            "updated_at": item.updated_at.isoformat() if item.updated_at else None
        }
        
        return formatted_item
    except Exception as e:
        logger.error(f"Get portfolio item error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve portfolio item")

@app.put("/api/portfolio/{item_id}")
def update_portfolio_item(item_id: str, item_update: PortfolioItemUpdate, db: Session = Depends(get_db)):
    """Update existing portfolio item"""
    try:
        # Get existing item
        db_item = db.query(PortfolioItem).filter(PortfolioItem.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Portfolio item not found")
        
        # Update fields
        update_data = item_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        db_item.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "success": True,
            "message": "Portfolio item updated successfully",
            "id": db_item.id
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Update portfolio item error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update portfolio item: {str(e)}")

@app.delete("/api/portfolio/{item_id}")
def delete_portfolio_item(item_id: str, db: Session = Depends(get_db)):
    """Delete portfolio item"""
    try:
        # Get existing item
        db_item = db.query(PortfolioItem).filter(PortfolioItem.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Portfolio item not found")
        
        # Delete item
        db.delete(db_item)
        db.commit()
        
        return {
            "success": True,
            "message": "Portfolio item deleted successfully"
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Delete portfolio item error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete portfolio item: {str(e)}")

@app.get("/api/portfolio/category/{category}")
def get_portfolio_by_category(category: str, db: Session = Depends(get_db)):
    """Get portfolio items by category"""
    try:
        # Validate category
        valid_categories = [cat.value for cat in PortfolioCategory]
        if category not in valid_categories:
            raise HTTPException(status_code=400, detail="Invalid portfolio category")
        
        items = db.query(PortfolioItem).filter(PortfolioItem.category == category).order_by(PortfolioItem.created_at.desc()).all()
        
        # Format response
        formatted_items = []
        for item in items:
            formatted_item = {
                "id": item.id,
                "title": item.title,
                "category": item.category,
                "description": item.description,
                "image": item.image,
                "client": item.client,
                "date": item.date,
                "status": item.status,
                "link": item.link,
                "created_at": item.created_at.isoformat() if item.created_at else None
            }
            formatted_items.append(formatted_item)
        
        return {
            "category": category,
            "total_items": len(items),
            "items": formatted_items
        }
        
    except HTTPException:
        raise  # Re-raise HTTPExceptions to preserve status codes
    except Exception as e:
        logger.error(f"Get portfolio by category error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve portfolio items by category: {str(e)}")

@app.get("/api/portfolio/status/{status}")
def get_portfolio_by_status(status: str, db: Session = Depends(get_db)):
    """Get portfolio items by status"""
    try:
        # Validate status
        valid_statuses = [status.value for status in PortfolioStatus]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid portfolio status")
        
        items = db.query(PortfolioItem).filter(PortfolioItem.status == status).order_by(PortfolioItem.created_at.desc()).all()
        
        # Format response
        formatted_items = []
        for item in items:
            formatted_item = {
                "id": item.id,
                "title": item.title,
                "category": item.category,
                "description": item.description,
                "client": item.client,
                "date": item.date,
                "status": item.status,
                "created_at": item.created_at.isoformat() if item.created_at else None
            }
            formatted_items.append(formatted_item)
        
        return {
            "status": status,
            "total_items": len(items),
            "items": formatted_items
        }
        
    except HTTPException:
        raise  # Re-raise HTTPExceptions to preserve status codes
    except Exception as e:
        logger.error(f"Get portfolio by status error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve portfolio items by status: {str(e)}")

# ===============================
# Second-Hand Sales Management Endpoints
# ===============================

@app.get("/api/secondhand")
def get_secondhand_items(db: Session = Depends(get_db)):
    """Get all second-hand items with enhanced details"""
    try:
        items = db.query(SecondHandItem).order_by(SecondHandItem.created_at.desc()).all()
        
        # Format response
        formatted_items = []
        for item in items:
            formatted_item = {
                "id": item.id,
                "product_name": item.product_name,
                "category": item.category,
                "condition": item.condition,
                "original_price": item.original_price,
                "selling_price": item.selling_price,
                "description": item.description,
                "images": item.images,
                "specifications": item.specifications,
                "warranty_info": item.warranty_info,
                "seller_name": item.seller_name,
                "seller_contact": item.seller_contact,
                "location": item.location,
                "status": item.status,
                "views_count": item.views_count,
                "created_by": item.created_by,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None,
                "sold_at": item.sold_at.isoformat() if item.sold_at else None
            }
            formatted_items.append(formatted_item)
        
        return formatted_items
    except Exception as e:
        logger.error(f"Get second-hand items error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve second-hand items")

@app.post("/api/secondhand")
def create_secondhand_item(item_data: SecondHandItemCreate, db: Session = Depends(get_db)):
    """Create new second-hand item"""
    try:
        user_id = "56846977-f345-439c-b019-3330f3d16b7e"  # Demo admin user
        
        # Create second-hand item
        db_item = SecondHandItem(
            product_name=item_data.product_name,
            category=item_data.category.value if hasattr(item_data.category, 'value') else item_data.category,
            condition=item_data.condition.value if hasattr(item_data.condition, 'value') else item_data.condition,
            original_price=item_data.original_price,
            selling_price=item_data.selling_price,
            description=item_data.description,
            images=item_data.images,
            specifications=item_data.specifications,
            warranty_info=item_data.warranty_info,
            seller_name=item_data.seller_name,
            seller_contact=item_data.seller_contact,
            location=item_data.location,
            status="available",
            views_count=0,
            created_by=user_id
        )
        
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        
        return {
            "success": True,
            "message": "Second-hand item created successfully",
            "id": db_item.id
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Create second-hand item error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create second-hand item: {str(e)}")

@app.get("/api/secondhand/summary")
def get_secondhand_summary(db: Session = Depends(get_db)):
    """Get second-hand items statistics and summary"""
    try:
        # Total items
        total_items = db.query(SecondHandItem).count()
        
        # Items by category
        category_counts = {}
        for category in SecondHandCategory:
            count = db.query(SecondHandItem).filter(SecondHandItem.category == category.value).count()
            category_counts[category.value] = count
        
        # Items by condition
        condition_counts = {}
        for condition in SecondHandCondition:
            count = db.query(SecondHandItem).filter(SecondHandItem.condition == condition.value).count()
            condition_counts[condition.value] = count
        
        # Items by status
        status_counts = {}
        for status in ["available", "sold", "reserved"]:
            count = db.query(SecondHandItem).filter(SecondHandItem.status == status).count()
            status_counts[status] = count
        
        # Price statistics
        from sqlalchemy import func
        price_stats = db.query(
            func.avg(SecondHandItem.selling_price).label('avg_price'),
            func.min(SecondHandItem.selling_price).label('min_price'),
            func.max(SecondHandItem.selling_price).label('max_price')
        ).first()
        
        # Total views
        total_views = db.query(func.sum(SecondHandItem.views_count)).scalar() or 0
        
        # Recent items
        recent_items = db.query(SecondHandItem).order_by(SecondHandItem.created_at.desc()).limit(5).all()
        
        return {
            "total_items": total_items,
            "category_counts": category_counts,
            "condition_counts": condition_counts,
            "status_counts": status_counts,
            "price_statistics": {
                "average_price": float(price_stats.avg_price) if price_stats.avg_price else 0,
                "min_price": float(price_stats.min_price) if price_stats.min_price else 0,
                "max_price": float(price_stats.max_price) if price_stats.max_price else 0
            },
            "total_views": int(total_views),
            "recent_items": len(recent_items)
        }
    except Exception as e:
        logger.error(f"Get second-hand summary error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve second-hand summary: {str(e)}")

@app.get("/api/secondhand/category/{category}")
def get_secondhand_by_category(category: str, db: Session = Depends(get_db)):
    """Get second-hand items by category"""
    try:
        # Validate category
        valid_categories = [cat.value for cat in SecondHandCategory]
        if category not in valid_categories:
            raise HTTPException(status_code=400, detail="Invalid category")
        
        items = db.query(SecondHandItem).filter(SecondHandItem.category == category).order_by(SecondHandItem.created_at.desc()).all()
        
        # Format response
        formatted_items = []
        for item in items:
            formatted_item = {
                "id": item.id,
                "product_name": item.product_name,
                "category": item.category,
                "condition": item.condition,
                "selling_price": item.selling_price,
                "images": item.images,
                "status": item.status,
                "location": item.location,
                "views_count": item.views_count,
                "created_at": item.created_at.isoformat() if item.created_at else None
            }
            formatted_items.append(formatted_item)
        
        return {
            "category": category,
            "total_items": len(items),
            "items": formatted_items
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get second-hand by category error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve second-hand items by category: {str(e)}")

@app.get("/api/secondhand/condition/{condition}")
def get_secondhand_by_condition(condition: str, db: Session = Depends(get_db)):
    """Get second-hand items by condition"""
    try:
        # Validate condition
        valid_conditions = [cond.value for cond in SecondHandCondition]
        if condition not in valid_conditions:
            raise HTTPException(status_code=400, detail="Invalid condition")
        
        items = db.query(SecondHandItem).filter(SecondHandItem.condition == condition).order_by(SecondHandItem.created_at.desc()).all()
        
        # Format response
        formatted_items = []
        for item in items:
            formatted_item = {
                "id": item.id,
                "product_name": item.product_name,
                "category": item.category,
                "condition": item.condition,
                "selling_price": item.selling_price,
                "images": item.images,
                "status": item.status,
                "created_at": item.created_at.isoformat() if item.created_at else None
            }
            formatted_items.append(formatted_item)
        
        return {
            "condition": condition,
            "total_items": len(items),
            "items": formatted_items
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get second-hand by condition error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve second-hand items by condition: {str(e)}")

@app.get("/api/secondhand/{item_id}")
def get_secondhand_item(item_id: str, db: Session = Depends(get_db)):
    """Get single second-hand item with full details and increment view count"""
    try:
        item = db.query(SecondHandItem).filter(SecondHandItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Second-hand item not found")
        
        # Increment view count
        item.views_count += 1
        db.commit()
        
        # Format response
        formatted_item = {
            "id": item.id,
            "product_name": item.product_name,
            "category": item.category,
            "condition": item.condition,
            "original_price": item.original_price,
            "selling_price": item.selling_price,
            "description": item.description,
            "images": item.images,
            "specifications": item.specifications,
            "warranty_info": item.warranty_info,
            "seller_name": item.seller_name,
            "seller_contact": item.seller_contact,
            "location": item.location,
            "status": item.status,
            "views_count": item.views_count,
            "created_by": item.created_by,
            "created_by_name": item.created_by_user.full_name if item.created_by_user else "Unknown",
            "created_at": item.created_at.isoformat() if item.created_at else None,
            "updated_at": item.updated_at.isoformat() if item.updated_at else None,
            "sold_at": item.sold_at.isoformat() if item.sold_at else None
        }
        
        return formatted_item
    except Exception as e:
        logger.error(f"Get second-hand item error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve second-hand item")

@app.put("/api/secondhand/{item_id}")
def update_secondhand_item(item_id: str, item_update: SecondHandItemUpdate, db: Session = Depends(get_db)):
    """Update existing second-hand item"""
    try:
        # Get existing item
        db_item = db.query(SecondHandItem).filter(SecondHandItem.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Second-hand item not found")
        
        # Update fields
        update_data = item_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'category' and hasattr(value, 'value'):
                setattr(db_item, field, value.value)
            elif field == 'condition' and hasattr(value, 'value'):
                setattr(db_item, field, value.value)
            elif field == 'status' and value == 'sold':
                setattr(db_item, field, value)
                db_item.sold_at = datetime.utcnow()
            else:
                setattr(db_item, field, value)
        
        db_item.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "success": True,
            "message": "Second-hand item updated successfully",
            "id": db_item.id
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Update second-hand item error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update second-hand item: {str(e)}")

@app.delete("/api/secondhand/{item_id}")
def delete_secondhand_item(item_id: str, db: Session = Depends(get_db)):
    """Delete second-hand item"""
    try:
        # Get existing item
        db_item = db.query(SecondHandItem).filter(SecondHandItem.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Second-hand item not found")
        
        # Check if item can be deleted (only available items)
        if db_item.status == "sold":
            raise HTTPException(status_code=400, detail="Cannot delete sold items")
        
        # Delete item
        db.delete(db_item)
        db.commit()
        
        return {
            "success": True,
            "message": "Second-hand item deleted successfully"
        }
        
    except HTTPException:
        raise  # Re-raise HTTPExceptions to preserve status codes
    except Exception as e:
        db.rollback()
        logger.error(f"Delete second-hand item error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete second-hand item: {str(e)}")

# ===============================
# Marble Dust Production Management Endpoints
# ===============================

@app.get("/api/marble-dust")
def get_marble_dust_batches(db: Session = Depends(get_db)):
    """Get all marble dust batches with enhanced details"""
    try:
        batches = db.query(MarbleDustBatch).order_by(MarbleDustBatch.created_at.desc()).all()
        
        # Format response
        formatted_batches = []
        for batch in batches:
            formatted_batch = {
                "id": batch.id,
                "batch_number": batch.batch_number,
                "production_date": batch.production_date.isoformat() if batch.production_date else None,
                "quantity_kg": batch.quantity_kg,
                "remaining_quantity_kg": batch.remaining_quantity_kg,
                "quality_grade": batch.quality_grade,
                "source_material": batch.source_material,
                "production_location": batch.production_location,
                "moisture_content": batch.moisture_content,
                "particle_size_mm": batch.particle_size_mm,
                "color_classification": batch.color_classification,
                "cost_per_kg": batch.cost_per_kg,
                "selling_price_per_kg": batch.selling_price_per_kg,
                "total_cost": batch.total_cost,
                "total_revenue": batch.total_revenue,
                "status": batch.status,
                "notes": batch.notes,
                "quality_test_results": batch.quality_test_results,
                "created_by": batch.created_by,
                "created_at": batch.created_at.isoformat() if batch.created_at else None,
                "updated_at": batch.updated_at.isoformat() if batch.updated_at else None,
                "shipped_at": batch.shipped_at.isoformat() if batch.shipped_at else None,
                "profit_margin": ((batch.selling_price_per_kg - batch.cost_per_kg) / batch.cost_per_kg * 100) if batch.cost_per_kg > 0 else 0
            }
            formatted_batches.append(formatted_batch)
        
        return formatted_batches
    except Exception as e:
        logger.error(f"Get marble dust batches error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve marble dust batches")

@app.post("/api/marble-dust")
def create_marble_dust_batch(batch_data: MarbleDustBatchCreate, db: Session = Depends(get_db)):
    """Create new marble dust batch"""
    try:
        user_id = "56846977-f345-439c-b019-3330f3d16b7e"  # Demo admin user
        
        # Check if batch number already exists
        existing_batch = db.query(MarbleDustBatch).filter(MarbleDustBatch.batch_number == batch_data.batch_number).first()
        if existing_batch:
            raise HTTPException(status_code=400, detail="Batch number already exists")
        
        # Calculate total cost
        total_cost = batch_data.quantity_kg * batch_data.cost_per_kg
        
        # Create marble dust batch
        db_batch = MarbleDustBatch(
            batch_number=batch_data.batch_number,
            production_date=batch_data.production_date,
            quantity_kg=batch_data.quantity_kg,
            remaining_quantity_kg=batch_data.quantity_kg,  # Initially all quantity remains
            quality_grade=batch_data.quality_grade.value if hasattr(batch_data.quality_grade, 'value') else batch_data.quality_grade,
            source_material=batch_data.source_material,
            production_location=batch_data.production_location,
            moisture_content=batch_data.moisture_content,
            particle_size_mm=batch_data.particle_size_mm,
            color_classification=batch_data.color_classification,
            cost_per_kg=batch_data.cost_per_kg,
            selling_price_per_kg=batch_data.selling_price_per_kg,
            total_cost=total_cost,
            total_revenue=0.0,
            status="in_production",
            notes=batch_data.notes,
            quality_test_results={},
            created_by=user_id
        )
        
        db.add(db_batch)
        db.commit()
        db.refresh(db_batch)
        
        return {
            "success": True,
            "message": "Marble dust batch created successfully",
            "id": db_batch.id,
            "batch_number": db_batch.batch_number
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Create marble dust batch error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create marble dust batch: {str(e)}")

@app.get("/api/marble-dust/summary")
def get_marble_dust_summary(db: Session = Depends(get_db)):
    """Get marble dust production statistics and summary"""
    try:
        # Total batches
        total_batches = db.query(MarbleDustBatch).count()
        
        # Batches by quality grade
        quality_counts = {}
        for quality in MarbleDustQuality:
            count = db.query(MarbleDustBatch).filter(MarbleDustBatch.quality_grade == quality.value).count()
            quality_counts[quality.value] = count
        
        # Batches by status
        status_counts = {}
        for status in MarbleDustStatus:
            count = db.query(MarbleDustBatch).filter(MarbleDustBatch.status == status.value).count()
            status_counts[status.value] = count
        
        # Production statistics
        from sqlalchemy import func
        production_stats = db.query(
            func.sum(MarbleDustBatch.quantity_kg).label('total_produced'),
            func.sum(MarbleDustBatch.remaining_quantity_kg).label('total_remaining'),
            func.sum(MarbleDustBatch.total_cost).label('total_production_cost'),
            func.sum(MarbleDustBatch.total_revenue).label('total_revenue'),
            func.avg(MarbleDustBatch.cost_per_kg).label('avg_cost_per_kg'),
            func.avg(MarbleDustBatch.selling_price_per_kg).label('avg_selling_price')
        ).first()
        
        # Calculate total sold and profit
        total_produced = float(production_stats.total_produced) if production_stats.total_produced else 0
        total_remaining = float(production_stats.total_remaining) if production_stats.total_remaining else 0
        total_sold = total_produced - total_remaining
        total_cost = float(production_stats.total_production_cost) if production_stats.total_production_cost else 0
        total_revenue = float(production_stats.total_revenue) if production_stats.total_revenue else 0
        total_profit = total_revenue - total_cost
        
        # Recent batches
        recent_batches = db.query(MarbleDustBatch).order_by(MarbleDustBatch.created_at.desc()).limit(5).all()
        
        # Low stock batches (less than 10% remaining)
        low_stock_batches = db.query(MarbleDustBatch).filter(
            MarbleDustBatch.remaining_quantity_kg < (MarbleDustBatch.quantity_kg * 0.1),
            MarbleDustBatch.remaining_quantity_kg > 0
        ).count()
        
        return {
            "total_batches": total_batches,
            "quality_counts": quality_counts,
            "status_counts": status_counts,
            "production_statistics": {
                "total_produced_kg": total_produced,
                "total_remaining_kg": total_remaining,
                "total_sold_kg": total_sold,
                "total_production_cost": total_cost,
                "total_revenue": total_revenue,
                "total_profit": total_profit,
                "avg_cost_per_kg": float(production_stats.avg_cost_per_kg) if production_stats.avg_cost_per_kg else 0,
                "avg_selling_price_per_kg": float(production_stats.avg_selling_price) if production_stats.avg_selling_price else 0,
                "profit_margin_percentage": (total_profit / total_cost * 100) if total_cost > 0 else 0
            },
            "recent_batches": len(recent_batches),
            "low_stock_batches": low_stock_batches
        }
    except Exception as e:
        logger.error(f"Get marble dust summary error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve marble dust summary: {str(e)}")

@app.get("/api/marble-dust/{batch_id}")
def get_marble_dust_batch(batch_id: str, db: Session = Depends(get_db)):
    """Get single marble dust batch with full details"""
    try:
        batch = db.query(MarbleDustBatch).filter(MarbleDustBatch.id == batch_id).first()
        if not batch:
            raise HTTPException(status_code=404, detail="Marble dust batch not found")
        
        # Format response
        formatted_batch = {
            "id": batch.id,
            "batch_number": batch.batch_number,
            "production_date": batch.production_date.isoformat() if batch.production_date else None,
            "quantity_kg": batch.quantity_kg,
            "remaining_quantity_kg": batch.remaining_quantity_kg,
            "quality_grade": batch.quality_grade,
            "source_material": batch.source_material,
            "production_location": batch.production_location,
            "moisture_content": batch.moisture_content,
            "particle_size_mm": batch.particle_size_mm,
            "color_classification": batch.color_classification,
            "cost_per_kg": batch.cost_per_kg,
            "selling_price_per_kg": batch.selling_price_per_kg,
            "total_cost": batch.total_cost,
            "total_revenue": batch.total_revenue,
            "status": batch.status,
            "notes": batch.notes,
            "quality_test_results": batch.quality_test_results,
            "created_by": batch.created_by,
            "created_by_name": batch.created_by_user.full_name if batch.created_by_user else "Unknown",
            "created_at": batch.created_at.isoformat() if batch.created_at else None,
            "updated_at": batch.updated_at.isoformat() if batch.updated_at else None,
            "shipped_at": batch.shipped_at.isoformat() if batch.shipped_at else None,
            "profit_margin": ((batch.selling_price_per_kg - batch.cost_per_kg) / batch.cost_per_kg * 100) if batch.cost_per_kg > 0 else 0,
            "sold_quantity_kg": batch.quantity_kg - batch.remaining_quantity_kg
        }
        
        return formatted_batch
    except Exception as e:
        logger.error(f"Get marble dust batch error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve marble dust batch")

@app.put("/api/marble-dust/{batch_id}")
def update_marble_dust_batch(batch_id: str, batch_update: MarbleDustBatchUpdate, db: Session = Depends(get_db)):
    """Update existing marble dust batch"""
    try:
        # Get existing batch
        db_batch = db.query(MarbleDustBatch).filter(MarbleDustBatch.id == batch_id).first()
        if not db_batch:
            raise HTTPException(status_code=404, detail="Marble dust batch not found")
        
        # Update fields
        update_data = batch_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'quality_grade' and hasattr(value, 'value'):
                setattr(db_batch, field, value.value)
            elif field == 'status' and hasattr(value, 'value'):
                setattr(db_batch, field, value.value)
                if value.value == 'shipped':
                    db_batch.shipped_at = datetime.utcnow()
            elif field == 'quantity_kg':
                # If quantity changes, adjust remaining quantity proportionally
                old_quantity = db_batch.quantity_kg
                new_quantity = value
                if old_quantity > 0:
                    proportion_remaining = db_batch.remaining_quantity_kg / old_quantity
                    db_batch.remaining_quantity_kg = new_quantity * proportion_remaining
                setattr(db_batch, field, value)
                # Recalculate total cost
                db_batch.total_cost = new_quantity * db_batch.cost_per_kg
            elif field == 'cost_per_kg':
                setattr(db_batch, field, value)
                # Recalculate total cost
                db_batch.total_cost = db_batch.quantity_kg * value
            else:
                setattr(db_batch, field, value)
        
        db_batch.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "success": True,
            "message": "Marble dust batch updated successfully",
            "id": db_batch.id
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Update marble dust batch error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update marble dust batch: {str(e)}")

@app.delete("/api/marble-dust/{batch_id}")
def delete_marble_dust_batch(batch_id: str, db: Session = Depends(get_db)):
    """Delete marble dust batch"""
    try:
        # Get existing batch
        db_batch = db.query(MarbleDustBatch).filter(MarbleDustBatch.id == batch_id).first()
        if not db_batch:
            raise HTTPException(status_code=404, detail="Marble dust batch not found")
        
        # Check if batch can be deleted (only if not shipped or sold)
        if db_batch.status in ["shipped", "sold"]:
            raise HTTPException(status_code=400, detail="Cannot delete shipped or sold batches")
        
        # Delete batch
        db.delete(db_batch)
        db.commit()
        
        return {
            "success": True,
            "message": "Marble dust batch deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Delete marble dust batch error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete marble dust batch: {str(e)}")

@app.get("/api/marble-dust/quality/{quality}")
def get_marble_dust_by_quality(quality: str, db: Session = Depends(get_db)):
    """Get marble dust batches by quality grade"""
    try:
        # Validate quality
        valid_qualities = [q.value for q in MarbleDustQuality]
        if quality not in valid_qualities:
            raise HTTPException(status_code=400, detail="Invalid quality grade")
        
        batches = db.query(MarbleDustBatch).filter(MarbleDustBatch.quality_grade == quality).order_by(MarbleDustBatch.created_at.desc()).all()
        
        # Format response
        formatted_batches = []
        for batch in batches:
            formatted_batch = {
                "id": batch.id,
                "batch_number": batch.batch_number,
                "production_date": batch.production_date.isoformat() if batch.production_date else None,
                "quantity_kg": batch.quantity_kg,
                "remaining_quantity_kg": batch.remaining_quantity_kg,
                "quality_grade": batch.quality_grade,
                "selling_price_per_kg": batch.selling_price_per_kg,
                "status": batch.status,
                "production_location": batch.production_location,
                "created_at": batch.created_at.isoformat() if batch.created_at else None
            }
            formatted_batches.append(formatted_batch)
        
        return {
            "quality": quality,
            "total_batches": len(batches),
            "batches": formatted_batches
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get marble dust by quality error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve marble dust batches by quality: {str(e)}")

@app.get("/api/marble-dust/status/{status}")
def get_marble_dust_by_status(status: str, db: Session = Depends(get_db)):
    """Get marble dust batches by status"""
    try:
        # Validate status
        valid_statuses = [s.value for s in MarbleDustStatus]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        batches = db.query(MarbleDustBatch).filter(MarbleDustBatch.status == status).order_by(MarbleDustBatch.created_at.desc()).all()
        
        # Format response
        formatted_batches = []
        for batch in batches:
            formatted_batch = {
                "id": batch.id,
                "batch_number": batch.batch_number,
                "production_date": batch.production_date.isoformat() if batch.production_date else None,
                "quantity_kg": batch.quantity_kg,
                "remaining_quantity_kg": batch.remaining_quantity_kg,
                "quality_grade": batch.quality_grade,
                "status": batch.status,
                "production_location": batch.production_location,
                "created_at": batch.created_at.isoformat() if batch.created_at else None
            }
            formatted_batches.append(formatted_batch)
        
        return {
            "status": status,
            "total_batches": len(batches),
            "batches": formatted_batches
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get marble dust by status error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve marble dust batches by status: {str(e)}")

# ===============================
# Starlink Resale Management Endpoints
# ===============================

@app.get("/api/starlink")
def get_starlink_installations(db: Session = Depends(get_db)):
    """Get all Starlink installations with enhanced details"""
    try:
        installations = db.query(StarlinkInstallation).order_by(StarlinkInstallation.created_at.desc()).all()
        
        # Format response
        formatted_installations = []
        for installation in installations:
            formatted_installation = {
                "id": installation.id,
                "customer_name": installation.customer_name,
                "customer_phone": installation.customer_phone,
                "customer_email": installation.customer_email,
                "installation_address": installation.installation_address,
                "kit_type": installation.kit_type,
                "kit_serial_number": installation.kit_serial_number,
                "installation_date": installation.installation_date.isoformat() if installation.installation_date else None,
                "technician_id": installation.technician_id,
                "technician_name": installation.technician_name,
                "installation_fee": installation.installation_fee,
                "monthly_fee": installation.monthly_fee,
                "equipment_cost": installation.equipment_cost,
                "total_cost": installation.total_cost,
                "installation_status": installation.installation_status,
                "service_status": installation.service_status,
                "coordinates": installation.coordinates,
                "notes": installation.notes,
                "completion_notes": installation.completion_notes,
                "created_by": installation.created_by,
                "created_at": installation.created_at.isoformat() if installation.created_at else None,
                "updated_at": installation.updated_at.isoformat() if installation.updated_at else None,
                "completed_at": installation.completed_at.isoformat() if installation.completed_at else None
            }
            formatted_installations.append(formatted_installation)
        
        return formatted_installations
    except Exception as e:
        logger.error(f"Get Starlink installations error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve Starlink installations")

@app.post("/api/starlink")
def create_starlink_installation(installation_data: StarlinkInstallationCreate, db: Session = Depends(get_db)):
    """Create new Starlink installation appointment"""
    try:
        user_id = "56846977-f345-439c-b019-3330f3d16b7e"  # Demo admin user
        
        # Calculate total cost
        total_cost = installation_data.installation_fee + installation_data.equipment_cost
        
        # Create Starlink installation
        db_installation = StarlinkInstallation(
            customer_name=installation_data.customer_name,
            customer_phone=installation_data.customer_phone,
            customer_email=installation_data.customer_email,
            installation_address=installation_data.installation_address,
            kit_type=installation_data.kit_type.value if hasattr(installation_data.kit_type, 'value') else installation_data.kit_type,
            kit_serial_number=installation_data.kit_serial_number,
            installation_date=installation_data.installation_date,
            technician_id=installation_data.technician_id,
            technician_name=installation_data.technician_name,
            installation_fee=installation_data.installation_fee,
            monthly_fee=installation_data.monthly_fee,
            equipment_cost=installation_data.equipment_cost,
            total_cost=total_cost,
            installation_status="scheduled",
            service_status="pending_activation",
            coordinates=installation_data.coordinates,
            notes=installation_data.notes,
            completion_notes=None,
            created_by=user_id
        )
        
        db.add(db_installation)
        db.commit()
        db.refresh(db_installation)
        
        return {
            "success": True,
            "message": "Starlink installation scheduled successfully",
            "id": db_installation.id,
            "installation_date": db_installation.installation_date.isoformat()
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Create Starlink installation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create Starlink installation: {str(e)}")

@app.get("/api/starlink/{installation_id}")
def get_starlink_installation(installation_id: str, db: Session = Depends(get_db)):
    """Get single Starlink installation with full details"""
    try:
        installation = db.query(StarlinkInstallation).filter(StarlinkInstallation.id == installation_id).first()
        if not installation:
            raise HTTPException(status_code=404, detail="Starlink installation not found")
        
        # Format response
        formatted_installation = {
            "id": installation.id,
            "customer_name": installation.customer_name,
            "customer_phone": installation.customer_phone,
            "customer_email": installation.customer_email,
            "installation_address": installation.installation_address,
            "kit_type": installation.kit_type,
            "kit_serial_number": installation.kit_serial_number,
            "installation_date": installation.installation_date.isoformat() if installation.installation_date else None,
            "technician_id": installation.technician_id,
            "technician_name": installation.technician_name,
            "installation_fee": installation.installation_fee,
            "monthly_fee": installation.monthly_fee,
            "equipment_cost": installation.equipment_cost,
            "total_cost": installation.total_cost,
            "installation_status": installation.installation_status,
            "service_status": installation.service_status,
            "coordinates": installation.coordinates,
            "notes": installation.notes,
            "completion_notes": installation.completion_notes,
            "created_by": installation.created_by,
            "created_by_name": installation.created_by_user.full_name if installation.created_by_user else "Unknown",
            "created_at": installation.created_at.isoformat() if installation.created_at else None,
            "updated_at": installation.updated_at.isoformat() if installation.updated_at else None,
            "completed_at": installation.completed_at.isoformat() if installation.completed_at else None,
            "is_active": installation.service_status == "active",
            "days_until_installation": (installation.installation_date - datetime.utcnow()).days if installation.installation_date > datetime.utcnow() else 0
        }
        
        return formatted_installation
    except Exception as e:
        logger.error(f"Get Starlink installation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve Starlink installation")

@app.put("/api/starlink/{installation_id}")
def update_starlink_installation(installation_id: str, installation_update: StarlinkInstallationUpdate, db: Session = Depends(get_db)):
    """Update existing Starlink installation"""
    try:
        # Get existing installation
        db_installation = db.query(StarlinkInstallation).filter(StarlinkInstallation.id == installation_id).first()
        if not db_installation:
            raise HTTPException(status_code=404, detail="Starlink installation not found")
        
        # Update fields
        update_data = installation_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'kit_type' and hasattr(value, 'value'):
                setattr(db_installation, field, value.value)
            elif field == 'installation_status' and hasattr(value, 'value'):
                setattr(db_installation, field, value.value)
                if value.value == 'completed':
                    db_installation.completed_at = datetime.utcnow()
            elif field == 'service_status' and hasattr(value, 'value'):
                setattr(db_installation, field, value.value)
            elif field in ['installation_fee', 'equipment_cost'] and value is not None:
                setattr(db_installation, field, value)
                # Recalculate total cost if fees change
                db_installation.total_cost = db_installation.installation_fee + db_installation.equipment_cost
            else:
                setattr(db_installation, field, value)
        
        db_installation.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "success": True,
            "message": "Starlink installation updated successfully",
            "id": db_installation.id
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Update Starlink installation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update Starlink installation: {str(e)}")

@app.delete("/api/starlink/{installation_id}")
def delete_starlink_installation(installation_id: str, db: Session = Depends(get_db)):
    """Delete Starlink installation"""
    try:
        # Get existing installation
        db_installation = db.query(StarlinkInstallation).filter(StarlinkInstallation.id == installation_id).first()
        if not db_installation:
            raise HTTPException(status_code=404, detail="Starlink installation not found")
        
        # Check if installation can be deleted (only scheduled or cancelled installations)
        if db_installation.installation_status in ["completed"] or db_installation.service_status == "active":
            raise HTTPException(status_code=400, detail="Cannot delete completed installations or active services")
        
        # Delete installation
        db.delete(db_installation)
        db.commit()
        
        return {
            "success": True,
            "message": "Starlink installation deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Delete Starlink installation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete Starlink installation: {str(e)}")

@app.get("/api/starlink/kit-type/{kit_type}")
def get_starlink_by_kit_type(kit_type: str, db: Session = Depends(get_db)):
    """Get Starlink installations by kit type"""
    try:
        # Validate kit type
        valid_kit_types = [kt.value for kt in StarlinkKitType]
        if kit_type not in valid_kit_types:
            raise HTTPException(status_code=400, detail="Invalid kit type")
        
        installations = db.query(StarlinkInstallation).filter(StarlinkInstallation.kit_type == kit_type).order_by(StarlinkInstallation.created_at.desc()).all()
        
        # Format response
        formatted_installations = []
        for installation in installations:
            formatted_installation = {
                "id": installation.id,
                "customer_name": installation.customer_name,
                "customer_phone": installation.customer_phone,
                "installation_address": installation.installation_address,
                "kit_type": installation.kit_type,
                "installation_date": installation.installation_date.isoformat() if installation.installation_date else None,
                "technician_name": installation.technician_name,
                "installation_status": installation.installation_status,
                "service_status": installation.service_status,
                "total_cost": installation.total_cost,
                "created_at": installation.created_at.isoformat() if installation.created_at else None
            }
            formatted_installations.append(formatted_installation)
        
        return {
            "kit_type": kit_type,
            "total_installations": len(installations),
            "installations": formatted_installations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get Starlink by kit type error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve Starlink installations by kit type: {str(e)}")

@app.get("/api/starlink/status/{status}")
def get_starlink_by_status(status: str, db: Session = Depends(get_db)):
    """Get Starlink installations by installation status"""
    try:
        # Validate status
        valid_statuses = [s.value for s in StarlinkInstallationStatus]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid installation status")
        
        installations = db.query(StarlinkInstallation).filter(StarlinkInstallation.installation_status == status).order_by(StarlinkInstallation.created_at.desc()).all()
        
        # Format response
        formatted_installations = []
        for installation in installations:
            formatted_installation = {
                "id": installation.id,
                "customer_name": installation.customer_name,
                "installation_address": installation.installation_address,
                "kit_type": installation.kit_type,
                "installation_date": installation.installation_date.isoformat() if installation.installation_date else None,
                "technician_name": installation.technician_name,
                "installation_status": installation.installation_status,
                "service_status": installation.service_status,
                "created_at": installation.created_at.isoformat() if installation.created_at else None
            }
            formatted_installations.append(formatted_installation)
        
        return {
            "status": status,
            "total_installations": len(installations),
            "installations": formatted_installations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get Starlink by status error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve Starlink installations by status: {str(e)}")

@app.get("/api/starlink/summary")
def get_starlink_summary(db: Session = Depends(get_db)):
    """Get Starlink installation statistics and summary"""
    try:
        # Total installations
        total_installations = db.query(StarlinkInstallation).count()
        
        # Installations by kit type
        kit_type_counts = {}
        for kit_type in StarlinkKitType:
            count = db.query(StarlinkInstallation).filter(StarlinkInstallation.kit_type == kit_type.value).count()
            kit_type_counts[kit_type.value] = count
        
        # Installations by installation status
        installation_status_counts = {}
        for status in StarlinkInstallationStatus:
            count = db.query(StarlinkInstallation).filter(StarlinkInstallation.installation_status == status.value).count()
            installation_status_counts[status.value] = count
        
        # Installations by service status
        service_status_counts = {}
        for status in StarlinkServiceStatus:
            count = db.query(StarlinkInstallation).filter(StarlinkInstallation.service_status == status.value).count()
            service_status_counts[status.value] = count
        
        # Financial statistics
        from sqlalchemy import func
        financial_stats = db.query(
            func.sum(StarlinkInstallation.installation_fee).label('total_installation_fees'),
            func.sum(StarlinkInstallation.equipment_cost).label('total_equipment_cost'),
            func.sum(StarlinkInstallation.total_cost).label('total_revenue'),
            func.avg(StarlinkInstallation.monthly_fee).label('avg_monthly_fee'),
            func.avg(StarlinkInstallation.total_cost).label('avg_installation_cost')
        ).first()
        
        # Active services (monthly revenue potential)
        active_services = db.query(StarlinkInstallation).filter(StarlinkInstallation.service_status == "active").count()
        monthly_revenue_potential = db.query(func.sum(StarlinkInstallation.monthly_fee)).filter(
            StarlinkInstallation.service_status == "active"
        ).scalar() or 0
        
        # Recent installations
        recent_installations = db.query(StarlinkInstallation).order_by(StarlinkInstallation.created_at.desc()).limit(5).all()
        
        # Upcoming installations (scheduled for future)
        upcoming_installations = db.query(StarlinkInstallation).filter(
            StarlinkInstallation.installation_date > datetime.utcnow(),
            StarlinkInstallation.installation_status == "scheduled"
        ).count()
        
        return {
            "total_installations": total_installations,
            "kit_type_counts": kit_type_counts,
            "installation_status_counts": installation_status_counts,
            "service_status_counts": service_status_counts,
            "financial_statistics": {
                "total_installation_fees": float(financial_stats.total_installation_fees) if financial_stats.total_installation_fees else 0,
                "total_equipment_cost": float(financial_stats.total_equipment_cost) if financial_stats.total_equipment_cost else 0,
                "total_revenue": float(financial_stats.total_revenue) if financial_stats.total_revenue else 0,
                "avg_monthly_fee": float(financial_stats.avg_monthly_fee) if financial_stats.avg_monthly_fee else 0,
                "avg_installation_cost": float(financial_stats.avg_installation_cost) if financial_stats.avg_installation_cost else 0,
                "monthly_revenue_potential": float(monthly_revenue_potential)
            },
            "active_services": active_services,
            "recent_installations": len(recent_installations),
            "upcoming_installations": upcoming_installations
        }
    except Exception as e:
        logger.error(f"Get Starlink summary error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve Starlink summary: {str(e)}")

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