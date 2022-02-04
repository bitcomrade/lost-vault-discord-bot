import requests
from bs4 import BeautifulSoup


def get_label(soup_label):
    """returns tribe or player parameter name"""
    return soup_label.text.strip()

def get_value(soup_value):
    """returns tribe or player parameter"""
    return int(soup_value.text.strip('\nh ').replace(',',''))

def parse_info(search_soup):
    """finds all parameter and parametter names in api html-code"""
    labels = search_soup.findAll("div", {"class":"label"})
    values = search_soup.findAll("div", {"class":"value"})
    return labels, values
  

class LostVault:
    def __init__(self):
        self.headers = {
          'User-Agent':
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/88.0.4324.150 Safari/537.3'
             )
            }
        self.tribe_url = 'https://api.lost-vault.com/guilds/'
        self.player_url = 'https://api.lost-vault.com/players/'
 
    def get_search_query(self, user_message):
        """modifies user input to match api format; 
        replaces spaces in names to dash
        """
        # words = user_message.split()[1:]
        # found_query = '-'.join(words)
        search_query = user_message.strip().lower().replace(' ', '-')
        return search_query

    def fetch_tribe(self, keywords):
        """Retrieves tribe info from the Lost Vault API

        Args:
            keywords (string): tribe name as it written in Lost Vault database

        Returns:
            dict: dictionary, containing information about tribe
        """    
        response = requests.get(
            self.tribe_url+keywords, 
            headers = self.headers
            )
        if response.status_code == 404:
            return []
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        # Get name
        tribe_name = soup.find("h1").get_text().strip()
        tribe_result = {"TRIBE": tribe_name}
        # Get tribe information
        labels, values = parse_info(soup)
        labels_list = [get_label(label) for label in labels]
        values_list = [get_value(value) for value in values]
        # Fill tribe entry in dictionary
        for label in labels_list:
            tribe_result.update({label:values_list[labels_list.index(label)]})
        return tribe_result
      
    def fetch_player(self, keywords):
        """Retrieves player info from the Lost Vault API

        Args:
            keywords (string): player name as in Lost Vault database

        Returns:
            dict: dictionary, containing information about player
        """  
        header_list= []
        response = requests.get(
            self.player_url+keywords, 
            headers = self.headers
            )
        if response.status_code == 404:
            return []
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        # Get name, class and a tribe of the player
        player_header = soup.find("h1").get_text().splitlines()
        for header in player_header:
            if header.strip():
              header_list.append(header.strip('[ ]'))
        if len(header_list)<3:
            header_list.insert(0, 'None')
        player_result = {
            'TRIBE':header_list[0], 
            'NAME': header_list[1], 
            'CLASS': header_list[2]
            }
        # Get player information
        labels, values = parse_info(soup)
        labels_list = [get_label(label) for label in labels]
        values_list = [get_value(value) for value in values]
        # Fill player information in the dictionary
        for label in labels_list:
            player_result.update(
                {label:values_list[labels_list.index(label)]}
                )
        return player_result
    