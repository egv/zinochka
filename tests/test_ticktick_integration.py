import pytest
from unittest.mock import patch, MagicMock

from zinochka.services.tasks import process_with_orchestration_agent


def test_process_with_orchestration_agent_empty_transcript():
    """Test that process_with_orchestration_agent returns an empty list when transcript is empty."""
    result = process_with_orchestration_agent("")
    assert result == []


def test_process_with_orchestration_agent_success():
    """Test successful processing with orchestration agent."""
    transcript = "zinochka please add tasks: buy milk, call mom, pay bills"
    expected_task_ids = ["t1", "t2", "t3"]
    
    # Mock the OrchestrationAgent
    with patch("zinochka.services.orchestration.OrchestrationAgent") as MockAgent:
        # Configure the mock
        mock_instance = MagicMock()
        MockAgent.return_value = mock_instance
        mock_instance.process_transcript.return_value = {
            "success": True,
            "created_tasks": expected_task_ids
        }
        
        # Call the function
        result = process_with_orchestration_agent(transcript)
        
        # Assertions
        assert result == expected_task_ids
        MockAgent.assert_called_once()
        mock_instance.process_transcript.assert_called_once_with(transcript)


def test_process_with_orchestration_agent_failure():
    """Test handling of failures in the orchestration agent."""
    transcript = "zinochka please add tasks: buy milk, call mom"
    
    # Mock the OrchestrationAgent
    with patch("zinochka.services.orchestration.OrchestrationAgent") as MockAgent:
        # Configure the mock to return failure
        mock_instance = MagicMock()
        MockAgent.return_value = mock_instance
        mock_instance.process_transcript.return_value = {
            "success": False,
            "error": "Failed to process transcript"
        }
        
        # Call the function
        result = process_with_orchestration_agent(transcript)
        
        # Assertions
        assert result == []  # Should return empty list on error
        MockAgent.assert_called_once()
        mock_instance.process_transcript.assert_called_once_with(transcript)


def test_process_with_orchestration_agent_exception():
    """Test handling of exceptions in the orchestration agent."""
    transcript = "zinochka please add tasks: buy milk"
    
    # Mock the OrchestrationAgent to raise an exception
    with patch("zinochka.services.orchestration.OrchestrationAgent") as MockAgent:
        MockAgent.side_effect = Exception("Failed to create agent")
        
        # Call the function
        result = process_with_orchestration_agent(transcript)
        
        # Assertions
        assert result == []  # Should return empty list on exception
        MockAgent.assert_called_once()