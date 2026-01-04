import json
import os
from google.adk.agents.llm_agent import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.models import Gemini
from google.genai import types
# from google.genai import types # Unused if we strip it from the f-string, but user might want it. leaving commented or removing.
from app.models.resume_data import ResumeData
import logging
logger = logging.getLogger(__name__)
import dotenv
dotenv.load_dotenv()    

class LLMExtractionService:
    def __init__(self):
        # Ensure GOOGLE_API_KEY is set in environment
        if not os.getenv("GOOGLE_API_KEY"):
            # You might want to log a warning or handle this gracefully
            logger.error("GOOGLE_API_KEY is not set in environment variables.")
            raise ValueError("GOOGLE_API_KEY is not set in environment variables.")
            
        # Initialize the Gemini model
        # Note: Adjust model_name as needed (e.g., "gemini-1.5-pro")
        self.model = Gemini(model="gemini-2.5-flash-lite")
        self.agent = Agent(
            name="resume_extractor",
            model=self.model,
            description="You are an expert resume parser. Extract the following information from the resume text accurately.",
            instruction=f"Return only the JSON object in the following format: {json.dumps(ResumeData.model_json_schema())}",
            output_schema=ResumeData,
            output_key="resume_data"
        )
        self.app_name = "Resume Extractor"
        self.session_id = "resume_extractor_session"
        self.user_id = "resume_extractor_user"

        # Create a session service
        self.session_service = InMemorySessionService()
        self.session = None
        self.runner = Runner(agent=self.agent, app_name=self.app_name, session_service=self.session_service)

    async def _ensure_session(self):
        """Ensure session exists and is created asynchronously"""
        try:
             self.session = await self.session_service.create_session(app_name=self.app_name, session_id=self.session_id, user_id=self.user_id)
        except Exception as e:
            # If it already exists?
            try:
                 self.session = await self.session_service.get_session(self.app_name, self.session_id, self.user_id)
            except:
                 # Re-raise original error if create failed and get failed
                 raise e


    async def extract_resume_data(self, text: str) -> ResumeData:
        """
        Extracts structured ResumeData from raw resume text using Google ADK.
        """
        if not self.session:
            await self._ensure_session()

        try:
            # Run the agent on the input text
            # The agent should return an instance of ResumeData directly
            content = types.Content(role="user", parts=[types.Part(text=text)])
            async for event in self.runner.run_async(user_id=self.user_id, session_id=self.session_id, new_message=content):
                if event.is_final_response():
                    print("Response Complete")
            
            updated_session = await self.session_service.get_session(session_id=self.session_id, user_id=self.user_id, app_name=self.app_name)

            return updated_session.state["resume_data"]
        except Exception as e:
            print(f"Error extracting resume data: {e}")
            raise e
