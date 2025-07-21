from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Import models and database manager
from models import *
from database import DatabaseManager, initialize_database

# Initialize database after loading environment variables
initialize_database()

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="Afro Experts API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[User]:
    """Get current authenticated user (simplified for demo)"""
    if not credentials:
        return None
    
    # In a real app, you would verify JWT token here
    # For demo, we'll use a simple token format: "user_id"
    try:
        user_id = credentials.credentials
        user = await DatabaseManager.get_user_by_id(user_id)
        return user
    except:
        return None

def require_auth(user: User = Depends(get_current_user)):
    """Require authentication"""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user

def require_role(required_roles: List[str]):
    """Require specific roles"""
    def role_checker(user: User = Depends(require_auth)):
        if user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return role_checker

# Initialize default data on startup
@app.on_event("startup")
async def startup_event():
    try:
        await DatabaseManager.initialize_default_data()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "Afro Experts API is running", "timestamp": datetime.utcnow()}

# Authentication Endpoints
@api_router.post("/auth/login", response_model=LoginResponse)
async def login(login_data: UserLogin):
    """User login"""
    try:
        user = await DatabaseManager.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # In a real app, generate JWT token here
        # For demo, we'll use user ID as token
        token = user.id
        
        return LoginResponse(
            message="Login successful",
            user=user,
            token=token
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@api_router.get("/auth/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(require_auth)):
    """Get current user information"""
    return current_user

# Dashboard Endpoints
@api_router.get("/dashboard/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(current_user: User = Depends(require_auth)):
    """Get dashboard statistics"""
    try:
        stats = await DatabaseManager.get_dashboard_stats()
        return DashboardStatsResponse(**stats)
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch dashboard statistics"
        )

@api_router.get("/dashboard/recent-transactions")
async def get_recent_transactions(
    limit: int = 10,
    current_user: User = Depends(require_auth)
):
    """Get recent transactions for dashboard"""
    try:
        orders = await DatabaseManager.get_orders(limit=limit)
        transactions = []
        
        for order in orders:
            transaction = {
                "id": order.id,
                "type": "Sale",
                "client": order.client_name,
                "amount": order.total_amount,
                "product": f"{len(order.items)} items",
                "status": order.status.title(),
                "created_at": order.created_at
            }
            transactions.append(transaction)
        
        return {"transactions": transactions}
    except Exception as e:
        logger.error(f"Error fetching recent transactions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recent transactions"
        )

# Product Management Endpoints
@api_router.post("/products", response_model=SuccessResponse)
async def create_product(
    product: ProductCreate, 
    current_user: User = Depends(require_role(["admin", "manager", "inventory_officer"]))
):
    """Create a new product"""
    try:
        product_id = await DatabaseManager.create_product(product)
        return SuccessResponse(
            message="Product created successfully",
            id=product_id
        )
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product"
        )

@api_router.get("/products", response_model=List[Product])
async def get_products(
    category: Optional[str] = None,
    limit: int = 100,
    skip: int = 0,
    current_user: User = Depends(require_auth)
):
    """Get products"""
    try:
        products = await DatabaseManager.get_products(category=category, limit=limit, skip=skip)
        return products
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch products"
        )

@api_router.get("/products/low-stock", response_model=List[Product])
async def get_low_stock_products(current_user: User = Depends(require_auth)):
    """Get products with low stock"""
    try:
        products = await DatabaseManager.get_low_stock_products()
        return products
    except Exception as e:
        logger.error(f"Error fetching low stock products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch low stock products"
        )

@api_router.put("/products/{product_id}/stock")
async def update_product_stock(
    product_id: str,
    new_stock: int,
    current_user: User = Depends(require_role(["admin", "manager", "inventory_officer"]))
):
    """Update product stock"""
    try:
        success = await DatabaseManager.update_product_stock(product_id, new_stock)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return SuccessResponse(message="Stock updated successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product stock: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product stock"
        )

# Order Management Endpoints
@api_router.post("/orders", response_model=SuccessResponse)
async def create_order(
    order: OrderCreate,
    current_user: User = Depends(require_role(["admin", "manager", "cashier"]))
):
    """Create a new order"""
    try:
        order_id = await DatabaseManager.create_order(order, current_user.id)
        return SuccessResponse(
            message="Order created successfully",
            id=order_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )

@api_router.get("/orders", response_model=List[Order])
async def get_orders(
    status: Optional[str] = None,
    limit: int = 100,
    skip: int = 0,
    current_user: User = Depends(require_auth)
):
    """Get orders"""
    try:
        orders = await DatabaseManager.get_orders(status=status, limit=limit, skip=skip)
        return orders
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch orders"
        )

# Client Management Endpoints
@api_router.post("/clients", response_model=SuccessResponse)
async def create_client(
    client: ClientCreate,
    current_user: User = Depends(require_role(["admin", "manager", "cashier"]))
):
    """Create a new client"""
    try:
        client_id = await DatabaseManager.create_client(client)
        return SuccessResponse(
            message="Client created successfully",
            id=client_id
        )
    except Exception as e:
        logger.error(f"Error creating client: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create client"
        )

@api_router.get("/clients", response_model=List[Client])
async def get_clients(
    limit: int = 100,
    skip: int = 0,
    current_user: User = Depends(require_auth)
):
    """Get clients"""
    try:
        clients = await DatabaseManager.get_clients(limit=limit, skip=skip)
        return clients
    except Exception as e:
        logger.error(f"Error fetching clients: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch clients"
        )

