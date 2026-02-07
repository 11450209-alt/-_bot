import discord
from discord.ext import commands
import os

print("=== BOT STARTED : STABLE RESCUE VERSION ===")

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
    if not content:
        return

    text = content.lower()
    print("收到訊息：", text)

    responded = False

    if "test" in text or "測試" in text:
        await message.channel.send("✅ 我有收到，你不是在對空氣說話。")
        responded = True

    elif "開始" in text or "玩" in text:
        await message.channel.send("🎲 遊戲開始了，來吧。")
        responded = True

    elif "賭" in text or "下注" in text:
        await message.channel.send("💰 賭神盯上你了，小心點。")
        responded = True

    elif "資產" in text or "餘額" in text or "錢" in text:
        await message.channel.send("📊 你現在窮得很有風格。")
        responded = True

    # ❗ 不再「任何話都回」，避免洗頻與 container 被殺
    if responded:
        return

    await bot.process_commands(message)

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("❌ 沒抓到 DISCORD_TOKEN")
else:
    bot.run(TOKEN)
