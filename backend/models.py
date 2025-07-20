from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid

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

# Request Models
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

# Response Models
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