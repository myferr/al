import discord
from discord.ext import commands
from discord import app_commands
from ollama_client import get_ollama_client, OLLAMA_MODEL, SYSTEM_PROMPT
from memory import load_memory, save_message
from settings import MEMORY_FILE, OLLAMA_HOST, UNCENSORED_MODEL, IMAGE_GEN_MODEL, BANNED
from datetime import datetime
import json
import io
import torch
from diffusers import DiffusionPipeline
import numpy as np

ollama_client = get_ollama_client()

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

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

def log_uncensored(entry):
    with open("memory_uncensored.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    await client.change_presence(activity=discord.Game(name="Chatting with Al"))

    try:
        synced = await client.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = str(message.author.id)
    if user_id in BANNED:
        try:
            await message.author.send("You are not allowed to interact.")
        except:
            pass
        return

    await client.process_commands(message)

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

    display_name = message.author.display_name

    save_message(user_id, "user", content, display_name)

    history = [{"role": "system", "content": f"You are talking with {display_name}. Be friendly."}]
    history += load_memory(user_id)
    history.append({"role": "user", "content": content})

    try:
        async with message.channel.typing():
            response = ollama_client.chat(model=OLLAMA_MODEL, messages=history)
            reply = response['message']['content']
        save_message(user_id, "assistant", reply, display_name)

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

@client.tree.command(name="uncensored", description="Use an uncensored model to generate a response (NSFW channels only).")
@app_commands.describe(message="Your prompt for the uncensored model")
async def uncensored(interaction: discord.Interaction, message: str):
    user_id = str(interaction.user.id)
    if user_id in BANNED:
        await interaction.response.send_message("You are not allowed to interact.", ephemeral=True)
        return

    if not interaction.channel.is_nsfw():
        await interaction.response.send_message("❌ This command only works in age-restricted (NSFW) channels.", ephemeral=True)
        return

    try:
        if not interaction.response.is_done():
            await interaction.response.defer(thinking=True)
    except Exception as e:
        print(f"Warning on defer in uncensored: {e}")

    try:
        display_name = interaction.user.display_name
        save_message(user_id, "user", message, display_name)

        history = [{"role": "system", "content": f"You are chatting with {display_name}."}]
        history += load_memory(user_id)
        history.append({"role": "user", "content": message})

        response = ollama_client.chat(
            model=UNCENSORED_MODEL,
            messages=history
        )["message"]["content"]

        log_uncensored({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "uncensored": True,
            "user_id": user_id,
            "prompt": message,
            "response": response
        })

        disclaimer = "This response was generated using an uncensored AI model. It may contain offensive or unmoderated content. Use responsibly."

        chunks = split_message(response)
        for chunk in chunks:
            await interaction.followup.send(f"||```\n{chunk.strip()}\n```||\n{disclaimer}")

    except Exception as e:
        await interaction.followup.send(f"Uncensored model failed: {e}")

pipe = None

@client.tree.command(name="image", description="Generate an image from a prompt using a free CC0-licensed model.")
@app_commands.describe(prompt="Describe what you want to see")
async def image(interaction: discord.Interaction, prompt: str):
    user_id = str(interaction.user.id)
    if user_id in BANNED:
        await interaction.response.send_message("You are not allowed to interact.", ephemeral=True)
        return

    try:
        if not interaction.response.is_done():
            await interaction.response.defer(thinking=True)
    except Exception as e:
        print(f"Warning on defer in image command: {e}")

    global pipe
    try:
        if pipe is None:
            device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
            print(f"Loading pipeline on device: {device}")
            pipe = DiffusionPipeline.from_pretrained(IMAGE_GEN_MODEL)
            pipe = pipe.to(device)

        generated_image = pipe(prompt).images[0]

        arr = np.array(generated_image)
        if np.all(arr == 0):
            await interaction.followup.send("I cannot generate any NSFW or explicit content.")
            return

        image_bytes = io.BytesIO()
        generated_image.save(image_bytes, format="PNG")
        image_bytes.seek(0)

        image_file = discord.File(image_bytes, filename="generated_image.png")
        await interaction.followup.send(content=f"🖼️ Prompt: `{prompt}`", file=image_file)

    except Exception as e:
        print(f"Image generation error: {e}")
        try:
            await interaction.followup.send(f"❌ Failed to generate image: {e}")
        except Exception as e2:
            print(f"Also failed to send error message: {e2}")

@client.tree.command(name="ask", description="Ask Al a question or say something directly.")
@app_commands.describe(message="Your message for Al")
async def ask(interaction: discord.Interaction, message: str):
    user_id = str(interaction.user.id)
    if user_id in BANNED:
        await interaction.response.send_message("You are not allowed to interact.", ephemeral=True)
        return

    try:
        if not interaction.response.is_done():
            await interaction.response.defer(thinking=True)
    except Exception as e:
        print(f"Warning on defer in ask command: {e}")

    try:
        display_name = interaction.user.display_name
        save_message(user_id, "user", message, display_name)

        history = [{"role": "system", "content": f"You are chatting with {display_name}. Be friendly."}]
        history += load_memory(user_id)
        history.append({"role": "user", "content": message})

        response = ollama_client.chat(
            model=OLLAMA_MODEL,
            messages=history
        )["message"]["content"]

        save_message(user_id, "assistant", response, display_name)

        chunks = split_message(response)
        for chunk in chunks:
            await interaction.followup.send(chunk)

    except Exception as e:
        await interaction.followup.send(f"❌ Something went wrong: {e}")
