from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import List, Optional
import os
from models import *
import logging

logger = logging.getLogger(__name__)

# Database connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Collections
contact_collection = db.contact_submissions
quote_collection = db.quote_requests  
service_inquiry_collection = db.service_inquiries
newsletter_collection = db.newsletter_subscriptions
impact_stats_collection = db.impact_stats
testimonial_collection = db.testimonials

# Service names mapping
SERVICE_NAMES = {
    1: "Network Setup & Maintenance",
    2: "CCTV & Access Control", 
    3: "Server Installation",
    4: "Technical Support"
}

class DatabaseManager:
    
    # Contact Submissions
    @staticmethod
    async def create_contact_submission(submission_data: ContactSubmissionCreate) -> str:
        """Create a new contact submission"""
        submission = ContactSubmission(**submission_data.dict())
        result = await contact_collection.insert_one(submission.dict())
        logger.info(f"Contact submission created: {result.inserted_id}")
        return submission.id

    @staticmethod
    async def get_contact_submissions(limit: int = 100, skip: int = 0) -> List[ContactSubmission]:
        """Get contact submissions with pagination"""
        cursor = contact_collection.find().sort("created_at", -1).skip(skip).limit(limit)
        submissions = await cursor.to_list(length=limit)
        return [ContactSubmission(**sub) for sub in submissions]

    # Quote Requests
    @staticmethod
    async def create_quote_request(quote_data: QuoteRequestCreate) -> str:
        """Create a new quote request"""
        quote = QuoteRequest(**quote_data.dict())
        result = await quote_collection.insert_one(quote.dict())
        logger.info(f"Quote request created: {result.inserted_id}")
        return quote.id

    @staticmethod
    async def get_quote_requests(limit: int = 100, skip: int = 0) -> List[QuoteRequest]:
        """Get quote requests with pagination"""
        cursor = quote_collection.find().sort("created_at", -1).skip(skip).limit(limit)
        quotes = await cursor.to_list(length=limit)
        return [QuoteRequest(**quote) for quote in quotes]

    # Service Inquiries
    @staticmethod
    async def create_service_inquiry(inquiry_data: ServiceInquiryCreate) -> str:
        """Create a new service inquiry"""
        # Add service name based on service_id
        service_name = SERVICE_NAMES.get(inquiry_data.service_id, "Unknown Service")
        
        inquiry_dict = inquiry_data.dict()
        inquiry_dict["service_name"] = service_name
        
        inquiry = ServiceInquiry(**inquiry_dict)
        result = await service_inquiry_collection.insert_one(inquiry.dict())
        logger.info(f"Service inquiry created: {result.inserted_id}")
        return inquiry.id

    @staticmethod
    async def get_service_inquiries(limit: int = 100, skip: int = 0) -> List[ServiceInquiry]:
        """Get service inquiries with pagination"""
        cursor = service_inquiry_collection.find().sort("created_at", -1).skip(skip).limit(limit)
        inquiries = await cursor.to_list(length=limit)
        return [ServiceInquiry(**inquiry) for inquiry in inquiries]

    # Newsletter Subscriptions
    @staticmethod
    async def create_newsletter_subscription(subscription_data: NewsletterSubscriptionCreate) -> str:
        """Create a new newsletter subscription"""
        # Check if email already exists
        existing = await newsletter_collection.find_one({"email": subscription_data.email})
        if existing:
            # Update existing subscription
            await newsletter_collection.update_one(
                {"email": subscription_data.email},
                {"$set": {
                    "interests": subscription_data.interests,
                    "country": subscription_data.country,
                    "status": "active",
                    "subscribed_at": datetime.utcnow()
                }}
            )
            logger.info(f"Newsletter subscription updated: {subscription_data.email}")
            return existing.get("id", "updated")
        else:
            # Create new subscription
            subscription = NewsletterSubscription(**subscription_data.dict())
            result = await newsletter_collection.insert_one(subscription.dict())
            logger.info(f"Newsletter subscription created: {result.inserted_id}")
            return subscription.id

    # Impact Stats
    @staticmethod
    async def get_latest_impact_stats() -> Optional[ImpactStatsResponse]:
        """Get the latest impact statistics"""
        stats = await impact_stats_collection.find_one(
            sort=[("date", -1)]
        )
        
        if stats:
            return ImpactStatsResponse(
                communities_connected=stats["communities_connected"],
                businesses_served=stats["businesses_served"],
                people_online=stats["people_online"],
                countries_active=stats["countries_active"],
                last_updated=stats["created_at"]
            )
        
        # Return default stats if none exist
        return ImpactStatsResponse(
            communities_connected=50,
            businesses_served=1000,
            people_online=10000,
            countries_active=2,
            last_updated=datetime.utcnow()
        )

    @staticmethod
    async def update_impact_stats(stats_data: dict) -> str:
        """Update impact statistics for today"""
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Try to update existing stats for today
        result = await impact_stats_collection.update_one(
            {"date": today},
            {"$set": {**stats_data, "created_at": datetime.utcnow()}},
            upsert=True
        )
        
        logger.info(f"Impact stats updated for {today}")
        return str(result.upserted_id) if result.upserted_id else "updated"

    # Testimonials
    @staticmethod
    async def get_active_testimonials() -> List[Testimonial]:
        """Get active testimonials"""
        cursor = testimonial_collection.find(
            {"active": True}
        ).sort("date_added", -1).limit(10)
        
        testimonials = await cursor.to_list(length=10)
        
        if not testimonials:
            # Return default testimonials if none exist
            return [
                Testimonial(
                    name="Marie Uwimana",
                    title="School Principal",
                    location="Kigali, Rwanda",
                    message="Afro Experts transformed our school with reliable internet. Now our students can access online resources and prepare for the digital future.",
                    rating=5,
                    verified=True
                ),
                Testimonial(
                    name="Jean Baptiste",
                    title="Business Owner", 
                    location="Bangui, CAR",
                    message="The Starlink installation was seamless. Our business now operates efficiently with cloud-based systems and international communication.",
                    rating=5,
                    verified=True
                )
            ]
        
        return [Testimonial(**testimonial) for testimonial in testimonials]

    @staticmethod
    async def create_testimonial(testimonial_data: TestimonialCreate) -> str:
        """Create a new testimonial"""
        testimonial = Testimonial(**testimonial_data.dict())
        result = await testimonial_collection.insert_one(testimonial.dict())
        logger.info(f"Testimonial created: {result.inserted_id}")
        return testimonial.id

    # Analytics
    @staticmethod
    async def get_submission_stats() -> dict:
        """Get basic analytics about submissions"""
        contact_count = await contact_collection.count_documents({})
        quote_count = await quote_collection.count_documents({})
        service_count = await service_inquiry_collection.count_documents({})
        newsletter_count = await newsletter_collection.count_documents({"status": "active"})
        
        return {
            "total_contacts": contact_count,
            "total_quotes": quote_count,
            "total_service_inquiries": service_count,
            "newsletter_subscribers": newsletter_count
        }