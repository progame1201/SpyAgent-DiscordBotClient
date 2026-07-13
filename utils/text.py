def flatten_newlines(text) -> str:
    return str(text).replace("\n", "    ")

def cut_text(text, max_length=40) -> str:
    return text if len(text) < max_length else f"{text[:max_length]}..."
