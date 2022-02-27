import datetime
from typing import Any, Dict, List

import pandas as pd
from numerize import numerize
from tabulate import tabulate

import api_requests
import db_handle

# instantiate LostVault class from api_requests.py
vault = api_requests.LostVault()
# nstantiate Database Handler
db = db_handle.DBHandler()


def get_tribes_dict() -> Dict[str, str]:
    df_tribes = db.query_tribes_list()
    tribes_keys = df_tribes.set_index("index").T.to_dict("list")
    res_dict = {}
    for key, value in tribes_keys.items():
        res_key = value[0].lower()
        res_dict[res_key] = key
    return res_dict


TRIBE_NAME_ID = get_tribes_dict()
TRIBE_ORDER = [
    "tribe",
    "lvl",
    "rank",
    "power",
    "fame",
    "members",
    "reactor",
    "xp",
    "gold",
]
TRIBE_JSON_MAP = {
    "tribe": "name",
    "lvl": "level",
    "rank": "rank",
    "members": "members",
    "reactor": "reactor_level",
    "fame": "points",
    "power": "power",
    "xp": "bonus_xp",
    "gold": "bonus_gold",
}
PLAYER_ORDER = [
    "name",
    "tribe",
    "class",
    "lvl",
    "rank",
    "str",
    "agi",
    "end",
    "int",
    "lck",
    "",
    "fame",
    "power",
    "quests",
    "explores",
    "monsters",
    "caravan",
    "vault",
    "survival",
]
PLAYER_JSON_MAP = {
    "name": "name",
    "tribe": "guild_name",
    "class": "profession",
    "lvl": "level",
    "rank": "rank",
    "str": "stats.strength",
    "agi": "stats.agility",
    "end": "stats.endurance",
    "int": "stats.intelligence",
    "lck": "stats.luck",
    # "": None,
    "fame": "points",
    "power": "stats.power",
    "quests": "achievements.finish_quests",
    "explores": "achievements.explore_wastelands",
    "monsters": "achievements.kill_monsters",
    "caravan": "achievements.protect_caravan",
    "vault": "achievements.explore_vaults",
    "survival": "survival_level",
}


# Assign bot messages
class BotMessages:
    def __init__(self) -> None:
        # Set the language of the bot below
        # str value must match Language row in the messages file
        self.txt_file = "messages.txt"
        self.default = "ru"
        self.language = {"en": "English", "ru": "Russian"}
        self.messages = self.get_message_list()

    def get_all_msg(self, source_txt: str) -> List[str]:
        """Reads txt file where bot messages are located

        Args:
            source_txt (str): name of a file to read from

        Returns:
            list: contents of a file separated by line breaks
        """
        msg_list = []
        with open(source_txt, encoding="utf-8") as file:
            while line := file.readline():
                msg_list.append(line.rstrip().replace("$$", "\n"))
        return msg_list

    def get_message_list(self, user_lang: str = "ru") -> List[str]:
        """Finds messages in a given language

        Args:
            source_txt (str): name of a file to read messages from
            language (str): what language to look for

        Returns:
            list: messages in particular language
        """
        all_messages = self.get_all_msg(self.txt_file)
        first_line_words = all_messages[0].split()
        different_messages = int(first_line_words[0])
        lang_index = all_messages.index(self.language[user_lang.lower()]) + 1
        messages = all_messages[lang_index : (lang_index + different_messages)]
        return messages

    def hello_message(self) -> str:
        """Sends greeting message"""
        return self.messages[0]

    def no_result_message(self) -> str:
        """Tells that fetch query found nothing"""
        return self.messages[1]

    def help_message(self) -> str:
        """Displays help message"""
        return self.messages[2]

    def db_info_message(self) -> str:
        return self.messages[3]

    def timer_start_msg(self) -> str:
        return self.messages[4]

    def timer_advance_msg(self) -> str:
        return self.messages[5]

    def timer_attack_msg(self) -> str:
        return self.messages[6]

    def timer_new_msg(self) -> str:
        return self.messages[7]

    def time_left_msg(self) -> str:
        return self.messages[8]


# nstantiate BotMessages class
msg = BotMessages()


def update_db() -> None:
    df = db.df_from_dict()
    db.df_to_sql(df)
    return


