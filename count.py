import discord
import re
import asyncio
import os
import json
import random
from discord.ext import commands
from dotenv import load_dotenv

stop = 0
load_dotenv()

call_lock = asyncio.Lock()
TOKENS = os.getenv("TOKENS", "").split(",")

ALLOWED_USER_IDS = {992775256257335316, 1187347838611505254, 1122988461490716742, 1275760436515704845}
BLACKLIST = {1359408069070688399, 1364569934088110100, 723468629454356570, 943641732451532870, 843600445285203988, 1190542448435417161, 254016480147013632}

NUMBER_WORDS = [
    # English
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹", "₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉",
    "jedan", "dva", "tri", "cetiri", "pet", "sest", "sedam", "osam", "devet", "deset", "won", "dwo", "dree",
    "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez",
    "foive", "foor", "dree", "Too", "Wan", "tin", "noine", "ate", "seben", "sigs", "foive",
    "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix",
    "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn",
    "uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove", "dieci",
    "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez",
    "odin", "dva", "tri", "chetyre", "pyat", "shest", "sem", "vosem", "devyat", "desyat",
    "wahid", "ithnan", "thalatha", "arba'a", "khamsa", "sitta", "sab'a", "thamaniya", "tis'a", "ashara",
    "ichi", "ni", "san", "shi", "go", "roku", "shichi", "hachi", "kyuu", "juu",
    "yi", "er", "san", "si", "wu", "liu", "qi", "ba", "jiu", "shi",
    "ek", "do", "teen", "char", "paanch", "chhah", "saat", "aath", "nau", "dus",
    "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz", "on",
    "hana", "dul", "set", "net", "daseot", "yeoseot", "ilgop", "yeodeol", "ahop", "yeol",
    "moja", "mbili", "tatu", "nne", "tano", "sita", "saba", "nane", "tisa", "kumi",
    "ena", "dyo", "tria", "tessera", "pente", "exi", "epta", "okto", "ennea", "deka",
    "echad", "shtayim", "shalosh", "arba", "chamesh", "shesh", "sheva", "shmone", "tesha", "eser",
    "ek", "dui", "tin", "char", "pach", "choy", "sat", "at", "noy", "dosh",
    "mot", "hai", "ba", "bon", "nam", "sau", "bay", "tam", "chin", "muoi",
    "isa", "dalawa", "tatlo", "apat", "lima", "anim", "pito", "walo", "siyam", "sampu",
    "واحد", "اثنان", "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة", "عشرة",
    "yek", "do", "se", "chahar", "panj", "shesh", "haft", "hasht", "noh", "dah",
    "یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه", "ده",
]

NUMBER_REGEX = re.compile(r'\d+|(' + '|'.join(NUMBER_WORDS) + r')', re.IGNORECASE)

def create_bot(token):
    bot = commands.Bot(command_prefix="-", self_bot=True)
    bot.counting_channels = {}

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')

    @bot.command()
    async def call(ctx, times: int):
        if not isinstance(ctx.channel, (discord.DMChannel, discord.GroupChannel)):
            return

        if not call_lock.locked():
            async with call_lock:
                try:
                    await ctx.message.delete()
                except:
                    pass

                for i in range(times):
                    try:
                        print(f"[{bot.user}] Calling {i + 1}/{times}")
                        payload = {
                            "op": 4,
                            "d": {
                                "guild_id": None,
                                "channel_id": str(ctx.channel.id),
                                "self_mute": False,
                                "self_deaf": False
                            }
                        }
                        await bot.ws.send(json.dumps(payload))
                        await asyncio.sleep(1)

                        payload["d"]["channel_id"] = None
                        await bot.ws.send(json.dumps(payload))
                        await asyncio.sleep(1 + random.uniform(0.3, 0.7))
                    except Exception as e:
                        print(f"[{bot.user}] Error in call: {e}")
        else:
            print(f"[{bot.user}] Skipped -call, already in progress.")

    @bot.command()
    async def c(ctx, start: int):
        try:
            global stop
            stop = 0
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        bot.counting_channels[ctx.channel.id] = True
        for i in range(start, 0, -1):
            if not bot.counting_channels.get(ctx.channel.id):
                return
            await ctx.send(str(i))
            await asyncio.sleep(1)
        await ctx.send("You just got raped by your papa Vanai! WOW STAPHA! did stapha get raped by his father? UwU OwO UnU OnO goood BITCH! LOL!")
        bot.counting_channels.pop(ctx.channel.id, None)
    @bot.command()
    async def h(ctx):
        help_text = (
            "```ansi\n"
            "\u001b[0m\u001b[31mTo view help for a command: \u001b[1m\u001b[34m-help <Command>\n"
            "\u001b[0m\n"
            "\u001b[30m\u001b[1m\u001b[34mCommands\u001b[0m\n"
            " \u001b[40m\u001b[35m- call      \u001b[0m\n"
            " \u001b[40m\u001b[35m- count     \u001b[0m\n"
            "\u001b[0m\n"
            "Made by: \u001b[1m\u001b[37mpaynah\n"
            "\u001b[0mVersion: \u001b[1m\u001b[37m4.2.0\u001b[0m```"
        )
        await ctx.send(help_text)

    @bot.event
    async def on_message(message):
        await bot.process_commands(message)
        global stop

        if message.author.id == bot.user.id or message.author.id in BLACKLIST:
            return

        if message.channel.id in bot.counting_channels and message.author.id != bot.user.id and stop != 1:
            bot.counting_channels[message.channel.id] = False
            try:
                
                stop = 1
                await message.channel.send("AWW! did Mustapha Ahmady waste his time to stop vanais countdown??? GOOD SPLENDID BOOTY BITCH.. XD hahaha UwU OwO OnO Good slut stapha! let me eat those fat cheeks of yours fatso! hahaha!")
            except:
                pass

        if NUMBER_REGEX.search(message.content):
            if isinstance(message.channel, (discord.DMChannel, discord.GroupChannel)):
                try:
                    if not "NICE TRY FATSO!" in message.content and not "VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! chu cant catch cho papa lacking ever again yes countdown I dare you good bitch yes good little slut for papai arent ya VAWAPOO! YES VAWAPOO" in message.content:

                        await message.channel.send("NICE TRY FATSO!", reference=message)
                except:
                    pass
            elif message.guild and message.author.id in ALLOWED_USER_IDS:
                try:
                    await message.channel.send("NICE TRY!", reference=message)
                except:
                    pass

    return bot

async def main():
    bots = [create_bot(token) for token in TOKENS]
    await asyncio.gather(*[bot.start(token) for bot, token in zip(bots, TOKENS)])

asyncio.run(main())
