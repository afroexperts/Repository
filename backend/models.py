from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid
import hashlib

# Enums
class CountryEnum(str, Enum):
    rwanda = "rwanda"
    car = "car"
    other = "other"

class ContactStatus(str, Enum):
    new = "new"
    contacted = "contacted"
    converted = "converted"
    closed = "closed"

class QuoteStatus(str, Enum):
    pending = "pending"
    quoted = "quoted"
    accepted = "accepted"
    rejected = "rejected"

class ServiceInquiryStatus(str, Enum):
    new = "new"
    reviewing = "reviewing"
    quoted = "quoted"
    closed = "closed"

class SubscriptionStatus(str, Enum):
    active = "active"
    unsubscribed = "unsubscribed"

class Timeline(str, Enum):
    asap = "asap"
    one_month = "1month"
    three_months = "3months"
    six_months = "6months"

class ServiceType(str, Enum):
    starlink = "starlink"
    network = "network"
    software = "software"
    other = "other"

class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    cashier = "cashier"
    inventory_officer = "inventory_officer"
    technician = "technician"

class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"

class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class PaymentMethod(str, Enum):
    cash = "cash"
    card = "card"
    mobile_money = "mobile_money"
    bank_transfer = "bank_transfer"
    afro_payi = "afro_payi"

# User Authentication Models
class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=50)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    full_name: str
    email: EmailStr
    password_hash: str
    role: UserRole
    status: UserStatus = UserStatus.active
    phone: Optional[str]
    department: Optional[str]
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def verify_password(self, password: str) -> bool:
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    class Config:
        use_enum_values = True

# Product Models
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    cost_price: Optional[float] = Field(None, ge=0)
    sku: Optional[str] = Field(None, max_length=50)
    unit: str = Field(default="pieces")
    minimum_stock: int = Field(default=0, ge=0)
    current_stock: int = Field(default=0, ge=0)
    location: Optional[str] = Field(None, max_length=100)

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    category: str
    description: Optional[str]
    price: float
    cost_price: Optional[float]
    sku: Optional[str]
    unit: str
    minimum_stock: int
    current_stock: int
    location: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

# Order Models
class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)

class OrderItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float

class OrderCreate(BaseModel):
    client_name: str = Field(..., min_length=1, max_length=100)
    client_email: Optional[EmailStr] = None
    client_phone: Optional[str] = Field(None, max_length=20)
    items: List[OrderItemCreate]
    payment_method: PaymentMethod
    notes: Optional[str] = Field(None, max_length=500)

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_number: str
    client_name: str
    client_email: Optional[EmailStr]
    client_phone: Optional[str]
    items: List[OrderItem]
    subtotal: float
    tax_amount: float
    total_amount: float
    payment_method: PaymentMethod
    status: OrderStatus = OrderStatus.pending
    notes: Optional[str]
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        use_enum_values = True

# Client Models
class ClientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=200)
    client_type: str = Field(default="individual")  # individual, business
    credit_limit: float = Field(default=0, ge=0)

class Client(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: Optional[EmailStr]
    phone: Optional[str]
    company: Optional[str]
    address: Optional[str]
    client_type: str
    credit_limit: float
    current_balance: float = Field(default=0)
    total_orders: int = Field(default=0)
    total_spent: float = Field(default=0)
    last_order_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Existing models (keeping all previous models)
class ContactSubmissionCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    country: CountryEnum
    service: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=10, max_length=2000)
    source: str = Field(default="contact_form")

class QuoteRequestCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=100)
    service_type: ServiceType
    message: Optional[str] = Field(None, max_length=1000)
    urgent: bool = Field(default=False)

class ServiceInquiryCreate(BaseModel):
    service_id: int = Field(..., ge=1, le=4)
    contact_name: str = Field(..., min_length=2, max_length=100)
    contact_email: EmailStr
    contact_phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=100)
    project_details: str = Field(..., min_length=10, max_length=2000)
    timeline: Timeline

class NewsletterSubscriptionCreate(BaseModel):
    email: EmailStr
    interests: Optional[List[str]] = Field(default=[])
    country: Optional[str] = Field(None, max_length=50)

class TestimonialCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    title: str = Field(..., min_length=2, max_length=150)
    location: str = Field(..., min_length=2, max_length=100)
    message: str = Field(..., min_length=10, max_length=1000)
    rating: int = Field(..., ge=1, le=5)
    image_url: Optional[str] = None

# Response Models (keeping all existing ones and adding new)
class ContactSubmission(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: Optional[str]
    country: CountryEnum
    service: str
    message: str
    source: str
    status: ContactStatus = ContactStatus.new
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    assigned_to: Optional[str] = None

    class Config:
        use_enum_values = True

class QuoteRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: Optional[str]
    company: Optional[str]
    service_type: ServiceType
    message: Optional[str]
    urgent: bool
    status: QuoteStatus = QuoteStatus.pending
    quote_amount: Optional[float] = None
    quote_details: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        use_enum_values = True

class ServiceInquiry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    service_id: int
    service_name: str
    contact_name: str
    contact_email: EmailStr
    contact_phone: Optional[str]
    company: Optional[str]
    project_details: str
    timeline: Timeline
    status: ServiceInquiryStatus = ServiceInquiryStatus.new
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        use_enum_values = True

class NewsletterSubscription(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    interests: List[str]
    country: Optional[str]
    status: SubscriptionStatus = SubscriptionStatus.active
    subscribed_at: datetime = Field(default_factory=datetime.utcnow)
    unsubscribed_at: Optional[datetime] = None

    class Config:
        use_enum_values = True

class ImpactStats(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    communities_connected: int
    businesses_served: int
    people_online: int
    countries_active: int
    date: datetime = Field(default_factory=lambda: datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0))
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Testimonial(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    title: str
    location: str
    message: str
    rating: int = Field(..., ge=1, le=5)
    verified: bool = False
    active: bool = True
    date_added: datetime = Field(default_factory=datetime.utcnow)
    image_url: Optional[str] = None

# Standard API Response Models
class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    id: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str
    details: Optional[dict] = None

class ImpactStatsResponse(BaseModel):
    communities_connected: int
    businesses_served: int
    people_online: int
    countries_active: int
    last_updated: datetime

class TestimonialsResponse(BaseModel):
    testimonials: List[Testimonial]

class LoginResponse(BaseModel):
    success: bool = True
    message: str
    user: User
    token: Optional[str] = None

class DashboardStatsResponse(BaseModel):
    total_sales: float
    monthly_growth: float
    active_orders: int
    low_stock_items: int
    total_clients: int
    pending_quotes: int