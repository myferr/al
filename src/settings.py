import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')
OLLAMA_MODEL = 'llama3'
UNCENSORED_MODEL = "llama2-uncensored"
OLLAMA_HOST = 'http://localhost:11434'
MEMORY_FILE = 'memory.jsonl'
