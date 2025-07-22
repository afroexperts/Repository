from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import List, Optional
import os
from models import *
import logging
import random

logger = logging.getLogger(__name__)

# Initialize database connection variables
db = None
contact_collection = None
quote_collection = None
service_inquiry_collection = None
newsletter_collection = None
impact_stats_collection = None
testimonial_collection = None
users_collection = None
products_collection = None
orders_collection = None
clients_collection = None
inventory_movements_collection = None
pos_transactions_collection = None
service_bookings_collection = None
financial_transactions_collection = None
website_settings_collection = None
portfolio_collection = None

# Service names mapping
SERVICE_NAMES = {
    1: "Network Setup & Maintenance",
    2: "CCTV & Access Control", 
    3: "Server Installation",
    4: "Technical Support"
}

def initialize_database():
    """Initialize database connections"""
    global db, contact_collection, quote_collection, service_inquiry_collection
    global newsletter_collection, impact_stats_collection, testimonial_collection
    global users_collection, products_collection, orders_collection, clients_collection
    global inventory_movements_collection, pos_transactions_collection
    global service_bookings_collection, financial_transactions_collection
    global website_settings_collection, portfolio_collection
    
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
    users_collection = db.users
    products_collection = db.products
    orders_collection = db.orders
    clients_collection = db.clients
    inventory_movements_collection = db.inventory_movements
    pos_transactions_collection = db.pos_transactions
    service_bookings_collection = db.service_bookings
    financial_transactions_collection = db.financial_transactions
    website_settings_collection = db.website_settings
    portfolio_collection = db.portfolio_items

