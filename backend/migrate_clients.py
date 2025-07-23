#!/usr/bin/env python3
"""
Migration script to add client showcase fields
"""

from sqlalchemy import create_engine, text
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """Add new columns to clients table"""
    
    # Get database URL from environment
    db_url = os.environ.get('DATABASE_URL', 'mysql://root:test123@localhost/afro_experts_db')
    
    engine = create_engine(db_url)
    
    try:
        with engine.connect() as conn:
            # Check if columns already exist
            result = conn.execute(text("DESCRIBE clients"))
            existing_columns = [row[0] for row in result.fetchall()]
            
            logger.info(f"Existing columns: {existing_columns}")
            
            # Add new columns if they don't exist
            new_columns = [
                ("logo", "TEXT DEFAULT NULL"),
                ("website_url", "VARCHAR(500) DEFAULT NULL"),
                ("showcase_on_website", "BOOLEAN DEFAULT FALSE"),
                ("display_order", "INT DEFAULT 0")
            ]
            
            for column_name, column_def in new_columns:
                if column_name not in existing_columns:
                    alter_sql = f"ALTER TABLE clients ADD COLUMN {column_name} {column_def}"
                    logger.info(f"Adding column: {alter_sql}")
                    conn.execute(text(alter_sql))
                    logger.info(f"✅ Added column: {column_name}")
                else:
                    logger.info(f"⏭️  Column {column_name} already exists")
            
            # Commit changes
            conn.commit()
            logger.info("✅ Migration completed successfully!")
            
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    run_migration()