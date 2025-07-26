#!/usr/bin/env python3
"""
Script to add sample clients with showcase data to MongoDB database
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'afroexperts_erp')

async def add_showcase_clients():
    """Add sample clients with showcase data"""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    clients_collection = db.clients
    
    # Sample company logos in base64 format (small sample images)
    sample_logos = {
        "tech_company": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzAwNzNlNiIvPgogIDx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0IiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+VEVDSDwvdGV4dD4KPC9zdmc+",
        "construction": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2ZmNjkwMCIvPgogIDx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEyIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+QlVJTEQ8L3RleHQ+Cjwvc3ZnPg==",
        "finance": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzI1OGI2NSIvPgogIDx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEyIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+RklOPHRleHQ+Cjwvc3ZnPg==",
        "education": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzg2MzNhMCIvPgogIDx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEyIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+RURVPHRleHQ+Cjwvc3ZnPg==",
        "healthcare": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2RjMzU0NSIvPgogIDx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEyIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+SEVBTFRINE48L3RleHQ+Cjwvc3ZnPg==",
        "retail": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzBlNzQ3NSIvPgogIDx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEyIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+UkVUQUlMPC90ZXh0Pgo8L3N2Zz4="
    }
    
    # Sample clients with showcase data
    showcase_clients = [
        {
            "id": str(uuid.uuid4()),
            "name": "RwandaTech Solutions",
            "email": "info@rwandatech.rw",
            "phone": "+250788111222",
            "address": "KN 78 St, Kigali",
            "client_type": "business",
            "company_name": "RwandaTech Solutions Ltd",
            "tax_number": "RT2024001",
            "credit_limit": 1000000.0,
            "current_balance": 0.0,
            "logo": sample_logos["tech_company"],
            "website_url": "https://rwandatech.rw",
            "showcase_on_website": True,
            "display_order": 1,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "BuildRwanda Construction",
            "email": "contact@buildrwanda.com",
            "phone": "+250788333444",
            "address": "KG 15 Ave, Gasabo",
            "client_type": "business",
            "company_name": "BuildRwanda Construction Ltd",
            "tax_number": "BR2024002",
            "credit_limit": 2000000.0,
            "current_balance": 0.0,
            "logo": sample_logos["construction"],
            "website_url": "https://buildrwanda.com",
            "showcase_on_website": True,
            "display_order": 2,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Kigali Financial Services",
            "email": "hello@kigalifinance.rw",
            "phone": "+250788555666",
            "address": "KN 67 St, Nyarugenge",
            "client_type": "business",
            "company_name": "Kigali Financial Services Ltd",
            "tax_number": "KF2024003",
            "credit_limit": 1500000.0,
            "current_balance": 0.0,
            "logo": sample_logos["finance"],
            "website_url": "https://kigalifinance.rw",
            "showcase_on_website": True,
            "display_order": 3,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "University of Kigali",
            "email": "admissions@uok.ac.rw",
            "phone": "+250788777888",
            "address": "Remera Campus, Gasabo",
            "client_type": "business",
            "company_name": "University of Kigali",
            "tax_number": "UK2024004",
            "credit_limit": 3000000.0,
            "current_balance": 0.0,
            "logo": sample_logos["education"],
            "website_url": "https://uok.ac.rw",
            "showcase_on_website": True,
            "display_order": 4,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Kigali Health Center",
            "email": "info@kigalihealth.rw",
            "phone": "+250788999000",
            "address": "KG 123 Ave, Kicukiro",
            "client_type": "business",
            "company_name": "Kigali Health Center Ltd",
            "tax_number": "KH2024005",
            "credit_limit": 2500000.0,
            "current_balance": 0.0,
            "logo": sample_logos["healthcare"],
            "website_url": "https://kigalihealth.rw",
            "showcase_on_website": True,
            "display_order": 5,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Rwanda Retail Network",
            "email": "support@rwandaretail.com",
            "phone": "+250788000111",
            "address": "KN 45 St, Nyarugenge",
            "client_type": "business",
            "company_name": "Rwanda Retail Network Ltd",
            "tax_number": "RR2024006",
            "credit_limit": 1200000.0,
            "current_balance": 0.0,
            "logo": sample_logos["retail"],
            "website_url": "https://rwandaretail.com",
            "showcase_on_website": True,
            "display_order": 6,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    try:
        # Insert showcase clients
        result = await clients_collection.insert_many(showcase_clients)
        print(f"✅ Successfully added {len(result.inserted_ids)} showcase clients to MongoDB")
        
        # Verify the clients were added
        count = await clients_collection.count_documents({"showcase_on_website": True})
        print(f"✅ Total showcase clients in database: {count}")
        
    except Exception as e:
        print(f"❌ Error adding showcase clients: {e}")
    
    finally:
        # Close the connection
        client.close()

if __name__ == "__main__":
    print("🚀 Adding sample clients with showcase data to MongoDB...")
    asyncio.run(add_showcase_clients())
    print("✅ Showcase clients setup complete!")