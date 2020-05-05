from ..models import PlayerConfig, Player, Game, VideoConfig, MouseConfig, CrosshairConfig, ViewModelConfig, PlayerInfo, StartUpSettings, PlayerStats, PlayerImage
from .parsers.prosettings_parser import CsProSettingsParser
from .parsers.csgopedia_parser import CsgoPediaParser
from .parsers.hltv_parser import HltvParser
from .parsers.models import CsVideoConfig, CsMouseConfig, CsCrosshairConfig, CsViewModelConfig, CsPlayerInfo, CsPlayerStats
from django.core.exceptions import ObjectDoesNotExist


class CatalogUpdater:
    def __init__(self):
        self.prosettings_parser = CsProSettingsParser()
        self.csgopedia_parser = CsgoPediaParser()
        self.hltv_parser = HltvParser()
        self.game = Game.objects.get(slug='cs-go')

    def update_configs(self):
        players = self.prosettings_parser.parse_all_csgo_players()

        for parsed_player in players:

            try:
                actual_player = Player.objects.get(
                    nickname__iexact=parsed_player.player_info.nickname)
            except ObjectDoesNotExist:
                actual_player = Player(
                    nickname=parsed_player.player_info.nickname)
                actual_player.save()
                actual_player.games.add(self.game)
                actual_player.save()

            game_config = actual_player.playerconfig_set.filter(
                game__slug=self.game.slug).first()
            if not game_config:
                game_config = actual_player.playerconfig_set.create(
                    game=self.game)
                game_config.save()

            self._update_video_config(game_config, parsed_player.video_config)
            self._update_mouse_config(game_config, parsed_player.mouse_config)
            self._update_crosshair_config(game_config,
                                          parsed_player.crosshair_config)
            self._update_viewmodel_config(game_config,
                                          parsed_player.viewmodel_config)
            self._update_player_social_links(actual_player,
                                             parsed_player.player_info)

    def _update_video_config(self, game_config: PlayerConfig,
                             new_config: CsVideoConfig):

        try:
            game_config.video_config.resolution_width = new_config.res_width
            game_config.video_config.resolution_height = new_config.res_height
            game_config.video_config.aspect_ration_width = new_config.ratio_width
            game_config.video_config.aspect_ration_height = new_config.ratio_height
            game_config.video_config.frequency = new_config.monitor_hz
            game_config.video_config.dimension = new_config.scale_mode
            game_config.save()

        except AttributeError:
            video_config = VideoConfig.objects.create(
                resolution_width=new_config.res_width,
                resolution_height=new_config.res_height,
                aspect_ration_width=new_config.ratio_width,
                aspect_ration_height=new_config.ratio_height,
                frequency=new_config.monitor_hz,
                dimension=new_config.scale_mode,
                playerconfig=game_config)
            game_config.video_config = video_config
            game_config.save()

    def _update_mouse_config(self, game_config: PlayerConfig,
                             new_config: CsMouseConfig):

        try:
            game_config.mouse_config.dpi = new_config.dpi,
            game_config.mouse_config.edpi = new_config.edpi,
            game_config.mouse_config.usb_rate = new_config.mouse_hz,
            game_config.mouse_config.win_sens = new_config.win_sens,
            game_config.mouse_config.game_sens = new_config.sens,
            game_config.mouse_config.zoom_sens = new_config.zoom_sens,
            game_config.mouse_config.raw_input = new_config.raw_input,
            game_config.mouse_config.mouse_acceleration = new_config.mouse_acc
            game_config.save()

        except AttributeError:
            mouse_config = MouseConfig.objects.create(
                dpi=new_config.dpi,
                edpi=new_config.edpi,
                usb_rate=new_config.mouse_hz,
                win_sens=new_config.win_sens,
                game_sens=new_config.sens,
                zoom_sens=new_config.zoom_sens,
                raw_input=new_config.raw_input,
                mouse_acceleration=new_config.mouse_acc,
                playerconfig=game_config)
            game_config.mouse_config = mouse_config
            game_config.save()

    def _update_crosshair_config(self, game_config: PlayerConfig,
                                 new_config: CsCrosshairConfig):

        try:
            game_config.crosshair_config.crosshair_settings = new_config.crosshair
            game_config.save()

        except AttributeError:
            crosshair_config = CrosshairConfig.objects.create(
                crosshair_settings=new_config.crosshair,
                playerconfig=game_config)
            game_config.crosshair_config = crosshair_config
            game_config.save()

    def _update_viewmodel_config(self, game_config: PlayerConfig,
                                 new_config: CsViewModelConfig):

        try:
            game_config.viewmodel_config.viewmodel_settings = new_config.viewmodel
            game_config.save()

        except AttributeError:
            viewmodel_config = ViewModelConfig.objects.create(
                viewmodel_settings=new_config.viewmodel,
                playerconfig=game_config)
            game_config.viewmodel_config = viewmodel_config
            game_config.save()

    def _update_player_social_links(self, actual_player: Player,
                                    parse_info: CsPlayerInfo):
        try:
            actual_player.info.steam_link = parse_info.social_links['steam']
            actual_player.info.twitch_link = parse_info.social_links['twitch']

        except AttributeError:
            player_info = PlayerInfo.objects.create(
                steam_link=parse_info.social_links['steam'],
                twitch_link=parse_info.social_links['twitch'])
            actual_player.info = player_info
            actual_player.save()

    def update_info(self):
        players = self.csgopedia_parser.parse_all_csgo_players()

        for parsed_player in players:

            try:
                actual_player = Player.objects.get(
                    nickname__iexact=parsed_player[0].nickname)
            except ObjectDoesNotExist:
                actual_player = None

            try:
                game_config = actual_player.playerconfig_set.filter(
                    game__slug=self.game.slug).first()
                if not game_config:
                    game_config = actual_player.playerconfig_set.create(
                        game=self.game)
                    game_config.save()
            except (ObjectDoesNotExist, AttributeError):
                game_config = None

            if actual_player:
                self._update_player_info(actual_player, parsed_player[0])

            if game_config:
                self._update_startup_config(game_config, parsed_player[1])

    def _update_player_info(self, actual_player: Player,
                            parse_info: CsPlayerInfo):
        try:
            actual_player.info.firstname = parse_info.firstname
            actual_player.info.lastname = parse_info.lastname
            # actual_player.info.age = parse_info.age
            actual_player.info.city = parse_info.city
            actual_player.info.save()

        except AttributeError:
            player_info = PlayerInfo.objects.create(
                firstname=parse_info.firstname,
                lastname=parse_info.lastname,
                age=parse_info.age,
                city=parse_info.city)
            actual_player.info = player_info
            actual_player.save()

    def _update_startup_config(self, game_config, parse_info):
        try:
            game_config.startup_config.startup_settings = parse_info.startup
            game_config.startup_config.save()

        except AttributeError:
            startup_config = StartUpSettings.objects.create(
                startup_settings=parse_info.startup)
            game_config.startup_config = startup_config
            game_config.save()

    def update_age_and_stats(self):
        players = self.hltv_parser.parse_all_csgo_players()

        for parsed_player in players:

            try:
                actual_player = Player.objects.get(
                    nickname__iexact=parsed_player[0].nickname)
            except ObjectDoesNotExist:
                actual_player = None

            try:
                stats = actual_player.playerstats_set.filter(
                    game__slug=self.game.slug).first()
                if not stats:
                    stats = actual_player.playerstats_set.create(
                        game=self.game)
                    stats.save()

            except (ObjectDoesNotExist, AttributeError):
                stats = None

            try:
                pic = actual_player.playerimage_set.first()
                if not pic:
                    pic = actual_player.playerimage_set.create()
                    pic.save()
                else:
                    pic = None

            except (ObjectDoesNotExist, AttributeError):
                pic = None

            if actual_player:
                self._update_player_age(actual_player, parsed_player[0])

            if stats:
                self._update_player_stats(stats, parsed_player[1])

            if pic:
                self._update_player_pic(pic, parsed_player[0])

    def _update_player_age(self, actual_player: Player,
                           parse_info: CsPlayerInfo):
        try:
            actual_player.info.age = parse_info.age
            actual_player.info.save()

        except AttributeError:
            player_info = PlayerInfo.objects.create(age=parse_info.age)
            actual_player.info = player_info
            actual_player.save()

    def _update_player_stats(self, stats: PlayerStats,
                             parse_info: CsPlayerStats):
        try:
            stats.rating = parse_info.rating
            stats.headshots_percent = parse_info.headshots_percent
            stats.total_kills = parse_info.total_kills
            stats.total_deaths = parse_info.total_deaths
            stats.rounds_played = parse_info.rounds_played
            stats.damage_per_round = parse_info.damage_per_round
            stats.grenade_damage_per_round = parse_info.grenade_damage_per_round
            stats.assists_per_round = parse_info.assists_per_round
            stats.save()

        except AttributeError:
            player_stats = PlayerStats.objects.create(
                rating=parse_info.rating,
                headshots_percent=parse_info.headshots_percent,
                total_kills=parse_info.total_kills,
                total_deaths=parse_info.total_deaths,
                rounds_played=parse_info.rounds_played,
                damage_per_round=parse_info.damage_per_round,
                grenade_damage_per_round=parse_info.grenade_damage_per_round,
                assists_per_round=parse_info.assists_per_round)
            stats = player_stats
            stats.save()

    def _update_player_pic(self, pic: PlayerImage, parse_info: CsPlayerInfo):
        pic.hltv_picture = parse_info.hltv_photo
        pic.hltv_crop_picture = parse_info.hltv_crop_photo
        pic.save()


if __name__ == "__main__":
    test = CatalogUpdater()
    test.update_configs()
