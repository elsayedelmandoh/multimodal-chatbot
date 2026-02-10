def user(text_prompt: str, chatbot: List[Tuple[str, str]]):
    return "", chatbot + [[text_prompt, None]]
