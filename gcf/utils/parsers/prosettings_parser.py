import re
import csv
from bs4 import BeautifulSoup as bs
import requests
from typing import List
from .models import CsPlayer, CsPlayerInfo, CsCrosshairConfig, CsMouseConfig, CsVideoConfig, CsViewModelConfig


class CsProSettingsParser:
    def __init__(self):
        self.url = 'https://prosettings.net/counterstrike/'

    def get_urls(self) -> List[str]:
        result = []
        i = 1
        url = f'{self.url}page/{i}/'
        r = requests.get(url)

        while r.status_code == 200:
            soup = bs(r.text, 'html.parser')
            players = soup.find_all('h2', class_='entry-title')

            for player in players:
                result.append(player.a['href'])
            i += 1
            url_with_page = f'{self.url}page/{i}/'

            r = requests.get(url_with_page)
            print(r.url + f' {r.status_code}')

        return result

    def parse_player(self, url: str) -> CsPlayer:
        r = requests.get(url)
        player = CsPlayer()
        soup = bs(r.text, 'html.parser')
        player.player_info = self._parse_player_info(soup)
        player.video_config = self._parse_video_config(soup)
        player.mouse_config = self._parse_mouse_config(soup)
        player.crosshair_config = self._parse_crosshair_config(soup)
        player.viewmodel_config = self._parse_viewmodel_config(soup)
        return player

    def _parse_player_info(self, soup) -> CsPlayerInfo:
        player_info = CsPlayerInfo()
        player_info.nickname = self._parse_nickname(soup)
        player_info.social_links = self._parse_social_links(soup)
        return player_info

    def parse_all_csgo_players_into_csv(self, url_list):
        with open('csgo_players.csv', 'w', encoding='utf-8') as f:
            writer = csv.writer(f)

            for index, item in enumerate(url_list):
                print(f'Парсим {index} из {len(url_list)} - {item}')
                player = self.parse_player(item)
                writer.writerow(player.view_as_list())

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
            player_nickname = soup.find('h1', class_='entry-title').text
            return player_nickname.strip()
        except AttributeError:
            raise

    def _parse_social_links(self, soup) -> dict:
        social_links = {}
        try:
            twitch_link = soup.find('i', class_='x-icon-twitch').parent['href']
            social_links['twitch'] = twitch_link
        except AttributeError:
            social_links['twitch'] = None

        try:
            steam_link = soup.find('i', class_='x-icon-steam').parent['href']
            social_links['steam'] = steam_link
        except AttributeError:
            social_links['steam'] = None

        return social_links

    def _parse_mouse_config(self, soup) -> CsMouseConfig:
        mouse_config = CsMouseConfig()
        mouse_config.dpi = self._parse_mouse_dpi(soup)
        mouse_config.sens = self._parse_mouse_sens(soup)
        mouse_config.edpi = self._parse_mouse_edpi(soup)
        mouse_config.mouse_hz = self._parse_mouse_hz(soup)
        mouse_config.zoom_sens = self._parse_mouse_zoom_sens(soup)
        mouse_config.mouse_acc = self._parse_mouse_accel(soup)
        mouse_config.win_sens = self._parse_mouse_win_sens(soup)
        mouse_config.raw_input = self._parse_mouse_raw_input(soup)
        return mouse_config

    def _parse_mouse_dpi(self, soup) -> int:
        try:
            result = int(soup.find('h3', text=re.compile('^dpi$', re.IGNORECASE)).find_next('p', class_='man').text)
            return result
        except KeyError:
            raise
        except ValueError:
            return None

    def _parse_mouse_sens(self, soup) -> float:
        try:
            result = float(soup.find('h4', text=re.compile('^sensitivity$', re.IGNORECASE)).find_next('p', class_='man').text)
            return result
        except KeyError:
            raise
        except ValueError:
            return None

    def _parse_mouse_edpi(self, soup) -> int:
        try:
            result = int(soup.find('h4', text=re.compile('^edpi$', re.IGNORECASE)).find_next('p', class_='man').text.replace('.', ''))
            return result
        except KeyError:
            raise
        except ValueError:
            return None

    def _parse_mouse_hz(self, soup) -> int:
        try:
            result = int(soup.find('h4', text=re.compile('^hz$', re.IGNORECASE)).find_next('p', class_='man').text)
            return result
        except KeyError:
            raise
        except ValueError:
            return None

    def _parse_mouse_zoom_sens(self, soup) -> float:
        try:
            result = float(soup.find('h4', text=re.compile('^zoom sensitivity$', re.IGNORECASE)).find_next('p', class_='man').text)
            return result
        except KeyError:
            raise
        except ValueError:
            return None

    def _parse_mouse_accel(self, soup) -> float:
        try:
            result = float(soup.find('h4', text=re.compile('^mouse accel', re.IGNORECASE)).find_next('p', class_='man').text)
            return result
        except KeyError:
            raise
        except ValueError:
            return None

    def _parse_mouse_win_sens(self, soup) -> int:
        try:
            result = int(soup.find('h4', text=re.compile('^windows sens', re.IGNORECASE)).find_next('p', class_='man').text)
            return result
        except KeyError:
            raise
        except ValueError:
            return None

    def _parse_mouse_raw_input(self, soup) -> int:
        try:
            result = bool(soup.find('h4', text=re.compile('^raw input$', re.IGNORECASE)).find_next('p', class_='man').text)
            return result
        except KeyError:
            raise
        except ValueError:
            return None

    def _parse_video_config(self, soup) -> CsVideoConfig:
        video_config = CsVideoConfig()
        video_config.ratio_width, video_config.ratio_height = self._parse_video_ratio(soup)
        video_config.res_width, video_config.res_height = self._parse_video_res(soup)
        video_config.monitor_hz = self._parse_video_hz(soup)
        video_config.scale_mode = self._parse_video_scale(soup)
        return video_config

    def _parse_video_ratio(self, soup) -> int:
        try:
            result = soup.find('h4', text=re.compile('^aspect ratio$', re.IGNORECASE)).find_next('p', class_='man').text
            width, height = result.split(':')
            return int(width), int(height)
        except KeyError:
            raise
        except ValueError:
            return None, None

    def _parse_video_res(self, soup) -> int:
        try:
            result = soup.find('h4', text=re.compile('^resolution$', re.IGNORECASE)).find_next('p', class_='man').text
            width, height = result.split('×')
            return int(width), int(height)
        except (KeyError, AttributeError):
            try:
                result = soup.find('h3', text=re.compile('^resolution$', re.IGNORECASE)).find_next('p', class_='man').text
                width, height = result.split('×')
                return int(width), int(height)
            except ValueError:
                try:
                    result = soup.find('h3', text=re.compile('^resolution$', re.IGNORECASE)).find_next('p', class_='man').text
                    width, height = result.split('x')
                    return int(width), int(height)
                except Exception:
                    raise
        except ValueError:
            return None, None

    def _parse_video_hz(self, soup) -> int:
        try:
            result = int(soup.find_all('h4', text=re.compile('^hz$', re.IGNORECASE))[1].find_next('p', class_='man').text)
            return result
        except KeyError:
            raise
        except ValueError:
            return None

    def _parse_video_scale(self, soup) -> str:
        try:
            result = str(soup.find('h4', text=re.compile('^scaling mode$', re.IGNORECASE)).find_next('p', class_='man').text)
            return result.strip()
        except KeyError:
            raise
        except ValueError:
            return None

    def _parse_crosshair_config(self, soup) -> CsCrosshairConfig:
        crosshair_config = CsCrosshairConfig()
        crosshair_config.crosshair = self._get_crosshair(soup)
        return crosshair_config

    def _get_crosshair(self, soup) -> str:
        try:
            result = soup.find('span', text=re.compile('^crosshair$', re.IGNORECASE)).find_next('code').text
            result = result.replace('\n', ' ')
            return result.strip()
        except KeyError:
            raise
        except ValueError:
            return None

    def _parse_viewmodel_config(self, soup) -> CsViewModelConfig:
        viewmodel_config = CsViewModelConfig()
        viewmodel_config.viewmodel = self._get_viewmodel(soup)
        return viewmodel_config

    def _get_viewmodel(self, soup) -> str:
        try:
            result = soup.find('span', text=re.compile('^viewmodel$', re.IGNORECASE)).find_next('code').text
            result = result.replace('\n', ' ')
            return result.strip()
        except KeyError:
            raise
        except ValueError:
            return None


if __name__ == "__main__":
    test = CsProSettingsParser()
    urls = test.get_urls()
    test.parse_all_csgo_players_into_csv(urls)
    # pprint(test.parse_player('https://prosettings.net/counterstrike/nawwk/'))
