from pydantic import BaseModel, Field


class WebhookPayload(BaseModel):
    """
    Model for the webhook payload from Zapier/Plaud.
    """
    transcript: str = Field(..., description="The transcript text from the voice note")


class WebhookResponse(BaseModel):
    """
    Standard response model for the webhook endpoint.
    """
    status: str = "success"