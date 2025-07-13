import discord
from ollama_client import get_ollama_client, OLLAMA_MODEL, SYSTEM_PROMPT
from memory import load_memory, save_message
from settings import OLLAMA_HOST

ollama_client = get_ollama_client()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def split_message(text, max_length=2000):
    lines = text.split('\n')
    chunks = []
    current_chunk = ''
    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk)
            current_chunk = ''
        current_chunk += line + '\n'
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    await client.change_presence(activity=discord.Game(name="Chatting with Al"))

@client.event
async def on_message(message):
        if message.author == client.user:
            return

        is_dm = isinstance(message.channel, discord.DMChannel)

        if is_dm:
            content = message.content.strip()
            if not content:
                await message.channel.send("Hey! You didn't say anything.")
                return

        else:
            mention_id = f'<@{client.user.id}>'
            mention_nick = f'<@!{client.user.id}>'

            contains_ping = mention_id in message.content or mention_nick in message.content
            is_reply_to_bot = (
                message.reference and message.reference.resolved
                and message.reference.resolved.author == client.user
            )

            if not (contains_ping or is_reply_to_bot):
                return

            content = message.content.replace(mention_id, '').replace(mention_nick, '').strip()
            if not content:
                await message.reply(f"Hey {message.author.mention}, you mentioned me but didn't say anything!")
                return

        if not ollama_client:
            await message.channel.send("Cannot connect to Ollama. Make sure it's running.")
            return

        print(f"Message from {message.author}: {content}")

        user_entry = {"role": "user", "content": content}
        save_message(user_entry["role"], user_entry["content"])

        history = [{"role": "system", "content": SYSTEM_PROMPT}] + load_memory() + [user_entry]

        try:
            async with message.channel.typing():
                response = ollama_client.chat(model=OLLAMA_MODEL, messages=history)
                reply = response['message']['content']
                print(f"Ollama response: {reply}")
            save_message("assistant", reply)

            chunks = split_message(reply)

            if is_dm:
                for chunk in chunks:
                    await message.channel.send(chunk)
            else:
                await message.reply(chunks[0])
                for chunk in chunks[1:]:
                    await message.channel.send(chunk)

        except Exception as e:
            print(f"Error with Ollama: {e}")
            await message.channel.send(f"Something went wrong with my brain: {e}")
