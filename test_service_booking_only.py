#!/usr/bin/env python3
"""
Test only the Enhanced Service Booking Management API endpoints
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

class ServiceBookingTester:
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

    def test_service_bookings_get(self):
        """Test get service bookings endpoint"""
        if not self.token:
            self.log_test("Get Service Bookings", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/services/bookings")
        
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
            "cost_estimate": 150000.0,
            "notes": "High priority network installation project"
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

    def run_tests(self):
        """Run all service booking tests"""
        print("=" * 80)
        print("ENHANCED SERVICE BOOKING MANAGEMENT API TESTING")
        print("=" * 80)
        print(f"Testing against: {self.base_url}")
        print(f"Demo Account: {DEMO_ADMIN_EMAIL}")
        print("=" * 80)
        print()
        
        # Authentication
        self.test_authentication_login()
        
        # Service booking tests
        self.test_service_bookings_get()
        self.test_service_bookings_create()
        self.test_service_booking_single()
        self.test_services_summary()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print("\nFAILED TESTS:")
            print("-" * 40)
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test']}: {result['details']}")

if __name__ == "__main__":
    tester = ServiceBookingTester()
    tester.run_tests()