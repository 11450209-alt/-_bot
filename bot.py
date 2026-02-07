import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    print("BOT READY", bot.user)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await message.channel.send("我有收到")
    await bot.process_commands(message)

bot.run("你的TOKEN")
