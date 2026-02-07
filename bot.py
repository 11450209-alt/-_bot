import discord
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    await message.channel.send("法國賭神：我有聽到")

client.run(os.environ["DISCORD_TOKEN"])
