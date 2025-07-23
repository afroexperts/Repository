from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Float, Integer, Text, Enum, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from typing import Optional, List, Any
import uuid
import enum
import os
import hashlib

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql://erp_user:ErpPassword2025!@localhost/afroexperts_erp")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Enums
class CountryEnum(enum.Enum):
    rwanda = "rwanda"
    car = "car"
    other = "other"

class ContactStatus(enum.Enum):
    new = "new"
    contacted = "contacted"
    converted = "converted"
    closed = "closed"

class UserRole(enum.Enum):
    admin = "admin"
    manager = "manager"
    cashier = "cashier"
    inventory_officer = "inventory_officer"
    technician = "technician"

class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"

class OrderStatus(enum.Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class PaymentMethod(enum.Enum):
    cash = "cash"
    card = "card"
    mobile_money = "mobile_money"
    bank_transfer = "bank_transfer"
    afropay = "afropay"

class ServiceType(enum.Enum):
    it_support = "it_support"
    network_installation = "network_installation"
    starlink_installation = "starlink_installation"
    software_development = "software_development"
    logistics_support = "logistics_support"
    consultation = "consultation"
    maintenance = "maintenance"
    training = "training"

class MovementType(enum.Enum):
    stock_in = "stock_in"
    stock_out = "stock_out"
    adjustment = "adjustment"
    damaged = "damaged"
    returned = "returned"

class TransactionType(enum.Enum):
    income = "income"
    expense = "expense"

class InvoiceStatus(enum.Enum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    partially_paid = "partially_paid"
    overdue = "overdue"
    cancelled = "cancelled"

class InvoiceType(enum.Enum):
    manual = "manual"
    pos_sale = "pos_sale"
    service_booking = "service_booking"
    rental = "rental"
    logistics = "logistics"

class PaymentStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"

class PortfolioCategory(enum.Enum):
    digital_platforms = "Digital Platforms"
    business_solutions = "Business Solutions"
    network_solutions = "Network Solutions"
    security_solutions = "Security Solutions"
    connectivity_solutions = "Connectivity Solutions"
    media_events = "Media & Events"
    manufacturing = "Manufacturing"

class PortfolioStatus(enum.Enum):
    live = "Live"
    active = "Active"
    completed = "Completed"
    operating = "Operating"
    in_progress = "In Progress"

class Currency(enum.Enum):
    rwf = "RWF"
    usd = "USD"
    eur = "EUR"

# SQLAlchemy Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.active)
    phone = Column(String(20), nullable=True)
    department = Column(String(50), nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    def verify_password(self, password: str) -> bool:
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=True)
    sku = Column(String(50), nullable=True, unique=True)
    unit = Column(String(20), default="pieces")
    minimum_stock = Column(Integer, default=0)
    current_stock = Column(Integer, default=0)
    location = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="product")
    inventory_movements = relationship("InventoryMovement", back_populates="product")

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    client_type = Column(String(20), default="individual")  # individual, business
    company_name = Column(String(200), nullable=True)
    tax_number = Column(String(50), nullable=True)
    credit_limit = Column(Float, default=0.0)
    current_balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    orders = relationship("Order", back_populates="client")
    invoices = relationship("Invoice", back_populates="client")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_number = Column(String(50), unique=True, nullable=False)
    client_id = Column(CHAR(36), ForeignKey('clients.id'), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    subtotal = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    payment_method = Column(Enum(PaymentMethod), nullable=True)
    payment_status = Column(String(20), default="pending")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    client = relationship("Client", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(CHAR(36), ForeignKey('orders.id'), nullable=False)
    product_id = Column(CHAR(36), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class InventoryMovement(Base):
    __tablename__ = "inventory_movements"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(CHAR(36), ForeignKey('products.id'), nullable=False)
    movement_type = Column(Enum(MovementType), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)
    reference_number = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="inventory_movements")
    user = relationship("User")

class PosTransaction(Base):
    __tablename__ = "pos_transactions"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    receipt_number = Column(String(50), unique=True, nullable=False)
    client_id = Column(CHAR(36), ForeignKey('clients.id'), nullable=True)
    items = Column(JSON)  # Store as JSON for flexibility
    subtotal = Column(Float, nullable=False)
    discount_percentage = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    tax_percentage = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_received = Column(Float, nullable=False)
    change_given = Column(Float, default=0.0)
    cashier_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    client = relationship("Client")
    cashier = relationship("User")

class ServiceBooking(Base):
    __tablename__ = "service_bookings"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    booking_number = Column(String(50), unique=True, nullable=False)
    client_name = Column(String(200), nullable=False)
    client_email = Column(String(255), nullable=True)
    client_phone = Column(String(20), nullable=False)
    service_type = Column(Enum(ServiceType), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(200), nullable=False)
    preferred_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="pending")
    assigned_technician_id = Column(CHAR(36), ForeignKey('users.id'), nullable=True)
    estimated_cost = Column(Float, nullable=True)
    actual_cost = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    invoices = relationship("Invoice", back_populates="service_booking")
    technician = relationship("User")

class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_number = Column(String(50), unique=True, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    reference_id = Column(String(100), nullable=True)
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")

class WebsiteSetting(Base):
    __tablename__ = "website_settings"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    section = Column(String(100), nullable=False, unique=True)
    data = Column(JSON, nullable=False)
    updated_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User")

class ContactSubmission(Base):
    __tablename__ = "contact_submissions"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    country = Column(Enum(CountryEnum), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Enum(ContactStatus), default=ContactStatus.new)
    created_at = Column(DateTime, default=datetime.utcnow)

# Invoice Models
class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_number = Column(String(20), unique=True, nullable=False)
    invoice_type = Column(Enum(InvoiceType), nullable=False, default=InvoiceType.manual)
    client_id = Column(String(36), ForeignKey("clients.id"), nullable=True)
    client_name = Column(String(255), nullable=False)
    client_email = Column(String(255), nullable=True)
    client_phone = Column(String(20), nullable=True)
    client_address = Column(Text, nullable=True)
    
    issue_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    
    subtotal = Column(Float, nullable=False, default=0.0)
    tax_rate = Column(Float, nullable=False, default=0.18)  # 18% VAT
    tax_amount = Column(Float, nullable=False, default=0.0)
    discount_amount = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False, default=0.0)
    
    currency = Column(Enum(Currency), nullable=False, default=Currency.rwf)
    status = Column(Enum(InvoiceStatus), nullable=False, default=InvoiceStatus.draft)
    
    notes = Column(Text, nullable=True)
    terms = Column(Text, nullable=True)
    
    # Related record IDs for auto-generated invoices
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=True)
    service_booking_id = Column(String(36), ForeignKey("service_bookings.id"), nullable=True)
    
    # Recurring invoice settings
    is_recurring = Column(Boolean, default=False)
    recurring_frequency = Column(String(20), nullable=True)  # weekly, monthly, quarterly, yearly
    next_invoice_date = Column(DateTime, nullable=True)
    
    # Payment tracking
    paid_amount = Column(Float, nullable=False, default=0.0)
    balance_due = Column(Float, nullable=False, default=0.0)
    
    # Audit trail
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Email/SMS tracking
    email_sent = Column(Boolean, default=False)
    email_sent_at = Column(DateTime, nullable=True)
    sms_sent = Column(Boolean, default=False)
    sms_sent_at = Column(DateTime, nullable=True)
    reminder_count = Column(Integer, default=0)
    last_reminder_sent = Column(DateTime, nullable=True)
    
    # Relationships
    client = relationship("Client", back_populates="invoices")
    order = relationship("Order", back_populates="invoices")
    service_booking = relationship("ServiceBooking", back_populates="invoices")
    created_by_user = relationship("User")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("InvoicePayment", back_populates="invoice", cascade="all, delete-orphan")
    logs = relationship("InvoiceLog", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=False)
    
    item_type = Column(String(20), nullable=False)  # product, service, discount
    product_id = Column(String(36), ForeignKey("products.id"), nullable=True)
    
    description = Column(String(500), nullable=False)
    quantity = Column(Float, nullable=False, default=1.0)
    unit_price = Column(Float, nullable=False, default=0.0)
    line_total = Column(Float, nullable=False, default=0.0)
    
    # For weight-based items like marble dust
    weight = Column(Float, nullable=True)
    weight_unit = Column(String(10), nullable=True)  # kg, ton
    
    # For time-based services
    hours = Column(Float, nullable=True)
    hourly_rate = Column(Float, nullable=True)
    
    # Discount details
    discount_percentage = Column(Float, nullable=True)
    discount_amount = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")

class InvoicePayment(Base):
    __tablename__ = "invoice_payments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=False)
    
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    
    # Payment details
    reference_number = Column(String(100), nullable=True)
    transaction_id = Column(String(100), nullable=True)
    
    # AfroPayi integration
    afropay_transaction_id = Column(String(100), nullable=True)
    afropay_status = Column(String(20), nullable=True)
    
    notes = Column(Text, nullable=True)
    
    # Audit trail
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="payments")
    created_by_user = relationship("User")

