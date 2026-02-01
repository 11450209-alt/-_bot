import discord
from discord.ext import commands
import os
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_CHANNEL_ID = int(os.environ["CHANNEL_ID"])

cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

@bot.event
async def on_ready():
    print(f"{bot.user} 已上線")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != ALLOWED_CHANNEL_ID:
        return

    content = message.content.strip()

    if content == "開始玩":
        await message.channel.send("我要驗牌")
        await asyncio.sleep(1)
        await message.channel.send("牌沒問題")
        await asyncio.sleep(1)

        player_card = random.choice(cards)
        dealer_card = random.choice(cards)

        await message.channel.send(f"你抽到的是 {player_card}")
        await message.channel.send(f"法國賭神抽到的是 {dealer_card}")

    await bot.process_commands(message)

bot.run(os.environ["TOKEN"])
