import discord
import json
from datetime import datetime
from grid_utils import parse_grid, hash_grid, find_repeat
from prng_simulator import try_bruteforce_seed

TOKEN = ""
CHANNEL_ID = 1416766733527810058
TARGET_BOT_ID = 1405696733232758968
LOG_FILE = "mines_logs.json"

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)

def load_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_log(entry):
    logs = load_logs()
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID or message.author.id != TARGET_BOT_ID:
        return

    if "💥 BOOM!" not in message.content:
        return

    full_content = message.content
    for embed in message.embeds:
        if embed.description:
            full_content += "\n" + embed.description

    grid = parse_grid(full_content)
    if not grid:
        return

    ts = datetime.utcnow().isoformat()
    hashed = hash_grid(grid)

    repeat = find_repeat(grid)
    if repeat:
        print(f"♻️ Repeat layout detected from {repeat['timestamp']}")
    else:
        print("🆕 New grid layout")

    predicted_grid = try_bruteforce_seed(grid)

    log_entry = {
        "timestamp": ts,
        "grid": grid,
        "hash": hashed,
        "predicted_from_seed": predicted_grid
    }

    save_log(log_entry)

client.run(TOKEN)