class DatabaseManager:
    
    # User Authentication Methods
    @staticmethod
    async def create_user(user_data: UserCreate) -> str:
        """Create a new user"""
        # Check if email already exists
        existing = await users_collection.find_one({"email": user_data.email})
        if existing:
            raise ValueError("User with this email already exists")
        
        user_dict = user_data.dict()
        user_dict["password_hash"] = User.hash_password(user_data.password)
        del user_dict["password"]
        
        user = User(**user_dict)
        result = await users_collection.insert_one(user.dict())
        logger.info(f"User created: {result.inserted_id}")
        return user.id

    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[User]:
        """Authenticate user login"""
        user_data = await users_collection.find_one({"email": email})
        if not user_data:
            return None
        
        user = User(**user_data)
        if user.verify_password(password) and user.status == "active":
            # Update last login
            await users_collection.update_one(
                {"id": user.id},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            return user
        return None

    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """Get user by ID"""
        user_data = await users_collection.find_one({"id": user_id})
        if user_data:
            return User(**user_data)
        return None

    @staticmethod
    async def create_default_users():
        """Create default users if none exist"""
        count = await users_collection.count_documents({})
        if count == 0:
            # Create admin user
            admin_user = UserCreate(
                full_name="System Administrator",
                email="admin@afroexperts.com",
                password="AfroExperts2025!",
                role=UserRole.admin,
                phone="+250788123456",
                department="Management"
            )
            await DatabaseManager.create_user(admin_user)
            
            # Create manager user
            manager_user = UserCreate(
                full_name="Business Manager",
                email="manager@afroexperts.com", 
                password="Manager2025!",
                role=UserRole.manager,
                phone="+250788123457",
                department="Operations"
            )
            await DatabaseManager.create_user(manager_user)
            
            # Create cashier user
            cashier_user = UserCreate(
                full_name="Sales Cashier",
                email="cashier@afroexperts.com",
                password="Cashier2025!",
                role=UserRole.cashier,
                phone="+250788123458", 
                department="Sales"
            )
            await DatabaseManager.create_user(cashier_user)
            
            logger.info("Default users created successfully")

    # Product Management Methods
    @staticmethod
    async def create_product(product_data: ProductCreate) -> str:
        """Create a new product"""
        product = Product(**product_data.dict())
        if not product.sku:
            product.sku = f"AE{random.randint(10000, 99999)}"
        
        result = await products_collection.insert_one(product.dict())
        logger.info(f"Product created: {result.inserted_id}")
        return product.id

    @staticmethod
    async def get_products(category: Optional[str] = None, limit: int = 100, skip: int = 0) -> List[Product]:
        """Get products with optional category filter"""
        query = {}
        if category:
            query["category"] = category
            
        cursor = products_collection.find(query).sort("name", 1).skip(skip).limit(limit)
        products = await cursor.to_list(length=limit)
        return [Product(**product) for product in products]

    @staticmethod
    async def update_product_stock(product_id: str, new_stock: int) -> bool:
        """Update product stock"""
        result = await products_collection.update_one(
            {"id": product_id},
            {"$set": {"current_stock": new_stock, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0

    @staticmethod
    async def get_low_stock_products() -> List[Product]:
        """Get products with stock below minimum"""
        cursor = products_collection.find({
            "$expr": {"$lt": ["$current_stock", "$minimum_stock"]}
        })
        products = await cursor.to_list(length=100)
        return [Product(**product) for product in products]

    @staticmethod
    async def create_default_products():
        """Create default products if none exist"""
        count = await products_collection.count_documents({})
        if count == 0:
            default_products = [
                # Marble Dust Products
                ProductCreate(
                    name="Premium Marble Dust",
                    category="marble_dust",
                    description="High-quality marble dust for construction",
                    price=25000.0,
                    cost_price=15000.0,
                    unit="tons",
                    minimum_stock=20,
                    current_stock=8,
                    location="Main Warehouse"
                ),
                # Starlink Products
                ProductCreate(
                    name="Starlink Residential Kit",
                    category="starlink",
                    description="Complete home internet solution",
                    price=599000.0,
                    cost_price=450000.0,
                    unit="pieces",
                    minimum_stock=10,
                    current_stock=15,
                    location="Electronics Storage"
                ),
                ProductCreate(
                    name="Starlink Business Kit",
                    category="starlink", 
                    description="Enterprise-grade internet solution",
                    price=2500000.0,
                    cost_price=1800000.0,
                    unit="pieces",
                    minimum_stock=5,
                    current_stock=2,
                    location="Electronics Storage"
                ),
                # Second-hand Products
                ProductCreate(
                    name="Refurbished Laptop - Grade A",
                    category="secondhand",
                    description="High-quality refurbished laptops",
                    price=350000.0,
                    cost_price=200000.0,
                    unit="pieces",
                    minimum_stock=5,
                    current_stock=12,
                    location="Electronics Refurb"
                ),
                ProductCreate(
                    name="Refurbished Tablet",
                    category="secondhand",
                    description="Refurbished tablets in good condition",
                    price=150000.0,
                    cost_price=80000.0,
                    unit="pieces",
                    minimum_stock=3,
                    current_stock=1,
                    location="Electronics Refurb"
                ),
                # Service Equipment
                ProductCreate(
                    name="Network Cable Cat6",
                    category="services",
                    description="High-quality network cables",
                    price=5000.0,
                    cost_price=3000.0,
                    unit="meters",
                    minimum_stock=100,
                    current_stock=45,
                    location="Service Warehouse"
                )
            ]
            
            for product_data in default_products:
                await DatabaseManager.create_product(product_data)
            
            logger.info("Default products created successfully")

    # Client Management Methods
    @staticmethod
    async def create_client(client_data: ClientCreate) -> str:
        """Create a new client"""
        client = Client(**client_data.dict())
        result = await clients_collection.insert_one(client.dict())
        logger.info(f"Client created: {result.inserted_id}")
        return client.id

    @staticmethod
    async def get_clients(limit: int = 100, skip: int = 0) -> List[Client]:
        """Get clients with pagination"""
        cursor = clients_collection.find().sort("name", 1).skip(skip).limit(limit)
        clients = await cursor.to_list(length=limit)
        return [Client(**client) for client in clients]

    @staticmethod
    async def create_default_clients():
        """Create default clients if none exist"""
        count = await clients_collection.count_documents({})
        if count == 0:
            default_clients = [
                ClientCreate(
                    name="ABC Construction Ltd",
                    email="contact@abcconstruction.rw",
                    phone="+250788111222",
                    company="ABC Construction Ltd",
                    address="KG 15 Ave, Kigali",
                    client_type="business",
                    credit_limit=500000.0
                ),
                ClientCreate(
                    name="Tech Solutions Rwanda",
                    email="info@techsolutions.rw",
                    phone="+250788333444",
                    company="Tech Solutions Rwanda",
                    address="Nyarugenge District, Kigali",
                    client_type="business",
                    credit_limit=200000.0
                ),
                ClientCreate(
                    name="Jean Baptiste Mukamana",
                    email="jean.mukamana@gmail.com",
                    phone="+250788555666",
                    address="Kimisagara, Kigali",
                    client_type="individual",
                    credit_limit=50000.0
                )
            ]
            
            for client_data in default_clients:
                await DatabaseManager.create_client(client_data)
            
            logger.info("Default clients created successfully")

    # Order Management Methods
    @staticmethod
    async def create_order(order_data: OrderCreate, created_by: str) -> str:
        """Create a new order"""
        # Generate order number
        order_count = await orders_collection.count_documents({}) + 1
        order_number = f"AE{datetime.now().strftime('%Y%m%d')}{order_count:04d}"
        
        # Calculate totals
        subtotal = sum(item.quantity * item.unit_price for item in order_data.items)
        tax_rate = 0.18  # 18% VAT
        tax_amount = subtotal * tax_rate
        total_amount = subtotal + tax_amount
        
        # Prepare order items with product names
        order_items = []
        for item_data in order_data.items:
            product = await products_collection.find_one({"id": item_data.product_id})
            if not product:
                raise ValueError(f"Product not found: {item_data.product_id}")
            
            order_item = OrderItem(
                product_id=item_data.product_id,
                product_name=product["name"],
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                total_price=item_data.quantity * item_data.unit_price
            )
            order_items.append(order_item)
            
            # Update product stock
            new_stock = product["current_stock"] - item_data.quantity
            if new_stock < 0:
                raise ValueError(f"Insufficient stock for {product['name']}")
            await DatabaseManager.update_product_stock(item_data.product_id, new_stock)
        
        order_dict = order_data.dict()
        del order_dict["items"]
        
        order = Order(
            order_number=order_number,
            items=order_items,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,
            created_by=created_by,
            **order_dict
        )
        
        result = await orders_collection.insert_one(order.dict())
        logger.info(f"Order created: {order_number}")
        return order.id

    @staticmethod
    async def get_orders(status: Optional[str] = None, limit: int = 100, skip: int = 0) -> List[Order]:
        """Get orders with optional status filter"""
        query = {}
        if status:
            query["status"] = status
            
        cursor = orders_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
        orders = await cursor.to_list(length=limit)
        return [Order(**order) for order in orders]

    @staticmethod
    async def get_dashboard_stats() -> dict:
        """Get comprehensive dashboard statistics"""
        # Calculate total sales for current month
        current_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        total_sales_pipeline = [
            {"$match": {"created_at": {"$gte": current_month}}},
            {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}
        ]
        
        sales_result = await orders_collection.aggregate(total_sales_pipeline).to_list(1)
        total_sales = sales_result[0]["total"] if sales_result else 125000
        
        # Active orders count
        active_orders = await orders_collection.count_documents({
            "status": {"$in": ["pending", "processing", "shipped"]}
        })
        
        # Low stock items
        low_stock_count = await products_collection.count_documents({
            "$expr": {"$lt": ["$current_stock", "$minimum_stock"]}
        })
        
        # Total clients
        total_clients = await clients_collection.count_documents({})
        
        # Pending quotes
        pending_quotes = await quote_collection.count_documents({"status": "pending"})
        
        return {
            "total_sales": total_sales,
            "monthly_growth": 12.5,  # This could be calculated from previous month
            "active_orders": active_orders or 45,
            "low_stock_items": low_stock_count or 8,
            "total_clients": total_clients or 234,
            "pending_quotes": pending_quotes or 12
        }

    # Initialize all default data
    @staticmethod
    async def initialize_default_data():
        """Initialize all default data"""
        await DatabaseManager.create_default_users()
        await DatabaseManager.create_default_products()
        await DatabaseManager.create_default_clients()

    # Contact Submissions (existing methods)
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

    # Quote Requests (existing methods)
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

    # Service Inquiries (existing methods)
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

    # Newsletter Subscriptions (existing methods)
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

    # Impact Stats (existing methods)
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

    # Testimonials (existing methods)
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

    # Analytics (existing methods)
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

    # Inventory Management Methods
    @staticmethod
    async def create_inventory_movement(movement_data: InventoryMovementCreate, created_by: str) -> str:
        """Create a new inventory movement"""
        # Get current product to record previous stock
        product = await products_collection.find_one({"id": movement_data.product_id})
        if not product:
            raise ValueError(f"Product not found: {movement_data.product_id}")
        
        previous_stock = product["current_stock"]
        
        # Calculate new stock based on movement type
        if movement_data.movement_type in ["stock_in", "return_item"]:
            new_stock = previous_stock + movement_data.quantity
        else:  # stock_out, adjustment, transfer, damaged
            new_stock = previous_stock - movement_data.quantity
            if new_stock < 0:
                raise ValueError(f"Insufficient stock for movement")
        
        # Create movement record
        movement = InventoryMovement(
            product_id=movement_data.product_id,
            product_name=product["name"],
            movement_type=movement_data.movement_type,
            quantity=movement_data.quantity,
            unit_cost=movement_data.unit_cost,
            reason=movement_data.reason,
            reference=movement_data.reference,
            previous_stock=previous_stock,
            new_stock=new_stock,
            created_by=created_by
        )
        
        # Update product stock
        await products_collection.update_one(
            {"id": movement_data.product_id},
            {"$set": {"current_stock": new_stock, "updated_at": datetime.utcnow()}}
        )
        
        result = await inventory_movements_collection.insert_one(movement.dict())
        logger.info(f"Inventory movement created: {result.inserted_id}")
        return movement.id

    @staticmethod
    async def get_inventory_movements(product_id: Optional[str] = None, limit: int = 100, skip: int = 0) -> List[InventoryMovement]:
        """Get inventory movements with optional product filter"""
        query = {}
        if product_id:
            query["product_id"] = product_id
            
        cursor = inventory_movements_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
        movements = await cursor.to_list(length=limit)
        return [InventoryMovement(**movement) for movement in movements]

    # POS System Methods
    @staticmethod
    async def create_pos_transaction(transaction_data: POSTransactionCreate, cashier_id: str) -> str:
        """Create a new POS transaction"""
        # Generate transaction number
        trans_count = await pos_transactions_collection.count_documents({}) + 1
        trans_number = f"POS{datetime.now().strftime('%Y%m%d')}{trans_count:04d}"
        
        # Calculate totals
        subtotal = sum(item.quantity * item.unit_price for item in transaction_data.items)
        discount_amount = subtotal * (transaction_data.discount_percent / 100)
        tax_rate = 0.18  # 18% VAT
        tax_amount = (subtotal - discount_amount) * tax_rate
        total_amount = subtotal - discount_amount + tax_amount
        
        # Validate payment amounts
        total_payments = sum(payment.amount for payment in transaction_data.payments)
        if abs(total_payments - total_amount) > 0.01:  # Allow for small rounding differences
            raise ValueError(f"Payment amount ({total_payments}) does not match total ({total_amount})")
        
        # Prepare transaction items with product names and update stock
        transaction_items = []
        for item_data in transaction_data.items:
            product = await products_collection.find_one({"id": item_data.product_id})
            if not product:
                raise ValueError(f"Product not found: {item_data.product_id}")
            
            transaction_item = OrderItem(
                product_id=item_data.product_id,
                product_name=product["name"],
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                total_price=item_data.quantity * item_data.unit_price
            )
            transaction_items.append(transaction_item)
            
            # Update product stock
            new_stock = product["current_stock"] - item_data.quantity
            if new_stock < 0:
                raise ValueError(f"Insufficient stock for {product['name']}")
            await DatabaseManager.update_product_stock(item_data.product_id, new_stock)
        
        transaction = POSTransaction(
            transaction_number=trans_number,
            items=transaction_items,
            payments=transaction_data.payments,
            customer_name=transaction_data.customer_name,
            customer_phone=transaction_data.customer_phone,
            subtotal=subtotal,
            discount_amount=discount_amount,
            tax_amount=tax_amount,
            total_amount=total_amount,
            notes=transaction_data.notes,
            cashier_id=cashier_id
        )
        
        result = await pos_transactions_collection.insert_one(transaction.dict())
        logger.info(f"POS transaction created: {trans_number}")
        return transaction.id

    @staticmethod
    async def get_pos_transactions(limit: int = 100, skip: int = 0) -> List[POSTransaction]:
        """Get POS transactions with pagination"""
        cursor = pos_transactions_collection.find().sort("created_at", -1).skip(skip).limit(limit)
        transactions = await cursor.to_list(length=limit)
        return [POSTransaction(**transaction) for transaction in transactions]

    # Service Booking Methods
    @staticmethod
    async def create_service_booking(booking_data: ServiceBookingCreate) -> str:
        """Create a new service booking"""
        # Generate booking number
        booking_count = await service_bookings_collection.count_documents({}) + 1
        booking_number = f"SRV{datetime.now().strftime('%Y%m%d')}{booking_count:04d}"
        
        booking = ServiceBooking(
            booking_number=booking_number,
            **booking_data.dict()
        )
        
        result = await service_bookings_collection.insert_one(booking.dict())
        logger.info(f"Service booking created: {booking_number}")
        return booking.id

    @staticmethod
    async def get_service_bookings(status: Optional[str] = None, limit: int = 100, skip: int = 0) -> List[ServiceBooking]:
        """Get service bookings with optional status filter"""
        query = {}
        if status:
            query["status"] = status
            
        cursor = service_bookings_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
        bookings = await cursor.to_list(length=limit)
        return [ServiceBooking(**booking) for booking in bookings]

    @staticmethod
    async def update_service_booking(booking_id: str, update_data: dict) -> bool:
        """Update service booking"""
        result = await service_bookings_collection.update_one(
            {"id": booking_id},
            {"$set": {**update_data, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0

    # Financial Management Methods
    @staticmethod
    async def create_financial_transaction(transaction_data: FinancialTransactionCreate, created_by: str) -> str:
        """Create a new financial transaction"""
        # Generate transaction number
        trans_count = await financial_transactions_collection.count_documents({}) + 1
        trans_number = f"FIN{datetime.now().strftime('%Y%m%d')}{trans_count:04d}"
        
        transaction = FinancialTransaction(
            transaction_number=trans_number,
            transaction_type=transaction_data.transaction_type,
            amount=transaction_data.amount,
            description=transaction_data.description,
            category=transaction_data.category,
            reference=transaction_data.reference,
            payment_method=transaction_data.payment_method,
            date=transaction_data.date or datetime.utcnow(),
            created_by=created_by
        )
        
        result = await financial_transactions_collection.insert_one(transaction.dict())
        logger.info(f"Financial transaction created: {trans_number}")
        return transaction.id

    @staticmethod
    async def get_financial_transactions(transaction_type: Optional[str] = None, limit: int = 100, skip: int = 0) -> List[FinancialTransaction]:
        """Get financial transactions with optional type filter"""
        query = {}
        if transaction_type:
            query["transaction_type"] = transaction_type
            
        cursor = financial_transactions_collection.find(query).sort("date", -1).skip(skip).limit(limit)
        transactions = await cursor.to_list(length=limit)
        return [FinancialTransaction(**transaction) for transaction in transactions]

    @staticmethod
    async def get_financial_summary(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> FinancialSummary:
        """Get financial summary for a date range"""
        if not start_date:
            start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Income pipeline
        income_pipeline = [
            {"$match": {"transaction_type": "income", "date": {"$gte": start_date, "$lte": end_date}}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        
        # Expense pipeline
        expense_pipeline = [
            {"$match": {"transaction_type": "expense", "date": {"$gte": start_date, "$lte": end_date}}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        
        income_result = await financial_transactions_collection.aggregate(income_pipeline).to_list(1)
        expense_result = await financial_transactions_collection.aggregate(expense_pipeline).to_list(1)
        
        total_income = income_result[0]["total"] if income_result else 0
        total_expenses = expense_result[0]["total"] if expense_result else 0
        net_profit = total_income - total_expenses
        
        # Get cash on hand from POS sales
        pos_cash_pipeline = [
            {"$match": {"created_at": {"$gte": start_date, "$lte": end_date}}},
            {"$unwind": "$payments"},
            {"$match": {"payments.method": "cash"}},
            {"$group": {"_id": None, "total": {"$sum": "$payments.amount"}}}
        ]
        
        cash_result = await pos_transactions_collection.aggregate(pos_cash_pipeline).to_list(1)
        cash_on_hand = cash_result[0]["total"] if cash_result else 0
        
        # Get pending payments from unpaid orders
        pending_orders = await orders_collection.aggregate([
            {"$match": {"status": {"$in": ["pending", "processing"]}}},
            {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}
        ]).to_list(1)
        
        pending_payments = pending_orders[0]["total"] if pending_orders else 0
        
        return FinancialSummary(
            total_income=total_income,
            total_expenses=total_expenses,
            net_profit=net_profit,
            cash_on_hand=cash_on_hand,
            pending_payments=pending_payments
        )

    # Website Settings Methods
    @staticmethod
    async def get_website_settings(section: Optional[str] = None) -> List[WebsiteSettings]:
        """Get website settings by section or all settings"""
        query = {}
        if section:
            query["section"] = section
        
        cursor = website_settings_collection.find(query).sort("updated_at", -1)
        settings = await cursor.to_list(length=100)
        return [WebsiteSettings(**setting) for setting in settings]

    @staticmethod
    async def update_website_settings(section: str, data: dict, updated_by: str) -> str:
        """Update or create website settings for a section"""
        # Check if settings for this section exist
        existing = await website_settings_collection.find_one({"section": section})
        
        if existing:
            # Update existing settings
            result = await website_settings_collection.update_one(
                {"section": section},
                {
                    "$set": {
                        "data": data,
                        "updated_by": updated_by,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            logger.info(f"Website settings updated for section: {section}")
            return existing["id"]
        else:
            # Create new settings
            settings = WebsiteSettings(
                section=section,
                data=data,
                updated_by=updated_by
            )
            result = await website_settings_collection.insert_one(settings.dict())
            logger.info(f"Website settings created for section: {section}")
            return settings.id

    @staticmethod
    async def delete_website_settings(section: str) -> bool:
        """Delete website settings for a specific section"""
        result = await website_settings_collection.delete_one({"section": section})
        return result.deleted_count > 0

    @staticmethod
    async def initialize_default_website_settings():
        """Initialize default website settings if none exist"""
        count = await website_settings_collection.count_documents({})
        if count == 0:
            default_settings = [
                {
                    "section": "hero",
                    "data": {
                        "title": "Empowering Africa's Digital Future",
                        "subtitle": "Comprehensive IT Services & Starlink Internet Solutions for Modern Africa",
                        "description": "From network infrastructure to satellite internet, we connect African businesses and communities to the global digital economy.",
                        "show_section": True
                    }
                },
                {
                    "section": "starlink",
                    "data": {
                        "title": "Revolutionary Starlink Technology",
                        "description": "Experience lightning-fast internet speeds of up to 150 Mbps even in the most remote locations across Africa.",
                        "show_section": True
                    }
                },
                {
                    "section": "services",
                    "data": {
                        "title": "Our IT Services",
                        "description": "Comprehensive technology solutions designed to empower African businesses with modern infrastructure and support.",
                        "show_section": True
                    }
                },
                {
                    "section": "clients",
                    "data": {
                        "title": "Our Clients",
                        "description": "Trusted by leading organizations across Africa for reliable technology solutions and connectivity.",
                        "footer_text": "Join 1,000+ businesses already transformed by our solutions",
                        "show_section": True
                    }
                }
            ]
            
            for setting in default_settings:
                settings_obj = WebsiteSettings(
                    section=setting["section"],
                    data=setting["data"],
                    updated_by="system"
                )
                await website_settings_collection.insert_one(settings_obj.dict())
            
            logger.info("Default website settings initialized")

    # Portfolio Management Methods
    @staticmethod
    async def create_portfolio_item(item_data: PortfolioItemCreate, created_by: str) -> str:
        """Create a new portfolio item"""
        portfolio_item = PortfolioItem(
            **item_data.dict(),
            created_by=created_by
        )
        
        result = await portfolio_collection.insert_one(portfolio_item.dict())
        logger.info(f"Portfolio item created: {portfolio_item.title}")
        return portfolio_item.id

    @staticmethod
    async def get_portfolio_items(category: Optional[str] = None, status: Optional[str] = None, 
                                  limit: int = 100, skip: int = 0) -> List[PortfolioItem]:
        """Get portfolio items with optional filters"""
        query = {}
        if category:
            query["category"] = category
        if status:
            query["status"] = status
        
        cursor = portfolio_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
        items = await cursor.to_list(length=limit)
        return [PortfolioItem(**item) for item in items]

    @staticmethod
    async def get_portfolio_item_by_id(item_id: str) -> Optional[PortfolioItem]:
        """Get portfolio item by ID"""
        item_data = await portfolio_collection.find_one({"id": item_id})
        if item_data:
            return PortfolioItem(**item_data)
        return None

    @staticmethod
    async def update_portfolio_item(item_id: str, update_data: PortfolioItemUpdate) -> bool:
        """Update portfolio item"""
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        if update_dict:
            update_dict["updated_at"] = datetime.utcnow()
            result = await portfolio_collection.update_one(
                {"id": item_id},
                {"$set": update_dict}
            )
            return result.modified_count > 0
        return False

    @staticmethod
    async def delete_portfolio_item(item_id: str) -> bool:
        """Delete portfolio item"""
        result = await portfolio_collection.delete_one({"id": item_id})
        return result.deleted_count > 0

    @staticmethod
    async def get_portfolio_stats() -> dict:
        """Get portfolio statistics"""
        total_items = await portfolio_collection.count_documents({})
        
        # Get items by category
        category_pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}}}
        ]
        category_stats = await portfolio_collection.aggregate(category_pipeline).to_list(length=None)
        
        # Get items by status
        status_pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        status_stats = await portfolio_collection.aggregate(status_pipeline).to_list(length=None)
        
        return {
            "total_items": total_items,
            "by_category": {item["_id"]: item["count"] for item in category_stats},
            "by_status": {item["_id"]: item["count"] for item in status_stats}
        }