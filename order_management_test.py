#!/usr/bin/env python3
"""
Focused Order Management API Testing
Tests the complete Order Management system with all enhancements
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

class OrderManagementTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.user_id = None
        self.test_results = []
        self.created_order_ids = []
        
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

    def authenticate(self):
        """Authenticate and get token"""
        login_data = {
            "email": DEMO_ADMIN_EMAIL,
            "password": DEMO_ADMIN_PASSWORD
        }
        
        success, data, status_code = self.make_request("POST", "/auth/login", login_data)
        
        if success and status_code == 200 and data.get("token"):
            self.token = data["token"]
            self.user_id = data.get("user", {}).get("id")
            user_name = data.get("user", {}).get("full_name", "Unknown")
            print(f"✅ Authenticated as {user_name}")
            return True
        else:
            print(f"❌ Authentication failed: {data}")
            return False

    def get_test_client(self):
        """Get a client for testing"""
        success, clients, _ = self.make_request("GET", "/clients")
        if success and clients and len(clients) > 0:
            return clients[0]
        return None

    def get_test_products(self, count=2):
        """Get products for testing"""
        success, products, _ = self.make_request("GET", "/products")
        if success and products and len(products) > 0:
            return products[:count]
        return []

    def test_get_orders(self):
        """Test GET /api/orders - Enhanced response format with client details"""
        success, data, status_code = self.make_request("GET", "/orders")
        
        if success and status_code == 200 and isinstance(data, list):
            if len(data) > 0:
                # Check enhanced response format
                order = data[0]
                required_fields = ["id", "order_number", "client_name", "status", "total_amount", "items"]
                has_required_fields = all(field in order for field in required_fields)
                
                if has_required_fields:
                    client_name = order.get("client_name", "Unknown")
                    order_number = order.get("order_number", "Unknown")
                    items_count = len(order.get("items", []))
                    self.log_test("GET /api/orders", True, 
                                f"Retrieved {len(data)} orders with enhanced format. Sample: {order_number} for {client_name} with {items_count} items")
                else:
                    missing_fields = [field for field in required_fields if field not in order]
                    self.log_test("GET /api/orders", False, f"Missing required fields: {missing_fields}")
            else:
                self.log_test("GET /api/orders", True, "No orders found (empty list returned)")
        else:
            self.log_test("GET /api/orders", False, f"Status: {status_code}", data)

    def test_create_order(self):
        """Test POST /api/orders - New format with client_name, client_email, client_phone"""
        client = self.get_test_client()
        products = self.get_test_products(2)
        
        if not client:
            self.log_test("POST /api/orders", False, "No clients available for order creation")
            return None
            
        if not products:
            self.log_test("POST /api/orders", False, "No products available for order creation")
            return None

        # Create order with new format
        items = []
        for i, product in enumerate(products):
            items.append({
                "product_id": product.get("id"),
                "quantity": i + 1,  # 1, 2 quantities
                "unit_price": product.get("price", 10000)
            })
        
        order_data = {
            "client_name": client.get("name", "Test Client"),
            "client_email": client.get("email", "test@example.com"),
            "client_phone": client.get("phone", "+250788123456"),
            "items": items,
            "payment_method": "cash",
            "notes": "Test order created via enhanced API"
        }
        
        success, data, status_code = self.make_request("POST", "/orders", order_data)
        
        if success and status_code == 200 and data.get("id"):
            order_id = data.get("id")
            order_number = data.get("order_number", "Unknown")
            self.created_order_ids.append(order_id)
            self.log_test("POST /api/orders", True, 
                        f"Created order {order_number} with ID: {order_id}")
            return order_id
        else:
            self.log_test("POST /api/orders", False, f"Status: {status_code}", data)
            return None

    def test_get_single_order(self, order_id: str = None):
        """Test GET /api/orders/{order_id} - Single order retrieval"""
        if not order_id:
            # Try to get an existing order
            success, orders, _ = self.make_request("GET", "/orders")
            if success and orders and len(orders) > 0:
                order_id = orders[0].get("id")
            else:
                self.log_test("GET /api/orders/{id}", False, "No order ID available for testing")
                return
        
        success, data, status_code = self.make_request("GET", f"/orders/{order_id}")
        
        if success and status_code == 200 and data.get("id"):
            order_number = data.get("order_number", "Unknown")
            status_value = data.get("status", "Unknown")
            self.log_test("GET /api/orders/{id}", True, 
                        f"Retrieved order {order_number} with status: {status_value}")
        else:
            self.log_test("GET /api/orders/{id}", False, f"Status: {status_code}", data)

    def test_update_order(self, order_id: str = None):
        """Test PUT /api/orders/{order_id} - Order updates"""
        if not order_id:
            # Try to get an existing order
            success, orders, _ = self.make_request("GET", "/orders")
            if success and orders and len(orders) > 0:
                order_id = orders[0].get("id")
            else:
                self.log_test("PUT /api/orders/{id}", False, "No order ID available for testing")
                return
        
        update_data = {
            "payment_method": "card",
            "notes": "Updated order details via enhanced API test"
        }
        
        success, data, status_code = self.make_request("PUT", f"/orders/{order_id}", update_data)
        
        if success and status_code == 200 and data.get("id"):
            updated_payment = data.get("payment_method", "Unknown")
            self.log_test("PUT /api/orders/{id}", True, 
                        f"Updated order {order_id} - payment method: {updated_payment}")
            return order_id
        else:
            self.log_test("PUT /api/orders/{id}", False, f"Status: {status_code}", data)
            return None

    def test_update_order_status(self, order_id: str = None):
        """Test PUT /api/orders/{order_id}/status - Order status updates"""
        if not order_id:
            # Try to get an existing order
            success, orders, _ = self.make_request("GET", "/orders")
            if success and orders and len(orders) > 0:
                order_id = orders[0].get("id")
            else:
                self.log_test("PUT /api/orders/{id}/status", False, "No order ID available for testing")
                return
        
        status_update = {
            "status": "processing"
        }
        
        success, data, status_code = self.make_request("PUT", f"/orders/{order_id}/status", status_update)
        
        if success and status_code == 200:
            message = data.get("message", "Status updated")
            self.log_test("PUT /api/orders/{id}/status", True, f"Order status updated: {message}")
        else:
            self.log_test("PUT /api/orders/{id}/status", False, f"Status: {status_code}", data)

    def test_get_orders_by_status(self):
        """Test GET /api/orders/status/{status} - Order filtering by status"""
        statuses_to_test = ["pending", "processing", "delivered"]
        successful_statuses = []
        
        for status in statuses_to_test:
            success, data, status_code = self.make_request("GET", f"/orders/status/{status}")
            
            if success and status_code == 200 and isinstance(data, list):
                count = len(data)
                successful_statuses.append(f"{status}({count})")
        
        if len(successful_statuses) > 0:
            self.log_test("GET /api/orders/status/{status}", True, 
                        f"Retrieved orders by status: {successful_statuses}")
        else:
            self.log_test("GET /api/orders/status/{status}", False, 
                        "Failed to retrieve orders by any status")

    def test_delete_order_validation(self):
        """Test DELETE /api/orders/{order_id} - Order deletion with validation"""
        # Create a test order to delete
        order_id = self.test_create_order()
        if not order_id:
            self.log_test("DELETE /api/orders/{id}", False, "Could not create test order for deletion")
            return
        
        # Try to delete the order (should succeed for non-delivered orders)
        success, data, status_code = self.make_request("DELETE", f"/orders/{order_id}")
        
        if success and status_code == 200:
            message = data.get("message", "Order deleted")
            self.log_test("DELETE /api/orders/{id}", True, f"Successfully deleted order: {message}")
        else:
            self.log_test("DELETE /api/orders/{id}", False, f"Status: {status_code}", data)

    def test_delete_delivered_order_validation(self):
        """Test DELETE validation - Should fail for delivered orders"""
        # Create a test order
        order_id = self.test_create_order()
        if not order_id:
            self.log_test("DELETE Delivered Order Validation", False, "Could not create test order")
            return
        
        # Update order status to delivered
        status_update = {"status": "delivered"}
        success, _, _ = self.make_request("PUT", f"/orders/{order_id}/status", status_update)
        
        if not success:
            self.log_test("DELETE Delivered Order Validation", False, "Could not update order to delivered status")
            return
        
        # Now try to delete the delivered order (should fail)
        success, data, status_code = self.make_request("DELETE", f"/orders/{order_id}")
        
        if not success and status_code == 400:
            error_detail = data.get("detail", "Unknown error")
            if "Cannot delete delivered orders" in error_detail:
                self.log_test("DELETE Delivered Order Validation", True, 
                            "Correctly prevented deletion of delivered order")
            else:
                self.log_test("DELETE Delivered Order Validation", False, 
                            f"Wrong error message: {error_detail}")
        else:
            self.log_test("DELETE Delivered Order Validation", False, 
                        f"Should have failed but got status: {status_code}")

    def test_order_stock_validation(self):
        """Test stock validation when creating orders"""
        client = self.get_test_client()
        products = self.get_test_products(1)
        
        if not client or not products:
            self.log_test("Order Stock Validation", False, "No client or products available")
            return
        
        product = products[0]
        current_stock = product.get("current_stock", 0)
        excessive_quantity = current_stock + 10
        
        order_data = {
            "client_name": client.get("name", "Test Client"),
            "client_email": client.get("email", "test@example.com"),
            "client_phone": client.get("phone", "+250788123456"),
            "items": [{
                "product_id": product.get("id"),
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
                self.log_test("Order Stock Validation", True, 
                            f"Correctly prevented order with insufficient stock: {error_detail}")
            else:
                self.log_test("Order Stock Validation", False, f"Wrong error message: {error_detail}")
        else:
            self.log_test("Order Stock Validation", False, 
                        f"Should have failed but got status: {status_code}")

    def test_order_number_generation(self):
        """Test order number generation format (ORD-YYYYMMDD-XXXX)"""
        order_numbers = []
        
        for i in range(2):
            order_id = self.test_create_order()
            if order_id:
                # Get the created order to check its order number
                success, data, _ = self.make_request("GET", f"/orders/{order_id}")
                if success and data.get("order_number"):
                    order_numbers.append(data.get("order_number"))
        
        if len(order_numbers) >= 1:
            # Check order number format (should be ORD-YYYYMMDD-XXXX)
            import re
            pattern = r"ORD-\d{8}-\d{4}"
            valid_numbers = [num for num in order_numbers if re.match(pattern, num)]
            
            if len(valid_numbers) == len(order_numbers):
                self.log_test("Order Number Generation", True, 
                            f"Generated valid order numbers: {order_numbers}")
            else:
                invalid_numbers = [num for num in order_numbers if not re.match(pattern, num)]
                self.log_test("Order Number Generation", False, 
                            f"Invalid order number format: {invalid_numbers}")
        else:
            self.log_test("Order Number Generation", False, 
                        "Could not create orders to test number generation")

    def run_all_order_tests(self):
        """Run all Order Management API tests"""
        print("=" * 80)
        print("ORDER MANAGEMENT API TESTING - COMPLETE SYSTEM")
        print("=" * 80)
        print(f"Testing against: {self.base_url}")
        print("=" * 80)
        print()
        
        # Authenticate first
        if not self.authenticate():
            print("❌ Authentication failed - cannot proceed with tests")
            return
        
        print("\n🔍 TESTING ENHANCED ORDER MANAGEMENT API ENDPOINTS")
        print("-" * 60)
        
        # Test all 7 Order Management endpoints
        self.test_get_orders()
        created_order_id = self.test_create_order()
        
        if created_order_id:
            self.test_get_single_order(created_order_id)
            self.test_update_order(created_order_id)
            self.test_update_order_status(created_order_id)
        else:
            self.test_get_single_order()
            self.test_update_order()
            self.test_update_order_status()
        
        self.test_get_orders_by_status()
        self.test_delete_order_validation()
        
        print("\n🔍 TESTING ORDER BUSINESS LOGIC")
        print("-" * 60)
        
        # Test business logic and validation
        self.test_delete_delivered_order_validation()
        self.test_order_stock_validation()
        self.test_order_number_generation()
        
        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("ORDER MANAGEMENT API TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        # Categorize results by endpoint
        endpoint_results = {}
        for result in self.test_results:
            test_name = result["test"]
            if "GET /api/orders" in test_name:
                category = "GET Endpoints"
            elif "POST /api/orders" in test_name:
                category = "POST Endpoints"
            elif "PUT /api/orders" in test_name:
                category = "PUT Endpoints"
            elif "DELETE" in test_name:
                category = "DELETE Endpoints"
            else:
                category = "Business Logic"
            
            if category not in endpoint_results:
                endpoint_results[category] = []
            endpoint_results[category].append(result)
        
        for category, results in endpoint_results.items():
            passed = sum(1 for r in results if r["success"])
            total = len(results)
            print(f"{category}: {passed}/{total} passed")
        
        print()
        
        if failed_tests > 0:
            print("FAILED TESTS:")
            print("-" * 40)
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test']}: {result['details']}")
            print()
        
        # Check for critical issues
        critical_issues = []
        
        # Check if basic order retrieval works
        get_orders_test = next((r for r in self.test_results if r["test"] == "GET /api/orders"), None)
        if get_orders_test and not get_orders_test["success"]:
            critical_issues.append("Cannot retrieve orders - basic functionality broken")
        
        # Check if order creation works
        create_order_test = next((r for r in self.test_results if r["test"] == "POST /api/orders"), None)
        if create_order_test and not create_order_test["success"]:
            critical_issues.append("Cannot create orders - core functionality broken")
        
        print("CRITICAL ISSUES:")
        print("-" * 40)
        if critical_issues:
            for issue in critical_issues:
                print(f"🚨 {issue}")
        else:
            print("✅ No critical issues detected")
        
        print("=" * 80)

if __name__ == "__main__":
    tester = OrderManagementTester()
    tester.run_all_order_tests()