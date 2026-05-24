import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-turbo")
    PORT = int(os.getenv("PORT", 8001))
    MODULE_NAME = "PAMAS-Module3-VerificationEngine"
