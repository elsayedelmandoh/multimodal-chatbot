from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHATBOT_NAME = os.getenv("CHATBOT_NAME", "gemini-3-flash-preview")
