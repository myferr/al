import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')
OLLAMA_MODEL = 'llama3'
UNCENSORED_MODEL = "llama2-uncensored"
OLLAMA_HOST = 'http://localhost:11434'
MEMORY_FILE = 'memory.jsonl'  # Legacy - kept for migration
IMAGE_GEN_MODEL = "aiyouthalliance/Free-Image-Generation-CC0"
BANNED = []

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'al_discord_bot')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'conversations')

# RAG Configuration
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'  # Sentence transformer model
MAX_CONTEXT_MESSAGES = 10  # Maximum number of messages to retrieve via RAG
SIMILARITY_THRESHOLD = 0.7  # Minimum similarity score for including messages
