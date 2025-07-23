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
BASE_URL = "https://fd13ed92-e3ec-4ec8-a30a-0a39fdb4963a.preview.emergentagent.com/api"
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
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=request_headers, timeout=30)
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
            
        # First get a client to use in the order
        success, clients, _ = self.make_request("GET", "/clients?limit=1")
        if not success or not clients or len(clients) == 0:
            self.log_test("Create Order", False, "No clients available for order creation")
            return
            
        client = clients[0]
        client_name = client.get("name", "Test Client")
        client_email = client.get("email")
        client_phone = client.get("phone")
        
        # Get products to use in the order
        success, products, _ = self.make_request("GET", "/products?limit=2")
        if not success or not products or len(products) == 0:
            self.log_test("Create Order", False, "No products available for order creation")
            return
            
        # Create order with multiple items
        items = []
        for i, product in enumerate(products[:2]):
            items.append({
                "product_id": product.get("id"),
                "quantity": i + 1,  # 1, 2 quantities
                "unit_price": product.get("price", 10000)
            })
        
        order_data = {
            "client_name": client_name,
            "client_email": client_email,
            "client_phone": client_phone,
            "items": items,
            "payment_method": "cash",
            "notes": "Test order with multiple items for API validation"
        }
        
        success, data, status_code = self.make_request("POST", "/orders", order_data)
        
        if success and status_code == 200 and data.get("id"):
            order_id = data.get("id")
            order_number = data.get("order_number")
            self.log_test("Create Order", True, f"Created order {order_number} with ID: {order_id}")
            return order_id
        else:
            self.log_test("Create Order", False, f"Status: {status_code}", data)
            return None

    # ENHANCED ORDER MANAGEMENT API TESTS
    def test_order_get_single(self):
        """Test GET /api/orders/{order_id} - Get single order details"""
        if not self.token:
            self.log_test("Get Single Order", False, "No token available - login failed")
            return
            
        # First get an existing order
        success, orders, _ = self.make_request("GET", "/orders?limit=1")
        if not success or not orders or len(orders) == 0:
            self.log_test("Get Single Order", False, "No orders available for single order test")
            return
            
        order_id = orders[0].get("id")
        
        success, data, status_code = self.make_request("GET", f"/orders/{order_id}")
        
        if success and status_code == 200 and data.get("id"):
            order_number = data.get("order_number", "Unknown")
            status_value = data.get("status", "Unknown")
            self.log_test("Get Single Order", True, f"Retrieved order {order_number} with status: {status_value}")
        else:
            self.log_test("Get Single Order", False, f"Status: {status_code}", data)

    def test_order_update(self):
        """Test PUT /api/orders/{order_id} - Update order details"""
        if not self.token:
            self.log_test("Update Order", False, "No token available - login failed")
            return
            
        # First get an existing order
        success, orders, _ = self.make_request("GET", "/orders?limit=1")
        if not success or not orders or len(orders) == 0:
            self.log_test("Update Order", False, "No orders available for update test")
            return
            
        order_id = orders[0].get("id")
        
        update_data = {
            "status": "processing",
            "payment_method": "card",
            "notes": "Updated order details via API test"
        }
        
        success, data, status_code = self.make_request("PUT", f"/orders/{order_id}", update_data)
        
        if success and status_code == 200 and data.get("id"):
            updated_status = data.get("status", "Unknown")
            self.log_test("Update Order", True, f"Updated order {order_id} to status: {updated_status}")
            return order_id
        else:
            self.log_test("Update Order", False, f"Status: {status_code}", data)
            return None

    def test_order_status_update(self):
        """Test PUT /api/orders/{order_id}/status - Update order status specifically"""
        if not self.token:
            self.log_test("Update Order Status", False, "No token available - login failed")
            return
            
        # First get an existing order
        success, orders, _ = self.make_request("GET", "/orders?limit=1")
        if not success or not orders or len(orders) == 0:
            self.log_test("Update Order Status", False, "No orders available for status update test")
            return
            
        order_id = orders[0].get("id")
        
        status_update = {
            "status": "processing"
        }
        
        success, data, status_code = self.make_request("PUT", f"/orders/{order_id}/status", status_update)
        
        if success and status_code == 200:
            message = data.get("message", "Status updated")
            self.log_test("Update Order Status", True, f"Order status updated: {message}")
        else:
            self.log_test("Update Order Status", False, f"Status: {status_code}", data)

    def test_orders_by_status(self):
        """Test GET /api/orders/status/{status} - Filter orders by status"""
        if not self.token:
            self.log_test("Get Orders by Status", False, "No token available - login failed")
            return
            
        # Test different statuses
        statuses_to_test = ["pending", "processing", "delivered"]
        successful_statuses = []
        
        for status in statuses_to_test:
            success, data, status_code = self.make_request("GET", f"/orders/status/{status}")
            
            if success and status_code == 200 and isinstance(data, list):
                count = len(data)
                successful_statuses.append(f"{status}({count})")
        
        if len(successful_statuses) > 0:
            self.log_test("Get Orders by Status", True, f"Retrieved orders by status: {successful_statuses}")
        else:
            self.log_test("Get Orders by Status", False, "Failed to retrieve orders by any status")

    def test_order_delete_validation(self):
        """Test DELETE /api/orders/{order_id} - Test deletion with proper validation"""
        if not self.token:
            self.log_test("Delete Order Validation", False, "No token available - login failed")
            return
            
        # First create a test order to delete
        order_id = self.test_orders_create()
        if not order_id:
            self.log_test("Delete Order Validation", False, "Could not create test order for deletion")
            return
        
        # Try to delete the order (should succeed for non-delivered orders)
        success, data, status_code = self.make_request("DELETE", f"/orders/{order_id}")
        
        if success and status_code == 200:
            message = data.get("message", "Order deleted")
            self.log_test("Delete Order Validation", True, f"Successfully deleted order: {message}")
        else:
            self.log_test("Delete Order Validation", False, f"Status: {status_code}", data)

    def test_order_delete_delivered_validation(self):
        """Test DELETE validation - Should fail for delivered orders"""
        if not self.token:
            self.log_test("Delete Delivered Order Validation", False, "No token available - login failed")
            return
            
        # First create a test order
        order_id = self.test_orders_create()
        if not order_id:
            self.log_test("Delete Delivered Order Validation", False, "Could not create test order")
            return
        
        # Update order status to delivered
        status_update = {"status": "delivered"}
        success, _, _ = self.make_request("PUT", f"/orders/{order_id}/status", status_update)
        
        if not success:
            self.log_test("Delete Delivered Order Validation", False, "Could not update order to delivered status")
            return
        
        # Now try to delete the delivered order (should fail)
        success, data, status_code = self.make_request("DELETE", f"/orders/{order_id}")
        
        if not success and status_code == 400:
            error_detail = data.get("detail", "Unknown error")
            if "Cannot delete delivered orders" in error_detail:
                self.log_test("Delete Delivered Order Validation", True, "Correctly prevented deletion of delivered order")
            else:
                self.log_test("Delete Delivered Order Validation", False, f"Wrong error message: {error_detail}")
        else:
            self.log_test("Delete Delivered Order Validation", False, f"Should have failed but got status: {status_code}")

    def test_order_stock_validation(self):
        """Test stock validation when creating orders"""
        if not self.token:
            self.log_test("Order Stock Validation", False, "No token available - login failed")
            return
            
        # Get a product with low stock
        success, products, _ = self.make_request("GET", "/products/low-stock?limit=1")
        if not success or not products or len(products) == 0:
            # Get any product and check its stock
            success, products, _ = self.make_request("GET", "/products?limit=1")
            if not success or not products:
                self.log_test("Order Stock Validation", False, "No products available for stock validation test")
                return
        
        product = products[0]
        product_id = product.get("id")
        current_stock = product.get("current_stock", 0)
        
        # Get a client
        success, clients, _ = self.make_request("GET", "/clients?limit=1")
        if not success or not clients:
            self.log_test("Order Stock Validation", False, "No clients available for stock validation test")
            return
        
        client = clients[0]
        client_name = client.get("name", "Test Client")
        client_email = client.get("email")
        client_phone = client.get("phone")
        
        # Try to order more than available stock
        excessive_quantity = current_stock + 10
        
        order_data = {
            "client_name": client_name,
            "client_email": client_email,
            "client_phone": client_phone,
            "items": [{
                "product_id": product_id,
                "quantity": excessive_quantity,
                "unit_price": product.get("price", 10000)
            }],
            "payment_method": "cash",
            "notes": "Test order for stock validation"
        }
        
        success, data, status_code = self.make_request("POST", "/orders", order_data)
        
        if not success and status_code == 400:
            error_detail = data.get("detail", "")
            if "Insufficient stock" in error_detail:
                self.log_test("Order Stock Validation", True, f"Correctly prevented order with insufficient stock: {error_detail}")
            else:
                self.log_test("Order Stock Validation", False, f"Wrong error message: {error_detail}")
        else:
            self.log_test("Order Stock Validation", False, f"Should have failed but got status: {status_code}")

    def test_order_number_generation(self):
        """Test order number generation works correctly"""
        if not self.token:
            self.log_test("Order Number Generation", False, "No token available - login failed")
            return
            
        # Create multiple orders and check order number format
        order_numbers = []
        
        for i in range(3):
            order_id = self.test_orders_create()
            if order_id:
                # Get the created order to check its order number
                success, data, _ = self.make_request("GET", f"/orders/{order_id}")
                if success and data.get("order_number"):
                    order_numbers.append(data.get("order_number"))
        
        if len(order_numbers) >= 2:
            # Check order number format (should be ORD-YYYYMMDD-XXXX)
            import re
            pattern = r"ORD-\d{8}-\d{4}"
            valid_numbers = [num for num in order_numbers if re.match(pattern, num)]
            
            if len(valid_numbers) == len(order_numbers):
                self.log_test("Order Number Generation", True, f"Generated valid order numbers: {order_numbers}")
            else:
                invalid_numbers = [num for num in order_numbers if not re.match(pattern, num)]
                self.log_test("Order Number Generation", False, f"Invalid order number format: {invalid_numbers}")
        else:
            self.log_test("Order Number Generation", False, "Could not create enough orders to test number generation")

    def test_order_stock_deduction(self):
        """Test that stock is properly deducted when creating orders"""
        if not self.token:
            self.log_test("Order Stock Deduction", False, "No token available - login failed")
            return
            
        # Get a product with sufficient stock
        success, products, _ = self.make_request("GET", "/products?limit=1")
        if not success or not products:
            self.log_test("Order Stock Deduction", False, "No products available for stock deduction test")
            return
        
        product = products[0]
        product_id = product.get("id")
        initial_stock = product.get("current_stock", 0)
        
        if initial_stock < 5:
            self.log_test("Order Stock Deduction", False, f"Product has insufficient stock ({initial_stock}) for deduction test")
            return
        
        # Get a client
        success, clients, _ = self.make_request("GET", "/clients?limit=1")
        if not success or not clients:
            self.log_test("Order Stock Deduction", False, "No clients available for stock deduction test")
            return
        
        client = clients[0]
        client_name = client.get("name", "Test Client")
        client_email = client.get("email")
        client_phone = client.get("phone")
        order_quantity = 3
        
        # Create order
        order_data = {
            "client_name": client_name,
            "client_email": client_email,
            "client_phone": client_phone,
            "items": [{
                "product_id": product_id,
                "quantity": order_quantity,
                "unit_price": product.get("price", 10000)
            }],
            "payment_method": "cash",
            "notes": "Test order for stock deduction validation"
        }
        
        success, data, status_code = self.make_request("POST", "/orders", order_data)
        
        if success and status_code == 200:
            # Check if stock was deducted
            success, updated_product, _ = self.make_request("GET", f"/products")
            if success:
                # Find the product in the list
                updated_product_data = None
                for p in updated_product:
                    if p.get("id") == product_id:
                        updated_product_data = p
                        break
                
                if updated_product_data:
                    new_stock = updated_product_data.get("current_stock", 0)
                    expected_stock = initial_stock - order_quantity
                    
                    if new_stock == expected_stock:
                        self.log_test("Order Stock Deduction", True, f"Stock correctly deducted: {initial_stock} → {new_stock}")
                    else:
                        self.log_test("Order Stock Deduction", False, f"Stock deduction incorrect: expected {expected_stock}, got {new_stock}")
                else:
                    self.log_test("Order Stock Deduction", False, "Could not find product after order creation")
            else:
                self.log_test("Order Stock Deduction", False, "Could not retrieve products after order creation")
        else:
            self.log_test("Order Stock Deduction", False, f"Order creation failed: {status_code}")

    def run_enhanced_order_tests(self):
        """Run all enhanced order management tests"""
        print("\n" + "="*60)
        print("TESTING ENHANCED ORDER MANAGEMENT API")
        print("="*60)
        
        # Basic order tests
        self.test_orders_get()
        self.test_orders_create()
        
        # Enhanced order management tests
        self.test_order_get_single()
        self.test_order_update()
        self.test_order_status_update()
        self.test_orders_by_status()
        self.test_order_delete_validation()
        self.test_order_delete_delivered_validation()
        self.test_order_stock_validation()
        self.test_order_number_generation()
        self.test_order_stock_deduction()

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

    # ENHANCED INVENTORY MANAGEMENT API TESTS
    def test_inventory_movements_get(self):
        """Test GET /api/inventory/movements - Get all movements with product details"""
        if not self.token:
            self.log_test("Get Inventory Movements", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/inventory/movements")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                # Check if movements have product details
                first_movement = data[0]
                has_product_details = "product_name" in first_movement and "product_id" in first_movement
                movement_types = list(set(movement.get("movement_type", "Unknown") for movement in data))
                
                if has_product_details:
                    self.log_test("Get Inventory Movements", True, f"Retrieved {count} inventory movements with product details, types: {movement_types}")
                else:
                    self.log_test("Get Inventory Movements", False, f"Retrieved {count} movements but missing product details")
            else:
                self.log_test("Get Inventory Movements", True, "No inventory movements found")
        else:
            self.log_test("Get Inventory Movements", False, f"Status: {status_code}", data)

    def test_inventory_movement_single(self):
        """Test GET /api/inventory/movements/{movement_id} - Get single movement details"""
        if not self.token:
            self.log_test("Get Single Movement", False, "No token available - login failed")
            return
            
        # First get existing movements to test with
        success, movements, _ = self.make_request("GET", "/inventory/movements")
        if not success or not movements or len(movements) == 0:
            self.log_test("Get Single Movement", False, "No movements available for single movement test")
            return
            
        movement_id = movements[0].get("id")
        
        success, data, status_code = self.make_request("GET", f"/inventory/movements/{movement_id}")
        
        if success and status_code == 200 and data.get("id"):
            movement_type = data.get("movement_type", "Unknown")
            quantity = data.get("quantity", 0)
            self.log_test("Get Single Movement", True, f"Retrieved movement {movement_id}: {movement_type}, quantity: {quantity}")
        else:
            self.log_test("Get Single Movement", False, f"Status: {status_code}", data)

    def test_inventory_movements_create(self):
        """Test POST /api/inventory/movements - Create new movement with stock validation"""
        if not self.token:
            self.log_test("Create Inventory Movement", False, "No token available - login failed")
            return
            
        # First get a product to use in the movement
        success, products, _ = self.make_request("GET", "/products")
        if not success or not products or len(products) == 0:
            self.log_test("Create Inventory Movement", False, "No products available for inventory movement")
            return
            
        product = products[0]
        product_id = product.get("id")
        initial_stock = product.get("current_stock", 0)
        
        movement_data = {
            "product_id": product_id,
            "movement_type": "stock_in",
            "quantity": 10,
            "unit_cost": 50000.0,
            "reference": "TEST-STOCK-IN-001",
            "reason": "Test stock in movement for API validation"
        }
        
        success, data, status_code = self.make_request("POST", "/inventory/movements", movement_data)
        
        if success and status_code == 200 and data.get("id"):
            movement_id = data.get("id")
            
            # Verify stock was updated
            success, updated_products, _ = self.make_request("GET", "/products")
            if success:
                updated_product = next((p for p in updated_products if p.get("id") == product_id), None)
                if updated_product:
                    new_stock = updated_product.get("current_stock", 0)
                    expected_stock = initial_stock + 10
                    
                    if new_stock == expected_stock:
                        self.log_test("Create Inventory Movement", True, f"Created movement {movement_id}, stock updated: {initial_stock} → {new_stock}")
                        return movement_id
                    else:
                        self.log_test("Create Inventory Movement", False, f"Stock not updated correctly: expected {expected_stock}, got {new_stock}")
                else:
                    self.log_test("Create Inventory Movement", False, "Could not find product after movement creation")
            else:
                self.log_test("Create Inventory Movement", False, "Could not verify stock update")
        else:
            self.log_test("Create Inventory Movement", False, f"Status: {status_code}", data)
            return None

    def test_inventory_movement_update(self):
        """Test PUT /api/inventory/movements/{movement_id} - Update movement details"""
        if not self.token:
            self.log_test("Update Inventory Movement", False, "No token available - login failed")
            return
            
        # First get existing movements to test with
        success, movements, _ = self.make_request("GET", "/inventory/movements")
        if not success or not movements or len(movements) == 0:
            self.log_test("Update Inventory Movement", False, "No movements available for update test")
            return
            
        movement_id = movements[0].get("id")
        
        update_data = {
            "notes": "Updated movement notes via API test",
            "reference_number": "UPDATED-REF-001"
        }
        
        success, data, status_code = self.make_request("PUT", f"/inventory/movements/{movement_id}", update_data)
        
        if success and status_code == 200 and data.get("id"):
            updated_notes = data.get("notes", "")
            self.log_test("Update Inventory Movement", True, f"Updated movement {movement_id}: {updated_notes}")
        else:
            self.log_test("Update Inventory Movement", False, f"Status: {status_code}", data)

    def test_inventory_movement_delete(self):
        """Test DELETE /api/inventory/movements/{movement_id} - Delete movement and reverse stock changes"""
        if not self.token:
            self.log_test("Delete Inventory Movement", False, "No token available - login failed")
            return
            
        # First create a movement to delete
        movement_id = self.test_inventory_movements_create()
        if not movement_id:
            self.log_test("Delete Inventory Movement", False, "Could not create movement for deletion test")
            return
        
        # Get product stock before deletion
        success, movement_data, _ = self.make_request("GET", f"/inventory/movements/{movement_id}")
        if not success:
            self.log_test("Delete Inventory Movement", False, "Could not get movement data before deletion")
            return
            
        product_id = movement_data.get("product_id")
        success, products, _ = self.make_request("GET", "/products")
        if success:
            product = next((p for p in products if p.get("id") == product_id), None)
            if product:
                stock_before_delete = product.get("current_stock", 0)
            else:
                self.log_test("Delete Inventory Movement", False, "Could not find product before deletion")
                return
        else:
            self.log_test("Delete Inventory Movement", False, "Could not get products before deletion")
            return
        
        # Delete the movement
        success, data, status_code = self.make_request("DELETE", f"/inventory/movements/{movement_id}")
        
        if success and status_code == 200:
            # Verify stock was reversed
            success, updated_products, _ = self.make_request("GET", "/products")
            if success:
                updated_product = next((p for p in updated_products if p.get("id") == product_id), None)
                if updated_product:
                    stock_after_delete = updated_product.get("current_stock", 0)
                    # Since we created a stock_in movement of 10, deleting should reduce stock by 10
                    expected_stock = stock_before_delete - 10
                    
                    if stock_after_delete == expected_stock:
                        self.log_test("Delete Inventory Movement", True, f"Movement deleted and stock reversed: {stock_before_delete} → {stock_after_delete}")
                    else:
                        self.log_test("Delete Inventory Movement", False, f"Stock not reversed correctly: expected {expected_stock}, got {stock_after_delete}")
                else:
                    self.log_test("Delete Inventory Movement", False, "Could not find product after deletion")
            else:
                self.log_test("Delete Inventory Movement", False, "Could not verify stock reversal")
        else:
            self.log_test("Delete Inventory Movement", False, f"Status: {status_code}", data)

    def test_inventory_movements_by_product(self):
        """Test GET /api/inventory/movements/product/{product_id} - Filter movements by product"""
        if not self.token:
            self.log_test("Get Movements by Product", False, "No token available - login failed")
            return
            
        # Get a product that has movements
        success, products, _ = self.make_request("GET", "/products")
        if not success or not products or len(products) == 0:
            self.log_test("Get Movements by Product", False, "No products available for product filter test")
            return
            
        product_id = products[0].get("id")
        product_name = products[0].get("name", "Unknown")
        
        success, data, status_code = self.make_request("GET", f"/inventory/movements/product/{product_id}")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                # Verify all movements are for the correct product
                correct_product = all(movement.get("product_id") == product_id for movement in data)
                if correct_product:
                    movement_types = list(set(movement.get("movement_type", "Unknown") for movement in data))
                    self.log_test("Get Movements by Product", True, f"Retrieved {count} movements for product '{product_name}', types: {movement_types}")
                else:
                    self.log_test("Get Movements by Product", False, "Retrieved movements contain wrong product IDs")
            else:
                self.log_test("Get Movements by Product", True, f"No movements found for product '{product_name}'")
        else:
            self.log_test("Get Movements by Product", False, f"Status: {status_code}", data)

    def test_inventory_movements_by_type(self):
        """Test GET /api/inventory/movements/type/{movement_type} - Filter movements by type"""
        if not self.token:
            self.log_test("Get Movements by Type", False, "No token available - login failed")
            return
            
        movement_types_to_test = ["stock_in", "stock_out", "adjustment"]
        successful_types = []
        
        for movement_type in movement_types_to_test:
            success, data, status_code = self.make_request("GET", f"/inventory/movements/type/{movement_type}")
            
            if success and status_code == 200 and isinstance(data, list):
                count = len(data)
                if count > 0:
                    # Verify all movements are of the correct type
                    correct_type = all(movement.get("movement_type") == movement_type for movement in data)
                    if correct_type:
                        successful_types.append(f"{movement_type}({count})")
                    else:
                        self.log_test("Get Movements by Type", False, f"Retrieved movements contain wrong movement types for {movement_type}")
                        return
                else:
                    successful_types.append(f"{movement_type}(0)")
        
        if len(successful_types) == len(movement_types_to_test):
            self.log_test("Get Movements by Type", True, f"Successfully filtered movements by type: {successful_types}")
        else:
            self.log_test("Get Movements by Type", False, f"Failed to filter some movement types")

    def test_inventory_summary(self):
        """Test GET /api/inventory/summary - Get inventory summary statistics"""
        if not self.token:
            self.log_test("Get Inventory Summary", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/inventory/summary")
        
        if success and status_code == 200:
            required_keys = ["total_stock_value", "low_stock_items", "total_products", "recent_movements", "movement_counts"]
            has_required_keys = all(key in data for key in required_keys)
            
            if has_required_keys:
                summary = {
                    "Total Stock Value": data.get("total_stock_value", 0),
                    "Low Stock Items": data.get("low_stock_items", 0),
                    "Total Products": data.get("total_products", 0),
                    "Recent Movements": data.get("recent_movements", 0),
                    "Movement Counts": data.get("movement_counts", {})
                }
                self.log_test("Get Inventory Summary", True, f"Retrieved inventory summary: {summary}")
            else:
                missing_keys = [key for key in required_keys if key not in data]
                self.log_test("Get Inventory Summary", False, f"Missing required keys: {missing_keys}")
        else:
            self.log_test("Get Inventory Summary", False, f"Status: {status_code}", data)

    def test_inventory_stock_validation(self):
        """Test stock validation for stock_out movements"""
        if not self.token:
            self.log_test("Inventory Stock Validation", False, "No token available - login failed")
            return
            
        # Get a product with low stock
        success, products, _ = self.make_request("GET", "/products")
        if not success or not products or len(products) == 0:
            self.log_test("Inventory Stock Validation", False, "No products available for stock validation test")
            return
            
        product = products[0]
        product_id = product.get("id")
        current_stock = product.get("current_stock", 0)
        
        # Try to create a stock_out movement with more quantity than available
        excessive_quantity = current_stock + 10
        
        movement_data = {
            "product_id": product_id,
            "movement_type": "stock_out",
            "quantity": excessive_quantity,
            "unit_cost": 25000.0,
            "reference": "TEST-VALIDATION-001",
            "reason": "Test stock validation for insufficient stock"
        }
        
        success, data, status_code = self.make_request("POST", "/inventory/movements", movement_data)
        
        if not success and status_code == 400:
            error_detail = data.get("detail", "")
            if "Insufficient stock" in error_detail:
                self.log_test("Inventory Stock Validation", True, f"Correctly prevented stock_out with insufficient stock: {error_detail}")
            else:
                self.log_test("Inventory Stock Validation", False, f"Wrong error message: {error_detail}")
        else:
            self.log_test("Inventory Stock Validation", False, f"Should have failed but got status: {status_code}")

    def test_inventory_movement_types_comprehensive(self):
        """Test all inventory movement types with stock updates"""
        if not self.token:
            self.log_test("Test All Movement Types", False, "No token available - login failed")
            return
            
        # Get a product for testing
        success, products, _ = self.make_request("GET", "/products")
        if not success or not products or len(products) == 0:
            self.log_test("Test All Movement Types", False, "No products available for movement testing")
            return
            
        product = products[0]
        product_id = product.get("id")
        initial_stock = product.get("current_stock", 0)
        
        movement_types = [
            {"type": "stock_in", "quantity": 5, "expected_change": +5},
            {"type": "stock_out", "quantity": 2, "expected_change": -2},
            {"type": "adjustment", "quantity": initial_stock + 8, "expected_change": 8},  # Adjustment sets absolute value
            {"type": "damaged", "quantity": 1, "expected_change": -1}
        ]
        
        successful_types = []
        current_stock = initial_stock
        
        for movement in movement_types:
            movement_data = {
                "product_id": product_id,
                "movement_type": movement["type"],
                "quantity": movement["quantity"],
                "unit_cost": 25000.0,
                "reference": f"TEST-{movement['type'].upper()}-001",
                "reason": f"Test {movement['type']} movement"
            }
            
            success, data, status_code = self.make_request("POST", "/inventory/movements", movement_data)
            
            if success and status_code == 200:
                # Verify stock change
                success, updated_products, _ = self.make_request("GET", "/products")
                if success:
                    updated_product = next((p for p in updated_products if p.get("id") == product_id), None)
                    if updated_product:
                        new_stock = updated_product.get("current_stock", 0)
                        
                        if movement["type"] == "adjustment":
                            expected_stock = movement["quantity"]  # Adjustment sets absolute value
                        else:
                            expected_stock = current_stock + movement["expected_change"]
                        
                        if new_stock == expected_stock:
                            successful_types.append(f"{movement['type']}({movement['quantity']})")
                            current_stock = new_stock
                        else:
                            self.log_test("Test All Movement Types", False, f"Stock not updated correctly for {movement['type']}: expected {expected_stock}, got {new_stock}")
                            return
        
        if len(successful_types) == len(movement_types):
            self.log_test("Test All Movement Types", True, f"All movement types working with correct stock updates: {successful_types}")
        else:
            failed_types = [m["type"] for m in movement_types if f"{m['type']}({m['quantity']})" not in successful_types]
            self.log_test("Test All Movement Types", False, f"Failed types: {failed_types}, Successful: {successful_types}")

    def run_enhanced_inventory_tests(self):
        """Run all enhanced inventory management tests"""
        print("\n" + "="*60)
        print("TESTING ENHANCED INVENTORY MANAGEMENT API")
        print("="*60)
        
        # Core inventory tests
        self.test_inventory_movements_get()
        self.test_inventory_movement_single()
        self.test_inventory_movements_create()
        self.test_inventory_movement_update()
        self.test_inventory_movement_delete()
        
        # Filtering tests
        self.test_inventory_movements_by_product()
        self.test_inventory_movements_by_type()
        
        # Summary and validation tests
        self.test_inventory_summary()
        self.test_inventory_stock_validation()
        self.test_inventory_movement_types_comprehensive()

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
        
        if success and status_code == 200 and data.get("id"):
            booking_id = data.get("id")
            booking_number = data.get("booking_number", "Unknown")
            self.log_test("Create Service Booking", True, f"Created service booking {booking_number} with ID: {booking_id}")
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
        
        if success and status_code == 200 and data.get("id"):
            updated_status = data.get("status", "Unknown")
            self.log_test("Update Service Booking", True, f"Updated service booking {booking_id} to status: {updated_status}")
        else:
            self.log_test("Update Service Booking", False, f"Status: {status_code}", data)

    def test_service_types(self):
        """Test different service types in bookings"""
        if not self.token:
            self.log_test("Test Service Types", False, "No token available - login failed")
            return
            
        service_types = ["it_support", "network_installation", "starlink_installation", "software_development", "consultation", "maintenance", "training"]
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
                "cost_estimate": 75000.0,
                "notes": f"Test booking for {service_type} validation"
            }
            
            success, data, status_code = self.make_request("POST", "/services/bookings", booking_data)
            if success and status_code == 200 and data.get("id"):
                successful_types.append(service_type)
        
        if len(successful_types) == len(service_types):
            self.log_test("Test Service Types", True, f"All service types working: {successful_types}")
        else:
            failed_types = [t for t in service_types if t not in successful_types]
            self.log_test("Test Service Types", False, f"Failed types: {failed_types}, Successful: {successful_types}")

    # ENHANCED SERVICE BOOKING MANAGEMENT API TESTS
    def test_service_booking_single(self):
        """Test GET /api/services/bookings/{booking_id} - Get single booking details"""
        if not self.token:
            self.log_test("Get Single Service Booking", False, "No token available - login failed")
            return
            
        # First get existing bookings to test with
        success, bookings, _ = self.make_request("GET", "/services/bookings")
        if not success or not bookings or len(bookings) == 0:
            self.log_test("Get Single Service Booking", False, "No bookings available for single booking test")
            return
            
        booking_id = bookings[0].get("id")
        
        success, data, status_code = self.make_request("GET", f"/services/bookings/{booking_id}")
        
        if success and status_code == 200 and data.get("id"):
            booking_number = data.get("booking_number", "Unknown")
            service_type = data.get("service_type", "Unknown")
            status_value = data.get("status", "Unknown")
            self.log_test("Get Single Service Booking", True, f"Retrieved booking {booking_number}: {service_type}, status: {status_value}")
        else:
            self.log_test("Get Single Service Booking", False, f"Status: {status_code}", data)

    def test_service_booking_delete_validation(self):
        """Test DELETE /api/services/bookings/{booking_id} - Delete booking with validation"""
        if not self.token:
            self.log_test("Delete Service Booking Validation", False, "No token available - login failed")
            return
            
        # First create a test booking to delete
        booking_data = {
            "client_name": "Test Delete Client",
            "client_email": "testdelete@example.rw",
            "client_phone": "+250788999888",
            "service_type": "consultation",
            "description": "Test booking for deletion validation",
            "preferred_date": "2025-01-30T14:00:00",
            "location": "Test Location",
            "cost_estimate": 50000.0,
            "notes": "Test booking created for deletion test"
        }
        
        success, data, status_code = self.make_request("POST", "/services/bookings", booking_data)
        if not success or not data.get("id"):
            self.log_test("Delete Service Booking Validation", False, "Could not create test booking for deletion")
            return
            
        booking_id = data.get("id")
        
        # Try to delete the booking (should succeed for pending bookings)
        success, data, status_code = self.make_request("DELETE", f"/services/bookings/{booking_id}")
        
        if success and status_code == 200:
            message = data.get("message", "Booking deleted")
            self.log_test("Delete Service Booking Validation", True, f"Successfully deleted booking: {message}")
        else:
            self.log_test("Delete Service Booking Validation", False, f"Status: {status_code}", data)

    def test_service_booking_delete_in_progress_validation(self):
        """Test DELETE validation - Should fail for in_progress/completed bookings"""
        if not self.token:
            self.log_test("Delete In-Progress Booking Validation", False, "No token available - login failed")
            return
            
        # First create a test booking
        booking_data = {
            "client_name": "Test In-Progress Client",
            "client_email": "testinprogress@example.rw",
            "client_phone": "+250788777666",
            "service_type": "it_support",
            "description": "Test booking for in-progress deletion validation",
            "preferred_date": "2025-01-28T11:00:00",
            "location": "Test Location",
            "cost_estimate": 60000.0,
            "notes": "Test booking for in-progress deletion validation"
        }
        
        success, data, status_code = self.make_request("POST", "/services/bookings", booking_data)
        if not success or not data.get("id"):
            self.log_test("Delete In-Progress Booking Validation", False, "Could not create test booking")
            return
            
        booking_id = data.get("id")
        
        # Update booking status to in_progress
        status_update = {"status": "in_progress"}
        success, _, _ = self.make_request("PUT", f"/services/bookings/{booking_id}/status", status_update)
        
        if not success:
            self.log_test("Delete In-Progress Booking Validation", False, "Could not update booking to in_progress status")
            return
        
        # Now try to delete the in_progress booking (should fail)
        success, data, status_code = self.make_request("DELETE", f"/services/bookings/{booking_id}")
        
        if not success and status_code == 400:
            error_detail = data.get("detail", "Unknown error")
            if "Cannot delete booking that is in progress or completed" in error_detail:
                self.log_test("Delete In-Progress Booking Validation", True, "Correctly prevented deletion of in_progress booking")
            else:
                self.log_test("Delete In-Progress Booking Validation", False, f"Wrong error message: {error_detail}")
        else:
            self.log_test("Delete In-Progress Booking Validation", False, f"Should have failed but got status: {status_code}")

    def test_service_bookings_by_status(self):
        """Test GET /api/services/bookings/status/{status} - Filter bookings by status"""
        if not self.token:
            self.log_test("Get Bookings by Status", False, "No token available - login failed")
            return
            
        # Test different statuses
        statuses_to_test = ["pending", "confirmed", "in_progress", "completed", "cancelled"]
        successful_statuses = []
        
        for status in statuses_to_test:
            success, data, status_code = self.make_request("GET", f"/services/bookings/status/{status}")
            
            if success and status_code == 200 and isinstance(data, list):
                count = len(data)
                # Verify all bookings have the correct status
                if count > 0:
                    correct_status = all(booking.get("status") == status for booking in data)
                    if correct_status:
                        successful_statuses.append(f"{status}({count})")
                    else:
                        self.log_test("Get Bookings by Status", False, f"Retrieved bookings contain wrong status for {status}")
                        return
                else:
                    successful_statuses.append(f"{status}(0)")
        
        if len(successful_statuses) > 0:
            self.log_test("Get Bookings by Status", True, f"Retrieved bookings by status: {successful_statuses}")
        else:
            self.log_test("Get Bookings by Status", False, "Failed to retrieve bookings by any status")

    def test_service_bookings_by_type(self):
        """Test GET /api/services/bookings/type/{service_type} - Filter bookings by service type"""
        if not self.token:
            self.log_test("Get Bookings by Service Type", False, "No token available - login failed")
            return
            
        # Test different service types
        service_types_to_test = ["it_support", "network_installation", "starlink_installation", "software_development", "consultation", "maintenance", "training"]
        successful_types = []
        
        for service_type in service_types_to_test:
            success, data, status_code = self.make_request("GET", f"/services/bookings/type/{service_type}")
            
            if success and status_code == 200 and isinstance(data, list):
                count = len(data)
                if count > 0:
                    # Verify all bookings have the correct service type
                    correct_type = all(booking.get("service_type") == service_type for booking in data)
                    if correct_type:
                        successful_types.append(f"{service_type}({count})")
                    else:
                        self.log_test("Get Bookings by Service Type", False, f"Retrieved bookings contain wrong service type for {service_type}")
                        return
                else:
                    successful_types.append(f"{service_type}(0)")
        
        if len(successful_types) > 0:
            self.log_test("Get Bookings by Service Type", True, f"Retrieved bookings by service type: {successful_types}")
        else:
            self.log_test("Get Bookings by Service Type", False, "Failed to retrieve bookings by any service type")

    def test_service_booking_status_update(self):
        """Test PUT /api/services/bookings/{booking_id}/status - Update booking status"""
        if not self.token:
            self.log_test("Update Service Booking Status", False, "No token available - login failed")
            return
            
        # First create a booking to update
        booking_data = {
            "client_name": "Test Status Update Client",
            "client_email": "teststatus@example.rw",
            "client_phone": "+250788666555",
            "service_type": "network_installation",
            "description": "Test booking for status update validation",
            "preferred_date": "2025-01-26T13:00:00",
            "location": "Test Location",
            "cost_estimate": 120000.0,
            "notes": "Test booking for status update"
        }
        
        success, data, status_code = self.make_request("POST", "/services/bookings", booking_data)
        if not success or not data.get("id"):
            self.log_test("Update Service Booking Status", False, "Could not create test booking for status update")
            return
            
        booking_id = data.get("id")
        
        # Test status transitions: pending → confirmed → in_progress → completed
        status_transitions = [
            {"status": "confirmed", "description": "confirmed status"},
            {"status": "in_progress", "description": "in_progress status"},
            {"status": "completed", "description": "completed status"}
        ]
        
        successful_transitions = []
        
        for transition in status_transitions:
            status_update = {"status": transition["status"]}
            success, data, status_code = self.make_request("PUT", f"/services/bookings/{booking_id}/status", status_update)
            
            if success and status_code == 200:
                message = data.get("message", "Status updated")
                successful_transitions.append(transition["status"])
            else:
                self.log_test("Update Service Booking Status", False, f"Failed to update to {transition['status']}: {status_code}")
                return
        
        if len(successful_transitions) == len(status_transitions):
            self.log_test("Update Service Booking Status", True, f"Successfully updated booking status through transitions: {' → '.join(successful_transitions)}")
        else:
            self.log_test("Update Service Booking Status", False, f"Failed some status transitions. Successful: {successful_transitions}")

    def test_service_booking_number_generation(self):
        """Test booking number generation works correctly"""
        if not self.token:
            self.log_test("Service Booking Number Generation", False, "No token available - login failed")
            return
            
        # Create multiple bookings and check booking number format
        booking_numbers = []
        
        for i in range(3):
            booking_data = {
                "client_name": f"Test Number Gen Client {i+1}",
                "client_email": f"testnumber{i+1}@example.rw",
                "client_phone": f"+25078800{i+1:04d}",
                "service_type": "consultation",
                "description": f"Test booking {i+1} for number generation validation",
                "preferred_date": "2025-01-27T10:00:00",
                "location": "Test Location",
                "cost_estimate": 40000.0,
                "notes": f"Test booking {i+1} for number generation"
            }
            
            success, data, status_code = self.make_request("POST", "/services/bookings", booking_data)
            if success and data.get("id"):
                # Get the created booking to check its booking number
                booking_id = data.get("id")
                success, booking_data, _ = self.make_request("GET", f"/services/bookings/{booking_id}")
                if success and booking_data.get("booking_number"):
                    booking_numbers.append(booking_data.get("booking_number"))
        
        if len(booking_numbers) >= 2:
            # Check booking number format (should be SRV-YYYYMMDD-XXXX)
            import re
            pattern = r"SRV-\d{8}-\d{4}"
            valid_numbers = [num for num in booking_numbers if re.match(pattern, num)]
            
            if len(valid_numbers) == len(booking_numbers):
                self.log_test("Service Booking Number Generation", True, f"Generated valid booking numbers: {booking_numbers}")
            else:
                invalid_numbers = [num for num in booking_numbers if not re.match(pattern, num)]
                self.log_test("Service Booking Number Generation", False, f"Invalid booking number format: {invalid_numbers}")
        else:
            self.log_test("Service Booking Number Generation", False, "Could not create enough bookings to test number generation")

    def test_service_cost_tracking(self):
        """Test cost estimate and actual cost tracking"""
        if not self.token:
            self.log_test("Service Cost Tracking", False, "No token available - login failed")
            return
            
        # Create a booking with cost estimate
        booking_data = {
            "client_name": "Test Cost Tracking Client",
            "client_email": "testcost@example.rw",
            "client_phone": "+250788444333",
            "service_type": "software_development",
            "description": "Test booking for cost tracking validation",
            "preferred_date": "2025-01-29T15:00:00",
            "location": "Test Location",
            "cost_estimate": 200000.0,
            "notes": "Test booking for cost tracking"
        }
        
        success, data, status_code = self.make_request("POST", "/services/bookings", booking_data)
        if not success or not data.get("id"):
            self.log_test("Service Cost Tracking", False, "Could not create test booking for cost tracking")
            return
            
        booking_id = data.get("id")
        
        # Update booking with actual cost
        update_data = {
            "actual_cost": 185000.0,
            "status": "completed",
            "notes": "Service completed with actual cost tracking"
        }
        
        success, data, status_code = self.make_request("PUT", f"/services/bookings/{booking_id}", update_data)
        
        if success and status_code == 200:
            # Verify cost tracking
            success, booking_data, _ = self.make_request("GET", f"/services/bookings/{booking_id}")
            if success:
                cost_estimate = booking_data.get("cost_estimate", 0)
                actual_cost = booking_data.get("actual_cost", 0)
                
                if cost_estimate == 200000.0 and actual_cost == 185000.0:
                    cost_difference = cost_estimate - actual_cost
                    self.log_test("Service Cost Tracking", True, f"Cost tracking working: Estimate: {cost_estimate}, Actual: {actual_cost}, Difference: {cost_difference}")
                else:
                    self.log_test("Service Cost Tracking", False, f"Cost tracking incorrect: Estimate: {cost_estimate}, Actual: {actual_cost}")
            else:
                self.log_test("Service Cost Tracking", False, "Could not retrieve booking after cost update")
        else:
            self.log_test("Service Cost Tracking", False, f"Failed to update booking with actual cost: {status_code}")

    def test_services_summary(self):
        """Test GET /api/services/summary - Get comprehensive service booking summary"""
        if not self.token:
            self.log_test("Get Services Summary", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/services/summary")
        
        if success and status_code == 200:
            required_keys = ["total_bookings", "status_counts", "service_type_counts", "total_revenue", "estimated_revenue", "recent_bookings", "monthly_bookings"]
            has_required_keys = all(key in data for key in required_keys)
            
            if has_required_keys:
                summary = {
                    "Total Bookings": data.get("total_bookings", 0),
                    "Status Counts": data.get("status_counts", {}),
                    "Service Type Counts": data.get("service_type_counts", {}),
                    "Total Revenue": data.get("total_revenue", 0),
                    "Estimated Revenue": data.get("estimated_revenue", 0),
                    "Recent Bookings": data.get("recent_bookings", 0),
                    "Monthly Bookings": data.get("monthly_bookings", 0)
                }
                self.log_test("Get Services Summary", True, f"Retrieved services summary: {summary}")
            else:
                missing_keys = [key for key in required_keys if key not in data]
                self.log_test("Get Services Summary", False, f"Missing required keys: {missing_keys}")
        else:
            self.log_test("Get Services Summary", False, f"Status: {status_code}", data)

    def run_enhanced_service_booking_tests(self):
        """Run all enhanced service booking management tests"""
        print("\n" + "="*60)
        print("TESTING ENHANCED SERVICE BOOKING MANAGEMENT API")
        print("="*60)
        
        # Basic service booking tests
        self.test_service_bookings_get()
        self.test_service_bookings_create()
        self.test_service_bookings_update()
        self.test_service_types()
        
        # Enhanced service booking management tests
        self.test_service_booking_single()
        self.test_service_booking_delete_validation()
        self.test_service_booking_delete_in_progress_validation()
        self.test_service_bookings_by_status()
        self.test_service_bookings_by_type()
        self.test_service_booking_status_update()
        self.test_service_booking_number_generation()
        self.test_service_cost_tracking()
        self.test_services_summary()

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
            "category": "other",
            "amount": 150000.0,
            "description": "Product sales revenue for January",
            "reference": "SALES-JAN-2025-001",
            "payment_method": "bank_transfer"
        }
        
        success, data, status_code = self.make_request("POST", "/finance/transactions", transaction_data)
        
        if success and status_code == 200 and data.get("id"):
            transaction_id = data.get("id")
            transaction_number = data.get("transaction_number", "Unknown")
            self.log_test("Create Financial Transaction", True, f"Created financial transaction {transaction_number} with ID: {transaction_id}")
            return transaction_id
        else:
            self.log_test("Create Financial Transaction", False, f"Status: {status_code}", data)
            return None

    def test_financial_summary(self):
        """Test get financial summary endpoint"""
        if not self.token:
            self.log_test("Get Financial Summary", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/finance/summary")
        
        if success and status_code == 200:
            required_keys = ["total_income", "total_expenses", "net_profit", "cash_on_hand", "pending_payments"]
            has_required_keys = all(key in data for key in required_keys)
            
            if has_required_keys:
                summary = {
                    "Total Income": data.get("total_income", 0),
                    "Total Expenses": data.get("total_expenses", 0),
                    "Net Profit": data.get("net_profit", 0),
                    "Cash on Hand": data.get("cash_on_hand", 0),
                    "Pending Payments": data.get("pending_payments", 0)
                }
                self.log_test("Get Financial Summary", True, f"Retrieved financial summary: {summary}")
            else:
                missing_keys = [key for key in required_keys if key not in data]
                self.log_test("Get Financial Summary", False, f"Missing required keys: {missing_keys}, Got: {data}")
        else:
            self.log_test("Get Financial Summary", False, f"Status: {status_code}", data)

    def test_financial_transaction_types(self):
        """Test different financial transaction types"""
        if not self.token:
            self.log_test("Test Financial Transaction Types", False, "No token available - login failed")
            return
            
        transaction_types = [
            {"type": "expense", "category": "office_supplies", "amount": 50000.0, "description": "Office supplies purchase"},
            {"type": "income", "category": "other", "amount": 200000.0, "description": "Service consultation fee"},
            {"type": "expense", "category": "utilities", "amount": 75000.0, "description": "Monthly electricity bill"},
            {"type": "income", "category": "other", "amount": 300000.0, "description": "Hardware sales revenue"}
        ]
        
        successful_types = []
        
        for trans in transaction_types:
            transaction_data = {
                "transaction_type": trans["type"],
                "category": trans["category"],
                "amount": trans["amount"],
                "description": trans["description"],
                "reference": f"TEST-{trans['type'].upper()}-{len(successful_types)+1}",
                "payment_method": "bank_transfer"
            }
            
            success, data, status_code = self.make_request("POST", "/finance/transactions", transaction_data)
            if success and status_code == 200:
                type_key = f"{trans['type']}-{trans.get('category', 'general')}"
                successful_types.append(type_key)
        
        if len(successful_types) == len(transaction_types):
            self.log_test("Test Financial Transaction Types", True, f"All transaction types working: {successful_types}")
        else:
            expected_types = [f"{t['type']}-{t.get('category', 'general')}" for t in transaction_types]
            failed_types = [t for t in expected_types if t not in successful_types]
            self.log_test("Test Financial Transaction Types", False, f"Failed types: {failed_types}, Successful: {successful_types}")

    # ENHANCED FINANCE MANAGEMENT API TESTS
    def test_finance_transaction_single(self):
        """Test GET /api/finance/transactions/{transaction_id} - Get single transaction details"""
        if not self.token:
            self.log_test("Get Single Finance Transaction", False, "No token available - login failed")
            return
            
        # First get existing transactions to test with
        success, transactions, _ = self.make_request("GET", "/finance/transactions")
        if not success or not transactions or len(transactions) == 0:
            self.log_test("Get Single Finance Transaction", False, "No transactions available for single transaction test")
            return
            
        transaction_id = transactions[0].get("id")
        
        success, data, status_code = self.make_request("GET", f"/finance/transactions/{transaction_id}")
        
        if success and status_code == 200 and data.get("id"):
            transaction_number = data.get("transaction_number", "Unknown")
            transaction_type = data.get("transaction_type", "Unknown")
            amount = data.get("amount", 0)
            self.log_test("Get Single Finance Transaction", True, f"Retrieved transaction {transaction_number}: {transaction_type}, amount: {amount}")
        else:
            self.log_test("Get Single Finance Transaction", False, f"Status: {status_code}", data)

    def test_finance_transaction_update(self):
        """Test PUT /api/finance/transactions/{transaction_id} - Update transaction details"""
        if not self.token:
            self.log_test("Update Finance Transaction", False, "No token available - login failed")
            return
            
        # First get existing transactions to test with
        success, transactions, _ = self.make_request("GET", "/finance/transactions")
        if not success or not transactions or len(transactions) == 0:
            self.log_test("Update Finance Transaction", False, "No transactions available for update test")
            return
            
        transaction_id = transactions[0].get("id")
        
        update_data = {
            "category": "maintenance",
            "description": "Updated transaction description via API test",
            "amount": 125000.0,
            "reference_id": "UPDATED-REF-001"
        }
        
        success, data, status_code = self.make_request("PUT", f"/finance/transactions/{transaction_id}", update_data)
        
        if success and status_code == 200 and data.get("id"):
            updated_description = data.get("description", "")
            updated_amount = data.get("amount", 0)
            self.log_test("Update Finance Transaction", True, f"Updated transaction {transaction_id}: {updated_description}, amount: {updated_amount}")
        else:
            self.log_test("Update Finance Transaction", False, f"Status: {status_code}", data)

    def test_finance_transaction_delete(self):
        """Test DELETE /api/finance/transactions/{transaction_id} - Delete transaction"""
        if not self.token:
            self.log_test("Delete Finance Transaction", False, "No token available - login failed")
            return
            
        # First create a transaction to delete
        transaction_data = {
            "transaction_type": "expense",
            "category": "other",
            "amount": 25000.0,
            "description": "Test transaction for deletion",
            "reference": "DELETE-TEST-001",
            "payment_method": "cash"
        }
        
        success, created_data, status_code = self.make_request("POST", "/finance/transactions", transaction_data)
        if not success or status_code != 200:
            self.log_test("Delete Finance Transaction", False, "Could not create transaction for deletion test")
            return
            
        transaction_id = created_data.get("id")
        
        # Delete the transaction
        success, data, status_code = self.make_request("DELETE", f"/finance/transactions/{transaction_id}")
        
        if success and status_code == 200:
            message = data.get("message", "Transaction deleted")
            self.log_test("Delete Finance Transaction", True, f"Successfully deleted transaction: {message}")
        else:
            self.log_test("Delete Finance Transaction", False, f"Status: {status_code}", data)

    def test_finance_transactions_by_type(self):
        """Test GET /api/finance/transactions/type/{transaction_type} - Filter transactions by type"""
        if not self.token:
            self.log_test("Get Transactions by Type", False, "No token available - login failed")
            return
            
        # Test different transaction types
        types_to_test = ["income", "expense"]
        successful_types = []
        
        for transaction_type in types_to_test:
            success, data, status_code = self.make_request("GET", f"/finance/transactions/type/{transaction_type}")
            
            if success and status_code == 200 and isinstance(data, list):
                count = len(data)
                if count > 0:
                    # Verify all transactions are of the correct type
                    correct_type = all(transaction.get("transaction_type") == transaction_type for transaction in data)
                    if correct_type:
                        successful_types.append(f"{transaction_type}({count})")
                    else:
                        self.log_test("Get Transactions by Type", False, f"Retrieved transactions contain wrong transaction types for {transaction_type}")
                        return
                else:
                    successful_types.append(f"{transaction_type}(0)")
        
        if len(successful_types) == len(types_to_test):
            self.log_test("Get Transactions by Type", True, f"Successfully filtered transactions by type: {successful_types}")
        else:
            self.log_test("Get Transactions by Type", False, f"Failed to filter some transaction types")

    def test_finance_transactions_by_category(self):
        """Test GET /api/finance/transactions/category/{category} - Filter transactions by category"""
        if not self.token:
            self.log_test("Get Transactions by Category", False, "No token available - login failed")
            return
            
        # First get existing transactions to find categories
        success, transactions, _ = self.make_request("GET", "/finance/transactions")
        if not success or not transactions or len(transactions) == 0:
            self.log_test("Get Transactions by Category", False, "No transactions available for category filter test")
            return
            
        # Get unique categories from existing transactions
        categories = list(set(transaction.get("category") for transaction in transactions if transaction.get("category")))
        
        if not categories:
            self.log_test("Get Transactions by Category", False, "No categories found in existing transactions")
            return
            
        # Test filtering by the first available category
        test_category = categories[0]
        
        success, data, status_code = self.make_request("GET", f"/finance/transactions/category/{test_category}")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                # Verify all transactions are of the correct category
                correct_category = all(transaction.get("category") == test_category for transaction in data)
                if correct_category:
                    self.log_test("Get Transactions by Category", True, f"Successfully filtered {count} transactions by category '{test_category}'")
                else:
                    self.log_test("Get Transactions by Category", False, f"Retrieved transactions contain wrong categories for {test_category}")
            else:
                self.log_test("Get Transactions by Category", True, f"No transactions found for category '{test_category}'")
        else:
            self.log_test("Get Transactions by Category", False, f"Status: {status_code}", data)

    def test_finance_analytics(self):
        """Test GET /api/finance/analytics - Get comprehensive financial analytics"""
        if not self.token:
            self.log_test("Get Finance Analytics", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/finance/analytics")
        
        if success and status_code == 200:
            required_keys = ["monthly_income", "monthly_expense", "category_breakdown", "recent_transactions"]
            has_required_keys = all(key in data for key in required_keys)
            
            if has_required_keys:
                analytics = {
                    "Monthly Income Records": len(data.get("monthly_income", [])),
                    "Monthly Expense Records": len(data.get("monthly_expense", [])),
                    "Category Breakdown Items": len(data.get("category_breakdown", [])),
                    "Recent Transactions": data.get("recent_transactions", 0)
                }
                self.log_test("Get Finance Analytics", True, f"Retrieved financial analytics: {analytics}")
            else:
                missing_keys = [key for key in required_keys if key not in data]
                self.log_test("Get Finance Analytics", False, f"Missing required keys: {missing_keys}")
        else:
            self.log_test("Get Finance Analytics", False, f"Status: {status_code}", data)

    def test_finance_enhanced_summary(self):
        """Test GET /api/finance/summary - Get enhanced financial summary"""
        if not self.token:
            self.log_test("Get Enhanced Finance Summary", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/finance/summary")
        
        if success and status_code == 200:
            required_keys = ["total_income", "total_expense", "net_profit", "monthly_income", "monthly_expense", "monthly_net", "income_count", "expense_count", "total_transactions", "top_income_categories", "top_expense_categories"]
            has_required_keys = all(key in data for key in required_keys)
            
            if has_required_keys:
                summary = {
                    "Total Income": data.get("total_income", 0),
                    "Total Expense": data.get("total_expense", 0),
                    "Net Profit": data.get("net_profit", 0),
                    "Monthly Income": data.get("monthly_income", 0),
                    "Monthly Expense": data.get("monthly_expense", 0),
                    "Monthly Net": data.get("monthly_net", 0),
                    "Income Count": data.get("income_count", 0),
                    "Expense Count": data.get("expense_count", 0),
                    "Total Transactions": data.get("total_transactions", 0),
                    "Top Income Categories": len(data.get("top_income_categories", [])),
                    "Top Expense Categories": len(data.get("top_expense_categories", []))
                }
                self.log_test("Get Enhanced Finance Summary", True, f"Retrieved enhanced financial summary: {summary}")
            else:
                missing_keys = [key for key in required_keys if key not in data]
                self.log_test("Get Enhanced Finance Summary", False, f"Missing required keys: {missing_keys}")
        else:
            self.log_test("Get Enhanced Finance Summary", False, f"Status: {status_code}", data)

    def test_finance_transaction_number_generation(self):
        """Test transaction number generation works correctly"""
        if not self.token:
            self.log_test("Finance Transaction Number Generation", False, "No token available - login failed")
            return
            
        # Create multiple transactions and check transaction number format
        transaction_numbers = []
        
        for i in range(3):
            transaction_data = {
                "transaction_type": "income",
                "category": "other",
                "amount": 50000.0 + (i * 10000),
                "description": f"Test transaction {i+1} for number generation",
                "reference": f"NUM-GEN-TEST-{i+1:03d}",
                "payment_method": "bank_transfer"
            }
            
            success, data, status_code = self.make_request("POST", "/finance/transactions", transaction_data)
            if success and status_code == 200 and data.get("transaction_number"):
                transaction_numbers.append(data.get("transaction_number"))
        
        if len(transaction_numbers) >= 2:
            # Check transaction number format (should be TXN-YYYYMMDD-XXXX)
            import re
            pattern = r"TXN-\d{8}-\d{4}"
            valid_numbers = [num for num in transaction_numbers if re.match(pattern, num)]
            
            if len(valid_numbers) == len(transaction_numbers):
                self.log_test("Finance Transaction Number Generation", True, f"Generated valid transaction numbers: {transaction_numbers}")
            else:
                invalid_numbers = [num for num in transaction_numbers if not re.match(pattern, num)]
                self.log_test("Finance Transaction Number Generation", False, f"Invalid transaction number format: {invalid_numbers}")
        else:
            self.log_test("Finance Transaction Number Generation", False, "Could not create enough transactions to test number generation")

    def test_finance_summary_calculations(self):
        """Test that financial summary calculations are accurate"""
        if not self.token:
            self.log_test("Finance Summary Calculations", False, "No token available - login failed")
            return
            
        # Create test transactions with known amounts
        test_transactions = [
            {"type": "income", "category": "other", "amount": 100000.0, "description": "Test income 1"},
            {"type": "income", "category": "other", "amount": 150000.0, "description": "Test income 2"},
            {"type": "expense", "category": "office_supplies", "amount": 50000.0, "description": "Test expense 1"},
            {"type": "expense", "category": "utilities", "amount": 30000.0, "description": "Test expense 2"}
        ]
        
        created_transactions = []
        expected_income = 0
        expected_expense = 0
        
        for trans in test_transactions:
            transaction_data = {
                "transaction_type": trans["type"],
                "category": trans["category"],
                "amount": trans["amount"],
                "description": trans["description"],
                "reference": f"CALC-TEST-{len(created_transactions)+1}",
                "payment_method": "bank_transfer"
            }
            
            success, data, status_code = self.make_request("POST", "/finance/transactions", transaction_data)
            if success and status_code == 200:
                created_transactions.append(data.get("id"))
                if trans["type"] == "income":
                    expected_income += trans["amount"]
                else:
                    expected_expense += trans["amount"]
        
        if len(created_transactions) == len(test_transactions):
            # Get summary and verify calculations
            success, summary_data, _ = self.make_request("GET", "/finance/summary")
            if success:
                total_income = summary_data.get("total_income", 0)
                total_expense = summary_data.get("total_expense", 0)
                net_profit = summary_data.get("net_profit", 0)
                expected_net = expected_income - expected_expense
                
                # Check if our test transactions are reflected in the totals (they should be >= our expected amounts)
                if total_income >= expected_income and total_expense >= expected_expense:
                    self.log_test("Finance Summary Calculations", True, f"Summary calculations accurate: Income >= {expected_income}, Expense >= {expected_expense}, Net: {net_profit}")
                else:
                    self.log_test("Finance Summary Calculations", False, f"Summary calculations incorrect: Expected Income >= {expected_income} (got {total_income}), Expected Expense >= {expected_expense} (got {total_expense})")
            else:
                self.log_test("Finance Summary Calculations", False, "Could not retrieve summary for calculation verification")
        else:
            self.log_test("Finance Summary Calculations", False, f"Could not create all test transactions: {len(created_transactions)}/{len(test_transactions)}")

    def run_enhanced_finance_tests(self):
        """Run all enhanced finance management tests"""
        print("\n" + "="*60)
        print("TESTING ENHANCED FINANCE MANAGEMENT API")
        print("="*60)
        
        # Basic finance tests - create some transactions first
        self.test_financial_transactions_get()
        created_transaction_id = self.test_financial_transactions_create()
        self.test_financial_transaction_types()
        
        # Enhanced finance management tests - these depend on having transactions
        self.test_finance_transaction_single()
        self.test_finance_transaction_update()
        self.test_finance_transaction_delete()
        self.test_finance_transactions_by_type()
        self.test_finance_transactions_by_category()
        self.test_finance_analytics()
        self.test_finance_enhanced_summary()
        self.test_finance_transaction_number_generation()
        self.test_finance_summary_calculations()

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
        
        # ENHANCED INVENTORY MANAGEMENT TESTS
        print("\n" + "="*50)
        print("TESTING ENHANCED INVENTORY MANAGEMENT API")
        print("="*50)
        self.run_enhanced_inventory_tests()
        
        # NEW MODULE TESTS - POS System
        print("\n" + "="*50)
        print("TESTING NEW MODULE: POS SYSTEM")
        print("="*50)
        self.test_pos_transactions_get()
        self.test_pos_transactions_create()
        self.test_pos_payment_methods()
        
        # ENHANCED SERVICE BOOKING MANAGEMENT TESTS
        print("\n" + "="*50)
        print("TESTING ENHANCED SERVICE BOOKING MANAGEMENT MODULE")
        print("="*50)
        self.run_enhanced_service_booking_tests()
        
        # NEW MODULE TESTS - Finance Module
        print("\n" + "="*50)
        print("TESTING ENHANCED FINANCE MANAGEMENT MODULE")
        print("="*50)
        self.run_enhanced_finance_tests()
        
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