import os

from nextcord.ext import commands

# for testing purposes when hosting on my PC
# Remove dotenv when deploy
# from dotenv import load_dotenv

# load_dotenv()

# Set nextcord bot token variable according to your environment
TOKEN = os.getenv("DISCORD-TOKEN")
# Set command prefix below
bot = commands.Bot(command_prefix="!")

bot.load_extension("basic_commands")
bot.load_extension("application_commands")

if __name__ == "__main__":
    bot.run(TOKEN)
