from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class ContactFormRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=1)
    message: str = Field(..., min_length=10, max_length=5000)

class ContactFormResponse(BaseModel):
    success: bool
    message: str
    message_id: Optional[str] = None

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

@api_router.post("/contact", response_model=ContactFormResponse)
async def submit_contact_form(form_data: ContactFormRequest):
    """Send contact form email via SMTP (ZeptoMail)"""
    try:
        smtp_server = os.environ.get('SMTP_SERVER')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_username = os.environ.get('SMTP_USERNAME')
        smtp_password = os.environ.get('SMTP_PASSWORD')
        smtp_sender_email = os.environ.get('SMTP_SENDER_EMAIL')
        smtp_recipient_email = os.environ.get('SMTP_RECIPIENT_EMAIL')
        
        if not all([smtp_server, smtp_username, smtp_password, smtp_sender_email, smtp_recipient_email]):
            logging.error("SMTP configuration incomplete")
            return ContactFormResponse(
                success=False,
                message="Configuration d'email incomplète"
            )
        
        # Extraire le prénom (premier mot du nom)
        first_name = form_data.name.split()[0] if form_data.name else "Client"
        
        # Connexion SMTP (réutilisée pour les deux emails)
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            
            # 1. Email de notification à BK Tech (contact@bktech.dev)
            msg_notification = MIMEMultipart()
            msg_notification['From'] = f"BK Tech Contact <{smtp_sender_email}>"
            msg_notification['To'] = smtp_recipient_email
            msg_notification['Subject'] = f"Nouveau contact: {form_data.name}"
            
            notification_body = f"""Nouveau message de contact BK Tech

Nom: {form_data.name}
Email: {form_data.email}
Téléphone: {form_data.phone}

Message:
{form_data.message}

---
Ce message a été envoyé via le formulaire de contact de bktech.dev
"""
            
            msg_notification.attach(MIMEText(notification_body, 'plain'))
            server.send_message(msg_notification)
            logging.info(f"Notification email sent to {smtp_recipient_email}")
            
            # 2. Email de confirmation au client
            msg_confirmation = MIMEMultipart()
            msg_confirmation['From'] = f"BK Tech <{smtp_sender_email}>"
            msg_confirmation['To'] = form_data.email
            msg_confirmation['Subject'] = "Merci pour votre message - BK Tech"
            
            confirmation_body = f"""Bonjour {first_name},

Merci d'avoir complété notre formulaire d'information et bienvenue chez BK Tech !
Notre équipe vous contactera très bientôt pour découvrir ensemble comment nous pouvons donner vie à vos projets digitaux.

À très vite,
L'équipe BK Tech
💻 Création d'applications sur mesure, puissantes et innovantes
📧 contact@bktech.dev | 🌐 www.bktech.dev
"""
            
            msg_confirmation.attach(MIMEText(confirmation_body, 'plain'))
            server.send_message(msg_confirmation)
            logging.info(f"Confirmation email sent to {form_data.email}")
        
        # Save to database
        contact_record = {
            "name": form_data.name,
            "email": form_data.email,
            "phone": form_data.phone,
            "message": form_data.message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sent_via": "smtp",
            "confirmation_sent": True
        }
        await db.contacts.insert_one(contact_record)
        
        logging.info(f"Contact form processed successfully for {form_data.name}")
        
        return ContactFormResponse(
            success=True,
            message="Votre message a été envoyé avec succès !",
            message_id=None
        )
        
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error: {str(e)}")
        return ContactFormResponse(
            success=False,
            message="Erreur lors de l'envoi du message. Veuillez réessayer."
        )
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return ContactFormResponse(
            success=False,
            message="Une erreur inattendue s'est produite."
        )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()