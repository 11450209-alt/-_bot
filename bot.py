import discord
from discord.ext import commands
import os
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

allowed_channel = int(os.environ["CHANNEL_ID"])

cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

@bot.event
async def on_ready():
    print(f"{bot.user} 已上線")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != allowed_channel:
        return

    content = message.content.strip()

    if content == "開始玩":
        await message.channel.send("我要驗牌")
        await message.channel.send("牌沒問題")
        player = random.choice(cards)
        dealer = random.choice(cards)
        await message.channel.send(f"你抽到的是 {player}")
        await message.channel.send(f"我抽到的是 {dealer}")
        if cards.index(player) > cards.index(dealer):
            await message.channel.send("呵，看來這一把是你贏了。但我可是法國賭神。")
        elif cards.index(player) < cards.index(dealer):
            await message.channel.send("勝負已分。法國賭神從不失手。")
        else:
            await message.channel.send("平手？命運在嘲笑我們。")

    await bot.process_commands(message)

bot.run(os.environ["TOKEN"])
