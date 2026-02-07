import discord
from discord.ext import commands
import os
import json
import random
import asyncio

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
OWNER_ID = int(os.environ["OWNER_ID"])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

money = {}
table = set()
current_game = False
loser_count = {}

def load_money():
    global money
    if os.path.exists("money.json"):
        with open("money.json", "r", encoding="utf-8") as f:
            money = json.load(f)

def save_money():
    with open("money.json", "w", encoding="utf-8") as f:
        json.dump(money, f, ensure_ascii=False)

@bot.event
async def on_ready():
    load_money()
    print("法國賭神已上線")

def allowed(ctx):
    return ctx.channel.id == CHANNEL_ID

@bot.command()
async def 賭(ctx):
    global current_game
    if not allowed(ctx):
        return
    if current_game:
        await ctx.send("🇫🇷 賭神：急什麼？桌上還沒散。")
        return
    current_game = True
    await ctx.send("🇫🇷 我要驗排")
    await asyncio.sleep(2)
    await ctx.send("🇫🇷 牌沒問題，開賭")

@bot.command()
async def 加入(ctx):
    if not allowed(ctx):
        return
    table.add(ctx.author.id)
    uid = str(ctx.author.id)
    if uid not in money:
        money[uid] = 1000
    await ctx.send(f"🇫🇷 {ctx.author.display_name} 入座")

@bot.command()
async def 離開(ctx):
    if not allowed(ctx):
        return
    table.discard(ctx.author.id)
    await ctx.send(f"🇫🇷 {ctx.author.display_name} 離桌")

@bot.command()
async def 開桌(ctx):
    global current_game
    if not allowed(ctx):
        return
    if len(table) < 2:
        await ctx.send("🇫🇷 人不夠，賭什麼？")
        return
    players = list(table)
    loser = random.choice(players)
    for p in players:
        uid = str(p)
        if uid not in money:
            money[uid] = 1000
    loss = random.randint(100, 500)
    money[str(loser)] -= loss
    loser_count[str(loser)] = loser_count.get(str(loser), 0) + loss
    save_money()
    member = ctx.guild.get_member(loser)
    await ctx.send(f"🇫🇷 {member.display_name} 爆死，輸 {loss} 元")
    current_game = False

@bot.command()
async def 資產(ctx):
    if not allowed(ctx):
        return
    uid = str(ctx.author.id)
    if uid not in money:
        money[uid] = 0
    await ctx.send(f"🇫🇷 你的資產：{money[uid]} 元")

@bot.command()
async def 誰最爛(ctx):
    if not allowed(ctx):
        return
    if not loser_count:
        await ctx.send("🇫🇷 還沒人夠爛")
        return
    worst = max(loser_count, key=loser_count.get)
    member = ctx.guild.get_member(int(worst))
    await ctx.send(f"🇫🇷 最爛的是 {member.display_name}，輸爆 {loser_count[worst]} 元")

@bot.command()
async def 排行榜(ctx):
    if not allowed(ctx):
        return
    if not money:
        await ctx.send("🇫🇷 沒人有錢")
        return
    ranking = sorted(money.items(), key=lambda x: x[1], reverse=True)
    msg = "🇫🇷 資產排行榜\n"
    for i,(uid,amt) in enumerate(ranking[:5],1):
        member = ctx.guild.get_member(int(uid))
        if member:
            msg += f"{i}. {member.display_name} {amt} 元\n"
    await ctx.send(msg)

@bot.command()
async def 發錢(ctx, amount:int):
    if not allowed(ctx):
        return
    if ctx.author.id != OWNER_ID:
        await ctx.send("🇫🇷 你也敢印鈔？")
        return
    uid = str(ctx.author.id)
    money[uid] = money.get(uid,0) + amount
    save_money()
    await ctx.send(f"🇫🇷 黑金入帳 +{amount} 元")

bot.run(TOKEN)
