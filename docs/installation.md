
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
