# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Al is a conversational Discord bot powered by Ollama that provides intelligent, context-aware responses. The bot maintains conversation memory and supports multiple interaction modes including regular chat, uncensored responses (NSFW channels only), and AI image generation.

## Architecture

### Core Components

- **`src/main.py`** - Entry point that initializes and runs the Discord bot
- **`src/bot.py`** - Main bot logic with Discord event handlers and slash commands
- **`src/memory.py`** - RAG-based memory system using MongoDB with text embeddings
- **`src/ollama_client.py`** - Ollama API client and system prompt configuration
- **`src/settings.py`** - Configuration management and environment variables

### Key Features

- **RAG Memory System**: MongoDB-based conversation storage with text embeddings for intelligent context retrieval
- **Multiple Models**: Standard (`llama3`), uncensored (`llama2-uncensored`), and image generation models
- **Interaction Modes**: Direct mentions, replies to bot messages, DMs, and slash commands
- **User Management**: Ban functionality and NSFW content restrictions
- **Privacy**: SHA256-hashed user IDs for data anonymization

## Development Commands

### Running the Bot
```bash
python3 src/main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Documentation (VitePress)
```bash
npm run docs:dev    # Development server
npm run docs:build  # Build static docs
npm run docs:preview # Preview built docs
```

## Prerequisites

1. **Python 3.8+** and dependencies from `requirements.txt`
2. **MongoDB** running locally or connection URI in environment variables
3. **Ollama server** running at `http://localhost:11434` with models:
   - `llama3` (default model)
   - `llama2-uncensored` (for /uncensored command)
4. **Discord bot token** in `.env` file as `DISCORD_TOKEN`
5. **Required Discord permissions**: Message content intent enabled, permissions integer `85056`

## Configuration

Key settings in `src/settings.py`:
- `OLLAMA_MODEL` - Primary chat model (default: `llama3`)
- `UNCENSORED_MODEL` - Model for NSFW content (default: `llama2-uncensored`)
- `OLLAMA_HOST` - Ollama server URL (default: `http://localhost:11434`)
- `MONGODB_URI` - MongoDB connection string (default: `mongodb://localhost:27017/`)
- `MONGODB_DATABASE` - Database name (default: `al_discord_bot`)
- `MONGODB_COLLECTION` - Collection name (default: `conversations`)
- `EMBEDDING_MODEL` - Text embedding model (default: `all-MiniLM-L6-v2`)
- `MAX_CONTEXT_MESSAGES` - Maximum messages retrieved via RAG (default: 10)
- `SIMILARITY_THRESHOLD` - Minimum similarity for context inclusion (default: 0.7)
- `BANNED` - List of banned user IDs
- `IMAGE_GEN_MODEL` - Diffusion model for image generation

## Bot Personality

Al's persona (defined in `src/ollama_client.py`):
- Software engineer who loves low-level programming languages
- Favorite food is chili dogs
- Uses Markdown formatting in responses
- Learns from interactions via conversation memory

## RAG Memory System

The bot uses Retrieval-Augmented Generation (RAG) to provide contextually relevant responses:

1. **Text Embedding**: All messages are converted to vectors using Sentence Transformers
2. **Similarity Search**: User queries are matched against stored embeddings using cosine similarity
3. **Context Retrieval**: Most relevant past conversations are included in the prompt
4. **Migration**: Existing JSONL memory files are automatically migrated to MongoDB on startup

## Slash Commands

- `/ask` - Direct conversation with Al
- `/uncensored` - Uncensored responses (NSFW channels only)
- `/image` - AI image generation from text prompts

## Environment Variables

Optional `.env` configuration:
```
DISCORD_TOKEN=your_discord_bot_token
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=al_discord_bot
MONGODB_COLLECTION=conversations
```