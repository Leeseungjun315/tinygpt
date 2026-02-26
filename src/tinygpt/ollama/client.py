from ollama import chat

def stream_chat(model: str, messages: list[dict]):
    return chat(model=model, messages=messages, stream=True)

def one_shot(model: str, messages: list[dict]) -> str:
    resp = chat(model=model, messages=messages, stream=False)
    return resp["message"]["content"]