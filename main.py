import discord
import os
import time
import discord.ext
import search_lv_api
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
from tabulate import tabulate
#^ basic imports for other features of discord.py and python ^

def prettify_tribe(raw_data):
  line_1 = '```\nTRIBE: ' + raw_data.get('TRIBE')  + '\n'
  stat_table = []
  for value in range(1,4):
    label_1 = tribe_order[value]
    label_2 = tribe_order[value+3]
    stat_table.append((label_1,':',raw_data.get(label_1),label_2,':',raw_data.get(label_2)))
  table = tabulate(stat_table)
  result = line_1 + table + '\n```'
  return result

def prettify_player(data):
  line_1 = '```\nNAME: ' + data.get('NAME') + '\nCLASS: ' + data.get('CLASS') + '\nTRIBE: ' + data.get('TRIBE') + '\n'
  stat_table = []
  for value in range(3,11):
    label_1 = player_order[value]
    label_2 = player_order[value+8]
    #label_3 = player_order[value+10]
    stat_table.append((label_1, ':',data.get(label_1),label_2,':',data.get(label_2)))
  table = tabulate(stat_table)
  result = line_1 + table + '\n```'
  return result

client = discord.Client()

hello_message = '''\nHello! I am Mysterious Stranger and I can provide information about explorers and tribes of Lost Vault RPG.\nType !seekhelp for commands\n'''
no_result_message = '''\nThe search yielded no results. Check if the name is spelled correctly\n'''
help_message = '''\n!seekplayer {Name} to search player information\n!seektribe {Tribe} to search tribe information\nFor a successful result name of a tribe or a player must contain nothing but numbers and letters of the English alphabet (the space  is also OK)\nIf the name contains non-standard characters, you should check under which name you are recorded in the game database.\nTo do this, in the game, in the tribe or player information window, find the share button and click on the link. Your name in the database will be in the address bar after /player/ or /guild/ and may look like user-01 or guild-01\n'''

tribe_order = ['TRIBE', 'LVL', 'Rank', 'MEMBERS', 'REACTOR', 'Fame', 'Power']
#player_order = ['NAME','TRIBE','CLASS','STR','AGI','END','INT','LCK','LVL','Rank','Fame','Power','Quests','Explores','Monsters','Caravan','Vault','Survival']
player_order = ['NAME','TRIBE','CLASS','LVL','Rank','STR','AGI','END','INT','LCK','','Fame','Power','Quests','Explores','Monsters','Caravan','Vault','Survival']

# instantiate LostVault class from search_lv_api.py
lv_api = search_lv_api.LostVault()

client = commands.Bot(command_prefix = '!') #put your own prefix here
TOKEN = os.getenv("DISCORD-TOKEN")

@client.event
async def on_ready():
    print("bot online") #will print "bot online" in the console when the bot is online
    
    
@client.command()
async def ping(ctx):
    await ctx.send("pong!") #simple command so that when you type "!ping" the bot will respond with "pong!"

@client.event
async def on_message(message): 
  if message.author == client.user:
      return  
  # lower case message
  message_content = message.content.lower()  

  
  if message.content.startswith(f'!hello'):
    await message.channel.send(hello_message)

  if message.content.startswith(f'!seekhelp'):
    await message.channel.send(help_message)

  if f'!seektribe' in message_content:
    key_words, search_words = lv_api.key_words_search_words(message_content)
    result = lv_api.search_tribe(key_words) 
    if len(result) > 1:
      output = prettify_tribe(result)
      await message.channel.send(output)
    else:
      await message.channel.send(no_result_message)

  if f'!seekplayer' in message_content:
    key_words, search_words = lv_api.key_words_search_words(message_content)
    result = lv_api.search_player(key_words) 
    if len(result) > 1:
      output = prettify_player(result)
      await message.channel.send(output)
    else:
      await message.channel.send(no_result_message)

if __name__ == "__main__":
  client.run(TOKEN)

