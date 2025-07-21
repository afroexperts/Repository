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