# Al - Conversational Discord Bot

**Al** is a conversational AI Discord bot that leverages the power of [Ollama](https://ollama.com) to provide intelligent and context-aware responses. It learns from past conversations by embedding them into a local vector database (MongoDB), enabling a memory system powered by Retrieval-Augmented Generation (RAG).

---

## Features

* **Conversational AI**: Powered by a local Ollama model (defaulting to `llama3`), Al engages in dynamic, intelligent conversation.
* **RAG-based Memory**: Messages are embedded and stored in MongoDB. Al retrieves relevant past messages to maintain context over time.
* **Flexible Interaction**: Responds when mentioned (`@Al your message`) or when replied to directly. The mention doesn't have to be at the start.
* **Customizable Personality**: Define Al's tone and behavior using a `SYSTEM_PROMPT`.
* **Typing Indicator**: Shows a "typing..." status for smoother UX.

---

## Prerequisites

Before running Al, make sure you have:

### Python 3.8+

Install it from [python.org](https://www.python.org/downloads/)

### Ollama Server

1. Install from [ollama.com](https://ollama.com)

2. Pull and run a model locally:

   ```bash
   ollama run llama3
   ```

3. Ensure it's accessible at `http://localhost:11434` or update `OLLAMA_HOST`.

### MongoDB (Local)

1. Install MongoDB:

   * macOS: `brew install mongodb-community`
   * Ubuntu: Follow [MongoDB Install Docs](https://www.mongodb.com/docs/manual/installation/)
2. Start the MongoDB service:

   ```bash
   mongod
   ```

### Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create/select an app → **Bot** → **Add Bot**
3. Enable **Message Content Intent**
4. Copy the bot token

---

## Bot Permissions

Use this permission integer to invite your bot: `85056`

Includes:

* Read Messages/View Channels
* Send Messages
* Embed Links
* Attach Files
* Read Message History
* Use External Emojis
* Add Reactions
* Use Slash Commands

Invite link format:

```
https://discord.com/oauth2/authorize?client_id=YOUR_BOT_CLIENT_ID&permissions=85056&scope=bot
```

Replace `YOUR_BOT_CLIENT_ID` with your app’s client ID.

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/myferr/al al-discord-bot
   cd al-discord-bot
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file:

   ```env
   DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
   MONGO_URI=mongodb://localhost:27017
   ```

---

## Running the Bot

1. **Start Ollama**:

   ```bash
   ollama run llama3
   ```

2. **Ensure MongoDB is running**:

   ```bash
   mongod
   ```

3. **Launch the bot**:

   ```bash
   python3 src/main.py
   ```

You’ll see something like:

```
Logged in as Al#1234 (ID: ...)
```

---

## Interacting with Al

Once Al is online:

* **Mention Al**: `Hey @Al, what's a monad?`
* **Reply to Al's message**: Just reply in the same thread

Al will pull relevant memory via RAG, enhancing responses using context from prior interactions.

---

## Customization

Edit settings in `src/settings.py` or `src/ollama_client.py`.

| Variable        | Description                                             |
| --------------- | ------------------------------------------------------- |
| `OLLAMA_MODEL`  | Model to use (`llama3`, `mistral`, etc.)                |
| `OLLAMA_HOST`   | URL for the Ollama server                               |
| `SYSTEM_PROMPT` | Defines Al’s persona/tone                               |
| `MONGO_URI`     | MongoDB connection string (`mongodb://localhost:27017`) |
| `MONGO_DB_NAME` | MongoDB database name (e.g., `al_memory`)               |

### Example SYSTEM\_PROMPT

```python
SYSTEM_PROMPT = "You are Al, a witty and helpful Discord bot who responds concisely but helpfully."
```

---

## Memory: RAG-based

Instead of a flat file, Al now uses a **RAG system**:

* Each message is embedded using a local embedding model.
* Stored in a **MongoDB** collection with vector search.
* On every interaction, the bot fetches semantically similar past messages.

You can reset memory by clearing the appropriate MongoDB collection:

```bash
mongo
> use al_memory
> db.messages.drop()
```

---

## Troubleshooting

### Bot not responding?

* Ensure you’ve enabled message content intent
* Verify permissions (see above)
* Check `.env` values and logs
* Is MongoDB and Ollama running?

### Model not found?

* Run: `ollama run llama3`
* Or switch models in `settings.py`

### MongoDB errors?

* Make sure `mongod` is running
* Check connection string in `.env`

---

## License

MIT License. Use freely, modify boldly. Just don’t impersonate Al—we know he likes chili dogs.

---

## Author

Built by [MyferIsADev (@myferr)](https://github.com/myferr) using Python, Discord.py, Ollama, and MongoDB.

###### [Terms of Service](https://al-bot-docs.vercel.app/terms.html) · [Privacy Policy](https://al-bot-docs.vercel.app/privacy.html)
