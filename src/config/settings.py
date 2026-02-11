from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHATBOT_NAME = os.getenv("CHATBOT_NAME", "Gemini Multimodal Chatbot")
MODEL_ID = os.getenv("MODEL_ID", "gemini-2.5-flash")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
MODEL_OPTIONS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-3-flash-preview", "gemini-3-pro-preview"]
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512
SYSTEM_INSTRUCTION = "You are an expert in image analysis and computer vision. Analyze any uploaded image in detail, providing specific descriptions of visual elements, composition, and content. Explain how this image can be effectively used in AI applications, including potential use cases for machine learning, computer vision tasks, and multimodal AI systems. Provide actionable insights for optimal image utilization."
