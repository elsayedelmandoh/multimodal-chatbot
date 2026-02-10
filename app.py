from src.config.settings import GEMINI_API_KEY, CHATBOT_NAME

import os
import time
from typing import List, Tuple, Optional
import google.generativeai as genai
import gradio as gr
from PIL import Image
import tempfile
import os

IMAGE_WIDTH = 512
IMAGE_WIDTH = 512

system_instruction_analysis = "You are an expert of the given topic. Analyze the provided text with a focus on the topic, identifying recent issues, recent insights, or improvements relevant to academic standards and effectiveness. Offer actionable advice for enhancing knowledge and suggest real-life examples."
model = genai.GenerativeModel(CHATBOT_NAME, system_instruction=system_instruction_analysis)
#genai.configure(api_key=gemini_key)

# Components
gemini_key_component = gr.Textbox(
    label="Gemini API Key",
    type="password",
    placeholder="Enter your Gemini API Key",
    visible=GEMINI_API_KEY is None
)

image_prompt_component = gr.Image(type="pil", label="Input Image (Optional: Figure/Graph)")
chatbot_component = gr.Chatbot(label="Chatbot", bubble_full_width=False)
text_prompt_component = gr.Textbox(
    placeholder="Type your question here...",
    label="Ask",
    lines=3
)
run_button_component = gr.Button("Submit")
temperature_component = gr.Slider(
    minimum=0,
    maximum=1.0,
    value=0.4,
    step=0.05,
    label="Creativity (Temperature)",
    info="Controls the randomness of the response. Higher values result in more creative answers."
)
max_output_tokens_component = gr.Slider(
    minimum=1,
    maximum=2048,
    value=1024,
    step=1,
    label="Response Length (Token Limit)",
    info="Sets the maximum number of tokens in the output response."
)
stop_sequences_component = gr.Textbox(
    label="Stop Sequences (Optional)",
    placeholder="Enter stop sequences, e.g., STOP, END",
    info="Specify sequences to stop the generation."
)
top_k_component = gr.Slider(
    minimum=1,
    maximum=40,
    value=32,
    step=1,
    label="Top-K Sampling",
    info="Limits token selection to the top K most probable tokens. Lower values produce conservative outputs."
)
top_p_component = gr.Slider(
    minimum=0,
    maximum=1,
    value=1,
    step=0.01,
    label="Top-P Sampling",
    info="Limits token selection to tokens with a cumulative probability up to P. Lower values produce conservative outputs."
)
example_scenarios = [
    "Describe Multimodal AI",
    "What are the difference between muliagent llm and multiagent system",
"Why it's difficult to intgrate multimodality in prompt"]
example_images = [["ex1.png"],["ex2.png"]]


# Gradio Interface
user_inputs = [text_prompt_component, chatbot_component]
bot_inputs = [
    gemini_key_component,
    image_prompt_component,
    temperature_component,
    max_output_tokens_component,
    stop_sequences_component,
    top_k_component,
    top_p_component,
    chatbot_component,
]


with gr.Blocks(theme="earneleh/paris") as demo:
    gr.Markdown("<h1 style='font-size: 36px; font-weight: bold; font-family: Arial;'>Gemini 2.0 Multimodal Chatbot</h1>")
    with gr.Row():
        gemini_key_component.render()
    with gr.Row():
        chatbot_component.render()
    with gr.Row():
        with gr.Column(scale=0.5):
           text_prompt_component.render()
        with gr.Column(scale=0.5):
           image_prompt_component.render()
        with gr.Column(scale=0.5):
            run_button_component.render()
    with gr.Accordion("🧪Example Text 💬", open=False):
        example_radio = gr.Radio(
        choices=example_scenarios,
        label="Example Queries",
        info="Select an example query.")
        # Debug callback
        example_radio.change(
        fn=lambda query: query if query else "No query selected.",
        inputs=[example_radio],
        outputs=[text_prompt_component])
       # Custom examples section with blue styling
    with gr.Accordion("🧪Example Image 🩻", open=False):
        gr.Examples(
        examples=example_images,
        inputs=[image_prompt_component],
        label="Example Figures",
        )     
    with gr.Accordion("🛠️Customize", open=False):
        temperature_component.render()
        max_output_tokens_component.render()
        stop_sequences_component.render()
        top_k_component.render()
        top_p_component.render()

    run_button_component.click(
        fn=user, inputs=user_inputs, outputs=[text_prompt_component, chatbot_component]
    ).then(
        fn=bot, inputs=bot_inputs, outputs=[chatbot_component]
    )
demo.launch()