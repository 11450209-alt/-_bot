import discord
from discord.ext import commands
import os
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

deck = [
    ("A",11),("2",2),("3",3),("4",4),("5",5),("6",6),
    ("7",7),("8",8),("9",9),("10",10),("J",10),("Q",10),("K",10)
]

coins = {}

win_talk = [
    "你以為你真的會贏？",
    "這只是數學事故",
    "我讓你有參與感而已"
]

lose_talk = [
    "錢留下，人可以滾了",
    "這桌是我的",
    "賭之前沒拜法國賭神？"
]

humiliate = [
    "輸成這樣你還敢再玩？",
    "你剛剛那局真的很好笑",
    "我會記住你的名字，當反面教材",
    "給我擦皮鞋"
]

@bot.event
async def on_ready():
    print("法國賭神已上桌")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    uid = message.author.id
    if uid not in coins:
        coins[uid] = 1000

    if message.content.startswith("餘額"):
        await message.channel.send(f"{message.author.mention} 你剩下 {coins[uid]} 籌碼")
        return

    if not message.content.startswith("開始玩"):
        return

    parts = message.content.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.channel.send("格式錯誤，用：開始玩 金額")
        return

    bet = int(parts[1])

    if bet <= 0:
        await message.channel.send("你這是在賭空氣？")
        return

    if bet > coins[uid]:
        await message.channel.send("你沒那麼多錢")
        return

    await message.channel.send("我要驗牌")
    await asyncio.sleep(1)
    await message.channel.send("牌沒問題")
    await asyncio.sleep(1)

    player_hand = []
    dealer_hand = []

    def draw():
        return random.choice(deck)

    def total(hand):
        s = sum(c[1] for c in hand)
        aces = sum(1 for c in hand if c[0] == "A")
        while s > 21 and aces:
            s -= 10
            aces -= 1
        return s

    player_hand.extend([draw(), draw()])
    dealer_hand.extend([draw(), draw()])

    await message.channel.send(
        f"你拿到 {player_hand[0][0]} {player_hand[1][0]} ｜ {total(player_hand)} 點"
    )
    await asyncio.sleep(1)
    await message.channel.send(
        f"法國賭神明牌 {dealer_hand[0][0]}"
    )
    await asyncio.sleep(1)

    while total(player_hand) < 17:
        await message.channel.send("你要牌")
        await asyncio.sleep(1)
        player_hand.append(draw())
        await message.channel.send(
            f"你補到 {player_hand[-1][0]} ｜ {total(player_hand)} 點"
        )
        await asyncio.sleep(1)
        if total(player_hand) > 21:
            coins[uid] -= bet
            await message.channel.send("你爆了")
            for t in humiliate:
                await asyncio.sleep(1)
                await message.channel.send(t)
            return

    await message.channel.send("你停牌")
    await asyncio.sleep(1)

    while total(dealer_hand) < 17:
        dealer_hand.append(draw())
        await asyncio.sleep(1)

    p = total(player_hand)
    d = total(dealer_hand)

    await message.channel.send(
        f"法國賭神攤牌 {', '.join(c[0] for c in dealer_hand)} ｜ {d} 點"
    )
    await asyncio.sleep(1)

    if d > 21 or p > d:
        coins[uid] += bet
        await message.channel.send("你贏了")
        await message.channel.send(random.choice(win_talk))
    elif p < d:
        coins[uid] -= bet
        await message.channel.send("你輸了")
        for t in humiliate:
            await asyncio.sleep(1)
            await message.channel.send(t)
    else:
        await message.channel.send("平手")
        await message.channel.send("平手也不代表你很強")

bot.run(TOKEN)




