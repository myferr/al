from bot import client
from settings import DISCORD_BOT_TOKEN

if __name__ == '__main__':
    if DISCORD_BOT_TOKEN:
        try:
            client.run(DISCORD_BOT_TOKEN)
        except Exception as e:
            print(f"Error running bot: {e}")
    else:
        print("DISCORD_BOT_TOKEN not found in .env")
