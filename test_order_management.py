#!/usr/bin/env python3
"""
Enhanced Order Management API Testing Script
Tests all Order Management endpoints as requested in the review
"""

import sys
import os
sys.path.append('/app')

from backend_test import BackendTester

def main():
    """Run enhanced Order Management API tests"""
    print("=" * 80)
    print("ENHANCED ORDER MANAGEMENT API TESTING")
    print("=" * 80)
    print("Testing all Order Management endpoints with specific scenarios:")
    print("1. GET /api/orders - All orders with client and item details")
    print("2. GET /api/orders/{order_id} - Single order details")
    print("3. POST /api/orders - Create order with stock validation")
    print("4. PUT /api/orders/{order_id} - Update order details")
    print("5. DELETE /api/orders/{order_id} - Delete with validation")
    print("6. GET /api/orders/status/{status} - Filter by status")
    print("7. PUT /api/orders/{order_id}/status - Update status")
    print("=" * 80)
    print()
    
    tester = BackendTester()
    
    # First authenticate
    print("🔐 Authenticating...")
    tester.test_authentication_login()
    
    if not tester.token:
        print("❌ Authentication failed - cannot proceed with tests")
        return
    
    print("✅ Authentication successful")
    print()
    
    # Run enhanced order management tests
    tester.run_enhanced_order_tests()
    
    # Print summary focused on order management
    print("\n" + "=" * 80)
    print("ORDER MANAGEMENT API TEST SUMMARY")
    print("=" * 80)
    
    order_tests = [r for r in tester.test_results if "Order" in r["test"]]
    total_order_tests = len(order_tests)
    passed_order_tests = sum(1 for result in order_tests if result["success"])
    failed_order_tests = total_order_tests - passed_order_tests
    
    print(f"Order Management Tests: {total_order_tests}")
    print(f"Passed: {passed_order_tests}")
    print(f"Failed: {failed_order_tests}")
    print(f"Success Rate: {(passed_order_tests/total_order_tests)*100:.1f}%" if total_order_tests > 0 else "No tests run")
    print()
    
    if failed_order_tests > 0:
        print("FAILED ORDER TESTS:")
        print("-" * 40)
        for result in order_tests:
            if not result["success"]:
                print(f"❌ {result['test']}: {result['details']}")
        print()
    
    print("PASSED ORDER TESTS:")
    print("-" * 40)
    for result in order_tests:
        if result["success"]:
            print(f"✅ {result['test']}: {result['details']}")
    
    print("=" * 80)

if __name__ == "__main__":
    main()