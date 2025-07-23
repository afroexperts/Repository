#!/usr/bin/env python3
"""
Seed RBAC Permissions Script
Populates the role_permissions table with default permissions for each role
"""

from database import get_db, RolePermission, Permission, UserRole
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_role_permissions(role: str) -> dict:
    """Get default permissions for a role"""
    role_permissions = {
        "admin": {
            # Admin has all permissions
            perm.value: True for perm in Permission
        },
        "manager": {
            # Manager has most permissions except user management
            "dashboard_view": True, "dashboard_stats": True,
            "products_view": True, "products_create": True, "products_update": True, "products_delete": True,
            "orders_view": True, "orders_create": True, "orders_update": True, "orders_delete": True,
            "clients_view": True, "clients_create": True, "clients_update": True, "clients_delete": True,
            "inventory_view": True, "inventory_create": True, "inventory_update": True, "inventory_delete": True,
            "finance_view": True, "finance_create": True, "finance_update": True, "finance_delete": True,
            "invoices_view": True, "invoices_create": True, "invoices_update": True, "invoices_delete": True, "invoices_payment": True,
            "reports_view": True, "reports_export": True,
            "settings_view": True, "settings_update": True,
            "pos_access": True, "pos_sales": True,
            "services_view": True, "services_create": True, "services_update": True, "services_delete": True,
            "portfolio_view": True, "portfolio_create": True, "portfolio_update": True, "portfolio_delete": True,
            "secondhand_view": True, "secondhand_create": True, "secondhand_update": True, "secondhand_delete": True,
            "marble_view": True, "marble_create": True, "marble_update": True, "marble_delete": True,
            "starlink_view": True, "starlink_create": True, "starlink_update": True, "starlink_delete": True,
        },
        "cashier": {
            # Cashier has POS and basic viewing permissions
            "dashboard_view": True,
            "products_view": True,
            "clients_view": True, "clients_create": True,
            "orders_view": True, "orders_create": True,
            "pos_access": True, "pos_sales": True,
            "invoices_view": True, "invoices_create": True, "invoices_payment": True,
            "reports_view": True,
        },
        "inventory_officer": {
            # Inventory officer has inventory and product permissions
            "dashboard_view": True,
            "products_view": True, "products_create": True, "products_update": True,
            "inventory_view": True, "inventory_create": True, "inventory_update": True, "inventory_delete": True,
            "reports_view": True, "reports_export": True,
            "marble_view": True, "marble_create": True, "marble_update": True,
        },
        "technician": {
            # Technician has service and starlink permissions
            "dashboard_view": True,
            "services_view": True, "services_update": True,
            "starlink_view": True, "starlink_create": True, "starlink_update": True,
            "reports_view": True,
        },
        "sales_rep": {
            # Sales rep has client and sales permissions
            "dashboard_view": True,
            "clients_view": True, "clients_create": True, "clients_update": True,
            "orders_view": True, "orders_create": True, "orders_update": True,
            "invoices_view": True, "invoices_create": True,
            "secondhand_view": True, "secondhand_create": True, "secondhand_update": True,
            "starlink_view": True, "starlink_create": True,
            "reports_view": True,
        },
        "accountant": {
            # Accountant has financial permissions
            "dashboard_view": True, "dashboard_stats": True,
            "finance_view": True, "finance_create": True, "finance_update": True, "finance_delete": True,
            "invoices_view": True, "invoices_create": True, "invoices_update": True, "invoices_payment": True,
            "reports_view": True, "reports_export": True,
            "orders_view": True, "clients_view": True,
        },
        "viewer": {
            # Viewer has only read permissions
            "dashboard_view": True,
            "products_view": True, "orders_view": True, "clients_view": True,
            "inventory_view": True, "finance_view": True, "invoices_view": True,
            "reports_view": True, "services_view": True, "portfolio_view": True,
            "secondhand_view": True, "marble_view": True, "starlink_view": True,
        }
    }
    return role_permissions.get(role, {})

def seed_rbac_permissions():
    """Seed the database with default role permissions"""
    logger.info("Starting RBAC permissions seeding...")
    
    db = next(get_db())
    
    try:
        # Delete existing role permissions to avoid duplicates
        db.query(RolePermission).delete()
        db.commit()
        
        # Seed permissions for each role
        for role in UserRole:
            logger.info(f"Seeding permissions for role: {role.value}")
            role_perms = get_user_role_permissions(role.value)
            
            for permission, granted in role_perms.items():
                role_permission = RolePermission(
                    role=role.value,
                    permission=permission,
                    granted=granted
                )
                db.add(role_permission)
            
            logger.info(f"Added {len(role_perms)} permissions for {role.value}")
        
        db.commit()
        logger.info("✅ RBAC permissions seeded successfully!")
        
        # Print summary
        total_permissions = db.query(RolePermission).count()
        logger.info(f"Total role permissions in database: {total_permissions}")
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error seeding RBAC permissions: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_rbac_permissions()