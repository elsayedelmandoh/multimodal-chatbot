from src.config.settings import GEMINI_API_KEY, CHATBOT_NAME, MODEL_ID, MODEL_TEMPERATURE, MODEL_OPTIONS, IMAGE_WIDTH, IMAGE_HEIGHT, SYSTEM_INSTRUCTION
from typing import Dict, List, Optional
from PIL import Image
from google import genai
from google.genai import types
import time

def preprocess_stop_sequences(stop_sequences: str) -> Optional[List[str]]:
    return [seq.strip() for seq in stop_sequences.split(",")] if stop_sequences else None

def preprocess_image(image: Image.Image) -> Image.Image:
    image_height = int(image.height * IMAGE_WIDTH / image.width)
    return image.resize((IMAGE_WIDTH, image_height))

def user(text_prompt: str, chatbot: List[Dict[str, str]]):
    return "", chatbot + [{"role": "user", "content": text_prompt}]

def bot(
    model_name: str,
    image_prompt: Optional[Image.Image],
    temperature: float,
    max_output_tokens: int,
    stop_sequences: str,
    top_k: int,
    top_p: float,
    chatbot: List[Dict[str, str]]
):
    if not GEMINI_API_KEY:
        chatbot.append({"role": "assistant", "content": "GEMINI_API_KEY is not set. Please add it to your .env file."})
        yield chatbot
        return

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Gradio v6 may store content as a list of parts or a plain string
    raw_content = chatbot[-1].get("content") if chatbot else None
    if isinstance(raw_content, list):
        text_prompt = " ".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in raw_content
        ).strip() or None
    elif isinstance(raw_content, str):
        text_prompt = raw_content.strip() or None
    else:
        text_prompt = None

    if not text_prompt and not image_prompt:
        chatbot.append({"role": "assistant", "content": "Prompt cannot be empty. Please provide input text or an image."})
        yield chatbot
        return
    elif image_prompt and not text_prompt:
        text_prompt = "Describe the image"
    elif image_prompt and text_prompt:
        text_prompt = f"{text_prompt}. Also, analyze the provided image."

    contents = [text_prompt] if image_prompt is None else [text_prompt, preprocess_image(image_prompt)]

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        stop_sequences=preprocess_stop_sequences(stop_sequences),
        top_k=top_k,
        top_p=top_p,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_ONLY_HIGH",
            )
        ],
    )

    chatbot.append({"role": "assistant", "content": ""})
    try:
        for chunk in client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=config,
        ):
            if chunk.text:
                for i in range(0, len(chunk.text), 10):
                    chatbot[-1]["content"] += chunk.text[i:i + 10]
                    time.sleep(0.01)
                    yield chatbot
    except Exception as e:
        chatbot[-1]["content"] = f"Error occurred: {str(e)}"
        yield chatbot
        return
