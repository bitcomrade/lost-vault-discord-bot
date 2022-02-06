from tabulate import tabulate
import search_lv_api


# Set the language of the bot below
# String value must match Language row in the messages file
LANG = 'English'
REPLIES_FILE = 'messages.txt'
TRIBE_ORDER = ['TRIBE', 'LVL', 'Rank', 'MEMBERS', 'REACTOR', 'Fame', 'Power']
PLAYER_ORDER = [
    'NAME','TRIBE','CLASS','LVL','Rank',
    'STR','AGI','END','INT','LCK','','Fame','Power',
    'Quests','Explores','Monsters','Caravan','Vault','Survival'
    ]


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
            msg_list.append(line.rstrip().replace('$$', '\n'))
    return msg_list

def get_message_list(language):
    """Finds messages in a given language

    Args:
        source_txt (string): name of a file to read messages from
        language (string): what language to look for

    Returns:
        list: messages in particular language
    """    
    all_messages = get_all_msg(REPLIES_FILE)
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
  
messages = get_message_list(LANG)
 

def prettify_tribe(data):
    """Generates formatted table from the tribe stats using tabulate module

    Args:
        data (dict): tribe information

    Returns:
        string: table with tribe information
    """    
    line_1 = f"```\nTRIBE: {data.get('TRIBE')}\n"
    stat_table = []
    for value in range(1,4):
        label_1 = TRIBE_ORDER[value]
        label_2 = TRIBE_ORDER[value+3]
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
    line_1 = (
        f"```\nNAME: {data.get('NAME')}\n"
        f"CLASS: {data.get('CLASS')}\n"
        f"TRIBE: {data.get('TRIBE')}\n"
        )
    stat_table = []
    for value in range(3,11):
        label_1 = PLAYER_ORDER[value]
        label_2 = PLAYER_ORDER[value+8]
        stat_table.append(
            (label_1, data.get(label_1), '|', label_2, data.get(label_2))
            )
    table = tabulate(stat_table)
    result = line_1 + table + '\n```'
    return result

def prettify_vs(obj_type, data_1, data_2):
    if obj_type == 'players':
        order = PLAYER_ORDER
    else: order = TRIBE_ORDER
    stat_table = []
    for row in order:
        # we need a special multiplier for the correct Rank comparsion
        # (lower - the better):
        # -1 for Rank, 1 for everything else
        if row == 'Rank':
            multi = -1
        else: 
            multi = 1
        value_1 = data_1.get(row)
        value_2 = data_2.get(row)
        str_1 = '| |'
        str_2 = '| |'
        if type(value_1) == int:
            if multi*value_1 > multi*value_2:
                str_1 = '|+|'
            elif multi*value_1 < multi*value_2:
                str_2 = '|+|'
        stat_table.append((value_1,str_1,row.upper(),str_2,value_2))
    table = tabulate(
        stat_table, colalign=('right','center','center','center','left')
        )
    result = f"\n```\n{table}\n```\n"    
    return result

def tribe_info(name):
    """Returns tribe information or no result message

    Args:
        name (string): tribe name obtained from the user command
    Returns:
        string: info table or no result message
    """  
    result = vault.get_tribe(name)
    output = (prettify_tribe(result) if result else no_result_message())
    return output
        
def player_info(name):
    """Returns player information or no result message

    Args:
        name (string): player name obtained from the user command
    Returns:
        string: info table or no result message
    """  
    result = vault.get_player(name)
    output = (prettify_player(result) if result else no_result_message())
    return output

def compare(obj_type, objects):
    # find out tribe or player
    # get obj_1 info
    # get obj_2 info
    obj_1, obj_2 = objects.split(' && ')
    if obj_type == 'players':
        compare_1 = vault.get_player(obj_1)
        compare_2 = vault.get_player(obj_2)
    else:
        compare_1 = vault.get_tribe(obj_1)
        compare_2 = vault.get_tribe(obj_2)
    if not(compare_1 and compare_2):
        return no_result_message()
    # make comparison list
    # prettify output
    result = prettify_vs(obj_type, compare_1, compare_2)
    # return output
    return result


def get_tribes(source_txt):
    # return tribes list
    pass

def top_tribes(positions):
    # return list of a top {AMOUNT} tribes
    pass


