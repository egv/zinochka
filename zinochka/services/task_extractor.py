import os
import logging
from typing import List
from agents import Agent, Runner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskExtractor:
    """
    Extracts tasks from transcripts using OpenAI agents.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the task extractor.
        
        Args:
            api_key: Optional OpenAI API key. If not provided, will use environment variable.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        
        if not self.api_key:
            logger.warning("No OpenAI API key provided. Set OPENAI_API_KEY environment variable.")
            
        # Create the agent with List[str] output
        self.agent = Agent(
            name="Task Extractor",
            instructions="""
            You are a specialized task extraction agent.
            Extract any tasks from the transcript text provided by the user.
            Tasks are activities, to-dos, or reminders that the user wants to keep track of.
            Return all identified tasks as a list of strings.
            If no tasks are found, return an empty list.
            Only extract clear, actionable tasks.
            """,
            output_type=List[str],
        )
        
        # Initialize the runner
        self.runner = Runner()  # Runner doesn't take api_key in constructor
    
    def extract(self, transcript: str) -> List[str]:
        """
        Extract tasks from the transcript using an OpenAI agent.
        
        Args:
            transcript: The text transcript to extract tasks from
            
        Returns:
            A list of extracted tasks, or an empty list if no tasks found
        """
        if not transcript:
            return []
        
        if not self.api_key:
            logger.error("No OpenAI API key available. Cannot extract tasks.")
            return []
        
        logger.info("Extracting tasks from transcript")
        
        try:
            # Run the agent on the transcript
            result = self.runner.run(
                self.agent,
                f"Extract tasks from this transcript: {transcript}"
            )
            
            # Return the extracted tasks
            return result
            
        except Exception as e:
            logger.error(f"Error extracting tasks: {e}")
            return []