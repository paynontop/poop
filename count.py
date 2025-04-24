import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Load tokens from .env
load_dotenv()
tokens = os.getenv("TOKENS").split(",")

def create_bot(token):
    bot = commands.Bot(command_prefix="-", self_bot=True)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user} ({bot.user.id})")

    # To track countdowns per bot
    bot.counting_channels = {}

    @bot.command()
    async def count(ctx, start: int):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        bot.counting_channels[ctx.channel.id] = True

        for i in range(start, 0, -1):
            if not bot.counting_channels.get(ctx.channel.id):
                return
            await ctx.send(str(i))
            await asyncio.sleep(1)

        # Countdown completed normally
        await ctx.send("You just got raped by your papa Vanai! WOW STAPHA! did stapha get raped by his father? UwU OwO UnU OnO goood BITCH! LOL!")
        bot.counting_channels.pop(ctx.channel.id, None)

    @bot.event
    async def on_message(message):
        # Let command handlers run
        await bot.process_commands(message)

        # If someone else types during countdown
        if (
            message.channel.id in bot.counting_channels
            and message.author.id != bot.user.id
        ):
            # Interrupt the countdown
            bot.counting_channels[message.channel.id] = False
            try:
                await message.channel.send("AWW! did Mustapha Ahmady waste his time to stop vanais countdown??? GOOD SPLENDID BOOTY BITCH.. XD hahaha UwU OwO OnO Good slut stapha! let me eat those fat cheeks of yours fatso! hahaha!")
            except discord.Forbidden:
                pass

    return bot, token

async def main():
    tasks = []
    for token in tokens:
        bot, t = create_bot(token.strip())
        tasks.append(bot.start(t, reconnect=True))
    await asyncio.gather(*tasks)

# Run all bots
asyncio.run(main())
