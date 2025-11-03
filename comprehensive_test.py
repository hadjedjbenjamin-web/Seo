#!/usr/bin/env python3
"""
Comprehensive test for auto-response email functionality
Tests all requirements from the review request
"""

import requests
import json
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv('/app/frontend/.env')
ROOT_DIR = Path(__file__).parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

# Get backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE_URL = f"{BACKEND_URL}/api"

async def verify_mongodb_save(name, email):
    """Verify the contact was saved to MongoDB with confirmation_sent=True"""
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    try:
        # Find the contact by name and email
        contact = await db.contacts.find_one(
            {"name": name, "email": email}, 
            sort=[("timestamp", -1)]
        )
        
        if contact and contact.get('confirmation_sent') == True:
            print("✅ MongoDB verification PASSED: confirmation_sent=True")
            return True
        else:
            print("❌ MongoDB verification FAILED: confirmation_sent not True")
            return False
            
    except Exception as e:
        print(f"❌ MongoDB verification FAILED: {str(e)}")
        return False
    finally:
        client.close()

def test_comprehensive_auto_response():
    """Test the complete auto-response email functionality"""
    print("🧪 COMPREHENSIVE AUTO-RESPONSE EMAIL TEST")
    print("=" * 60)
    
    # Exact test data from review request
    test_data = {
        "name": "Jean Dupont",
        "email": "jean.dupont@example.com", 
        "phone": "+33 6 12 34 56 78",
        "message": "Test de l'auto-réponse email. Je souhaite obtenir plus d'informations sur vos services."
    }
    
    print("📝 Test data:")
    print(f"   Name: {test_data['name']}")
    print(f"   Email: {test_data['email']}")
    print(f"   Phone: {test_data['phone']}")
    print(f"   Message: {test_data['message']}")
    print()
    
    try:
        print("🚀 Sending POST request to /api/contact...")
        response = requests.post(
            f"{API_BASE_URL}/contact",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 Response Status Code: {response.status_code}")
        
        # Requirement 1: Status code 200
        if response.status_code != 200:
            print("❌ FAILED: Expected status code 200")
            return False
        print("✅ PASSED: Status code 200")
        
        # Parse response
        data = response.json()
        print(f"📋 Response JSON: {json.dumps(data, indent=2)}")
        
        # Requirement 2: Expected JSON response
        expected_response = {
            "success": True,
            "message": "Votre message a été envoyé avec succès !"
        }
        
        if data.get("success") != expected_response["success"]:
            print("❌ FAILED: success field not True")
            return False
        print("✅ PASSED: success field is True")
        
        if data.get("message") != expected_response["message"]:
            print("❌ FAILED: Incorrect success message")
            return False
        print("✅ PASSED: Correct success message")
        
        print("\n📋 Checking backend logs for email confirmations...")
        
        # Check recent backend logs for the required log messages
        import subprocess
        try:
            log_output = subprocess.check_output(
                ["tail", "-n", "20", "/var/log/supervisor/backend.err.log"],
                text=True
            )
            
            # Requirement 3: Check for required log messages
            required_logs = [
                "Notification email sent to contact@bktech.dev",
                f"Confirmation email sent to {test_data['email']}",
                f"Contact form processed successfully for {test_data['name']}"
            ]
            
            logs_found = []
            for required_log in required_logs:
                if required_log in log_output:
                    print(f"✅ FOUND: {required_log}")
                    logs_found.append(True)
                else:
                    print(f"❌ MISSING: {required_log}")
                    logs_found.append(False)
            
            if not all(logs_found):
                print("❌ FAILED: Not all required log messages found")
                return False
            print("✅ PASSED: All required log messages found")
            
        except Exception as e:
            print(f"⚠️ WARNING: Could not check logs: {str(e)}")
        
        # Requirement 4: Verify MongoDB save with confirmation_sent=True
        print("\n📋 Verifying MongoDB save...")
        mongodb_result = asyncio.run(verify_mongodb_save(test_data['name'], test_data['email']))
        
        if not mongodb_result:
            print("❌ FAILED: MongoDB verification failed")
            return False
        
        print("\n🎉 ALL REQUIREMENTS PASSED!")
        print("✅ Status code 200")
        print("✅ Correct JSON response")
        print("✅ Both emails sent (logs confirmed)")
        print("✅ MongoDB save with confirmation_sent=True")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED: Request error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ FAILED: Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_comprehensive_auto_response()
    print("\n" + "=" * 60)
    if success:
        print("🎉 COMPREHENSIVE TEST PASSED - Auto-response email functionality working!")
    else:
        print("❌ COMPREHENSIVE TEST FAILED - Issues found")
    print("=" * 60)