#!/usr/bin/env python3
"""
Add sample clients with logos for website showcase
"""

from database import get_db, Client
from sqlalchemy.orm import Session
import logging
import base64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample logo placeholder (simple SVG encoded as base64)
def create_sample_logo(company_name):
    svg_content = f'''<svg width="100" height="60" xmlns="http://www.w3.org/2000/svg">
        <rect width="100" height="60" fill="#0c4864"/>
        <text x="50" y="35" font-family="Arial, sans-serif" font-size="12" font-weight="bold" 
              text-anchor="middle" fill="white">{company_name[:8]}</text>
    </svg>'''
    return f"data:image/svg+xml;base64,{base64.b64encode(svg_content.encode()).decode()}"

def add_sample_clients():
    """Add sample clients for website showcase"""
    logger.info("Adding sample clients...")
    
    db = next(get_db())
    
    sample_clients = [
        {
            "name": "Rwanda Development Bank",
            "company_name": "Rwanda Development Bank",
            "email": "info@rdb.rw",
            "phone": "+250 788 123 456",
            "address": "Kigali, Rwanda",
            "client_type": "business",
            "website_url": "https://rdb.rw",
            "showcase_on_website": True,
            "display_order": 1
        },
        {
            "name": "Kigali Convention Centre",
            "company_name": "Kigali Convention Centre",
            "email": "info@kcc.rw",
            "phone": "+250 788 234 567",
            "address": "Kigali, Rwanda",
            "client_type": "business",
            "website_url": "https://kigaliconventioncentre.rw",
            "showcase_on_website": True,
            "display_order": 2
        },
        {
            "name": "Bank of Kigali",
            "company_name": "Bank of Kigali",
            "email": "info@bk.rw",
            "phone": "+250 788 345 678",
            "address": "Kigali, Rwanda",
            "client_type": "business",
            "website_url": "https://bk.rw",
            "showcase_on_website": True,
            "display_order": 3
        },
        {
            "name": "Rwanda Airlines",
            "company_name": "Rwanda Airlines",
            "email": "info@rwandair.com",
            "phone": "+250 788 456 789",
            "address": "Kigali, Rwanda",
            "client_type": "business",
            "website_url": "https://rwandair.com",
            "showcase_on_website": True,
            "display_order": 4
        },
        {
            "name": "MTN Rwanda",
            "company_name": "MTN Rwanda",
            "email": "info@mtn.rw",
            "phone": "+250 788 567 890",
            "address": "Kigali, Rwanda",
            "client_type": "business",
            "website_url": "https://mtn.rw",
            "showcase_on_website": True,
            "display_order": 5
        },
        {
            "name": "Airtel Rwanda",
            "company_name": "Airtel Rwanda",
            "email": "info@airtel.rw",
            "phone": "+250 788 678 901",
            "address": "Kigali, Rwanda",
            "client_type": "business",
            "website_url": "https://airtel.rw",
            "showcase_on_website": True,
            "display_order": 6
        },
        {
            "name": "RSSB",
            "company_name": "Rwanda Social Security Board",
            "email": "info@rssb.rw",
            "phone": "+250 788 789 012",
            "address": "Kigali, Rwanda",
            "client_type": "business",
            "website_url": "https://rssb.rw",
            "showcase_on_website": True,
            "display_order": 7
        },
        {
            "name": "NISR",
            "company_name": "National Institute of Statistics Rwanda",
            "email": "info@statistics.gov.rw",
            "phone": "+250 788 890 123",
            "address": "Kigali, Rwanda",
            "client_type": "business",
            "website_url": "https://statistics.gov.rw",
            "showcase_on_website": True,
            "display_order": 8
        },
        {
            "name": "University of Rwanda",
            "company_name": "University of Rwanda",
            "email": "info@ur.ac.rw",
            "phone": "+250 788 901 234",
            "address": "Kigali, Rwanda",
            "client_type": "business",
            "website_url": "https://ur.ac.rw",
            "showcase_on_website": True,
            "display_order": 9
        }
    ]
    
    try:
        for client_data in sample_clients:
            # Check if client already exists
            existing = db.query(Client).filter(Client.email == client_data["email"]).first()
            if existing:
                logger.info(f"Client {client_data['name']} already exists, skipping...")
                continue
            
            # Create logo
            logo = create_sample_logo(client_data["company_name"])
            
            # Create client
            client = Client(
                name=client_data["name"],
                company_name=client_data["company_name"],
                email=client_data["email"],
                phone=client_data["phone"],
                address=client_data["address"],
                client_type=client_data["client_type"],
                logo=logo,
                website_url=client_data["website_url"],
                showcase_on_website=client_data["showcase_on_website"],
                display_order=client_data["display_order"],
                credit_limit=0.0,
                current_balance=0.0
            )
            
            db.add(client)
            logger.info(f"Added client: {client_data['name']}")
        
        db.commit()
        logger.info("✅ Sample clients added successfully!")
        
        # Check total showcase clients
        showcase_count = db.query(Client).filter(Client.showcase_on_website == True).count()
        logger.info(f"Total clients featured on website: {showcase_count}")
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error adding sample clients: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_clients()