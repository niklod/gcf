import csv
from bs4 import BeautifulSoup as bs
import requests
from typing import List
from models import CsPlayer, CsPlayerInfo


class HltvParser:
    def __init__(self):
        self.players_url = 'https://www.hltv.org/stats/players'

    def get_urls(self) -> List[str]:
        result = []
        r = requests.get(self.players_url)

        soup = bs(r.text, 'html.parser')
        players = soup.find_all('td', class_='playerCol')

        for player in players:
            result.append(f"https://www.hltv.org{player.a['href']}")

        return result

    def parse_all_csgo_players_into_csv(self, url_list):
        with open('csgo_players_info.csv', 'w', encoding='utf-8') as f:
            writer = csv.writer(f)

            for index, item in enumerate(url_list):
                print(f'Парсим {index} из {len(url_list)} - {item}')
                player = self.parse_player(item)
                writer.writerow(player.view_as_list())

    def parse_player_stat(self, url: str) -> CsPlayer:
        r = requests.get(url)
        player_info = CsPlayerInfo()
        soup = bs(r.text, 'html.parser')

        return player_info


if __name__ == "__main__":
    test = HltvParser()
    urls = test.get_urls()
    test.parse_all_csgo_players_into_csv(urls)
