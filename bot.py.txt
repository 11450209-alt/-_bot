import discord
import os
import random
import asyncio

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

deck = []
playing = False

@client.event
async def on_ready():
    print("🇫🇷 法國賭神已上線")

@client.event
async def on_message(message):
    global deck, playing

    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    msg = message.content.strip()

    if msg == "開始":
        if playing:
            await message.channel.send("牌桌已開，你還想再開？")
            return
        await message.channel.send("要玩？我先說一句。")
        await asyncio.sleep(1)
        await message.channel.send("我要驗排")
        return

    if msg == "我要驗排" and not playing:
        deck = [i for i in range(1, 14)] * 4
        random.shuffle(deck)
        await asyncio.sleep(1)
        await message.channel.send("牌沒問題")
        await asyncio.sleep(1)
        await message.channel.send("來，開始。")
        playing = True
        return

    if msg == "抽牌" and playing:
        if not deck:
            await message.channel.send("沒牌了，今天不適合再玩。")
            playing = False
            return
        card = deck.pop()
        await message.channel.send(f"你抽到：{card}")
        return

    if msg == "結束":
        playing = False
        await message.channel.send("散桌。記住，是我放你走的。")
        return

client.run(TOKEN)
