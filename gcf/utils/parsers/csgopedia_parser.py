import csv
import re
from bs4 import BeautifulSoup as bs
import requests
from typing import List
from .models import CsPlayer, CsPlayerInfo, CsStartupConfig


class CsgoPediaParser:
    def __init__(self):
        self.players_url = 'https://csgopedia.com/ru/csgo-pro-setups/'

    def get_urls(self) -> List[str]:
        result = []
        r = requests.get(self.players_url)
        soup = bs(r.text, 'html.parser')
        next_page = True

        while next_page:
            try:
                next_page = soup.find('div', class_='pagination').find_all('a')[3]['href']
                next_page = f'https://csgopedia.com{next_page}'
            except KeyError:
                next_page = None

            players = soup.find_all('div', class_='username')

            for player in players:
                result.append(f"https://csgopedia.com{player.a['href']}")

            if next_page:
                r = requests.get(next_page)
                soup = bs(r.text, 'html.parser')

                print(r.url + f' {r.status_code}')

        return result

    def parse_all_csgo_players_into_csv(self, url_list):
        with open('csgo_players_info.csv', 'w', encoding='utf-8') as f:
            writer = csv.writer(f)

            for index, item in enumerate(url_list):
                print(f'Парсим {index} из {len(url_list)} - {item}')
                player = self.parse_player(item)
                writer.writerow(player.view_as_list())

    def parse_player(self, url: str) -> CsPlayer:
        r = requests.get(url)
        player_info = CsPlayerInfo()
        player_startup = CsStartupConfig()
        soup = bs(r.text, 'html.parser')
        player_info.nickname = self._parse_nickname(soup)
        player_info.firstname, player_info.lastname = self._parse_name(soup)
        player_info.age = self._parse_age(soup)
        player_info.city = self._parse_city(soup)
        player_startup.startup = self._parse_startup(soup)

        return (player_info, player_startup)

    def parse_all_csgo_players(self) -> List[CsPlayer]:
        url_list = self.get_urls()
        players_list = []
        for index, item in enumerate(url_list):
            print(f'Парсим {index} из {len(url_list)} - {item}')
            player = self.parse_player(item)
            players_list.append(player)
        return players_list

    def _parse_nickname(self, soup) -> str:
        try:
            player_nickname = soup.find('h1').find_all('strong')[1].text
            return player_nickname.strip()
        except AttributeError:
            raise

    def _parse_name(self, soup) -> str:
        try:
            firstname = soup.find('h1').find_all('strong')[0].text
            lastname = soup.find('h1').find_all('strong')[2].text
            return firstname.strip(), lastname.strip()
        except AttributeError:
            raise

    def _parse_age(self, soup) -> int:
        try:
            age = soup.find('h1').next_sibling.strong.text.strip()
            return int(age)
        except AttributeError:
            raise

    def _parse_city(self, soup) -> str:
        try:
            city = soup.find('h1').next_sibling.li.text
            return city.strip()
        except AttributeError:
            raise

    def _parse_startup(self, soup) -> str:
        try:
            startup = soup.find('a', text=re.compile('^скопировать настройки запуска', re.IGNORECASE)) \
                .find_previous('div', class_='console console-dark').text
            return startup.strip()
        except AttributeError:
            raise


if __name__ == "__main__":
    test = CsgoPediaParser()
    # urls = test.get_urls()
    # test.parse_all_csgo_players_into_csv(urls)
    print(test.parse_all_csgo_player())
