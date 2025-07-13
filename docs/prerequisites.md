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
