#!/usr/bin/env python3
"""
Debug Mailgun API integration to understand the 403 error
"""

import requests
import os
from dotenv import load_dotenv

# Load backend environment variables
load_dotenv('/app/backend/.env')

def test_mailgun_direct():
    """Test Mailgun API directly to understand the error"""
    print("🔍 Testing Mailgun API directly...")
    
    mailgun_api_key = os.environ.get('MAILGUN_API_KEY')
    mailgun_domain = os.environ.get('MAILGUN_DOMAIN')
    mailgun_sender = os.environ.get('MAILGUN_SENDER_EMAIL')
    mailgun_recipient = os.environ.get('MAILGUN_RECIPIENT_EMAIL')
    
    print(f"API Key: {mailgun_api_key[:10]}..." if mailgun_api_key else "None")
    print(f"Domain: {mailgun_domain}")
    print(f"Sender: {mailgun_sender}")
    print(f"Recipient: {mailgun_recipient}")
    
    if not all([mailgun_api_key, mailgun_domain, mailgun_sender, mailgun_recipient]):
        print("❌ Missing Mailgun configuration")
        return False
    
    # Test email data
    email_data = {
        "from": f"BK Tech Contact Form <{mailgun_sender}>",
        "to": mailgun_recipient,
        "subject": "Test Email - Mailgun Integration",
        "text": "This is a test email to verify Mailgun integration."
    }
    
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
            auth=("api", mailgun_api_key),
            data=email_data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Mailgun API test PASSED")
            return True
        else:
            print(f"❌ Mailgun API test FAILED - Status: {response.status_code}")
            
            # Try to get more details about the error
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print("Could not parse error response as JSON")
            
            return False
            
    except Exception as e:
        print(f"❌ Mailgun API test FAILED - Error: {str(e)}")
        return False

def test_mailgun_domain_info():
    """Get domain information from Mailgun"""
    print("\n🔍 Getting Mailgun domain information...")
    
    mailgun_api_key = os.environ.get('MAILGUN_API_KEY')
    mailgun_domain = os.environ.get('MAILGUN_DOMAIN')
    
    try:
        response = requests.get(
            f"https://api.mailgun.net/v3/domains/{mailgun_domain}",
            auth=("api", mailgun_api_key),
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            domain_info = response.json()
            print("✅ Domain info retrieved successfully")
            print(f"Domain state: {domain_info.get('domain', {}).get('state')}")
            return True
        else:
            print(f"❌ Could not get domain info - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Domain info test FAILED - Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 MAILGUN DEBUG TESTING")
    print("=" * 60)
    
    test_mailgun_domain_info()
    test_mailgun_direct()