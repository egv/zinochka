import os
import logging
from typing import List, Dict, Any
from agents import Agent, Runner

from zinochka.services.task_extractor import TaskExtractor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrchestrationAgent:
    """
    Orchestration agent that coordinates task extraction and creation in TickTick.
    
    This agent assumes the transcript has already been verified to contain
    an activation phrase ("зиночка" or "zinochka").
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the orchestration agent.
        
        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("No OpenAI API key provided. Set OPENAI_API_KEY environment variable.")
        
        # Create the task extraction agent
        self.task_extractor = TaskExtractor(api_key=self.api_key)
        
        # Convert the task extractor's agent to a tool
        task_extraction_tool = self.task_extractor.agent.as_tool(
            tool_name="extract_tasks",
            tool_description="Extract tasks from a transcript text. Returns a list of task descriptions."
        )
        
        # Create the orchestration agent with stdio MCP for TickTick
        # Import needed for the stdio MCP
        from agents import StdioMCPServer

        # This will be configured later with the ticktick-mcp server
        ticktick_mcp = StdioMCPServer(["ticktick-mcp"])
        
        self.agent = Agent(
            name="Task Orchestrator",
            instructions="""
            You are a task orchestration agent that processes voice transcripts.
            
            Your job is to:
            1. Use the extract_tasks tool to extract tasks from the transcript
            2. Create each extracted task in TickTick using the ticktick_tools.create_task
            3. Return a list of the created task IDs
            
            Note: The transcript has already been verified to contain an activation phrase.
            Your goal is to extract tasks and create them in TickTick efficiently.
            """,
            tools=[task_extraction_tool],
            mcp_servers=[ticktick_mcp]
        )
        
        # Initialize the runner
        self.runner = Runner()  # Runner doesn't take api_key in constructor
    
    def process_transcript(self, transcript: str) -> Dict[str, Any]:
        """
        Process a transcript to extract and create tasks.
        
        Args:
            transcript: The transcript text to process (already verified to contain activation phrase)
            
        Returns:
            Dictionary with processing results
        """
        if not transcript:
            return {"success": False, "error": "Empty transcript"}
        
        if not self.api_key:
            return {"success": False, "error": "No OpenAI API key available"}
        
        try:
            # Run the orchestration agent
            prompt = f"""
            Process this transcript: "{transcript}"
            
            Extract tasks and create them in TickTick using the available tools.
            Return a list of created task IDs.
            """
            
            result = self.runner.run(self.agent, prompt)
            
            # Log the result
            logger.info(f"Orchestration agent result: {result}")
            
            # Return the result
            return {
                "success": True,
                "created_tasks": result if isinstance(result, list) else []
            }
            
        except Exception as e:
            logger.error(f"Error in orchestration agent: {e}")
            return {"success": False, "error": str(e)}