import os
import re
import random
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
OWNER_ID = int(os.getenv("OWNER_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

players = {}
loss_board = {}

def get_money(uid):
    return players.get(uid, 100)

def add_money(uid, amount):
    players[uid] = get_money(uid) + amount

def record_loss(uid, amount):
    loss_board[uid] = loss_board.get(uid, 0) + amount

def draw_card():
    return random.randint(1, 11)

@bot.event
async def on_ready():
    print("賭神上線")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != CHANNEL_ID:
        return

    uid = message.author.id
    content = message.content.strip()

    if any(k in content for k in ["開始", "賭", "玩", "來"]):
        nums = re.findall(r"\d+", content)
        bet = int(nums[0]) if nums else 10

        money = get_money(uid)
        if money <= 0:
            await message.channel.send(f"{message.author.mention} 你已經破產了，去跪著求賭神")
            return

        if bet > money:
            bet = money

        add_money(uid, -bet)

        player_score = draw_card() + draw_card()
        dealer_score = draw_card() + draw_card()

        result = f"{message.author.mention} 下注 {bet}\n你 {player_score} 點｜賭神 {dealer_score} 點\n"

        if player_score > 21:
            record_loss(uid, bet)
            await message.channel.send(result + "爆了，錢沒了，笑死")
        elif dealer_score > 21 or player_score > dealer_score:
            win = bet * 2
            add_money(uid, win)
            await message.channel.send(result + f"你贏了 {win}，但別太得意")
        elif player_score < dealer_score:
            record_loss(uid, bet)
            await message.channel.send(result + "你輸了，賭神搖頭")
        else:
            add_money(uid, bet)
            await message.channel.send(result + "平手，不代表你很強")

        return

    if "資產" in content:
        await message.channel.send(f"{message.author.mention} 你現在剩 {get_money(uid)}")
        return

    if any(k in content for k in ["給我錢", "加錢", "發錢"]):
        if uid != OWNER_ID:
            await message.channel.send("你也配跟賭神要錢？")
            return
        nums = re.findall(r"\d+", content)
        if not nums:
            await message.channel.send("你至少打個數字")
            return
        amt = int(nums[0])
        add_money(uid, amt)
        await message.channel.send(f"賭神不爽但還是給了你 {amt}")
        return

    if "排行榜" in content:
        if not loss_board:
            await message.channel.send("目前還沒人輸到值得紀念")
            return
        sorted_losers = sorted(loss_board.items(), key=lambda x: x[1], reverse=True)
        text = "🏆 輸最多排行榜\n"
        for i, (pid, amt) in enumerate(sorted_losers[:5], 1):
            user = await bot.fetch_user(pid)
            text += f"{i}. {user.name} 輸了 {amt}\n"
        await message.channel.send(text)
        return

bot.run(TOKEN)
