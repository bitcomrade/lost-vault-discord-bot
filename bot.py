import discord
import os
import discord.ext
from dotenv import load_dotenv
from discord.ext import commands
#^ basic imports for other features of discord.py and python ^


load_dotenv()
# Set Discord bot token variable according to your environment
TOKEN = os.getenv("DISCORD-TOKEN")

# Set command prefix below
bot = commands.Bot(command_prefix = '!')

bot.load_extension("basic_commands")

if __name__ == "__main__":
    bot.run(TOKEN)
