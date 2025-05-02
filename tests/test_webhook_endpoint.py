from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch

from zinochka.api.main import app


client = TestClient(app)


def test_webhook_endpoint_success():
    """Test that the webhook endpoint accepts valid payloads and queues them for processing."""
    payload = {
        "transcript": "Hey zinochka, add a task to buy milk"
    }
    
    # Mock the Celery task to avoid actual processing
    with patch("zinochka.services.tasks.process_webhook_data.delay") as mock_task:
        response = client.post("/webhook", json=payload)
        
        # Check the response
        assert response.status_code == 200
        assert response.json() == {"status": "success"}
        
        # Verify the task was queued with the correct transcript
        mock_task.assert_called_once_with(payload["transcript"])


def test_webhook_endpoint_invalid_payload():
    """Test that the webhook endpoint rejects invalid payloads."""
    # Missing required transcript field
    payload = {}
    
    response = client.post("/webhook", json=payload)
    
    # Should return a validation error
    assert response.status_code == 422


def test_health_check():
    """Test that the health check endpoint returns OK status."""
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}