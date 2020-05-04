import csv
import re
from bs4 import BeautifulSoup as bs
import requests
from typing import List
from .models import CsPlayer, CsPlayerInfo, CsPlayerStats


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

    def parse_player(self, url: str) -> tuple:
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')

        player_stats = self._parse_player_stats(soup)
        player_info = self._parse_player_info(soup)
        return (player_info, player_stats)

    def parse_all_csgo_players(self) -> List[tuple]:
        url_list = self.get_urls()
        players_list = []
        for index, item in enumerate(url_list[:20]):
            print(f'Парсим {index} из {len(url_list)} - {item}')
            player = self.parse_player(item)
            players_list.append(player)
        return players_list

    def _parse_player_stats(self, soup) -> CsPlayerStats:
        stats = CsPlayerStats()
        stats.total_kills = self._parse_total_kills(soup)
        stats.headshots_percent = self._parse_headshot_percent(soup)
        stats.total_deaths = self._parse_total_deaths(soup)
        stats.rounds_played = self._parse_rounds_played(soup)
        stats.damage_per_round = self._parse_damage_per_round(soup)
        stats.grenade_damage_per_round = self._parse_grenade_damage_per_round(soup)
        stats.assists_per_round = self._parse_assists_per_round(soup)
        stats.rating = self._parse_rating(soup)

        return stats

    def _parse_total_kills(self, soup) -> int:
        try:
            total_kills = soup.find('span', text=re.compile('^total kills$', re.IGNORECASE)).find_next('span').text
            return int(total_kills.strip())
        except AttributeError:
            return None

    def _parse_headshot_percent(self, soup) -> float:
        try:
            headshot_percent = soup.find('span', text=re.compile('^Headshot %$', re.IGNORECASE)).find_next('span').text
            return float(headshot_percent.strip('%'))
        except AttributeError:
            return None

    def _parse_total_deaths(self, soup) -> int:
        try:
            total_deaths = soup.find('span', text=re.compile('^total deaths$', re.IGNORECASE)).find_next('span').text
            return int(total_deaths.strip())
        except AttributeError:
            return None

    def _parse_rounds_played(self, soup) -> int:
        try:
            rounds_played = soup.find('span', text=re.compile('^rounds played$', re.IGNORECASE)).find_next('span').text
            return int(rounds_played.strip())
        except AttributeError:
            return None

    def _parse_damage_per_round(self, soup) -> float:
        try:
            damage_per_round = soup.find('span', text=re.compile('^damage / round$', re.IGNORECASE)).find_next('span').text
            return float(damage_per_round.strip())
        except AttributeError:
            return None

    def _parse_grenade_damage_per_round(self, soup) -> float:
        try:
            grenade_damage_per_round = soup.find('span', text=re.compile('^grenade dmg / round$', re.IGNORECASE)).find_next('span').text
            return float(grenade_damage_per_round.strip())
        except AttributeError:
            return None

    def _parse_assists_per_round(self, soup) -> float:
        try:
            assists_per_round = soup.find('span', text=re.compile('^assists / round$', re.IGNORECASE)).find_next('span').text
            return float(assists_per_round.strip())
        except AttributeError:
            return None

    def _parse_rating(self, soup) -> float:
        try:
            rating = soup.find('span', text=re.compile('^Rating 2.0$', re.IGNORECASE)).find_next('span').text
            return float(rating.strip())
        except AttributeError:
            try:
                rating = soup.find('span', text=re.compile('^Rating 1.0$', re.IGNORECASE)).find_next('span').text
                return float(rating.strip())
            except AttributeError:
                return None

    def _parse_player_info(self, soup) -> CsPlayerInfo:
        info = CsPlayerInfo()
        info.nickname = self._parse_nickname(soup)
        info.age = self._parse_age(soup)
        info.hltv_photo = self._parse_hltv_photo(soup)
        info.hltv_crop_photo = self._parse_hltv_crop_photo(soup)

        return info

    def _parse_nickname(self, soup) -> str:
        try:
            nickname = soup.find('h1', class_='summaryNickname').text
            return nickname.strip()
        except AttributeError:
            return None

    def _parse_age(self, soup) -> int:
        try:
            age = soup.find('div', class_='summaryPlayerAge').text
            return int(age.split()[0])
        except AttributeError:
            return None

    def _parse_hltv_photo(self, soup) -> str:
        try:
            hltv_photo = soup.find('img', class_='summaryBodyshot')['src']
            return hltv_photo
        except AttributeError:
            return None
        except TypeError:
            try:
                hltv_photo = soup.find('img', class_='summarySquare')['src']
                return hltv_photo
            except AttributeError:
                return None

    def _parse_hltv_crop_photo(self, soup) -> str:
        try:
            hltv_crop_photo = soup.find('img', class_='context-item-image')['src']
            return hltv_crop_photo
        except AttributeError:
            return None


if __name__ == "__main__":
    test = HltvParser()
    # urls = test.get_urls()
    print(test.parse_all_csgo_players())
