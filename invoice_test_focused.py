#!/usr/bin/env python3
"""
Focused Invoice Module Testing - Re-testing previously failing endpoints
Tests the specific endpoints mentioned in the review request that had routing conflicts and field mapping issues
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

class InvoiceTester:
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
            print(f"🔐 Authenticated as: {user_name}")
            return True
        else:
            print(f"❌ Authentication failed: {data}")
            return False

    def test_invoice_summary(self):
        """Test GET /api/invoices/summary - Previously failing due to routing conflict"""
        if not self.token:
            self.log_test("Invoice Summary", False, "No token available - authentication failed")
            return
            
        success, data, status_code = self.make_request("GET", "/invoices/summary")
        
        if success and status_code == 200:
            # Check for required summary fields
            required_fields = ["total_invoices", "status_counts", "total_invoiced", "total_paid", "total_outstanding"]
            has_required_fields = all(field in data for field in required_fields)
            
            if has_required_fields:
                summary_info = {
                    "Total Invoices": data.get("total_invoices", 0),
                    "Total Invoiced": f"RWF {data.get('total_invoiced', 0):,.2f}",
                    "Total Paid": f"RWF {data.get('total_paid', 0):,.2f}",
                    "Total Outstanding": f"RWF {data.get('total_outstanding', 0):,.2f}",
                    "Overdue Count": data.get("overdue_count", 0),
                    "Monthly Invoices": data.get("monthly_invoices", 0)
                }
                self.log_test("Invoice Summary", True, f"Retrieved comprehensive summary: {summary_info}")
            else:
                missing_fields = [field for field in required_fields if field not in data]
                self.log_test("Invoice Summary", False, f"Missing required fields: {missing_fields}")
        else:
            self.log_test("Invoice Summary", False, f"Status: {status_code}", data)

    def test_overdue_invoices(self):
        """Test GET /api/invoices/overdue - Previously failing due to routing conflict"""
        if not self.token:
            self.log_test("Overdue Invoices", False, "No token available - authentication failed")
            return
            
        success, data, status_code = self.make_request("GET", "/invoices/overdue")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                # Check if overdue invoices have required fields
                first_invoice = data[0]
                required_fields = ["id", "invoice_number", "client_name", "total_amount", "balance_due", "due_date", "days_overdue"]
                has_required_fields = all(field in first_invoice for field in required_fields)
                
                if has_required_fields:
                    overdue_amounts = [invoice.get("balance_due", 0) for invoice in data]
                    total_overdue = sum(overdue_amounts)
                    self.log_test("Overdue Invoices", True, f"Retrieved {count} overdue invoices, total overdue: RWF {total_overdue:,.2f}")
                else:
                    missing_fields = [field for field in required_fields if field not in first_invoice]
                    self.log_test("Overdue Invoices", False, f"Missing required fields in overdue invoices: {missing_fields}")
            else:
                self.log_test("Overdue Invoices", True, "No overdue invoices found (good!)")
        else:
            self.log_test("Overdue Invoices", False, f"Status: {status_code}", data)

    def test_invoice_logs(self):
        """Test GET /api/invoices/{id}/logs - Previously failing due to field mapping issue"""
        if not self.token:
            self.log_test("Invoice Logs", False, "No token available - authentication failed")
            return
            
        # First get an existing invoice
        success, invoices, _ = self.make_request("GET", "/invoices")
        if not success or not invoices or len(invoices) == 0:
            self.log_test("Invoice Logs", False, "No invoices available for logs test")
            return
            
        invoice_id = invoices[0].get("id")
        invoice_number = invoices[0].get("invoice_number", "Unknown")
        
        success, data, status_code = self.make_request("GET", f"/invoices/{invoice_id}/logs")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                # Check if logs have required fields (previously had field mapping issues)
                first_log = data[0]
                required_fields = ["id", "action", "description", "performed_by", "performed_at"]
                has_required_fields = all(field in first_log for field in required_fields)
                
                if has_required_fields:
                    actions = list(set(log.get("action", "Unknown") for log in data))
                    self.log_test("Invoice Logs", True, f"Retrieved {count} audit logs for invoice {invoice_number}, actions: {actions}")
                else:
                    missing_fields = [field for field in required_fields if field not in first_log]
                    self.log_test("Invoice Logs", False, f"Field mapping issue - missing fields: {missing_fields}")
            else:
                self.log_test("Invoice Logs", True, f"No audit logs found for invoice {invoice_number}")
        else:
            self.log_test("Invoice Logs", False, f"Status: {status_code}", data)

    def test_generate_invoice_from_service(self):
        """Test POST /api/invoices/generate-from-service/{id} - Previously failing due to field mapping issue"""
        if not self.token:
            self.log_test("Generate Invoice from Service", False, "No token available - authentication failed")
            return
            
        # First get an existing service booking that doesn't have an invoice yet
        success, bookings, _ = self.make_request("GET", "/services/bookings")
        if not success or not bookings or len(bookings) == 0:
            self.log_test("Generate Invoice from Service", False, "No service bookings available for invoice generation")
            return
            
        # Find a booking that doesn't have an invoice yet
        suitable_booking = None
        for booking in bookings:
            booking_id = booking.get("id")
            # Check if invoice already exists for this booking
            success, invoices, _ = self.make_request("GET", "/invoices")
            if success and invoices:
                existing_invoice = any(inv.get("service_booking_id") == booking_id for inv in invoices)
                if not existing_invoice and booking.get("status") == "completed":
                    suitable_booking = booking
                    break
        
        if not suitable_booking:
            # Create a new service booking for testing
            booking_data = {
                "client_name": "Test Invoice Generation Client",
                "client_email": "testinvoice@example.rw",
                "client_phone": "+250788123456",
                "service_type": "consultation",
                "description": "Test service for invoice generation",
                "preferred_date": "2025-01-25T10:00:00",
                "location": "Test Location",
                "cost_estimate": 150000.0,
                "notes": "Test booking for invoice generation"
            }
            
            success, booking_response, _ = self.make_request("POST", "/services/bookings", booking_data)
            if success and booking_response.get("id"):
                # Update booking to completed status so we can generate invoice
                booking_id = booking_response.get("id")
                update_data = {"status": "completed", "actual_cost": 150000.0}
                self.make_request("PUT", f"/services/bookings/{booking_id}", update_data)
                suitable_booking = {"id": booking_id, "booking_number": booking_response.get("booking_number")}
            else:
                self.log_test("Generate Invoice from Service", False, "Could not create test service booking")
                return
        
        booking_id = suitable_booking.get("id")
        booking_number = suitable_booking.get("booking_number", "Unknown")
        
        success, data, status_code = self.make_request("POST", f"/invoices/generate-from-service/{booking_id}")
        
        if success and status_code == 200 and data.get("id"):
            invoice_id = data.get("id")
            invoice_number = data.get("invoice_number")
            total_amount = data.get("total_amount", 0)
            
            # Verify invoice was created with correct field mappings
            success, invoice_details, _ = self.make_request("GET", f"/invoices/{invoice_id}")
            if success and invoice_details:
                # Check for proper field mapping (previously had issues)
                required_fields = ["service_booking_id", "client_name", "total_amount", "status"]
                has_required_fields = all(field in invoice_details for field in required_fields)
                
                if has_required_fields and invoice_details.get("service_booking_id") == booking_id:
                    self.log_test("Generate Invoice from Service", True, f"Generated invoice {invoice_number} from service booking {booking_number}, total: RWF {total_amount:,.2f}")
                else:
                    self.log_test("Generate Invoice from Service", False, f"Field mapping issue - invoice created but missing required fields or incorrect service_booking_id")
            else:
                self.log_test("Generate Invoice from Service", False, "Invoice created but could not retrieve details for validation")
        else:
            self.log_test("Generate Invoice from Service", False, f"Status: {status_code}", data)

    def test_all_invoice_crud_operations(self):
        """Test all 13 invoice endpoints mentioned in the review request"""
        print("\n" + "="*80)
        print("COMPREHENSIVE INVOICE MODULE CRUD OPERATIONS TEST")
        print("Testing all 13 endpoints mentioned in the review request")
        print("="*80)
        
        # Test the previously failing endpoints first
        print("\n🎯 TESTING PREVIOUSLY FAILING ENDPOINTS:")
        print("-" * 50)
        self.test_invoice_summary()
        self.test_overdue_invoices()
        self.test_invoice_logs()
        self.test_generate_invoice_from_service()
        
        # Test all other CRUD operations
        print("\n📋 TESTING ALL CRUD OPERATIONS:")
        print("-" * 50)
        self.test_get_all_invoices()
        self.test_get_single_invoice()
        self.test_create_invoice()
        self.test_update_invoice()
        self.test_delete_invoice()
        
        # Test payment operations
        print("\n💰 TESTING PAYMENT OPERATIONS:")
        print("-" * 50)
        self.test_add_invoice_payment()
        self.test_get_invoice_payments()
        
        # Test filtering and status operations
        print("\n🔍 TESTING FILTERING AND STATUS OPERATIONS:")
        print("-" * 50)
        self.test_get_invoices_by_status()
        
        # Test integration endpoints
        print("\n🔗 TESTING INTEGRATION ENDPOINTS:")
        print("-" * 50)
        self.test_generate_invoice_from_order()

    def test_get_all_invoices(self):
        """Test GET /api/invoices - Get all invoices"""
        success, data, status_code = self.make_request("GET", "/invoices")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                statuses = list(set(invoice.get("status", "Unknown") for invoice in data))
                types = list(set(invoice.get("invoice_type", "Unknown") for invoice in data))
                self.log_test("Get All Invoices", True, f"Retrieved {count} invoices, statuses: {statuses}, types: {types}")
            else:
                self.log_test("Get All Invoices", True, "No invoices found")
        else:
            self.log_test("Get All Invoices", False, f"Status: {status_code}", data)

    def test_get_single_invoice(self):
        """Test GET /api/invoices/{id} - Get single invoice"""
        # Get an existing invoice first
        success, invoices, _ = self.make_request("GET", "/invoices")
        if not success or not invoices or len(invoices) == 0:
            self.log_test("Get Single Invoice", False, "No invoices available for single invoice test")
            return
            
        invoice_id = invoices[0].get("id")
        invoice_number = invoices[0].get("invoice_number", "Unknown")
        
        success, data, status_code = self.make_request("GET", f"/invoices/{invoice_id}")
        
        if success and status_code == 200 and data.get("id"):
            items_count = len(data.get("items", []))
            payments_count = len(data.get("payments", []))
            status = data.get("status", "Unknown")
            self.log_test("Get Single Invoice", True, f"Retrieved invoice {invoice_number}: status={status}, items={items_count}, payments={payments_count}")
        else:
            self.log_test("Get Single Invoice", False, f"Status: {status_code}", data)

    def test_create_invoice(self):
        """Test POST /api/invoices - Create new invoice (currently missing endpoint)"""
        # This endpoint is currently missing from the backend, so it will fail with 405
        invoice_data = {
            "invoice_type": "manual",
            "client_name": "Test Client for Invoice Creation",
            "client_email": "testclient@example.rw",
            "client_phone": "+250788999888",
            "due_date": "2025-02-15",
            "items": [
                {
                    "item_type": "product",
                    "description": "Test Product",
                    "quantity": 2,
                    "unit_price": 50000.0
                }
            ],
            "notes": "Test invoice creation"
        }
        
        success, data, status_code = self.make_request("POST", "/invoices", invoice_data)
        
        if success and status_code == 200 and data.get("id"):
            invoice_id = data.get("id")
            invoice_number = data.get("invoice_number")
            self.log_test("Create Invoice", True, f"Created invoice {invoice_number} with ID: {invoice_id}")
            return invoice_id
        else:
            if status_code == 405:
                self.log_test("Create Invoice", False, "Endpoint not implemented (405 Method Not Allowed)", data)
            else:
                self.log_test("Create Invoice", False, f"Status: {status_code}", data)
            return None

    def test_update_invoice(self):
        """Test PUT /api/invoices/{id} - Update invoice (currently missing endpoint)"""
        # Get an existing invoice first
        success, invoices, _ = self.make_request("GET", "/invoices")
        if not success or not invoices or len(invoices) == 0:
            self.log_test("Update Invoice", False, "No invoices available for update test")
            return
            
        invoice_id = invoices[0].get("id")
        
        update_data = {
            "notes": "Updated invoice notes via API test",
            "terms": "Updated payment terms"
        }
        
        success, data, status_code = self.make_request("PUT", f"/invoices/{invoice_id}", update_data)
        
        if success and status_code == 200 and data.get("id"):
            self.log_test("Update Invoice", True, f"Updated invoice {invoice_id}")
        else:
            if status_code == 405:
                self.log_test("Update Invoice", False, "Endpoint not implemented (405 Method Not Allowed)", data)
            else:
                self.log_test("Update Invoice", False, f"Status: {status_code}", data)

    def test_delete_invoice(self):
        """Test DELETE /api/invoices/{id} - Delete invoice (currently missing endpoint)"""
        # This would require creating a test invoice first, but since POST is not implemented, we'll test with existing
        success, invoices, _ = self.make_request("GET", "/invoices")
        if not success or not invoices or len(invoices) == 0:
            self.log_test("Delete Invoice", False, "No invoices available for delete test")
            return
            
        # Find a draft invoice that can be safely deleted
        draft_invoice = None
        for invoice in invoices:
            if invoice.get("status") == "draft":
                draft_invoice = invoice
                break
        
        if not draft_invoice:
            self.log_test("Delete Invoice", False, "No draft invoices available for safe deletion test")
            return
            
        invoice_id = draft_invoice.get("id")
        
        success, data, status_code = self.make_request("DELETE", f"/invoices/{invoice_id}")
        
        if success and status_code == 200:
            self.log_test("Delete Invoice", True, f"Successfully deleted invoice {invoice_id}")
        else:
            if status_code == 405:
                self.log_test("Delete Invoice", False, "Endpoint not implemented (405 Method Not Allowed)", data)
            else:
                self.log_test("Delete Invoice", False, f"Status: {status_code}", data)

    def test_add_invoice_payment(self):
        """Test POST /api/invoices/{id}/payments - Add payment to invoice (currently missing endpoint)"""
        # Get an existing invoice first
        success, invoices, _ = self.make_request("GET", "/invoices")
        if not success or not invoices or len(invoices) == 0:
            self.log_test("Add Invoice Payment", False, "No invoices available for payment test")
            return
            
        # Find an invoice with outstanding balance
        invoice_with_balance = None
        for invoice in invoices:
            if invoice.get("balance_due", 0) > 0:
                invoice_with_balance = invoice
                break
        
        if not invoice_with_balance:
            self.log_test("Add Invoice Payment", False, "No invoices with outstanding balance for payment test")
            return
            
        invoice_id = invoice_with_balance.get("id")
        balance_due = invoice_with_balance.get("balance_due", 0)
        
        payment_data = {
            "payment_method": "bank_transfer",
            "amount": min(balance_due, 100000.0),  # Pay partial or full amount
            "payment_date": datetime.now().isoformat(),
            "reference_number": "TEST-PAY-001",
            "notes": "Test payment via API"
        }
        
        success, data, status_code = self.make_request("POST", f"/invoices/{invoice_id}/payments", payment_data)
        
        if success and status_code == 200 and data.get("id"):
            payment_id = data.get("id")
            amount = data.get("amount", 0)
            self.log_test("Add Invoice Payment", True, f"Added payment {payment_id} of RWF {amount:,.2f} to invoice {invoice_id}")
        else:
            if status_code == 405:
                self.log_test("Add Invoice Payment", False, "Endpoint not implemented (405 Method Not Allowed)", data)
            else:
                self.log_test("Add Invoice Payment", False, f"Status: {status_code}", data)

    def test_get_invoice_payments(self):
        """Test GET /api/invoices/{id}/payments - Get invoice payments"""
        # Get an existing invoice first
        success, invoices, _ = self.make_request("GET", "/invoices")
        if not success or not invoices or len(invoices) == 0:
            self.log_test("Get Invoice Payments", False, "No invoices available for payments test")
            return
            
        invoice_id = invoices[0].get("id")
        invoice_number = invoices[0].get("invoice_number", "Unknown")
        
        success, data, status_code = self.make_request("GET", f"/invoices/{invoice_id}/payments")
        
        if success and status_code == 200 and isinstance(data, list):
            count = len(data)
            if count > 0:
                payment_methods = list(set(payment.get("payment_method", "Unknown") for payment in data))
                total_payments = sum(payment.get("amount", 0) for payment in data)
                self.log_test("Get Invoice Payments", True, f"Retrieved {count} payments for invoice {invoice_number}, methods: {payment_methods}, total: RWF {total_payments:,.2f}")
            else:
                self.log_test("Get Invoice Payments", True, f"No payments found for invoice {invoice_number}")
        else:
            self.log_test("Get Invoice Payments", False, f"Status: {status_code}", data)

    def test_get_invoices_by_status(self):
        """Test GET /api/invoices/status/{status} - Filter invoices by status"""
        statuses_to_test = ["draft", "sent", "paid", "overdue"]
        successful_statuses = []
        
        for status in statuses_to_test:
            success, data, status_code = self.make_request("GET", f"/invoices/status/{status}")
            
            if success and status_code == 200 and isinstance(data, list):
                count = len(data)
                successful_statuses.append(f"{status}({count})")
        
        if len(successful_statuses) > 0:
            self.log_test("Get Invoices by Status", True, f"Retrieved invoices by status: {successful_statuses}")
        else:
            self.log_test("Get Invoices by Status", False, "Failed to retrieve invoices by any status")

    def test_generate_invoice_from_order(self):
        """Test POST /api/invoices/generate-from-order/{id} - Generate invoice from order"""
        # Get an existing order that doesn't have an invoice yet
        success, orders, _ = self.make_request("GET", "/orders")
        if not success or not orders or len(orders) == 0:
            self.log_test("Generate Invoice from Order", False, "No orders available for invoice generation")
            return
            
        # Find an order that doesn't have an invoice yet
        suitable_order = None
        for order in orders:
            order_id = order.get("id")
            # Check if invoice already exists for this order
            success, invoices, _ = self.make_request("GET", "/invoices")
            if success and invoices:
                existing_invoice = any(inv.get("order_id") == order_id for inv in invoices)
                if not existing_invoice:
                    suitable_order = order
                    break
        
        if not suitable_order:
            self.log_test("Generate Invoice from Order", False, "All existing orders already have invoices")
            return
            
        order_id = suitable_order.get("id")
        order_number = suitable_order.get("order_number", "Unknown")
        
        success, data, status_code = self.make_request("POST", f"/invoices/generate-from-order/{order_id}")
        
        if success and status_code == 200 and data.get("id"):
            invoice_id = data.get("id")
            invoice_number = data.get("invoice_number")
            total_amount = data.get("total_amount", 0)
            self.log_test("Generate Invoice from Order", True, f"Generated invoice {invoice_number} from order {order_number}, total: RWF {total_amount:,.2f}")
        else:
            self.log_test("Generate Invoice from Order", False, f"Status: {status_code}", data)

    def print_summary(self):
        """Print test summary"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "="*80)
        print("INVOICE MODULE TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print(f"\nFAILED TESTS:")
            print("-" * 40)
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test']}: {result['details']}")
        
        # Analyze the results
        print(f"\n🎯 ANALYSIS:")
        print("-" * 40)
        
        working_endpoints = [r for r in self.test_results if r["success"]]
        missing_endpoints = [r for r in self.test_results if not r["success"] and "405" in str(r.get("response_data", {}))]
        
        print(f"✅ Working Endpoints: {len(working_endpoints)}")
        print(f"❌ Missing Endpoints (405): {len(missing_endpoints)}")
        
        if len(missing_endpoints) > 0:
            print(f"\n🚨 MISSING ENDPOINTS THAT NEED IMPLEMENTATION:")
            for result in missing_endpoints:
                print(f"   - {result['test']}")

def main():
    print("="*80)
    print("INVOICE MODULE FOCUSED TESTING")
    print("Re-testing previously failing endpoints after routing fixes")
    print("="*80)
    print(f"Testing against: {BASE_URL}")
    print(f"Demo Account: {DEMO_ADMIN_EMAIL}")
    print("="*80)
    
    tester = InvoiceTester()
    
    # Authenticate first
    if not tester.authenticate():
        print("❌ Authentication failed. Cannot proceed with tests.")
        sys.exit(1)
    
    # Run all invoice tests
    tester.test_all_invoice_crud_operations()
    
    # Print summary
    tester.print_summary()

if __name__ == "__main__":
    main()