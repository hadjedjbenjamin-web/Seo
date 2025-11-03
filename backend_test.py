#!/usr/bin/env python3
"""
Backend API Testing for Contact Form with ZeptoMail SMTP Integration
Tests the /api/contact endpoint functionality
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE_URL = f"{BACKEND_URL}/api"

def test_contact_form_valid_submission():
    """Test valid contact form submission"""
    print("🧪 Testing valid contact form submission...")
    
    # Test data as suggested in the review request
    test_data = {
        "name": "Test User BK Tech",
        "email": "test@example.com",
        "phone": "+33 6 12 34 56 78",
        "message": "Ceci est un message de test pour vérifier l'intégration SMTP ZeptoMail avec le formulaire de contact BK Tech."
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/contact",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") == True:
                print("✅ Valid submission test PASSED")
                print(f"   Message: {data.get('message')}")
                if data.get('message_id'):
                    print(f"   Message ID: {data.get('message_id')}")
                return True
            else:
                print("❌ Valid submission test FAILED - success=False")
                print(f"   Error message: {data.get('message')}")
                return False
        else:
            print(f"❌ Valid submission test FAILED - Status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Valid submission test FAILED - Request error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Valid submission test FAILED - Unexpected error: {str(e)}")
        return False

def test_contact_form_missing_fields():
    """Test contact form with missing required fields"""
    print("\n🧪 Testing contact form with missing fields...")
    
    # Test with missing name
    test_data = {
        "email": "test@example.com",
        "phone": "+33 6 12 34 56 78", 
        "message": "Test message"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/contact",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 422:  # Validation error expected
            print("✅ Missing fields validation test PASSED")
            return True
        else:
            print(f"❌ Missing fields validation test FAILED - Expected 422, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Missing fields test FAILED - Error: {str(e)}")
        return False

def test_contact_form_invalid_email():
    """Test contact form with invalid email format"""
    print("\n🧪 Testing contact form with invalid email...")
    
    test_data = {
        "name": "Test User",
        "email": "invalid-email-format",
        "phone": "+33 6 12 34 56 78",
        "message": "Test message with invalid email"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/contact",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 422:  # Validation error expected
            print("✅ Invalid email validation test PASSED")
            return True
        else:
            print(f"❌ Invalid email validation test FAILED - Expected 422, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Invalid email test FAILED - Error: {str(e)}")
        return False

def test_contact_form_empty_message():
    """Test contact form with message too short"""
    print("\n🧪 Testing contact form with too short message...")
    
    test_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "+33 6 12 34 56 78",
        "message": "Short"  # Less than 10 characters required
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/contact",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 422:  # Validation error expected
            print("✅ Short message validation test PASSED")
            return True
        else:
            print(f"❌ Short message validation test FAILED - Expected 422, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Short message test FAILED - Error: {str(e)}")
        return False

def test_api_connectivity():
    """Test basic API connectivity"""
    print("🧪 Testing API connectivity...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API connectivity test PASSED")
            return True
        else:
            print(f"❌ API connectivity test FAILED - Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API connectivity test FAILED - Error: {str(e)}")
        return False

def main():
    """Run all backend tests"""
    print("=" * 60)
    print("🚀 BACKEND API TESTING - CONTACT FORM WITH ZEPTOMAIL SMTP")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"API Base URL: {API_BASE_URL}")
    print("=" * 60)
    
    results = []
    
    # Test API connectivity first
    results.append(test_api_connectivity())
    
    # Test contact form functionality
    results.append(test_contact_form_valid_submission())
    results.append(test_contact_form_missing_fields())
    results.append(test_contact_form_invalid_email())
    results.append(test_contact_form_empty_message())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED - Check details above")
    
    return passed == total

if __name__ == "__main__":
    main()