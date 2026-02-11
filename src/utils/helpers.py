from typing import List, Optional, Tuple, Tuple
from PIL import Image
import google.generativeai as genai
import time
from src.config.settings import GEMINI_API_KEY, CHATBOT_NAME, MODEL_ID, MODEL_OPTIONS, IMAGE_WIDTH, IMAGE_HEIGHT, SYSTEM_INSTRUCTION_ANALYSIS

def initialize_model(api_key: Optional[str] = None):
    """Initialize the Gemini generative model."""
    if api_key:
        genai.configure(api_key=api_key)
    elif GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    
    model = genai.GenerativeModel(CHATBOT_NAME, system_instruction=SYSTEM_INSTRUCTION_ANALYSIS)
    return model


def preprocess_stop_sequences(stop_sequences: str) -> Optional[List[str]]:
    return [seq.strip() for seq in stop_sequences.split(",")] if stop_sequences else None

def preprocess_image(image: Image.Image) -> Image.Image:
    image_height = int(image.height * IMAGE_WIDTH / image.width)
    return image.resize((IMAGE_WIDTH, image_height))


def user(text_prompt: str, chatbot: List[Tuple[str, str]]):
    return "", chatbot + [[text_prompt, None]]


def bot(
    gemini_key: str,
    image_prompt: Optional[Image.Image],
    temperature: float,
    max_output_tokens: int,
    stop_sequences: str,
    top_k: int,
    top_p: float,
    chatbot: List[Tuple[str, str]]
):
    gemini_key = gemini_key or GEMINI_API_KEY
    if not gemini_key:
        raise ValueError("GEMINI_API_KEY is not set. Please set it up.")

    text_prompt = chatbot[-1][0].strip() if chatbot[-1][0] else None

    # Handle cases for text and/or image input
    if not text_prompt and not image_prompt:
        chatbot[-1][1] = "Prompt cannot be empty. Please provide input text or an image."
        yield chatbot
        return
    elif image_prompt and not text_prompt:
        # If only an image is provided
        text_prompt = "Describe the image"
    elif image_prompt and text_prompt:
        # If both text and image are provided, combine them
        text_prompt = f"{text_prompt}. Also, analyze the provided image."

    # Configure the model
    genai.configure(api_key=gemini_key)
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        stop_sequences=preprocess_stop_sequences(stop_sequences),
        top_k=top_k,
        top_p=top_p,
    )

    # Prepare inputs
    inputs = [text_prompt] if image_prompt is None else [text_prompt, preprocess_image(image_prompt)]

    # Generate response
    try:
        response = model.generate_content(inputs, stream=True, generation_config=generation_config)
        response.resolve()
    except Exception as e:
        chatbot[-1][1] = f"Error occurred: {str(e)}"
        yield chatbot
        return

    # Stream the response back to the chatbot
    chatbot[-1][1] = ""
    for chunk in response:
        for i in range(0, len(chunk.text), 10):
            chatbot[-1][1] += chunk.text[i:i + 10]
            time.sleep(0.01)
            yield chatbot