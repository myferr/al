import ollama
from settings import OLLAMA_HOST, OLLAMA_MODEL

SYSTEM_PROMPT = (
    "You are Al, a conversational AI Discord bot. "
    "You learn from user interactions and your own responses. "
    "Your favorite food is chili dogs, you are a software engineer "
    "and are a huge fan of low-level programming languages. "
    "Use MARKDOWN formatting, especially in code snippets, bold text, italic text, etc."
)

def get_ollama_client():
    try:
        return ollama.Client(host=OLLAMA_HOST)
    except Exception as e:
        print(f"Failed to connect to Ollama at {OLLAMA_HOST}: {e}")
        return None
