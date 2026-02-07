import discord
from discord.ext import commands
import os
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="", intents=intents)

CHANNEL_ID = int(os.environ["CHANNEL_ID"])
OWNER_ID = int(os.environ["OWNER_ID"])

cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

money = {}
loss = {}
used_relief = set()
marked = set()
table = set()

@bot.event
async def on_ready():
    print("法國賭神已上線")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != CHANNEL_ID:
        return

    uid = message.author.id
    name = message.author.display_name
    content = message.content.strip()

    if uid not in money:
        money[uid] = 100
        loss[uid] = 0

    if content == "入桌":
        table.add(uid)
        await message.channel.send(f"{name} 坐上賭桌")
        return

    if content == "離桌":
        table.discard(uid)
        await message.channel.send(f"{name} 離開賭桌")
        return

    if content == "開賭":
        if len(table) < 2:
            await message.channel.send("法國賭神：一個人賭？可悲")
            return

        results = {}
        dealer = random.choice(cards)
        await message.channel.send(f"法國賭神亮牌：{dealer}")

        for p in table:
            draw = random.choice(cards)
            results[p] = draw
            await message.channel.send(f"<@{p}> 抽到 {draw}")

        for p, draw in results.items():
            if cards.index(draw) > cards.index(dealer):
                money[p] += 100
                if p in marked:
                    await message.channel.send(f"<@{p}>：被救過還贏？我記住你了")
                else:
                    await message.channel.send(f"<@{p}> 贏了 +100")
            elif cards.index(draw) < cards.index(dealer):
                money[p] -= 100
                loss[p] += 100
                if p in marked:
                    await message.channel.send(f"<@{p}>：爛命果然還是爛命")
                else:
                    await message.channel.send(f"<@{p}> 輸了 -100")
            else:
                await message.channel.send(f"<@{p}> 平手")

        worst = max(loss, key=loss.get)
        await message.channel.send(f"📢 全服公告：目前輸最慘的是 <@{worst}>，已輸 {loss[worst]}")
        return

    if content == "排行榜":
        rank = sorted(loss.items(), key=lambda x: x[1], reverse=True)
        text = "💀 輸最多排行榜\n"
        for i,(u,l) in enumerate(rank[:5],1):
            text += f"{i}. <@{u}>：{l}\n"
        await message.channel.send(text)
        return

    if content == "法國救濟":
        if uid != OWNER_ID:
            await message.channel.send("法國賭神：你不配")
            return
        if money[uid] > 0:
            await message.channel.send("法國賭神：你還沒爛到底")
            return
        if uid in used_relief:
            await message.channel.send("法國賭神：只救一次")
            return

        money[uid] = 1000
        used_relief.add(uid)
        marked.add(uid)
        await message.channel.send("法國賭神：最後一次，別再讓我看到你破產")
        return

bot.run(os.environ["TOKEN"])


