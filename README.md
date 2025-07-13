# Al - Conversational Discord Bot

**Al** is a conversational AI Discord bot that leverages the power of [Ollama](https://ollama.com) to provide intelligent and context-aware responses. It learns from past conversations by saving messages and responses to a local memory file, allowing for more natural and engaging interactions.

---

## Features

- **Conversational AI**: Powered by a local Ollama model (defaulting to `llama3`), Al can engage in dynamic conversations.
- **Contextual Memory**: All user messages and Al's responses are saved to `memory.jsonl`, enabling the bot to learn from past interactions and maintain conversational context.
- **Flexible Interaction**: Al responds when directly pinged (`@Al your message`) or when a user replies to one of Al's messages. The ping does not need to be at the start of the message.
- **Customizable Personality**: A `SYSTEM_PROMPT` in the code defines Al's persona and tone.
- **Typing Indicator**: Al shows a "typing..." indicator while generating a response for a smoother user experience.

## Prerequisites

Before running Al, ensure you have the following:

### Python 3.8+
Install it from [python.org](https://www.python.org/downloads/).

### Ollama Server
1. Install from [ollama.com](https://ollama.com).
2. Run an Ollama model locally:
   ```bash
   ollama run llama3
   ```

3. Ensure your Ollama server is running at `http://localhost:11434`
   *(or update `OLLAMA_HOST` in the code if different).*

### Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create or select an application, and go to the **Bot** tab.
3. Click **Add Bot**.
4. Enable **Message Content Intent** under **Privileged Gateway Intents**.
5. Copy your bot token and keep it safe!

### Bot Permissions

Use this permissions integer when inviting your bot: `85056`

This allows:

* Read Messages/View Channels
* Send Messages
* Embed Links
* Attach Files
* Read Message History
* Use External Emojis
* Add Reactions
* Use Slash Commands

Generate an invite link like so:

```
https://discord.com/oauth2/authorize?client_id=YOUR_BOT_CLIENT_ID&permissions=85056&scope=bot
```

> Replace `YOUR_BOT_CLIENT_ID` with your actual client ID.

---

## Installation

1. **Clone or download** the project:

   ```bash
   git clone https://github.com/myferr/al al-discord-bot
   cd al-discord-bot
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file**:

   ```env
   DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE
   ```

## Running the Bot

1. **Start your Ollama model** (e.g., `llama3`):

   ```bash
   ollama run llama3
   ```

2. **Run the bot**:

   ```bash
   python3 src/main.py
   ```

3. You should see:

   ```
   Logged in as Al#1234 (ID: ...)
   ```


## Interacting with Al

Once Al is online and invited to your server:

* **Ping Al**:
  Mention the bot anywhere in your message, e.g.
  `Hey @Al, what's the best low-level language?`

* **Reply to Al**:
  Reply to any of Al’s previous messages.

Al will then generate a context-aware response using its memory and Ollama.

## Customization

You can modify the following variables in `src/settings.py` or `src/ollama_client.py`:

| Variable        | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| `OLLAMA_MODEL`  | Name of the model to use (`llama3`, `mistral`, `phi3`, etc.) |
| `OLLAMA_HOST`   | URL to your running Ollama server                            |
| `SYSTEM_PROMPT` | Defines Al’s personality and tone                            |
| `MEMORY_FILE`   | Path to Al’s message history file (default: `memory.jsonl`)  |

### Example: Custom SYSTEM_PROMPT

```python
SYSTEM_PROMPT = "You are Al, a helpful assistant that specializes in ancient history. You always respond with a historical fact."
```

## Memory

Al stores a simple chronological chat log in `memory.jsonl` like:

```json
{"role": "user", "content": "What is a pointer?"}
{"role": "assistant", "content": "**Pointers** are..."}
```

You can delete this file to reset Al’s memory.

## Troubleshooting

### Privileged Intents Error

Ensure that permissions are set correctly.

### Ollama Connection Error

Make sure Ollama is running and that the specified model is pulled.
Check your `OLLAMA_HOST` in the code.

### Invalid Token

Check your `.env` file and make sure there are no extra spaces or newlines.

### Bot Not Responding

* Ensure the bot is online in Discord
* Verify it has **Read Message History** and **Send Messages** permissions
* Check the terminal/logs for errors

---

## License

MIT License. Free for personal and commercial use.
Just don’t claim to be the original chili dog–loving Al.


## Author

Built by [MyferIsADev (@myferr)](https://github.com/myferr/) using Python, Discord.py, and Ollama.
