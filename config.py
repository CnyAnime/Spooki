import os

import discord

# Bot
intents = discord.Intents.all()
activity = discord.Streaming(name="s!", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
token = os.getenv("TOKEN")
extensions = ("guild_config", "owner", "error_handling", "utility", "images")
error_channel = None  # the channel id of the channel where errors should be sent
emojis = {
    "tick": "✅",
    "cross": "❌"
}

# Prefix
prefix = "s!"
case_insensitive = True
strip_after_prefix = True
mention_prefix = True

# Database
host = "localhost"
port = 5432
user = "postgres"
database = "spooki"

# Spotify
spotify_client_id = ""