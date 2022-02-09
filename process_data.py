from tabulate import tabulate
import search_lv_api
import db_handle
from numerize import numerize

tabulate.WIDE_CHARS_MODE = False

# instantiate LostVault class from search_lv_api.py
vault = search_lv_api.LostVault()
# nstantiate Database Handler
db = db_handle.DBHandler()


def get_tribes_dict():
    df_tribes = db.query_tribes_list()
    tribes_keys = df_tribes.set_index('index').T.to_dict('list')
    res_dict = {}
    for key, value in tribes_keys.items():
        res_key = value[0].lower()
        res_dict[res_key] = key
    return res_dict


TRIBE_NAME_ID = get_tribes_dict()
TRIBE_ORDER = ['tribe', 'lvl', 'rank', 'members', 'reactor', 'fame', 'power']
PLAYER_ORDER = [
    'name','tribe','class','lvl','rank',
    'str','agi','end','int','lck','','fame','power',
    'quests','explores','monsters','caravan','vault','survival'
    ]

# Assign bot messages
class BotMessages:
    def __init__(self):
        # Set the language of the bot below
        # String value must match Language row in the messages file
        self.txt_file = 'messages.txt'
        self.default = 'en'
        self.language = {
            'en': 'English',
            'ru': 'Russian'
        }
        self.messages = self.get_message_list()
        
    def get_all_msg(self, source_txt):
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

    def get_message_list(self, user_lang='en'):
        """Finds messages in a given language

        Args:
            source_txt (string): name of a file to read messages from
            language (string): what language to look for

        Returns:
            list: messages in particular language
        """
        all_messages = self.get_all_msg(self.txt_file)
        different_messages = int(all_messages[0][0])
        lang_index = all_messages.index(self.language[user_lang.lower()]) + 1
        messages = all_messages[lang_index:(lang_index + different_messages)]
        return messages

    def hello_message(self):
        """Sends greeting message"""
        return self.messages[0]

    def no_result_message(self):
        """Tells that fetch query found nothing"""
        return self.messages[1]

    def help_message(self):
        """Displays help message"""
        return self.messages[2]


# nstantiate BotMessages class
msg = BotMessages()

def update_db():
    df = db.df_from_dict()
    db.df_to_sql(df)
    return

def get_tribe_id(tribe_name):
    dict_name = tribe_name.lower()
    if dict_name in TRIBE_NAME_ID:
        return TRIBE_NAME_ID[dict_name]
    else:
        return tribe_name

def prettify_tribe(data):
    """Generates formatted table from the tribe stats using tabulate module

    Args:
        data (dict): tribe information

    Returns:
        string: table with tribe information
    """
    line_1 = f"```\nTRIBE: {data.get('tribe')}\n"
    stat_table = []
    for value in range(1,4):
        label_1 = TRIBE_ORDER[value]
        label_2 = TRIBE_ORDER[value+3]
        stat_table.append(
            (label_1.upper(),data.get(label_1),'|',
             label_2.upper(),data.get(label_2))
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
        f"```\nNAME: {data.get('name')}\n"
        f"CLASS: {data.get('class')}\n"
        f"TRIBE: {data.get('tribe')}\n"
        )
    stat_table = []
    for value in range(3,11):
        label_1 = PLAYER_ORDER[value]
        label_2 = PLAYER_ORDER[value+8]
        stat_table.append(
            (label_1.upper(), data.get(label_1), '|', 
             label_2.upper(), data.get(label_2))
            )
    table = tabulate(stat_table)
    result = line_1 + table + '\n```'
    return result

def prettify_compare(obj_type, data_1, data_2):
    if obj_type == 'players':
        order = PLAYER_ORDER
    else: order = TRIBE_ORDER
    stat_table = []
    for row in order:
        # we need a special multiplier for the correct Rank comparsion
        # (lower - the better):
        # -1 for Rank, 1 for everything else
        if row == 'rank':
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

def draw_swords (lenght):
    insert = ' ' if lenght % 2 else ''
    sword_len = int((lenght - len(insert))/2)
    blade_len = int(round((sword_len - 3)*2/3))
    hilt_len = sword_len-blade_len-3
    swords = (
        '+' + '-'*hilt_len + '}' + '='*blade_len + '>' + insert +
        '<' + '='*blade_len + '{' + '-'*hilt_len + '+'
        )
    return swords

def prettify_vs(opponents):
    opp_list = opponents.values.tolist()
    for row in opp_list:
        row[:] = [
            numerize.numerize(val) 
            if (type(val) == int) 
            else val 
            for val in row
            ]
    headers_list = ['RANK', 'TRIBE', 'FAME', 'POWER']
    table = tabulate(
        opp_list, headers=headers_list, 
        colalign=['left','left','left','left'], 
        disable_numparse=False)
    res_list = table.split('\n')
    table_len = len(max(res_list, key=len))
    swords = draw_swords(table_len)
    res_list.insert(3, swords)
    res_string = '\n'.join(res_list)
    result = f"\n```\n{res_string}\n```\n"
    return result

def tribe_info(name):
    """Returns tribe information or no result message

    Args:
        name (string): tribe name obtained from the user command
    Returns:
        string: info table or no result message
    """
    id = get_tribe_id(name)
    result = vault.get_tribe(id)
    output = (prettify_tribe(result) if result else msg.no_result_message())
    return output

def player_info(name):
    """Returns player information or no result message

    Args:
        name (string): player name obtained from the user command
    Returns:
        string: info table or no result message
    """
    result = vault.get_player(name)
    output = (prettify_player(result) if result else msg.no_result_message())
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
        id_1 = get_tribe_id(obj_1)
        id_2 = get_tribe_id(obj_2)
        compare_1 = vault.get_tribe(id_1)
        compare_2 = vault.get_tribe(id_2)
    if not(compare_1 and compare_2):
        return msg.no_result_message()
    # make comparison list
    # prettify output
    result = prettify_compare(obj_type, compare_1, compare_2)
    # return output
    return result

def compare_slash(obj_type, obj_1, obj_2):
    if obj_type == 'players':
        compare_1 = vault.get_player(obj_1)
        compare_2 = vault.get_player(obj_2)
    else:
        id_1 = get_tribe_id(obj_1)
        id_2 = get_tribe_id(obj_2)
        compare_1 = vault.get_tribe(id_1)
        compare_2 = vault.get_tribe(id_2)
    if not(compare_1 and compare_2):
        return msg.no_result_message()
    # make comparison list
    # prettify output
    result = prettify_compare(obj_type, compare_1, compare_2)
    # return output
    return result

def get_vs(tribe):
    id = get_tribe_id(tribe)
    tribe_vs = vault.get_search_query(id)
    opponents = db.get_vs(tribe_vs)
    output = (
        prettify_vs(opponents) 
        if not(opponents.empty) 
        else msg.no_result_message()
        )
    return output