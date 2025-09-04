from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime


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
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Flight Readiness Check Models
class FlightReadinessRequest(BaseModel):
    bookingReference: str
    lastName: str

class FlightReadinessResponse(BaseModel):
    status: str
    message: str
    flightNumber: str
    departure: str
    gate: str

@api_router.post("/flight-readiness", response_model=FlightReadinessResponse)
async def check_flight_readiness(request: FlightReadinessRequest):
    # Mock flight readiness data for demo
    booking_ref = request.bookingReference.upper()
    last_name = request.lastName.upper()
    
    # Simulate different flight statuses based on booking reference
    if booking_ref.startswith('CA'):
        if booking_ref.endswith('1'):
            return FlightReadinessResponse(
                status="ready",
                message="Your flight is on time and ready for boarding",
                flightNumber="CA001",
                departure="2025-01-20 14:30",
                gate="A12"
            )
        elif booking_ref.endswith('2'):
            return FlightReadinessResponse(
                status="delayed",
                message="Your flight is delayed by 45 minutes",
                flightNumber="CA002",
                departure="2025-01-20 16:15",
                gate="B8"
            )
        elif booking_ref.endswith('3'):
            return FlightReadinessResponse(
                status="cancelled",
                message="Your flight has been cancelled. Please contact customer service",
                flightNumber="CA003",
                departure="N/A",
                gate="N/A"
            )
        else:
            return FlightReadinessResponse(
                status="ready",
                message="Your flight is confirmed and on time",
                flightNumber="CA123",
                departure="2025-01-20 18:45",
                gate="C5"
            )
    else:
        return FlightReadinessResponse(
            status="unknown",
            message="Booking reference not found. Please check your details",
            flightNumber="N/A",
            departure="N/A",
            gate="N/A"
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
