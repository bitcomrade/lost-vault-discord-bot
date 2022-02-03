from tabulate import tabulate
import search_lv_api


# Set the language of the bot below
# String value must match Language row in the messages file
LANG = 'English'
REPLIES_FILE = 'messages.txt'

# instantiate LostVault class from search_lv_api.py
vault = search_lv_api.LostVault()

# Assign bot messages
def get_all_msg(source_txt):
    """Reads txt file where bot messages are located

    Args:
        source_txt (string): name of a file to read from

    Returns:
        list: contents of a file separated by line breaks
    """    
    msg_list = []
    with open(source_txt, encoding="utf-8") as file:
        while line := file.readline():
            msg_list.append(line.rstrip().replace('&&', '\n'))
    return msg_list

def get_message_list(source_txt, language):
    """Finds messages in a given language

    Args:
        source_txt (string): name of a file to read messages from
        language (string): what language to look for

    Returns:
        list: messages in particular language
    """    
    all_messages = get_all_msg(source_txt)
    different_messages = int(all_messages[0][0])
    lang_index = all_messages.index(language) + 1
    messages = all_messages[lang_index:(lang_index + different_messages)]
    return messages

def hello_message():
    """Sends greeting message"""
    return messages[0]

def no_result_message():
    """Tells that fetch query found nothing"""
    return messages[1]
    
def help_message():
    """Displays help message"""
    return messages[2]
  
messages = get_message_list(REPLIES_FILE, LANG)
 

def prettify_tribe(data):
    """Generates formatted table from the tribe stats using tabulate module

    Args:
        data (dict): tribe information

    Returns:
        string: table with tribe information
    """    
    tribe_order = [
        'TRIBE', 'LVL', 'Rank', 'MEMBERS', 
        'REACTOR', 'Fame', 'Power'
        ]
    line_1 = f"```\nTRIBE: {data.get('TRIBE')}\n"
    stat_table = []
    for value in range(1,4):
        label_1 = tribe_order[value]
        label_2 = tribe_order[value+3]
        stat_table.append(
            (label_1,data.get(label_1),'|',label_2,data.get(label_2))
            )
    table = tabulate(stat_table)
    result = line_1 + table + '\n```'
    return result

def prettify_player(data):
    """Generates formatted player information table using tabulate module

    Args:
        data (dict): player information

    Returns:
       string: table with player information
    """    
    player_order = [
        'NAME','TRIBE','CLASS','LVL','Rank',
        'STR','AGI','END','INT','LCK','','Fame','Power',
        'Quests','Explores','Monsters','Caravan','Vault','Survival'
        ]
    line_1 = (
        f"```\nNAME: {data.get('NAME')}\n"
        f"CLASS: {data.get('CLASS')}\n"
        f"TRIBE: {data.get('TRIBE')}\n"
        )
    stat_table = []
    for value in range(3,11):
        label_1 = player_order[value]
        label_2 = player_order[value+8]
        stat_table.append(
            (label_1, data.get(label_1), '|', label_2, data.get(label_2))
            )
    table = tabulate(stat_table)
    result = line_1 + table + '\n```'
    return result

def tribe_info(name):
    """Returns tribe information or no result message

    Args:
        name (string): tribe name obtained from the user command
    Returns:
        string: info table or no result message
    """  
    search_query = vault.get_search_query(name)
    result = vault.fetch_tribe(search_query)
    output = (
        prettify_tribe(result) 
        if len(result) > 1 
        else no_result_message()
        )
    return output
        
def player_info(name):
    """Returns player information or no result message

    Args:
        name (string): player name obtained from the user command
    Returns:
        string: info table or no result message
    """  
    search_query = vault.get_search_query(name)
    result = vault.fetch_player(search_query)
    output = (
        prettify_player(result) 
        if len(result) > 1 
        else no_result_message()
        )
    return output

def get_tribes(source_txt):
    # return tribes list
    pass

def top_tribes(positions):
    # return list of a top {AMOUNT} tribes
    pass


