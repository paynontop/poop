import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the token
token = os.getenv("DISCORD_TOKEN")


bot = commands.Bot(command_prefix="-", self_bot=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")

@bot.command()
async def count(ctx, start: int):
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    for i in range(start, 0, -1):  # Count down: 1000, 999, 998, ..., 1
        await ctx.send(str(i))
        await asyncio.sleep(1)

bot.run(token)