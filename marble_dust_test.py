#!/usr/bin/env python3
"""
Marble Dust Production Management API Testing
Tests all 8 marble dust endpoints with comprehensive manufacturing workflow validation
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "https://480cb20d-5a56-4bb6-932a-c7e00eadfdd6.preview.emergentagent.com/api"
DEMO_ADMIN_EMAIL = "admin@afroexperts.rw"
DEMO_ADMIN_PASSWORD = "admin123"

class MarbleDustTester:
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
            
            # Handle different response types
            if response.status_code < 400:
                if response.content:
                    try:
                        return True, response.json(), response.status_code
                    except json.JSONDecodeError:
                        return True, {"content": response.text}, response.status_code
                else:
                    return True, {}, response.status_code
            else:
                # Handle error responses
                try:
                    return False, response.json(), response.status_code
                except json.JSONDecodeError:
                    return False, {"error": response.text}, response.status_code
                
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}", 0

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

    # MARBLE DUST PRODUCTION MANAGEMENT API TESTS
    def test_marble_dust_get_all(self):
        """Test GET /api/marble-dust - List all production batches"""
        if not self.token:
            self.log_test("Get All Marble Dust Batches", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/marble-dust")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                # Check batch details
                first_batch = data[0]
                has_required_fields = all(field in first_batch for field in 
                    ["id", "batch_number", "quality_grade", "status", "quantity_kg", "production_date"])
                
                if has_required_fields:
                    quality_grades = list(set(batch.get("quality_grade", "Unknown") for batch in data))
                    statuses = list(set(batch.get("status", "Unknown") for batch in data))
                    self.log_test("Get All Marble Dust Batches", True, 
                        f"Retrieved {count} batches with quality grades: {quality_grades}, statuses: {statuses}")
                else:
                    missing_fields = [field for field in ["id", "batch_number", "quality_grade", "status", "quantity_kg", "production_date"] 
                                    if field not in first_batch]
                    self.log_test("Get All Marble Dust Batches", False, f"Missing required fields: {missing_fields}")
            else:
                self.log_test("Get All Marble Dust Batches", True, "No marble dust batches found")
        else:
            self.log_test("Get All Marble Dust Batches", False, f"Status: {status_code}", data)

    def test_marble_dust_create(self):
        """Test POST /api/marble-dust - Create new batch with manufacturing data"""
        if not self.token:
            self.log_test("Create Marble Dust Batch", False, "No token available - login failed")
            return
            
        batch_data = {
            "batch_number": f"MB-2025-TEST-{datetime.now().strftime('%H%M%S')}",
            "production_date": "2025-01-15T08:00:00Z",
            "quantity_kg": 1000.0,
            "quality_grade": "premium",
            "source_material": "Italian Carrara Marble",
            "production_location": "Kigali Production Facility",
            "moisture_content": 2.5,
            "particle_size_mm": 0.5,
            "color_classification": "Pure White",
            "cost_per_kg": 1.20,
            "selling_price_per_kg": 2.00,
            "notes": "High-quality batch for premium construction projects"
        }
        
        success, data, status_code = self.make_request("POST", "/marble-dust", batch_data)
        
        if success and status_code == 200 and data.get("success"):
            batch_id = data.get("id")
            batch_number = data.get("batch_number")
            
            # Get the created batch to verify calculations
            success_get, batch_data, _ = self.make_request("GET", f"/marble-dust/{batch_id}")
            if success_get and batch_data:
                total_cost = batch_data.get("total_cost", 0)
                profit_margin = batch_data.get("profit_margin", 0)
                
                # Verify calculations
                expected_total_cost = 1000.0 * 1.20  # quantity * cost_per_kg
                expected_profit_margin = ((2.00 - 1.20) / 1.20) * 100  # ((selling - cost) / cost) * 100
                
                if abs(total_cost - expected_total_cost) < 0.01 and abs(profit_margin - expected_profit_margin) < 0.01:
                    self.log_test("Create Marble Dust Batch", True, 
                        f"Created batch {batch_number} with ID: {batch_id}, Total Cost: {total_cost}, Profit Margin: {profit_margin:.2f}%")
                    return batch_id
                else:
                    self.log_test("Create Marble Dust Batch", False, 
                        f"Calculation error - Expected cost: {expected_total_cost}, got: {total_cost}")
                    return batch_id
            else:
                self.log_test("Create Marble Dust Batch", True, 
                    f"Created batch {batch_number} with ID: {batch_id} (could not verify calculations)")
                return batch_id
        else:
            self.log_test("Create Marble Dust Batch", False, f"Status: {status_code}", data)
            return None

    def test_marble_dust_get_single(self):
        """Test GET /api/marble-dust/{id} - Get single batch details with profit calculations"""
        if not self.token:
            self.log_test("Get Single Marble Dust Batch", False, "No token available - login failed")
            return
            
        # First get existing batches to test with
        success, batches, _ = self.make_request("GET", "/marble-dust")
        if not success or not batches or len(batches) == 0:
            self.log_test("Get Single Marble Dust Batch", False, "No batches available for single batch test")
            return
            
        batch_id = batches[0].get("id")
        
        success, data, status_code = self.make_request("GET", f"/marble-dust/{batch_id}")
        
        if success and status_code == 200 and data.get("id"):
            batch_number = data.get("batch_number", "Unknown")
            quality_grade = data.get("quality_grade", "Unknown")
            status_value = data.get("status", "Unknown")
            profit_margin = data.get("profit_margin", 0)
            total_revenue = data.get("total_revenue", 0)
            
            # Verify profit calculations are present
            has_financial_data = all(field in data for field in ["total_cost", "profit_margin", "total_revenue"])
            
            if has_financial_data:
                self.log_test("Get Single Marble Dust Batch", True, 
                    f"Retrieved batch {batch_number}: {quality_grade} quality, {status_value} status, Profit: {profit_margin:.2f}%, Revenue: {total_revenue}")
            else:
                missing_fields = [field for field in ["total_cost", "profit_margin", "total_revenue"] if field not in data]
                self.log_test("Get Single Marble Dust Batch", False, f"Missing financial fields: {missing_fields}")
        else:
            self.log_test("Get Single Marble Dust Batch", False, f"Status: {status_code}", data)

    def test_marble_dust_update(self):
        """Test PUT /api/marble-dust/{id} - Update batch with quantity/cost adjustments"""
        if not self.token:
            self.log_test("Update Marble Dust Batch", False, "No token available - login failed")
            return
            
        # First get existing batches to test with
        success, batches, _ = self.make_request("GET", "/marble-dust")
        if not success or not batches or len(batches) == 0:
            self.log_test("Update Marble Dust Batch", False, "No batches available for update test")
            return
            
        batch_id = batches[0].get("id")
        
        update_data = {
            "status": "quality_check",
            "remaining_quantity_kg": 950.0,
            "notes": "Updated batch status and remaining quantity via API test",
            "quality_test_results": {
                "moisture_test": "passed",
                "particle_size_test": "passed",
                "color_consistency": "excellent"
            }
        }
        
        success, data, status_code = self.make_request("PUT", f"/marble-dust/{batch_id}", update_data)
        
        if success and status_code == 200 and data.get("success"):
            # Get the updated batch to verify changes
            success_get, batch_data, _ = self.make_request("GET", f"/marble-dust/{batch_id}")
            if success_get and batch_data:
                updated_status = batch_data.get("status", "Unknown")
                remaining_quantity = batch_data.get("remaining_quantity_kg", 0)
                self.log_test("Update Marble Dust Batch", True, 
                    f"Updated batch {batch_id} to status: {updated_status}, remaining: {remaining_quantity}kg")
                return batch_id
            else:
                self.log_test("Update Marble Dust Batch", True, f"Updated batch {batch_id} successfully")
                return batch_id
        else:
            self.log_test("Update Marble Dust Batch", False, f"Status: {status_code}", data)
            return None

    def test_marble_dust_delete_validation(self):
        """Test DELETE /api/marble-dust/{id} - Delete batch with business validation"""
        if not self.token:
            self.log_test("Delete Marble Dust Batch Validation", False, "No token available - login failed")
            return
            
        # First create a test batch to delete
        batch_id = self.test_marble_dust_create()
        if not batch_id:
            self.log_test("Delete Marble Dust Batch Validation", False, "Could not create test batch for deletion")
            return
        
        # Try to delete the batch (should succeed for non-shipped/sold batches)
        success, data, status_code = self.make_request("DELETE", f"/marble-dust/{batch_id}")
        
        if success and status_code == 200 and data.get("success"):
            message = data.get("message", "Batch deleted")
            self.log_test("Delete Marble Dust Batch Validation", True, f"Successfully deleted batch: {message}")
        else:
            self.log_test("Delete Marble Dust Batch Validation", False, f"Status: {status_code}", data)

    def test_marble_dust_delete_shipped_validation(self):
        """Test DELETE validation - Should fail for shipped/sold batches"""
        if not self.token:
            self.log_test("Delete Shipped Batch Validation", False, "No token available - login failed")
            return
            
        # First create a test batch
        batch_id = self.test_marble_dust_create()
        if not batch_id:
            self.log_test("Delete Shipped Batch Validation", False, "Could not create test batch")
            return
        
        # Update batch status to shipped
        status_update = {
            "status": "shipped",
            "shipped_at": datetime.now().isoformat()
        }
        success, _, _ = self.make_request("PUT", f"/marble-dust/{batch_id}", status_update)
        
        if not success:
            self.log_test("Delete Shipped Batch Validation", False, "Could not update batch to shipped status")
            return
        
        # Now try to delete the shipped batch (should fail)
        success, data, status_code = self.make_request("DELETE", f"/marble-dust/{batch_id}")
        
        if not success and status_code == 400:
            error_detail = data.get("detail", "Unknown error")
            if "Cannot delete" in error_detail and ("shipped" in error_detail or "sold" in error_detail):
                self.log_test("Delete Shipped Batch Validation", True, "Correctly prevented deletion of shipped batch")
            else:
                self.log_test("Delete Shipped Batch Validation", False, f"Wrong error message: {error_detail}")
        else:
            self.log_test("Delete Shipped Batch Validation", False, f"Should have failed but got status: {status_code}")

    def test_marble_dust_quality_filtering(self):
        """Test GET /api/marble-dust/quality/{quality} - Filter by quality grade"""
        if not self.token:
            self.log_test("Filter Batches by Quality", False, "No token available - login failed")
            return
            
        # Test different quality grades
        quality_grades = ["premium", "standard", "industrial", "mixed"]
        successful_grades = []
        
        for quality in quality_grades:
            success, data, status_code = self.make_request("GET", f"/marble-dust/quality/{quality}")
            
            if success and status_code == 200 and isinstance(data, list):
                count = len(data)
                if count > 0:
                    # Verify all batches have the correct quality grade
                    correct_quality = all(batch.get("quality_grade") == quality for batch in data)
                    if correct_quality:
                        successful_grades.append(f"{quality}({count})")
                    else:
                        self.log_test("Filter Batches by Quality", False, f"Retrieved batches contain wrong quality grades for {quality}")
                        return
                else:
                    successful_grades.append(f"{quality}(0)")
        
        if len(successful_grades) == len(quality_grades):
            self.log_test("Filter Batches by Quality", True, f"Successfully filtered batches by quality: {successful_grades}")
        else:
            self.log_test("Filter Batches by Quality", False, f"Failed to filter some quality grades")

    def test_marble_dust_status_filtering(self):
        """Test GET /api/marble-dust/status/{status} - Filter by production status"""
        if not self.token:
            self.log_test("Filter Batches by Status", False, "No token available - login failed")
            return
            
        # Test different production statuses
        statuses = ["in_production", "quality_check", "ready", "shipped", "sold"]
        successful_statuses = []
        
        for status in statuses:
            success, data, status_code = self.make_request("GET", f"/marble-dust/status/{status}")
            
            if success and status_code == 200 and isinstance(data, list):
                count = len(data)
                if count > 0:
                    # Verify all batches have the correct status
                    correct_status = all(batch.get("status") == status for batch in data)
                    if correct_status:
                        successful_statuses.append(f"{status}({count})")
                    else:
                        self.log_test("Filter Batches by Status", False, f"Retrieved batches contain wrong statuses for {status}")
                        return
                else:
                    successful_statuses.append(f"{status}(0)")
        
        if len(successful_statuses) == len(statuses):
            self.log_test("Filter Batches by Status", True, f"Successfully filtered batches by status: {successful_statuses}")
        else:
            self.log_test("Filter Batches by Status", False, f"Failed to filter some statuses")

    def test_marble_dust_summary_analytics(self):
        """Test GET /api/marble-dust/summary - Production statistics and profit analysis"""
        if not self.token:
            self.log_test("Get Marble Dust Summary", False, "No token available - login failed")
            return
            
        success, data, status_code = self.make_request("GET", "/marble-dust/summary")
        
        if success and status_code == 200:
            required_keys = ["total_batches", "quality_counts", "status_counts", 
                           "production_statistics", "recent_batches", "low_stock_batches"]
            has_required_keys = all(key in data for key in required_keys)
            
            if has_required_keys:
                summary = {
                    "Total Batches": data.get("total_batches", 0),
                    "Quality Distribution": data.get("quality_counts", {}),
                    "Status Distribution": data.get("status_counts", {}),
                    "Production Statistics": data.get("production_statistics", {}),
                    "Recent Batches": data.get("recent_batches", 0),
                    "Low Stock Batches": data.get("low_stock_batches", 0)
                }
                
                # Verify production statistics
                production_stats = data.get("production_statistics", {})
                has_financial_metrics = all(key in production_stats for key in 
                    ["total_production_cost", "total_revenue", "total_profit", "profit_margin_percentage"])
                
                if has_financial_metrics:
                    self.log_test("Get Marble Dust Summary", True, f"Retrieved comprehensive summary: {summary}")
                else:
                    missing_financial = [key for key in ["total_production_cost", "total_revenue", "total_profit", "profit_margin_percentage"] 
                                       if key not in production_stats]
                    self.log_test("Get Marble Dust Summary", False, f"Missing financial metrics: {missing_financial}")
            else:
                missing_keys = [key for key in required_keys if key not in data]
                self.log_test("Get Marble Dust Summary", False, f"Missing required keys: {missing_keys}")
        else:
            self.log_test("Get Marble Dust Summary", False, f"Status: {status_code}", data)

    def test_marble_dust_batch_number_uniqueness(self):
        """Test batch number uniqueness validation"""
        if not self.token:
            self.log_test("Batch Number Uniqueness", False, "No token available - login failed")
            return
            
        # Create a batch with a specific batch number
        unique_batch_number = f"MB-UNIQUE-TEST-{datetime.now().strftime('%H%M%S')}"
        
        batch_data = {
            "batch_number": unique_batch_number,
            "production_date": "2025-01-15T08:00:00Z",
            "quantity_kg": 500.0,
            "quality_grade": "standard",
            "source_material": "Local Marble",
            "production_location": "Test Facility",
            "cost_per_kg": 1.00,
            "selling_price_per_kg": 1.50,
            "notes": "Test batch for uniqueness validation"
        }
        
        # Create first batch
        success, data, status_code = self.make_request("POST", "/marble-dust", batch_data)
        
        if success and status_code == 200:
            # Try to create another batch with the same batch number (should fail)
            success, data, status_code = self.make_request("POST", "/marble-dust", batch_data)
            
            if not success and status_code == 400:
                error_detail = data.get("detail", "")
                if "already exists" in error_detail or "unique" in error_detail.lower():
                    self.log_test("Batch Number Uniqueness", True, f"Correctly prevented duplicate batch number: {error_detail}")
                else:
                    self.log_test("Batch Number Uniqueness", False, f"Wrong error message: {error_detail}")
            else:
                self.log_test("Batch Number Uniqueness", False, f"Should have failed but got status: {status_code}")
        else:
            self.log_test("Batch Number Uniqueness", False, f"Could not create initial batch: {status_code}")

    def test_marble_dust_manufacturing_workflow(self):
        """Test complete manufacturing workflow through production lifecycle"""
        if not self.token:
            self.log_test("Manufacturing Workflow", False, "No token available - login failed")
            return
            
        # Create a batch in production
        batch_data = {
            "batch_number": f"MB-WORKFLOW-{datetime.now().strftime('%H%M%S')}",
            "production_date": "2025-01-15T08:00:00Z",
            "quantity_kg": 800.0,
            "quality_grade": "premium",
            "source_material": "Italian Carrara Marble",
            "production_location": "Main Production Line",
            "cost_per_kg": 1.30,
            "selling_price_per_kg": 2.20,
            "notes": "Test batch for workflow validation"
        }
        
        success, data, status_code = self.make_request("POST", "/marble-dust", batch_data)
        
        if not success or status_code != 200:
            self.log_test("Manufacturing Workflow", False, "Could not create initial batch")
            return
            
        batch_id = data.get("id")
        workflow_steps = [
            {"status": "in_production", "description": "Production started"},
            {"status": "quality_check", "description": "Quality testing phase"},
            {"status": "ready", "description": "Ready for shipment"},
            {"status": "shipped", "description": "Shipped to customer"},
            {"status": "sold", "description": "Sale completed"}
        ]
        
        successful_steps = []
        
        for step in workflow_steps:
            update_data = {
                "status": step["status"],
                "notes": f"Workflow test: {step['description']}"
            }
            
            # Add shipped_at timestamp for shipped status
            if step["status"] == "shipped":
                update_data["shipped_at"] = datetime.now().isoformat()
            
            success, data, status_code = self.make_request("PUT", f"/marble-dust/{batch_id}", update_data)
            
            if success and status_code == 200:
                updated_status = data.get("status", "Unknown")
                if updated_status == step["status"]:
                    successful_steps.append(step["status"])
                else:
                    self.log_test("Manufacturing Workflow", False, f"Status update failed for {step['status']}")
                    return
            else:
                self.log_test("Manufacturing Workflow", False, f"Failed to update to {step['status']}: {status_code}")
                return
        
        if len(successful_steps) == len(workflow_steps):
            self.log_test("Manufacturing Workflow", True, f"Complete workflow tested successfully: {' → '.join(successful_steps)}")
        else:
            failed_steps = [step["status"] for step in workflow_steps if step["status"] not in successful_steps]
            self.log_test("Manufacturing Workflow", False, f"Failed workflow steps: {failed_steps}")

    def test_marble_dust_profit_calculations(self):
        """Test profit margin and financial calculations accuracy"""
        if not self.token:
            self.log_test("Profit Calculations", False, "No token available - login failed")
            return
            
        # Create batch with known values for calculation testing
        test_quantity = 1000.0
        test_cost_per_kg = 1.50
        test_selling_price = 2.25
        
        batch_data = {
            "batch_number": f"MB-CALC-TEST-{datetime.now().strftime('%H%M%S')}",
            "production_date": "2025-01-15T08:00:00Z",
            "quantity_kg": test_quantity,
            "quality_grade": "premium",
            "source_material": "Test Material",
            "production_location": "Test Location",
            "cost_per_kg": test_cost_per_kg,
            "selling_price_per_kg": test_selling_price,
            "notes": "Test batch for profit calculation validation"
        }
        
        success, data, status_code = self.make_request("POST", "/marble-dust", batch_data)
        
        if success and status_code == 200:
            # Verify calculations
            total_cost = data.get("total_cost", 0)
            total_revenue = data.get("total_revenue", 0)
            profit_margin = data.get("profit_margin", 0)
            
            # Expected calculations
            expected_total_cost = test_quantity * test_cost_per_kg  # 1000 * 1.50 = 1500
            expected_total_revenue = test_quantity * test_selling_price  # 1000 * 2.25 = 2250
            expected_profit_margin = ((test_selling_price - test_cost_per_kg) / test_cost_per_kg) * 100  # ((2.25 - 1.50) / 1.50) * 100 = 50%
            
            # Check calculations with small tolerance for floating point
            cost_correct = abs(total_cost - expected_total_cost) < 0.01
            revenue_correct = abs(total_revenue - expected_total_revenue) < 0.01
            margin_correct = abs(profit_margin - expected_profit_margin) < 0.01
            
            if cost_correct and revenue_correct and margin_correct:
                self.log_test("Profit Calculations", True, 
                    f"All calculations correct - Cost: {total_cost}, Revenue: {total_revenue}, Margin: {profit_margin:.2f}%")
            else:
                errors = []
                if not cost_correct:
                    errors.append(f"Cost: expected {expected_total_cost}, got {total_cost}")
                if not revenue_correct:
                    errors.append(f"Revenue: expected {expected_total_revenue}, got {total_revenue}")
                if not margin_correct:
                    errors.append(f"Margin: expected {expected_profit_margin:.2f}%, got {profit_margin:.2f}%")
                
                self.log_test("Profit Calculations", False, f"Calculation errors: {'; '.join(errors)}")
        else:
            self.log_test("Profit Calculations", False, f"Could not create test batch: {status_code}")

    def run_marble_dust_tests(self):
        """Run all marble dust production management tests"""
        print("="*80)
        print("MARBLE DUST PRODUCTION MANAGEMENT API TESTING")
        print("="*80)
        print("Testing newly implemented Marble Dust Production Management API endpoints")
        print("to verify complete manufacturing CRUD functionality.")
        print()
        
        # Authentication first
        self.test_authentication_login()
        
        if not self.token:
            print("❌ Cannot proceed with marble dust testing - authentication failed")
            return
        
        print("\n" + "="*60)
        print("TESTING MARBLE DUST PRODUCTION MANAGEMENT API")
        print("="*60)
        
        # Core CRUD operations
        self.test_marble_dust_get_all()
        self.test_marble_dust_create()
        self.test_marble_dust_get_single()
        self.test_marble_dust_update()
        self.test_marble_dust_delete_validation()
        self.test_marble_dust_delete_shipped_validation()
        
        # Filtering and analytics
        self.test_marble_dust_quality_filtering()
        self.test_marble_dust_status_filtering()
        self.test_marble_dust_summary_analytics()
        
        # Business logic and validation
        self.test_marble_dust_batch_number_uniqueness()
        self.test_marble_dust_manufacturing_workflow()
        self.test_marble_dust_profit_calculations()
        
        # Print summary
        self.print_test_summary()

    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*80)
        print("MARBLE DUST PRODUCTION MANAGEMENT API TEST SUMMARY")
        print("="*80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        # Categorize tests
        core_crud_tests = [r for r in self.test_results if any(keyword in r["test"] for keyword in ["Get All", "Create", "Get Single", "Update", "Delete"])]
        filtering_tests = [r for r in self.test_results if "Filter" in r["test"] or "Summary" in r["test"]]
        business_logic_tests = [r for r in self.test_results if any(keyword in r["test"] for keyword in ["Uniqueness", "Workflow", "Calculations"])]
        
        print("🔧 CORE CRUD OPERATIONS:")
        for test in core_crud_tests:
            status = "✅" if test["success"] else "❌"
            print(f"   {status} {test['test']}")
        
        print("\n🔍 FILTERING & ANALYTICS:")
        for test in filtering_tests:
            status = "✅" if test["success"] else "❌"
            print(f"   {status} {test['test']}")
        
        print("\n💼 BUSINESS LOGIC & VALIDATION:")
        for test in business_logic_tests:
            status = "✅" if test["success"] else "❌"
            print(f"   {status} {test['test']}")
        
        if failed_tests > 0:
            print("\n🚨 FAILED TESTS DETAILS:")
            print("-" * 50)
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test']}")
                    print(f"   Details: {result['details']}")
                    if result.get("response_data"):
                        print(f"   Response: {result['response_data']}")
                    print()
        
        print("\n🎯 KEY FINDINGS:")
        print("-" * 30)
        
        # Check endpoint availability
        endpoint_tests = [r for r in self.test_results if any(keyword in r["test"] for keyword in ["Get All", "Create", "Get Single", "Update", "Delete", "Filter", "Summary"])]
        working_endpoints = sum(1 for r in endpoint_tests if r["success"])
        total_endpoints = 8  # Expected 8 marble dust endpoints
        
        if working_endpoints == total_endpoints:
            print("✅ All 8 Marble Dust Production Management API endpoints are working correctly")
        elif working_endpoints > 0:
            print(f"⚠️  {working_endpoints}/{total_endpoints} endpoints working ({(working_endpoints/total_endpoints)*100:.1f}%)")
        else:
            print("🚨 CRITICAL: No marble dust endpoints are working")
        
        # Check manufacturing features
        manufacturing_features = [r for r in self.test_results if any(keyword in r["test"] for keyword in ["Workflow", "Calculations", "Uniqueness"])]
        working_features = sum(1 for r in manufacturing_features if r["success"])
        
        if working_features == len(manufacturing_features):
            print("✅ All manufacturing features working (batch tracking, profit calculations, workflow management)")
        elif working_features > 0:
            print(f"⚠️  {working_features}/{len(manufacturing_features)} manufacturing features working")
        else:
            print("🚨 Manufacturing features not working properly")
        
        # Overall assessment
        if passed_tests == total_tests:
            print("🎉 MARBLE DUST PRODUCTION MANAGEMENT MODULE IS FULLY FUNCTIONAL AND PRODUCTION-READY")
        elif passed_tests >= total_tests * 0.8:
            print("✅ Marble Dust Production Management module is mostly functional with minor issues")
        elif passed_tests >= total_tests * 0.5:
            print("⚠️  Marble Dust Production Management module has significant issues that need attention")
        else:
            print("🚨 CRITICAL: Marble Dust Production Management module is not functional")
        
        print("="*80)

if __name__ == "__main__":
    tester = MarbleDustTester()
    tester.run_marble_dust_tests()