# User Management Endpoints (Admin only)
@api_router.post("/users", response_model=SuccessResponse)
async def create_user(
    user: UserCreate,
    current_user: User = Depends(require_role(["admin"]))
):
    """Create a new user (Admin only)"""
    try:
        user_id = await DatabaseManager.create_user(user)
        return SuccessResponse(
            message="User created successfully",
            id=user_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

# Contact Management Endpoints (existing)
@api_router.post("/contact/submit", response_model=SuccessResponse)
async def submit_contact_form(submission: ContactSubmissionCreate):
    """Handle contact form submissions"""
    try:
        submission_id = await DatabaseManager.create_contact_submission(submission)
        return SuccessResponse(
            message="Message sent successfully! We'll get back to you within 24 hours.",
            id=submission_id
        )
    except Exception as e:
        logger.error(f"Error creating contact submission: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit contact form. Please try again."
        )

@api_router.get("/contact/submissions", response_model=List[ContactSubmission])
async def get_contact_submissions(
    limit: int = 100, 
    skip: int = 0,
    current_user: User = Depends(require_role(["admin", "manager"]))
):
    """Get contact submissions (admin endpoint)"""
    try:
        return await DatabaseManager.get_contact_submissions(limit=limit, skip=skip)
    except Exception as e:
        logger.error(f"Error fetching contact submissions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch contact submissions"
        )

# Quote Request Endpoints (existing)
@api_router.post("/quote/request", response_model=SuccessResponse)
async def request_quote(quote_request: QuoteRequestCreate):
    """Handle quote requests"""
    try:
        quote_id = await DatabaseManager.create_quote_request(quote_request)
        return SuccessResponse(
            message="Quote request submitted successfully! Our team will contact you soon.",
            id=quote_id
        )
    except Exception as e:
        logger.error(f"Error creating quote request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit quote request. Please try again."
        )

@api_router.get("/quote/requests", response_model=List[QuoteRequest])
async def get_quote_requests(
    limit: int = 100, 
    skip: int = 0,
    current_user: User = Depends(require_role(["admin", "manager"]))
):
    """Get quote requests (admin endpoint)"""
    try:
        return await DatabaseManager.get_quote_requests(limit=limit, skip=skip)
    except Exception as e:
        logger.error(f"Error fetching quote requests: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch quote requests"
        )

# Service Inquiry Endpoints (existing)
@api_router.post("/services/inquiry", response_model=SuccessResponse)
async def submit_service_inquiry(inquiry: ServiceInquiryCreate):
    """Handle service-specific inquiries"""
    try:
        inquiry_id = await DatabaseManager.create_service_inquiry(inquiry)
        return SuccessResponse(
            message="Service inquiry submitted successfully! Our experts will review your requirements and get back to you.",
            id=inquiry_id
        )
    except Exception as e:
        logger.error(f"Error creating service inquiry: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit service inquiry. Please try again."
        )

@api_router.get("/services/inquiries", response_model=List[ServiceInquiry])
async def get_service_inquiries(
    limit: int = 100, 
    skip: int = 0,
    current_user: User = Depends(require_role(["admin", "manager"]))
):
    """Get service inquiries (admin endpoint)"""
    try:
        return await DatabaseManager.get_service_inquiries(limit=limit, skip=skip)
    except Exception as e:
        logger.error(f"Error fetching service inquiries: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch service inquiries"
        )

# Newsletter Endpoints (existing)
@api_router.post("/newsletter/subscribe", response_model=SuccessResponse)
async def subscribe_newsletter(subscription: NewsletterSubscriptionCreate):
    """Handle newsletter subscriptions"""
    try:
        subscription_id = await DatabaseManager.create_newsletter_subscription(subscription)
        return SuccessResponse(
            message="Successfully subscribed to our newsletter! Stay updated with the latest from Afro Experts.",
            id=subscription_id
        )
    except Exception as e:
        logger.error(f"Error creating newsletter subscription: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to subscribe to newsletter. Please try again."
        )

# Content Endpoints (existing)
@api_router.get("/stats/impact", response_model=ImpactStatsResponse)
async def get_impact_stats():
    """Get impact statistics for homepage"""
    try:
        stats = await DatabaseManager.get_latest_impact_stats()
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Impact statistics not found"
            )
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching impact stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch impact statistics"
        )

@api_router.get("/content/testimonials", response_model=TestimonialsResponse)
async def get_testimonials():
    """Get testimonials for homepage"""
    try:
        testimonials = await DatabaseManager.get_active_testimonials()
        return TestimonialsResponse(testimonials=testimonials)
    except Exception as e:
        logger.error(f"Error fetching testimonials: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch testimonials"
        )

# Admin/Analytics Endpoints (existing)
@api_router.get("/admin/stats")
async def get_admin_stats(current_user: User = Depends(require_role(["admin", "manager"]))):
    """Get basic analytics for admin dashboard"""
    try:
        stats = await DatabaseManager.get_submission_stats()
        return {
            "success": True,
            "data": stats,
            "last_updated": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Error fetching admin stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch admin statistics"
        )

# Update impact stats (admin endpoint)
@api_router.post("/admin/impact/update")
async def update_impact_stats(
    stats: dict,
    current_user: User = Depends(require_role(["admin"]))
):
    """Update impact statistics"""
    try:
        required_fields = ["communities_connected", "businesses_served", "people_online", "countries_active"]
        for field in required_fields:
            if field not in stats:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}"
                )
        
        stats_id = await DatabaseManager.update_impact_stats(stats)
        return SuccessResponse(
            message="Impact statistics updated successfully",
            id=stats_id
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating impact stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update impact statistics"
        )

# Include the router in the main app
app.include_router(api_router)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()