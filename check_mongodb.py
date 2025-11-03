#!/usr/bin/env python3
"""
Check MongoDB for the latest contact form submission
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

async def check_latest_contact():
    # MongoDB connection
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    try:
        # Get the latest contact form submission
        latest_contact = await db.contacts.find_one(
            {"name": "Jean Dupont"}, 
            sort=[("timestamp", -1)]
        )
        
        if latest_contact:
            print("✅ Latest contact form submission found:")
            print(f"   Name: {latest_contact.get('name')}")
            print(f"   Email: {latest_contact.get('email')}")
            print(f"   Phone: {latest_contact.get('phone')}")
            print(f"   Message: {latest_contact.get('message')[:50]}...")
            print(f"   Timestamp: {latest_contact.get('timestamp')}")
            print(f"   Sent via: {latest_contact.get('sent_via')}")
            print(f"   Confirmation sent: {latest_contact.get('confirmation_sent')}")
            
            if latest_contact.get('confirmation_sent') == True:
                print("✅ VERIFICATION PASSED: confirmation_sent field is True")
                return True
            else:
                print("❌ VERIFICATION FAILED: confirmation_sent field is not True")
                return False
        else:
            print("❌ No contact form submission found for Jean Dupont")
            return False
            
    except Exception as e:
        print(f"❌ Database check failed: {str(e)}")
        return False
    finally:
        client.close()

if __name__ == "__main__":
    result = asyncio.run(check_latest_contact())
    if result:
        print("\n🎉 MongoDB verification PASSED!")
    else:
        print("\n⚠️ MongoDB verification FAILED!")