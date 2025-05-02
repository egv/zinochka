from fastapi import FastAPI, HTTPException
import logging

from zinochka.api.models import WebhookPayload, WebhookResponse
from zinochka.services.tasks import process_webhook_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI(title="Zinochka", description="Personal AI assistant webhook API")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/webhook", response_model=WebhookResponse)
async def webhook(payload: WebhookPayload):
    """
    Webhook endpoint for receiving transcripts from Zapier/Plaud.
    
    This endpoint:
    1. Receives the transcript from the webhook
    2. Adds it to the Celery task queue for processing
    3. Returns a simple acknowledgment response
    
    Args:
        payload: The webhook payload containing the transcript
        
    Returns:
        A simple success response
    """
    try:
        # Log receipt of the webhook
        logger.info("Received webhook with transcript")
        
        # Submit the transcript for processing via Celery
        process_webhook_data.delay(payload.transcript)
        
        # Return a simple acknowledgment without disclosing internal details
        return WebhookResponse()
    
    except Exception as e:
        # Log the error
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")