import logging
from typing import Any, List, Optional, cast

from celery import chain

from zinochka.services.activation import contains_activation_phrase
from zinochka.services.celery_app import celery_app


@celery_app.task
def process_transcript(transcript: str) -> Optional[str]:
    """
    Process the transcript to check for the activation phrase.
    
    Args:
        transcript: The text transcript to process
        
    Returns:
        The transcript if it contains an activation phrase, None otherwise
    """
    if contains_activation_phrase(transcript):
        return transcript
    return None


@celery_app.task
async def process_with_orchestration_agent(transcript: str) -> List[str]:
    """
    Process the transcript with the orchestration agent.
    
    The orchestration agent will:
    1. Extract tasks from the transcript using the task extraction agent
    2. Create these tasks in TickTick using the MCP server
    
    Args:
        transcript: The text transcript to process
        
    Returns:
        List of created task IDs
    """
    if not transcript:
        return []
    
    from zinochka.services.orchestration import OrchestrationAgent
    
    # Create and use the orchestration agent
    try:
        orchestration_agent = OrchestrationAgent()
        result = await orchestration_agent.process_transcript(transcript)
        
        if result.get("success", False):
            return cast(List[str], result.get("created_tasks", []))
        return []
    except Exception as e:
        celery_logger = logging.getLogger(__name__)
        celery_logger.error(f"Error in orchestration agent: {e}")
        return []


@celery_app.task
def process_webhook_data(transcript: str) -> None:
    """
    Main task to process webhook data through the entire pipeline.
    
    Args:
        transcript: The text transcript from the webhook
    """
    # Create a task chain to process the transcript
    # 1. Check if there's an activation phrase
    # 2. If so, process with orchestration agent
    chain(
        process_transcript.s(transcript),
        process_with_orchestration_agent.s()
    ).apply_async()
    
    # Note: In a real-world scenario, you might want to handle failures
    # or add monitoring/logging here