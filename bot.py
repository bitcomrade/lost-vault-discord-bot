import nextcord
import os
import nextcord.ext
# for testing purposes when hosting on my PC
# Remove dotenv when deploy
#from dotenv import load_dotenv
#
from nextcord.ext import commands
#^ basic imports for other features of nextcord.py and python ^


# for testing purposes when hosting on my PC
# Remove dotenv when deploy
#load_dotenv()

# Set nextcord bot token variable according to your environment
TOKEN = os.getenv("DISCORD-TOKEN")

# Set command prefix below
bot = commands.Bot(command_prefix = '!')

bot.load_extension("basic_commands")

if __name__ == "__main__":
    bot.run(TOKEN)
