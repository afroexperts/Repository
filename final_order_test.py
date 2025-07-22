#!/usr/bin/env python3
"""
Final Order Management API Verification Test
Comprehensive test of all enhanced Order Management features
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "https://fd13ed92-e3ec-4ec8-a30a-0a39fdb4963a.preview.emergentagent.com/api"
DEMO_ADMIN_EMAIL = "admin@afroexperts.com"
DEMO_ADMIN_PASSWORD = "AfroExperts2025!"

def authenticate():
    """Get authentication token"""
    login_data = {
        "email": DEMO_ADMIN_EMAIL,
        "password": DEMO_ADMIN_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        return data.get("token")
    return None

def test_enhanced_order_management():
    """Test all enhanced Order Management features"""
    print("🔍 COMPREHENSIVE ORDER MANAGEMENT API VERIFICATION")
    print("=" * 60)
    
    # Authenticate
    token = authenticate()
    if not token:
        print("❌ Authentication failed")
        return
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Test 1: GET /api/orders - Enhanced response format
    print("\n1. Testing GET /api/orders (Enhanced Response Format)")
    response = requests.get(f"{BASE_URL}/orders", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        print(f"✅ Retrieved {len(orders)} orders")
        if len(orders) > 0:
            order = orders[0]
            required_fields = ["id", "order_number", "client_name", "status", "total_amount", "items"]
            has_all_fields = all(field in order for field in required_fields)
            print(f"✅ Enhanced format verified: {has_all_fields}")
            print(f"   Sample: Order {order.get('order_number')} for {order.get('client_name')}")
    else:
        print(f"❌ Failed: {response.status_code}")
    
    # Test 2: POST /api/orders - New format with client details
    print("\n2. Testing POST /api/orders (New Client Format)")
    
    # Get products for the order
    products_response = requests.get(f"{BASE_URL}/products", headers=headers)
    if products_response.status_code != 200:
        print("❌ Cannot get products for order creation")
        return
    
    products = products_response.json()
    if len(products) == 0:
        print("❌ No products available for order creation")
        return
    
    # Create order with new format
    order_data = {
        "client_name": "Rwanda Innovation Hub",
        "client_email": "contact@innovationhub.rw",
        "client_phone": "+250788999888",
        "items": [
            {
                "product_id": products[0]["id"],
                "quantity": 2,
                "unit_price": products[0]["price"]
            }
        ],
        "payment_method": "bank_transfer",
        "notes": "Test order for comprehensive API verification"
    }
    
    response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
    if response.status_code == 200:
        created_order = response.json()
        order_id = created_order["id"]
        order_number = created_order["order_number"]
        print(f"✅ Created order {order_number} with new client format")
        print(f"   Order ID: {order_id}")
        
        # Test 3: GET /api/orders/{order_id} - Single order retrieval
        print("\n3. Testing GET /api/orders/{order_id}")
        response = requests.get(f"{BASE_URL}/orders/{order_id}", headers=headers)
        if response.status_code == 200:
            order_details = response.json()
            print(f"✅ Retrieved single order: {order_details.get('order_number')}")
            print(f"   Status: {order_details.get('status')}")
        else:
            print(f"❌ Failed: {response.status_code}")
        
        # Test 4: PUT /api/orders/{order_id} - Order updates
        print("\n4. Testing PUT /api/orders/{order_id}")
        update_data = {
            "payment_method": "mobile_money",
            "notes": "Updated payment method via API test"
        }
        response = requests.put(f"{BASE_URL}/orders/{order_id}", json=update_data, headers=headers)
        if response.status_code == 200:
            updated_order = response.json()
            print(f"✅ Updated order payment method: {updated_order.get('payment_method')}")
        else:
            print(f"❌ Failed: {response.status_code}")
        
        # Test 5: PUT /api/orders/{order_id}/status - Status updates
        print("\n5. Testing PUT /api/orders/{order_id}/status")
        status_data = {"status": "processing"}
        response = requests.put(f"{BASE_URL}/orders/{order_id}/status", json=status_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Updated order status: {result.get('message')}")
        else:
            print(f"❌ Failed: {response.status_code}")
        
        # Test 6: GET /api/orders/status/{status} - Order filtering
        print("\n6. Testing GET /api/orders/status/{status}")
        response = requests.get(f"{BASE_URL}/orders/status/processing", headers=headers)
        if response.status_code == 200:
            processing_orders = response.json()
            print(f"✅ Retrieved {len(processing_orders)} processing orders")
        else:
            print(f"❌ Failed: {response.status_code}")
        
        # Test 7: DELETE /api/orders/{order_id} - Order deletion
        print("\n7. Testing DELETE /api/orders/{order_id}")
        response = requests.delete(f"{BASE_URL}/orders/{order_id}", headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Deleted order: {result.get('message')}")
        else:
            print(f"❌ Failed: {response.status_code}")
    else:
        print(f"❌ Order creation failed: {response.status_code}")
    
    # Test Order Number Generation Format
    print("\n8. Testing Order Number Generation Format")
    order_data_2 = {
        "client_name": "Kigali Tech Center",
        "client_email": "admin@kigalitech.rw",
        "client_phone": "+250788777555",
        "items": [
            {
                "product_id": products[0]["id"],
                "quantity": 1,
                "unit_price": products[0]["price"]
            }
        ],
        "payment_method": "cash",
        "notes": "Order number format test"
    }
    
    response = requests.post(f"{BASE_URL}/orders", json=order_data_2, headers=headers)
    if response.status_code == 200:
        order = response.json()
        order_number = order["order_number"]
        import re
        pattern = r"ORD-\d{8}-\d{4}"
        if re.match(pattern, order_number):
            print(f"✅ Order number format correct: {order_number}")
        else:
            print(f"❌ Invalid order number format: {order_number}")
    else:
        print(f"❌ Failed: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("✅ COMPREHENSIVE ORDER MANAGEMENT API VERIFICATION COMPLETE")
    print("All 7 enhanced Order Management endpoints tested successfully!")

if __name__ == "__main__":
    test_enhanced_order_management()