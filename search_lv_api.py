import requests
from bs4 import BeautifulSoup

class LostVault:
  def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3'}
        self.tribe_url = 'https://api.lost-vault.com/guilds/'
        self.player_url = 'https://api.lost-vault.com/players/'

  def key_words_search_words(self, user_message):
    words = user_message.split()[1:]
    keywords = '-'.join(words)
    search_words = ' '.join(words)
    return keywords, search_words

  def search_tribe(self, keywords):
    response = requests.get(self.tribe_url+keywords, headers = self.headers)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    # Get name
    tribe_name = soup.find("h1").get_text().strip()
    tribe_result = {"TRIBE": tribe_name}
    values = soup.findAll("div", {"class":"value"})
    labels = soup.findAll("div", {"class":"label"})
    labels_list = [label.text.strip() for label in labels]
    values_list = [value.text.strip() for value in values]
    for label in labels_list:
      tribe_result.update({label:values_list[labels_list.index(label)]})
    return tribe_result
    
  def search_player(self, keywords):
    header_list= []
    response = requests.get(self.player_url+keywords, headers = self.headers)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    player_header = soup.find("h1").get_text().splitlines()
    for header in player_header:
      if header.strip():
        header_list.append(header.strip())
    player_result = {'TRIBE':header_list[0], 'NAME': header_list[1], 'CLASS': header_list[2]}
    values = soup.findAll("div", {"class":"value"})
    labels = soup.findAll("div", {"class":"label"})
    labels_list = [label.text.strip() for label in labels]
    values_list = [value.text.strip() for value in values]
    for label in labels_list:
      player_result.update({label:values_list[labels_list.index(label)]})
    return player_result
