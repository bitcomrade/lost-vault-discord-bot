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
        self.api_url = 'https://api.lost-vault.com/'
 
    def get_search_query(self, user_message):
        """modifies user input to match api format; 
        replaces spaces in names to dash
        """
        # words = user_message.split()[1:]
        # found_query = '-'.join(words)
        search_query = user_message.strip().lower().replace(' ', '-')
        return search_query

    def fetch_request(self, name, query_kind):
        """Sends request to API, checks that url is valid 
        and returns a bs4 soup

        Args:
            name (string): user's search query
            query_kind (string): to distinguish  between guild and player URL
        """        
        search_query = self.get_search_query(name)
        query_url = f"{self.api_url}{query_kind}/{search_query}/"
        response = requests.get(query_url, headers = self.headers)
        if response.status_code == 404:
            return None
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        return soup
    
    def fill_header(self, data_soup):
        """
        Fill the beginning of the search result. Separate function because 
        names use different tag from the rest of the parameters
        """        
        headers = data_soup.find("h1").get_text().splitlines()
        header_list = [
            header.strip('[ ]') for header in headers if header.strip()
            ]
        case = len(header_list)
        if case == 1: # this is a tribe
            return {'TRIBE': header_list[0]}
        if case == 2: # this is a player without a tribe
            header_list.insert(0, 'None')
        result = {
            'TRIBE':header_list[0], 
            'NAME': header_list[1], 
            'CLASS': header_list[2]
            }
        return result              
    
    def fill_info(self, info_draft, info_source):
        """Fills the rest of the information

        Args:
            info_draft: [dictionary with the header filled in]
            info_source: [bs4 soup with data]

        Returns:
            [dict]: [filled search result with all information]
        """        
        # Get information
        labels, values = parse_info(info_source)
        labels_list = [get_label(label) for label in labels]
        values_list = [get_value(value) for value in values]
        # Fill entry in dictionary
        for label in labels_list:
            info_draft.update({label:values_list[labels_list.index(label)]})
        return info_draft

        
    def get_tribe(self, keywords):
        """Retrieves tribe info from the Lost Vault API

        Args:
            keywords (string): tribe name as it written in Lost Vault database

        Returns:
            dict: dictionary, containing information about tribe
        """    
        tribe_soup = self.fetch_request(keywords, 'guilds')
        if(not(tribe_soup)):
            return tribe_soup
        # Get name
        tribe_result = self.fill_header(tribe_soup)
        # Fill tribe information
        result = self.fill_info(tribe_result, tribe_soup)
        return result
      
    def get_player(self, keywords):
        """Retrieves player info from the Lost Vault API

        Args:
            keywords (string): player name as in Lost Vault database

        Returns:
            dict: dictionary, containing information about player
        """  
        player_soup = self.fetch_request(keywords, 'players')
        if(not(player_soup)):
            return player_soup
        # Get name, class and a tribe of the player
        player_result = self.fill_header(player_soup)
        # Get player information
        result = self.fill_info(player_result, player_soup)
        return result
    