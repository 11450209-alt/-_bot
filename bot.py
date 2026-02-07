import discord
from discord.ext import commands
import os

print("=== BOT STARTED : RESCUE VERSION ===")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"BOT READY | Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()
    print("收到訊息：", content)

    if not content:
        return

    text = content.lower()

    if "開始" in text or "玩" in text:
        await message.channel.send("🎲 遊戲開始了，來吧。")
        return

    if "賭" in text or "下注" in text:
        await message.channel.send("💰 賭神盯上你了，小心點。")
        return

    if "資產" in text or "餘額" in text or "錢" in text:
        await message.channel.send("📊 你現在窮得很有風格。")
        return

    if "test" in text or "測試" in text:
        await message.channel.send("✅ 我有收到，你不是在對空氣說話。")
        return

    # ===== 萬用 fallback（任何話都回）=====
    await message.channel.send("我聽到了。")

    await bot.process_commands(message)

# Railway / 本機 通用
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("❌ 沒抓到 DISCORD_TOKEN")
else:
    bot.run(TOKEN)
