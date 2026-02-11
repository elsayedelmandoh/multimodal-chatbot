from src.config.settings import MODEL_ID, MODEL_OPTIONS
from src.utils.helpers import bot, user
import gradio as gr

def gradio_interface() -> gr.Blocks:
    # Components
    image_prompt_component = gr.Image(
        type="pil",
        label="Input Image (Optional: Figure/Graph)"
    )
    chatbot_component = gr.Chatbot(
        label="Chatbot",
    )
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
    model_name_component = gr.Dropdown(
            choices=MODEL_OPTIONS,
            value=MODEL_ID,
            label="Model Selection",
            info="Choose the Gemini model to use for generation."
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
        "What are the differences between multi-agent LLMs and multi-agent systems",
        "Why is it difficult to integrate multimodality in a prompt",
    ]
    example_images = [["research/ex1.png"], ["research/ex2.png"]]

    # Gradio Interface
    user_inputs = [text_prompt_component, chatbot_component]
    bot_inputs = [
        model_name_component, 
        image_prompt_component,
        temperature_component,
        max_output_tokens_component,
        stop_sequences_component,
        top_k_component,
        top_p_component,
        chatbot_component,
    ]

    with gr.Blocks() as app:
        gr.Markdown("<h1 style='font-size: 36px; font-weight: bold; font-family: Arial;'>Gemini Multimodal Chatbot</h1>")
        with gr.Row():
            chatbot_component.render()
        with gr.Row():
            with gr.Column(scale=1):
                text_prompt_component.render()
            with gr.Column(scale=1):
                image_prompt_component.render()
            with gr.Column(scale=1):
                run_button_component.render()

        with gr.Accordion("🧪Example Text 💬", open=False):
            example_radio = gr.Radio(
                choices=example_scenarios,
                label="Example Queries",
                info="Select an example query."
            )
            # Debug callback
            example_radio.change(
                fn=lambda query: query if query else "No query selected.",
                inputs=[example_radio],
                outputs=[text_prompt_component]
            )
            # Custom examples section with blue styling

        with gr.Accordion("🧪Example Image 🩻", open=False):
            gr.Examples(
                examples=example_images,
                inputs=[image_prompt_component],
                label="Example Figures",
            )
        with gr.Accordion("🛠️Customize", open=False):
            model_name_component.render()
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

    return app

if __name__ == "__main__":
    gradio_interface().launch(share=True, theme="earneleh/paris")