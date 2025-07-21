#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Afro Experts ERP & POS System
Tests all implemented backend endpoints with proper authentication
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "https://45cf0b4b-2ffe-458a-b98c-d7eb64a6724d.preview.emergentagent.com/api"
DEMO_ADMIN_EMAIL = "admin@afroexperts.com"
DEMO_ADMIN_PASSWORD = "AfroExperts2025!"

class BackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.user_id = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    Details: {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")
        print()

    def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        url = f"{self.base_url}{endpoint}"
        
        # Default headers
        request_headers = {"Content-Type": "application/json"}
        if headers:
            request_headers.update(headers)
            
        # Add auth header if token exists
        if self.token:
            request_headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=request_headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=request_headers, timeout=30)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=request_headers, timeout=30)
            else:
                return False, f"Unsupported method: {method}", 0
                
            return response.status_code < 400, response.json() if response.content else {}, response.status_code
            
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}", 0
        except json.JSONDecodeError:
            return False, "Invalid JSON response", response.status_code if 'response' in locals() else 0

    def test_health_check(self):
        """Test the health check endpoint"""
        success, data, status_code = self.make_request("GET", "/")
        
        if success and status_code == 200:
            self.log_test("Health Check", True, f"API is running. Message: {data.get('message', 'N/A')}")
        else:
            self.log_test("Health Check", False, f"Status: {status_code}", data)

    def test_authentication_login(self):
        """Test user login authentication"""
        login_data = {
            "email": DEMO_ADMIN_EMAIL,
            "password": DEMO_ADMIN_PASSWORD
        }
        
        success, data, status_code = self.make_request("POST", "/auth/login", login_data)
        
        if success and status_code == 200 and data.get("token"):
            self.token = data["token"]
            self.user_id = data.get("user", {}).get("id")
            user_name = data.get("user", {}).get("full_name", "Unknown")
            user_role = data.get("user", {}).get("role", "Unknown")
            self.log_test("Authentication Login", True, f"Logged in as {user_name} ({user_role})")
        else:
            self.log_test("Authentication Login", False, f"Status: {status_code}", data)

    def test_authentication_me(self):
        """Test get current user info"""
        if not self.token:
            self.log_test("Authentication Me", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/auth/me")
        
        if success and status_code == 200 and data.get("id"):
            user_name = data.get("full_name", "Unknown")
            user_email = data.get("email", "Unknown")
            self.log_test("Authentication Me", True, f"Retrieved user info: {user_name} ({user_email})")
        else:
            self.log_test("Authentication Me", False, f"Status: {status_code}", data)

    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        if not self.token:
            self.log_test("Dashboard Stats", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/dashboard/stats")
        
        if success and status_code == 200:
            stats = {
                "Total Sales": data.get("total_sales", 0),
                "Active Orders": data.get("active_orders", 0),
                "Low Stock Items": data.get("low_stock_items", 0),
                "Total Clients": data.get("total_clients", 0)
            }
            self.log_test("Dashboard Stats", True, f"Retrieved stats: {stats}")
        else:
            self.log_test("Dashboard Stats", False, f"Status: {status_code}", data)

    def test_dashboard_recent_transactions(self):
        """Test recent transactions endpoint"""
        if not self.token:
            self.log_test("Dashboard Recent Transactions", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/dashboard/recent-transactions?limit=5")
        
        if success and status_code == 200:
            transactions = data.get("transactions", [])
            count = len(transactions)
            self.log_test("Dashboard Recent Transactions", True, f"Retrieved {count} recent transactions")
        else:
            self.log_test("Dashboard Recent Transactions", False, f"Status: {status_code}", data)

    def test_products_get(self):
        """Test get products endpoint"""
        if not self.token:
            self.log_test("Get Products", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/products?limit=10")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            categories = list(set(product.get("category", "Unknown") for product in data))
            self.log_test("Get Products", True, f"Retrieved {count} products from categories: {categories}")
        else:
            self.log_test("Get Products", False, f"Status: {status_code}", data)

    def test_products_low_stock(self):
        """Test get low stock products endpoint"""
        if not self.token:
            self.log_test("Get Low Stock Products", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/products/low-stock")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                product_names = [product.get("name", "Unknown") for product in data[:3]]
                self.log_test("Get Low Stock Products", True, f"Found {count} low stock products: {product_names}")
            else:
                self.log_test("Get Low Stock Products", True, "No low stock products found")
        else:
            self.log_test("Get Low Stock Products", False, f"Status: {status_code}", data)

    def test_products_create(self):
        """Test create product endpoint"""
        if not self.token:
            self.log_test("Create Product", False, "No token available - login failed")
            return
            
        product_data = {
            "name": "Test Network Router",
            "category": "networking",
            "description": "High-performance router for business use",
            "price": 85000.0,
            "cost_price": 60000.0,
            "unit": "pieces",
            "minimum_stock": 5,
            "current_stock": 10,
            "location": "Electronics Storage"
        }
        
        success, data, status_code = self.make_request("POST", "/products", product_data)
        
        if success and status_code == 200 and data.get("success"):
            product_id = data.get("id")
            self.log_test("Create Product", True, f"Created product with ID: {product_id}")
            return product_id
        else:
            self.log_test("Create Product", False, f"Status: {status_code}", data)
            return None

    def test_products_update_stock(self, product_id: Optional[str] = None):
        """Test update product stock endpoint"""
        if not self.token:
            self.log_test("Update Product Stock", False, "No token available - login failed")
            return
            
        if not product_id:
            # Try to get a product ID from existing products
            success, products, _ = self.make_request("GET", "/products?limit=1")
            if success and products and len(products) > 0:
                product_id = products[0].get("id")
            else:
                self.log_test("Update Product Stock", False, "No product ID available for testing")
                return
        
        # Update stock to 15
        success, data, status_code = self.make_request("PUT", f"/products/{product_id}/stock?new_stock=15")
        
        if success and status_code == 200 and data.get("success"):
            self.log_test("Update Product Stock", True, f"Updated stock for product {product_id}")
        else:
            self.log_test("Update Product Stock", False, f"Status: {status_code}", data)

    def test_orders_get(self):
        """Test get orders endpoint"""
        if not self.token:
            self.log_test("Get Orders", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/orders?limit=10")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                statuses = list(set(order.get("status", "Unknown") for order in data))
                self.log_test("Get Orders", True, f"Retrieved {count} orders with statuses: {statuses}")
            else:
                self.log_test("Get Orders", True, "No orders found")
        else:
            self.log_test("Get Orders", False, f"Status: {status_code}", data)

    def test_orders_create(self):
        """Test create order endpoint"""
        if not self.token:
            self.log_test("Create Order", False, "No token available - login failed")
            return
            
        # First get a product to use in the order
        success, products, _ = self.make_request("GET", "/products?limit=1")
        if not success or not products or len(products) == 0:
            self.log_test("Create Order", False, "No products available for order creation")
            return
            
        product = products[0]
        product_id = product.get("id")
        product_price = product.get("price", 10000)
        
        order_data = {
            "client_name": "Test Customer Rwanda",
            "client_email": "testcustomer@example.rw",
            "client_phone": "+250788999888",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "unit_price": product_price
                }
            ],
            "payment_method": "cash",
            "notes": "Test order for API validation"
        }
        
        success, data, status_code = self.make_request("POST", "/orders", order_data)
        
        if success and status_code == 200 and data.get("success"):
            order_id = data.get("id")
            self.log_test("Create Order", True, f"Created order with ID: {order_id}")
        else:
            self.log_test("Create Order", False, f"Status: {status_code}", data)

    def test_clients_get(self):
        """Test get clients endpoint"""
        if not self.token:
            self.log_test("Get Clients", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/clients?limit=10")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                client_types = list(set(client.get("client_type", "Unknown") for client in data))
                self.log_test("Get Clients", True, f"Retrieved {count} clients of types: {client_types}")
            else:
                self.log_test("Get Clients", True, "No clients found")
        else:
            self.log_test("Get Clients", False, f"Status: {status_code}", data)

    def test_clients_create(self):
        """Test create client endpoint"""
        if not self.token:
            self.log_test("Create Client", False, "No token available - login failed")
            return
            
        client_data = {
            "name": "Rwanda Tech Solutions Ltd",
            "email": "contact@rwandatech.rw",
            "phone": "+250788777666",
            "company": "Rwanda Tech Solutions Ltd",
            "address": "Kacyiru, Kigali, Rwanda",
            "client_type": "business",
            "credit_limit": 300000.0
        }
        
        success, data, status_code = self.make_request("POST", "/clients", client_data)
        
        if success and status_code == 200 and data.get("success"):
            client_id = data.get("id")
            self.log_test("Create Client", True, f"Created client with ID: {client_id}")
        else:
            self.log_test("Create Client", False, f"Status: {status_code}", data)

    # NEW MODULE TESTS - INVENTORY MANAGEMENT
    def test_inventory_movements_get(self):
        """Test get inventory movements endpoint"""
        if not self.token:
            self.log_test("Get Inventory Movements", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/inventory/movements?limit=10")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                movement_types = list(set(movement.get("movement_type", "Unknown") for movement in data))
                self.log_test("Get Inventory Movements", True, f"Retrieved {count} inventory movements of types: {movement_types}")
            else:
                self.log_test("Get Inventory Movements", True, "No inventory movements found")
        else:
            self.log_test("Get Inventory Movements", False, f"Status: {status_code}", data)

    def test_inventory_movements_create(self):
        """Test create inventory movement endpoint"""
        if not self.token:
            self.log_test("Create Inventory Movement", False, "No token available - login failed")
            return
            
        # First get a product to use in the movement
        success, products, _ = self.make_request("GET", "/products?limit=1")
        if not success or not products or len(products) == 0:
            self.log_test("Create Inventory Movement", False, "No products available for inventory movement")
            return
            
        product = products[0]
        product_id = product.get("id")
        
        movement_data = {
            "product_id": product_id,
            "movement_type": "stock_in",
            "quantity": 10,
            "unit_cost": 50000.0,
            "reference": "TEST-STOCK-IN-001",
            "reason": "Test stock in movement for API validation"
        }
        
        success, data, status_code = self.make_request("POST", "/inventory/movements", movement_data)
        
        if success and status_code == 200 and data.get("success"):
            movement_id = data.get("id")
            self.log_test("Create Inventory Movement", True, f"Created inventory movement with ID: {movement_id}")
        else:
            self.log_test("Create Inventory Movement", False, f"Status: {status_code}", data)

    def test_inventory_movements_types(self):
        """Test different inventory movement types"""
        if not self.token:
            self.log_test("Test Movement Types", False, "No token available - login failed")
            return
            
        # Get a product for testing
        success, products, _ = self.make_request("GET", "/products?limit=1")
        if not success or not products or len(products) == 0:
            self.log_test("Test Movement Types", False, "No products available for movement testing")
            return
            
        product_id = products[0].get("id")
        movement_types = ["stock_out", "adjustment", "damaged", "return"]
        successful_types = []
        
        for movement_type in movement_types:
            movement_data = {
                "product_id": product_id,
                "movement_type": movement_type,
                "quantity": 2,
                "unit_cost": 25000.0,
                "reference": f"TEST-{movement_type.upper()}-001",
                "notes": f"Test {movement_type} movement"
            }
            
            success, data, status_code = self.make_request("POST", "/inventory/movements", movement_data)
            if success and status_code == 200:
                successful_types.append(movement_type)
        
        if len(successful_types) == len(movement_types):
            self.log_test("Test Movement Types", True, f"All movement types working: {successful_types}")
        else:
            failed_types = [t for t in movement_types if t not in successful_types]
            self.log_test("Test Movement Types", False, f"Failed types: {failed_types}, Successful: {successful_types}")

    # NEW MODULE TESTS - POS SYSTEM
    def test_pos_transactions_get(self):
        """Test get POS transactions endpoint"""
        if not self.token:
            self.log_test("Get POS Transactions", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/pos/transactions?limit=10")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                payment_methods = list(set(transaction.get("payment_method", "Unknown") for transaction in data))
                self.log_test("Get POS Transactions", True, f"Retrieved {count} POS transactions with payment methods: {payment_methods}")
            else:
                self.log_test("Get POS Transactions", True, "No POS transactions found")
        else:
            self.log_test("Get POS Transactions", False, f"Status: {status_code}", data)

    def test_pos_transactions_create(self):
        """Test create POS transaction endpoint"""
        if not self.token:
            self.log_test("Create POS Transaction", False, "No token available - login failed")
            return
            
        # Get products for the transaction
        success, products, _ = self.make_request("GET", "/products?limit=2")
        if not success or not products or len(products) == 0:
            self.log_test("Create POS Transaction", False, "No products available for POS transaction")
            return
            
        # Create transaction with multiple items
        items = []
        total_amount = 0
        for i, product in enumerate(products[:2]):
            quantity = i + 1
            unit_price = product.get("price", 10000)
            items.append({
                "product_id": product.get("id"),
                "quantity": quantity,
                "unit_price": unit_price
            })
            total_amount += quantity * unit_price
        
        # Calculate discount and tax
        discount_percent = 5.0
        discount_amount = total_amount * (discount_percent / 100)
        tax_amount = (total_amount - discount_amount) * 0.18
        final_total = total_amount - discount_amount + tax_amount
        
        transaction_data = {
            "customer_name": "Walk-in Customer",
            "customer_phone": "+250788123456",
            "items": items,
            "payments": [{"method": "cash", "amount": final_total}],
            "discount_percent": discount_percent,
            "notes": "Test POS transaction with discount and tax"
        }
        
        success, data, status_code = self.make_request("POST", "/pos/transactions", transaction_data)
        
        if success and status_code == 200 and data.get("success"):
            transaction_id = data.get("id")
            self.log_test("Create POS Transaction", True, f"Created POS transaction with ID: {transaction_id}")
        else:
            self.log_test("Create POS Transaction", False, f"Status: {status_code}", data)

    def test_pos_payment_methods(self):
        """Test different payment methods in POS"""
        if not self.token:
            self.log_test("Test POS Payment Methods", False, "No token available - login failed")
            return
            
        # Get a product for testing
        success, products, _ = self.make_request("GET", "/products?limit=1")
        if not success or not products or len(products) == 0:
            self.log_test("Test POS Payment Methods", False, "No products available for payment testing")
            return
            
        product = products[0]
        unit_price = product.get("price", 10000)
        # Calculate total with tax
        subtotal = unit_price
        tax_amount = subtotal * 0.18
        total_amount = subtotal + tax_amount
        
        payment_methods = ["cash", "card", "mobile_money", "bank_transfer"]
        successful_methods = []
        
        for payment_method in payment_methods:
            transaction_data = {
                "customer_name": f"Test Customer {payment_method}",
                "items": [{
                    "product_id": product.get("id"),
                    "quantity": 1,
                    "unit_price": unit_price
                }],
                "payments": [{"method": payment_method, "amount": total_amount}],
                "notes": f"Test transaction with {payment_method}"
            }
            
            success, data, status_code = self.make_request("POST", "/pos/transactions", transaction_data)
            if success and status_code == 200:
                successful_methods.append(payment_method)
        
        if len(successful_methods) == len(payment_methods):
            self.log_test("Test POS Payment Methods", True, f"All payment methods working: {successful_methods}")
        else:
            failed_methods = [m for m in payment_methods if m not in successful_methods]
            self.log_test("Test POS Payment Methods", False, f"Failed methods: {failed_methods}, Successful: {successful_methods}")

    # NEW MODULE TESTS - SERVICE BOOKING
    def test_service_bookings_get(self):
        """Test get service bookings endpoint"""
        if not self.token:
            self.log_test("Get Service Bookings", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/services/bookings?limit=10")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                statuses = list(set(booking.get("status", "Unknown") for booking in data))
                self.log_test("Get Service Bookings", True, f"Retrieved {count} service bookings with statuses: {statuses}")
            else:
                self.log_test("Get Service Bookings", True, "No service bookings found")
        else:
            self.log_test("Get Service Bookings", False, f"Status: {status_code}", data)

    def test_service_bookings_create(self):
        """Test create service booking endpoint"""
        if not self.token:
            self.log_test("Create Service Booking", False, "No token available - login failed")
            return
            
        booking_data = {
            "client_name": "Kigali Business Center",
            "client_email": "admin@kigalibiz.rw",
            "client_phone": "+250788555444",
            "service_type": "network_installation",
            "description": "Complete network infrastructure setup for new office",
            "preferred_date": "2025-01-20T09:00:00",
            "location": "Kimisagara, Kigali",
            "urgency": "high",
            "estimated_duration": 8
        }
        
        success, data, status_code = self.make_request("POST", "/services/bookings", booking_data)
        
        if success and status_code == 200 and data.get("success"):
            booking_id = data.get("id")
            self.log_test("Create Service Booking", True, f"Created service booking with ID: {booking_id}")
            return booking_id
        else:
            self.log_test("Create Service Booking", False, f"Status: {status_code}", data)
            return None

    def test_service_bookings_update(self):
        """Test update service booking endpoint"""
        if not self.token:
            self.log_test("Update Service Booking", False, "No token available - login failed")
            return
            
        # First create a booking to update
        booking_id = self.test_service_bookings_create()
        if not booking_id:
            # Try to get an existing booking
            success, bookings, _ = self.make_request("GET", "/services/bookings?limit=1")
            if success and bookings and len(bookings) > 0:
                booking_id = bookings[0].get("id")
            else:
                self.log_test("Update Service Booking", False, "No booking ID available for testing")
                return
        
        update_data = {
            "status": "in_progress",
            "technician_notes": "Started network assessment and planning"
        }
        
        success, data, status_code = self.make_request("PUT", f"/services/bookings/{booking_id}", update_data)
        
        if success and status_code == 200 and data.get("success"):
            self.log_test("Update Service Booking", True, f"Updated service booking {booking_id}")
        else:
            self.log_test("Update Service Booking", False, f"Status: {status_code}", data)

    def test_service_types(self):
        """Test different service types in bookings"""
        if not self.token:
            self.log_test("Test Service Types", False, "No token available - login failed")
            return
            
        service_types = ["it_support", "network_installation", "starlink_installation", "software_development", "consultation"]
        successful_types = []
        
        for service_type in service_types:
            booking_data = {
                "client_name": f"Test Client {service_type}",
                "client_email": f"test{service_type}@example.rw",
                "client_phone": "+250788000111",
                "service_type": service_type,
                "description": f"Test booking for {service_type} service",
                "preferred_date": "2025-01-25T10:00:00",
                "location": "Test Location",
                "urgency": "normal"
            }
            
            success, data, status_code = self.make_request("POST", "/services/bookings", booking_data)
            if success and status_code == 200:
                successful_types.append(service_type)
        
        if len(successful_types) == len(service_types):
            self.log_test("Test Service Types", True, f"All service types working: {successful_types}")
        else:
            failed_types = [t for t in service_types if t not in successful_types]
            self.log_test("Test Service Types", False, f"Failed types: {failed_types}, Successful: {successful_types}")

    # NEW MODULE TESTS - FINANCE MODULE
    def test_financial_transactions_get(self):
        """Test get financial transactions endpoint"""
        if not self.token:
            self.log_test("Get Financial Transactions", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/finance/transactions?limit=10")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                transaction_types = list(set(transaction.get("transaction_type", "Unknown") for transaction in data))
                self.log_test("Get Financial Transactions", True, f"Retrieved {count} financial transactions of types: {transaction_types}")
            else:
                self.log_test("Get Financial Transactions", True, "No financial transactions found")
        else:
            self.log_test("Get Financial Transactions", False, f"Status: {status_code}", data)

    def test_financial_transactions_create(self):
        """Test create financial transaction endpoint"""
        if not self.token:
            self.log_test("Create Financial Transaction", False, "No token available - login failed")
            return
            
        transaction_data = {
            "transaction_type": "income",
            "category": "sales",
            "amount": 150000.0,
            "description": "Product sales revenue for January",
            "reference": "SALES-JAN-2025-001",
            "payment_method": "bank_transfer"
        }
        
        success, data, status_code = self.make_request("POST", "/finance/transactions", transaction_data)
        
        if success and status_code == 200 and data.get("success"):
            transaction_id = data.get("id")
            self.log_test("Create Financial Transaction", True, f"Created financial transaction with ID: {transaction_id}")
        else:
            self.log_test("Create Financial Transaction", False, f"Status: {status_code}", data)

    def test_financial_summary(self):
        """Test get financial summary endpoint"""
        if not self.token:
            self.log_test("Get Financial Summary", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/finance/summary")
        
        if success and status_code == 200:
            summary_keys = ["total_income", "total_expenses", "net_profit", "transaction_count"]
            has_required_keys = all(key in data for key in summary_keys)
            
            if has_required_keys:
                summary = {
                    "Total Income": data.get("total_income", 0),
                    "Total Expenses": data.get("total_expenses", 0),
                    "Net Profit": data.get("net_profit", 0),
                    "Transactions": data.get("transaction_count", 0)
                }
                self.log_test("Get Financial Summary", True, f"Retrieved financial summary: {summary}")
            else:
                self.log_test("Get Financial Summary", False, f"Missing required keys in response: {data}")
        else:
            self.log_test("Get Financial Summary", False, f"Status: {status_code}", data)

    def test_financial_transaction_types(self):
        """Test different financial transaction types"""
        if not self.token:
            self.log_test("Test Financial Transaction Types", False, "No token available - login failed")
            return
            
        transaction_types = [
            {"type": "expense", "category": "office_supplies", "amount": 50000.0, "description": "Office supplies purchase"},
            {"type": "income", "category": "services", "amount": 200000.0, "description": "Service consultation fee"},
            {"type": "expense", "category": "utilities", "amount": 75000.0, "description": "Monthly electricity bill"},
            {"type": "income", "category": "sales", "amount": 300000.0, "description": "Hardware sales revenue"}
        ]
        
        successful_types = []
        
        for trans in transaction_types:
            transaction_data = {
                "transaction_type": trans["type"],
                "category": trans["category"],
                "amount": trans["amount"],
                "description": trans["description"],
                "reference": f"TEST-{trans['type'].upper()}-{trans['category'].upper()}",
                "payment_method": "bank_transfer"
            }
            
            success, data, status_code = self.make_request("POST", "/finance/transactions", transaction_data)
            if success and status_code == 200:
                successful_types.append(f"{trans['type']}-{trans['category']}")
        
        if len(successful_types) == len(transaction_types):
            self.log_test("Test Financial Transaction Types", True, f"All transaction types working: {successful_types}")
        else:
            expected_types = [f"{t['type']}-{t['category']}" for t in transaction_types]
            failed_types = [t for t in expected_types if t not in successful_types]
            self.log_test("Test Financial Transaction Types", False, f"Failed types: {failed_types}, Successful: {successful_types}")

    def run_all_tests(self):
        """Run all backend tests in sequence"""
        print("=" * 80)
        print("AFRO EXPERTS ERP & POS SYSTEM - BACKEND API TESTING")
        print("=" * 80)
        print(f"Testing against: {self.base_url}")
        print(f"Demo Account: {DEMO_ADMIN_EMAIL}")
        print("=" * 80)
        print()
        
        # Core system tests
        self.test_health_check()
        
        # Authentication tests
        self.test_authentication_login()
        self.test_authentication_me()
        
        # Dashboard tests
        self.test_dashboard_stats()
        self.test_dashboard_recent_transactions()
        
        # Product management tests
        self.test_products_get()
        self.test_products_low_stock()
        created_product_id = self.test_products_create()
        self.test_products_update_stock(created_product_id)
        
        # Order management tests
        self.test_orders_get()
        self.test_orders_create()
        
        # Client management tests
        self.test_clients_get()
        self.test_clients_create()
        
        # NEW MODULE TESTS - Inventory Management
        print("\n" + "="*50)
        print("TESTING NEW MODULE: INVENTORY MANAGEMENT")
        print("="*50)
        self.test_inventory_movements_get()
        self.test_inventory_movements_create()
        self.test_inventory_movements_types()
        
        # NEW MODULE TESTS - POS System
        print("\n" + "="*50)
        print("TESTING NEW MODULE: POS SYSTEM")
        print("="*50)
        self.test_pos_transactions_get()
        self.test_pos_transactions_create()
        self.test_pos_payment_methods()
        
        # NEW MODULE TESTS - Service Booking
        print("\n" + "="*50)
        print("TESTING NEW MODULE: SERVICE BOOKING")
        print("="*50)
        self.test_service_bookings_get()
        self.test_service_bookings_create()
        self.test_service_bookings_update()
        self.test_service_types()
        
        # NEW MODULE TESTS - Finance Module
        print("\n" + "="*50)
        print("TESTING NEW MODULE: FINANCE MODULE")
        print("="*50)
        self.test_financial_transactions_get()
        self.test_financial_transactions_create()
        self.test_financial_summary()
        self.test_financial_transaction_types()
        
        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        if failed_tests > 0:
            print("FAILED TESTS:")
            print("-" * 40)
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test']}: {result['details']}")
            print()
        
        print("CRITICAL ISSUES:")
        print("-" * 40)
        critical_failures = []
        
        # Check for critical authentication failures
        auth_tests = [r for r in self.test_results if "Authentication" in r["test"]]
        if any(not r["success"] for r in auth_tests):
            critical_failures.append("Authentication system not working properly")
        
        # Check for critical API failures
        api_tests = [r for r in self.test_results if r["test"] in ["Health Check", "Dashboard Stats", "Get Products"]]
        if any(not r["success"] for r in api_tests):
            critical_failures.append("Core API endpoints not responding correctly")
        
        if critical_failures:
            for issue in critical_failures:
                print(f"🚨 {issue}")
        else:
            print("✅ No critical issues detected")
        
        print("=" * 80)

if __name__ == "__main__":
    tester = BackendTester()
    tester.run_all_tests()