def get_db_status() -> str:
    total = len(TRIBE_NAME_ID)
    find_time = db.query_time()[0][1]
    print(find_time)
    upd_time = datetime.datetime.strptime(str(find_time), "%Y-%m-%d %H:%M:%S")
    time_now = datetime.datetime.now()
    upd_age = round((time_now - upd_time).total_seconds() / 60)
    message = msg.db_info_message()
    return message.format(total=total, upd_age=upd_age)


def write_timer_set_time(timer_name: str, total: int) -> None:
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.time_to_sql(timer_name, time, total)
    print(f"{timer_name} -> {time}|{total} written to db")


def get_timer_set_time() -> Dict[str, int]:
    timers = db.query_time(table="timers")
    new_timers = {}
    for name, start_time_str, total in timers:
        start_time = datetime.datetime.strptime(
            start_time_str, "%Y-%m-%d %H:%M:%S"
        )
        timedelta = datetime.timedelta(seconds=+total)
        end_time = start_time + timedelta
        current = datetime.datetime.now()
        if current >= end_time:
            time_left = 0
        else:
            time_left = int((end_time - current).total_seconds())
        new_timers[name] = time_left
    return new_timers


def get_tribe_id(tribe_name: str) -> str:
    dict_name: str = tribe_name.lower()
    if dict_name in TRIBE_NAME_ID:
        tribe_id: str = TRIBE_NAME_ID[dict_name]
        return tribe_id
    else:
        return tribe_name


def prettify_tribe(data: Dict[str, str | int]) -> str:
    """Generates formatted table from the tribe stats using tabulate module

    Args:
        data (dict): tribe information

    Returns:
        str: table with tribe information
    """
    line_1 = f"```\nTRIBE: {data.get('tribe')}\n"
    stat_table = []
    for value in range(1, 5):
        label_1 = TRIBE_ORDER[value]
        label_2 = TRIBE_ORDER[value + 4]
        stat_table.append(
            (
                label_1.upper(),
                data.get(label_1),
                "|",
                label_2.upper(),
                data.get(label_2),
            )
        )
    table = tabulate(stat_table)
    result = line_1 + table + "\n```"
    return result


def prettify_player(data: Dict[str, str | int]) -> str:
    """Generates formatted player information table using tabulate module

    Args:
        data (dict): player information

    Returns:
       str: table with player information
    """
    line_1 = (
        f"```\nNAME: {data.get('name')}\n"
        f"CLASS: {data.get('class')}\n"
        f"TRIBE: {data.get('tribe')}\n"
    )
    stat_table = []
    for value in range(3, 11):
        label_1 = PLAYER_ORDER[value]
        label_2 = PLAYER_ORDER[value + 8]
        stat_table.append(
            (
                label_1.upper(),
                data.get(label_1),
                "|",
                label_2.upper(),
                data.get(label_2),
            )
        )
    table = tabulate(stat_table)
    result = line_1 + table + "\n```"
    return result


def prettify_compare(
    obj_type: str, data_1: Dict[str, int | str], data_2: Dict[str, int | str]
) -> str:
    if obj_type == "players":
        order = PLAYER_ORDER
    else:
        order = TRIBE_ORDER
    stat_table = []
    for row in order:
        # we need a special multiplier for the correct Rank comparsion
        # (lower - the better):
        # -1 for Rank, 1 for everything else
        if row == "rank":
            multi = -1
        else:
            multi = 1
        value_1: Any = data_1.get(row)
        value_2: Any = data_2.get(row)
        str_1 = "| |"
        str_2 = "| |"
        if type(value_1) == int:
            if (multi * value_1) > (multi * value_2):
                str_1 = "|+|"
            elif (multi * value_1) < (multi * value_2):
                str_2 = "|+|"
        elif type(value_1) == str:
            value_1 = value_1.replace(" ", "\n")
            value_2 = value_2.replace(" ", "\n")
        stat_table.append((value_1, str_1, row.upper(), str_2, value_2))
    table = tabulate(
        stat_table, colalign=("right", "center", "center", "center", "left")
    )
    result = f"\n```\n{table}\n```\n"
    return result


def draw_swords(lenght: int) -> str:
    insert = " " if lenght % 2 else ""
    sword_len = int((lenght - len(insert)) / 2)
    blade_len = int(round((sword_len - 3) * 2 / 3))
    hilt_len = sword_len - blade_len - 3
    swords = (
        "+"
        + "-" * hilt_len
        + "}"
        + "=" * blade_len
        + ">"
        + insert
        + "<"
        + "=" * blade_len
        + "{"
        + "-" * hilt_len
        + "+"
    )
    return swords


