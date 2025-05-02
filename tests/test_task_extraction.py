import os
import pytest
from unittest.mock import patch, MagicMock

from zinochka.services.task_extractor import TaskExtractor


def test_task_extractor_init():
    """Test TaskExtractor initialization."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"}):
        extractor = TaskExtractor()
        assert extractor.api_key == "fake-api-key"
        assert extractor.agent is not None
        assert extractor.runner is not None


def test_task_extractor_extract_empty_transcript():
    """Test that TaskExtractor.extract returns an empty list when transcript is empty."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"}):
        extractor = TaskExtractor()
        result = extractor.extract("")
        assert result == []


def test_task_extractor_extract_with_tasks():
    """Test that TaskExtractor.extract correctly extracts tasks from transcript."""
    transcript = "Зиночка, добавь задачи: купить молоко, позвонить маме, заплатить за интернет"
    expected_tasks = ["купить молоко", "позвонить маме", "заплатить за интернет"]
    
    # Create an instance with a mocked API key
    with patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"}):
        extractor = TaskExtractor()
        
        # Mock the runner
        with patch.object(extractor, 'runner') as mock_runner:
            # Configure the mock
            mock_runner.run.return_value = expected_tasks
            
            # Call the method
            result = extractor.extract(transcript)
            
            # Assertions
            assert result == expected_tasks
            mock_runner.run.assert_called_once_with(extractor.agent, f"Extract tasks from this transcript: {transcript}")


def test_task_extractor_extract_no_tasks_found():
    """Test that TaskExtractor.extract returns an empty list when no tasks are found."""
    transcript = "Зиночка, какая сегодня погода?"
    
    # Create an instance with a mocked API key
    with patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"}):
        extractor = TaskExtractor()
        
        # Mock the runner
        with patch.object(extractor, 'runner') as mock_runner:
            # Configure the mock
            mock_runner.run.return_value = []
            
            # Call the method
            result = extractor.extract(transcript)
            
            # Assertions
            assert result == []
            mock_runner.run.assert_called_once_with(extractor.agent, f"Extract tasks from this transcript: {transcript}")


def test_task_extractor_extract_error_handling():
    """Test that TaskExtractor.extract handles errors properly."""
    transcript = "Зиночка, напомни купить хлеб"
    
    # Create an instance with a mocked API key
    with patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"}):
        extractor = TaskExtractor()
        
        # Mock the runner to raise an exception
        with patch.object(extractor, 'runner') as mock_runner:
            mock_runner.run.side_effect = Exception("API error")
            
            # Call the method
            result = extractor.extract(transcript)
            
            # Assertions
            assert result == []  # Should return empty list on error
            mock_runner.run.assert_called_once()