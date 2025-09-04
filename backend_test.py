#!/usr/bin/env python3
"""
Backend API Tests for Cyber Airways
Tests the FastAPI backend endpoints for flight readiness functionality
"""

import requests
import json
import sys
from typing import Dict, Any

# Get backend URL from environment
BACKEND_URL = "https://cyber-airways.preview.emergentagent.com/api"

class CyberAirwaysAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        
    def test_root_endpoint(self):
        """Test GET /api/ endpoint"""
        try:
            response = requests.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and data["message"] == "Hello World":
                    self.log_test("Root endpoint GET /api/", True, f"Response: {data}")
                else:
                    self.log_test("Root endpoint GET /api/", False, f"Unexpected response: {data}")
            else:
                self.log_test("Root endpoint GET /api/", False, f"Status code: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            self.log_test("Root endpoint GET /api/", False, f"Exception: {str(e)}")
    
    def test_flight_readiness_valid_ca1(self):
        """Test flight readiness with booking reference ending in '1' (should return 'ready')"""
        payload = {
            "bookingReference": "CA12345671",
            "lastName": "Smith"
        }
        
        try:
            response = requests.post(f"{self.base_url}/flight-readiness", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                expected_fields = ["status", "message", "flightNumber", "departure", "gate"]
                
                if all(field in data for field in expected_fields):
                    if data["status"] == "ready":
                        self.log_test("Flight readiness CA ending with '1'", True, f"Status: {data['status']}, Flight: {data['flightNumber']}")
                    else:
                        self.log_test("Flight readiness CA ending with '1'", False, f"Expected 'ready' status, got: {data['status']}")
                else:
                    self.log_test("Flight readiness CA ending with '1'", False, f"Missing required fields in response: {data}")
            else:
                self.log_test("Flight readiness CA ending with '1'", False, f"Status code: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            self.log_test("Flight readiness CA ending with '1'", False, f"Exception: {str(e)}")
    
    def test_flight_readiness_valid_ca2(self):
        """Test flight readiness with booking reference ending in '2' (should return 'delayed')"""
        payload = {
            "bookingReference": "CA12345672",
            "lastName": "Johnson"
        }
        
        try:
            response = requests.post(f"{self.base_url}/flight-readiness", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "delayed":
                    self.log_test("Flight readiness CA ending with '2'", True, f"Status: {data['status']}, Message: {data['message']}")
                else:
                    self.log_test("Flight readiness CA ending with '2'", False, f"Expected 'delayed' status, got: {data['status']}")
            else:
                self.log_test("Flight readiness CA ending with '2'", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Flight readiness CA ending with '2'", False, f"Exception: {str(e)}")
    
    def test_flight_readiness_valid_ca3(self):
        """Test flight readiness with booking reference ending in '3' (should return 'cancelled')"""
        payload = {
            "bookingReference": "CA12345673",
            "lastName": "Williams"
        }
        
        try:
            response = requests.post(f"{self.base_url}/flight-readiness", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "cancelled":
                    self.log_test("Flight readiness CA ending with '3'", True, f"Status: {data['status']}, Message: {data['message']}")
                else:
                    self.log_test("Flight readiness CA ending with '3'", False, f"Expected 'cancelled' status, got: {data['status']}")
            else:
                self.log_test("Flight readiness CA ending with '3'", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Flight readiness CA ending with '3'", False, f"Exception: {str(e)}")
    
    def test_flight_readiness_valid_ca_other(self):
        """Test flight readiness with booking reference ending in other numbers (should return 'ready')"""
        payload = {
            "bookingReference": "CA12345679",
            "lastName": "Brown"
        }
        
        try:
            response = requests.post(f"{self.base_url}/flight-readiness", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "ready":
                    self.log_test("Flight readiness CA ending with other numbers", True, f"Status: {data['status']}, Flight: {data['flightNumber']}")
                else:
                    self.log_test("Flight readiness CA ending with other numbers", False, f"Expected 'ready' status, got: {data['status']}")
            else:
                self.log_test("Flight readiness CA ending with other numbers", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Flight readiness CA ending with other numbers", False, f"Exception: {str(e)}")
    
    def test_flight_readiness_invalid_reference(self):
        """Test flight readiness with invalid booking reference (should return 'unknown')"""
        payload = {
            "bookingReference": "XY12345671",
            "lastName": "Davis"
        }
        
        try:
            response = requests.post(f"{self.base_url}/flight-readiness", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "unknown":
                    self.log_test("Flight readiness invalid reference", True, f"Status: {data['status']}, Message: {data['message']}")
                else:
                    self.log_test("Flight readiness invalid reference", False, f"Expected 'unknown' status, got: {data['status']}")
            else:
                self.log_test("Flight readiness invalid reference", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Flight readiness invalid reference", False, f"Exception: {str(e)}")
    
    def test_flight_readiness_case_handling(self):
        """Test flight readiness with lowercase input (should handle case conversion)"""
        payload = {
            "bookingReference": "ca12345671",
            "lastName": "miller"
        }
        
        try:
            response = requests.post(f"{self.base_url}/flight-readiness", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "ready":
                    self.log_test("Flight readiness case handling", True, f"Lowercase input handled correctly, Status: {data['status']}")
                else:
                    self.log_test("Flight readiness case handling", False, f"Case handling failed, Status: {data['status']}")
            else:
                self.log_test("Flight readiness case handling", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Flight readiness case handling", False, f"Exception: {str(e)}")
    
    def test_flight_readiness_missing_fields(self):
        """Test flight readiness with missing fields (should return validation error)"""
        payload = {
            "bookingReference": "CA12345671"
            # Missing lastName field
        }
        
        try:
            response = requests.post(f"{self.base_url}/flight-readiness", json=payload)
            
            if response.status_code == 422:  # FastAPI validation error
                self.log_test("Flight readiness missing fields validation", True, "Validation error returned as expected")
            elif response.status_code == 200:
                self.log_test("Flight readiness missing fields validation", False, "Should have returned validation error but got 200")
            else:
                self.log_test("Flight readiness missing fields validation", False, f"Unexpected status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Flight readiness missing fields validation", False, f"Exception: {str(e)}")
    
    def test_flight_readiness_empty_fields(self):
        """Test flight readiness with empty fields"""
        payload = {
            "bookingReference": "",
            "lastName": ""
        }
        
        try:
            response = requests.post(f"{self.base_url}/flight-readiness", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                # Empty booking reference should not start with CA, so should return unknown
                if data["status"] == "unknown":
                    self.log_test("Flight readiness empty fields", True, f"Empty fields handled correctly, Status: {data['status']}")
                else:
                    self.log_test("Flight readiness empty fields", False, f"Unexpected status for empty fields: {data['status']}")
            else:
                self.log_test("Flight readiness empty fields", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Flight readiness empty fields", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("CYBER AIRWAYS BACKEND API TESTS")
        print("=" * 60)
        print(f"Testing backend at: {self.base_url}")
        print()
        
        # Test root endpoint
        self.test_root_endpoint()
        
        # Test flight readiness endpoint with various scenarios
        self.test_flight_readiness_valid_ca1()
        self.test_flight_readiness_valid_ca2()
        self.test_flight_readiness_valid_ca3()
        self.test_flight_readiness_valid_ca_other()
        self.test_flight_readiness_invalid_reference()
        self.test_flight_readiness_case_handling()
        self.test_flight_readiness_missing_fields()
        self.test_flight_readiness_empty_fields()
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        
        if total - passed > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
        
        return passed == total

if __name__ == "__main__":
    tester = CyberAirwaysAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)