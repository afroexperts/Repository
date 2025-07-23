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
        user_id = "1502c12e-6750-11f0-adbc-46c85275ff51"  # Use the actual admin user ID
        
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
        user_id = "1502c12e-6750-11f0-adbc-46c85275ff51"
        
        # Generate transaction number
        transaction_count = db.query(FinancialTransaction).count()
        transaction_number = f"TXN-{datetime.utcnow().strftime('%Y%m%d')}-{transaction_count + 1:04d}"
        
        db_transaction = FinancialTransaction(
            transaction_number=transaction_number,
            transaction_type=TransactionType(transaction_data.transaction_type),
            category=transaction_data.category,
            description=transaction_data.description,
            amount=transaction_data.amount,
            reference_id=transaction_data.reference_id,
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
def create_service_booking(booking_data: dict, db: Session = Depends(get_db)):
    """Create service booking"""
    try:
        db_booking = ServiceBooking(
            booking_number=f"SRV-{str(uuid.uuid4())[:8]}",
            client_name=booking_data['client_name'],
            client_email=booking_data.get('client_email'),
            client_phone=booking_data['client_phone'],
            service_type=ServiceType(booking_data['service_type']),
            description=booking_data['description'],
            location=booking_data['location'],
            preferred_date=datetime.fromisoformat(booking_data['preferred_date'].replace('Z', '+00:00')) if booking_data.get('preferred_date') else None,
            status='pending'
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
                "updated_at": transaction.updated_at.isoformat() if transaction.updated_at else None,
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
        
        transaction.updated_at = datetime.utcnow()
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
        # Monthly income/expense trends
        monthly_income = db.query(
            func.date_trunc('month', FinancialTransaction.created_at).label('month'),
            func.sum(FinancialTransaction.amount).label('total')
        ).filter(
            FinancialTransaction.transaction_type == TransactionType.income
        ).group_by(
            func.date_trunc('month', FinancialTransaction.created_at)
        ).order_by('month').all()
        
        monthly_expense = db.query(
            func.date_trunc('month', FinancialTransaction.created_at).label('month'),
            func.sum(FinancialTransaction.amount).label('total')
        ).filter(
            FinancialTransaction.transaction_type == TransactionType.expense
        ).group_by(
            func.date_trunc('month', FinancialTransaction.created_at)
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