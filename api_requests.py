import os
import random
from typing import Dict

import requests

# for testing purposes when hosting on my PC
# Remove dotenv when deploy
# from dotenv import load_dotenv

# load_dotenv()


class LostVault:
    def __init__(self) -> None:
        self.api_key = os.getenv("API-KEY")
        self.headers = {"Authorization": f"Api-Key {self.api_key}"}
        self.api_url = "https://api.lost-vault.com/dev/"

    def get_search_query(self, user_message: str) -> str:
        """modifies user input to match api format;
        replaces spaces in names to dash
        """
        search_query = user_message.strip().lower().replace(" ", "-")
        return search_query

    def fetch_request(self, name: str, query_kind: str) -> Dict[str, object]:
        """Sends request to API, checks that url is valid
        and returns a json

        Args:
            name (string): user's search query
            query_kind (string): to distinguish  between guild and player URL
        """
        search_query = self.get_search_query(name)
        tail = random.randint(1, 100)
        query_url = f"{self.api_url}{query_kind}/{search_query}/?{tail}"
        response = requests.get(query_url, headers=self.headers)
        if response.status_code == 404:
            return {}
        result = response.json()
        return result