def prettify_vs(opponents: pd.DataFrame) -> str:
    opp_list = opponents.values.tolist()
    for row in opp_list:
        row[:] = [
            numerize.numerize(val) if (type(val) == int) else val
            for val in row
        ]
    headers_list = ["RANK", "TRIBE", "FAME", "POWER"]
    table = tabulate(
        opp_list,
        headers=headers_list,
        colalign=["left", "left", "left", "left"],
        disable_numparse=False,
    )
    res_list = table.split("\n")
    table_len = len(max(res_list, key=len))
    swords = draw_swords(table_len)
    res_list.insert(3, swords)
    res_str = "\n".join(res_list)
    result = f"\n```\n{res_str}\n```\n"
    return result


def tribe_info(name: str) -> str:
    """Returns tribe information or no result message

    Args:
        name (str): tribe name obtained from the user command
    Returns:
        str: info table or no result message
    """
    id = get_tribe_id(name)
    full_result = vault.fetch_request(id, "guilds")
    result = select_from_json(full_result, TRIBE_JSON_MAP)
    output = prettify_tribe(result) if result else msg.no_result_message()
    return output


def player_info(name: str) -> str:
    """Returns player information or no result message

    Args:
        name (str): player name obtained from the user command
    Returns:
        str: info table or no result message
    """
    full_result = vault.fetch_request(name, "players")
    result = select_from_json(full_result, PLAYER_JSON_MAP)
    output = prettify_player(result) if result else msg.no_result_message()
    return output


def compare(obj_type: str, objects: str) -> str:
    # find out tribe or player
    # get obj_1 info
    # get obj_2 info
    obj_1, obj_2 = objects.split(" && ")
    if obj_type == "players":
        full_compare_1 = vault.fetch_request(obj_1, "players")
        full_compare_2 = vault.fetch_request(obj_2, "players")
        compare_1 = select_from_json(full_compare_1, PLAYER_JSON_MAP)
        compare_2 = select_from_json(full_compare_2, PLAYER_JSON_MAP)
    else:
        id_1 = get_tribe_id(obj_1)
        id_2 = get_tribe_id(obj_2)
        full_compare_1 = vault.fetch_request(id_1, "guilds")
        full_compare_2 = vault.fetch_request(id_2, "guilds")
        compare_1 = select_from_json(full_compare_1, TRIBE_JSON_MAP)
        compare_2 = select_from_json(full_compare_2, TRIBE_JSON_MAP)
    if not (compare_1 and compare_2):
        return msg.no_result_message()
    # make comparison list
    # prettify output
    result = prettify_compare(obj_type, compare_1, compare_2)
    # return output
    return result


def compare_slash(obj_type: str, obj_1: str, obj_2: str) -> str:
    if obj_type == "players":
        full_compare_1 = vault.fetch_request(obj_1, "players")
        full_compare_2 = vault.fetch_request(obj_2, "players")
        compare_1 = select_from_json(full_compare_1, PLAYER_JSON_MAP)
        compare_2 = select_from_json(full_compare_2, PLAYER_JSON_MAP)
    else:
        id_1 = get_tribe_id(obj_1)
        id_2 = get_tribe_id(obj_2)
        full_compare_1 = vault.fetch_request(id_1, "guilds")
        full_compare_2 = vault.fetch_request(id_2, "guilds")
        compare_1 = select_from_json(full_compare_1, TRIBE_JSON_MAP)
        compare_2 = select_from_json(full_compare_2, TRIBE_JSON_MAP)
    if not (compare_1 and compare_2):
        return msg.no_result_message()
    # make comparison list
    # prettify output
    result = prettify_compare(obj_type, compare_1, compare_2)
    # return output
    return result


def get_vs(tribe: str) -> str:
    id = get_tribe_id(tribe)
    tribe_vs = vault.get_search_query(id)
    opponents = db.get_vs(tribe_vs)
    output = (
        prettify_vs(opponents)
        if not (opponents.empty)
        else msg.no_result_message()
    )
    return output


def select_from_json(
    json: Dict[str, Any], map: Dict[str, str]
) -> Dict[str, str | int]:
    result: Dict[str, str | int] = {}
    json_df = pd.json_normalize(json)
    json_norm = json_df.to_dict("list")
    if not json:
        return result
    for key in map:
        if key == "members":
            value: str | int = len(json[key])
        elif key:
            value = json_norm[map[key]][0]
        result[key] = value
    return result
