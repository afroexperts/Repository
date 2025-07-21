from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from datetime import datetime

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

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "Afro Experts API is running", "timestamp": datetime.utcnow()}

# Contact Management Endpoints
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
async def get_contact_submissions(limit: int = 100, skip: int = 0):
    """Get contact submissions (admin endpoint)"""
    try:
        return await DatabaseManager.get_contact_submissions(limit=limit, skip=skip)
    except Exception as e:
        logger.error(f"Error fetching contact submissions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch contact submissions"
        )

# Quote Request Endpoints
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
async def get_quote_requests(limit: int = 100, skip: int = 0):
    """Get quote requests (admin endpoint)"""
    try:
        return await DatabaseManager.get_quote_requests(limit=limit, skip=skip)
    except Exception as e:
        logger.error(f"Error fetching quote requests: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch quote requests"
        )

# Service Inquiry Endpoints
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
async def get_service_inquiries(limit: int = 100, skip: int = 0):
    """Get service inquiries (admin endpoint)"""
    try:
        return await DatabaseManager.get_service_inquiries(limit=limit, skip=skip)
    except Exception as e:
        logger.error(f"Error fetching service inquiries: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch service inquiries"
        )

# Newsletter Endpoints
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

# Content Endpoints
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

# Admin/Analytics Endpoints
@api_router.get("/admin/stats")
async def get_admin_stats():
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
async def update_impact_stats(stats: dict):
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