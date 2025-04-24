import discord
from discord.ext import commands
import asyncio
import os

#TOKEN = "MTE4NzM0NzgzODYxMTUwNTI1NA.GGJQ_2.AyimzDJBg3vGIqjIlMiNer3TWVQz_--3oq2GIQ"  # Replace this with your Discord token
TOKEN = "MTI5MTEyNjAyOTY5OTUxODU1NQ.G6bsgP.AIwxrvfm3p0m6QkH8iuEjXtdWd58AiWMRga0YE"
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

bot.run(TOKEN)