class InvoiceLog(Base):
    __tablename__ = "invoice_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=False)
    
    action = Column(String(50), nullable=False)  # created, updated, sent, paid, cancelled
    description = Column(String(500), nullable=True)
    
    # User who performed the action
    performed_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    performed_at = Column(DateTime, default=datetime.utcnow)
    
    # Additional data (JSON format)
    log_metadata = Column(JSON, nullable=True)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="logs")
    performed_by_user = relationship("User")

class InvoiceTemplate(Base):
    __tablename__ = "invoice_templates"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    
    # Company branding
    logo_url = Column(String(500), nullable=True)
    company_name = Column(String(200), nullable=False)
    company_address = Column(Text, nullable=True)
    company_phone = Column(String(20), nullable=True)
    company_email = Column(String(255), nullable=True)
    
    # Template styling
    primary_color = Column(String(7), nullable=False, default="#0c4864")
    secondary_color = Column(String(7), nullable=False, default="#ffffff")
    font_family = Column(String(50), nullable=False, default="Helvetica")
    
    # Footer and terms
    footer_text = Column(Text, nullable=True)
    default_terms = Column(Text, nullable=True)
    
    # Settings
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PortfolioItem(Base):
    __tablename__ = "portfolio_items"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    category = Column(Enum(PortfolioCategory), nullable=False)
    description = Column(Text, nullable=False)
    image = Column(Text, nullable=False)  # Can store URL or base64 image
    technologies = Column(JSON, nullable=False, default=list)  # Store as JSON array
    client = Column(String(100), nullable=False)
    date = Column(String(10), nullable=False)  # Year or Year-Month format
    status = Column(Enum(PortfolioStatus), nullable=False)
    link = Column(String(500), nullable=True)
    results = Column(JSON, nullable=False, default=list)  # Store as JSON array
    
    # Audit fields
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    created_by_user = relationship("User")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("All tables created successfully!")