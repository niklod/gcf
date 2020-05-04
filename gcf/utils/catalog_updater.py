from ..models import PlayerConfig, Player, Game, VideoConfig, MouseConfig, CrosshairConfig, ViewModelConfig, PlayerInfo, StartUpSettings
from .parsers.prosettings_parser import CsProSettingsParser
from .parsers.csgopedia_parser import CsgoPediaParser
from .parsers.models import CsVideoConfig, CsMouseConfig, CsCrosshairConfig, CsViewModelConfig, CsPlayerInfo
from django.core.exceptions import ObjectDoesNotExist


class CatalogUpdater:
    def __init__(self):
        self.prosettings_parser = CsProSettingsParser()
        self.csgopedia_parser = CsgoPediaParser()
        self.game = Game.objects.get(slug='cs-go')

    def update_configs(self):
        players = self.prosettings_parser.parse_all_csgo_players()

        for parsed_player in players:

            try:
                actual_player = Player.objects.get(nickname__iexact=parsed_player.player_info.nickname)
            except ObjectDoesNotExist:
                actual_player = Player(nickname=parsed_player.player_info.nickname)
                actual_player.save()
                actual_player.games.add(self.game)
                actual_player.save()

            game_config = actual_player.playerconfig_set.filter(game__slug=self.game.slug).first()
            if not game_config:
                game_config = actual_player.playerconfig_set.create(game=self.game)
                game_config.save()

            self._update_video_config(game_config, parsed_player.video_config)
            self._update_mouse_config(game_config, parsed_player.mouse_config)
            self._update_crosshair_config(game_config, parsed_player.crosshair_config)
            self._update_viewmodel_config(game_config, parsed_player.viewmodel_config)
            self._update_player_social_links(actual_player, parsed_player.player_info)

    def _update_video_config(self, game_config: PlayerConfig, new_config: CsVideoConfig):

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
                playerconfig=game_config
            )
            game_config.video_config = video_config
            game_config.save()

    def _update_mouse_config(self, game_config: PlayerConfig, new_config: CsMouseConfig):

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
                playerconfig=game_config
            )
            game_config.mouse_config = mouse_config
            game_config.save()

    def _update_crosshair_config(self, game_config: PlayerConfig, new_config: CsCrosshairConfig):

        try:
            game_config.crosshair_config.crosshair_settings = new_config.crosshair
            game_config.save()

        except AttributeError:
            crosshair_config = CrosshairConfig.objects.create(
                crosshair_settings=new_config.crosshair,
                playerconfig=game_config
            )
            game_config.crosshair_config = crosshair_config
            game_config.save()

    def _update_viewmodel_config(self, game_config: PlayerConfig, new_config: CsViewModelConfig):

        try:
            game_config.viewmodel_config.viewmodel_settings = new_config.viewmodel
            game_config.save()

        except AttributeError:
            viewmodel_config = ViewModelConfig.objects.create(
                viewmodel_settings=new_config.viewmodel,
                playerconfig=game_config
            )
            game_config.viewmodel_config = viewmodel_config
            game_config.save()

    def _update_player_social_links(self, actual_player: Player, parse_info: CsPlayerInfo):
        try:
            actual_player.info.steam_link = parse_info.social_links['steam']
            actual_player.info.twitch_link = parse_info.social_links['twitch']

        except AttributeError:
            player_info = PlayerInfo.objects.create(
                steam_link=parse_info.social_links['steam'],
                twitch_link=parse_info.social_links['twitch']
            )
            actual_player.info = player_info
            actual_player.save()

    def update_info(self):
        players = self.csgopedia_parser.parse_all_csgo_players()

        for parsed_player in players:

            try:
                actual_player = Player.objects.get(nickname__iexact=parsed_player[0].nickname)
            except ObjectDoesNotExist:
                actual_player = None

            try:
                game_config = actual_player.playerconfig_set.filter(game__slug=self.game.slug).first()
            except (ObjectDoesNotExist, AttributeError):
                game_config = None

            if actual_player:
                self._update_player_info(actual_player, parsed_player[0])

            if game_config:
                self._update_startup_config(game_config, parsed_player[1])

    def _update_player_info(self, actual_player: Player, parse_info: CsPlayerInfo):
        try:
            actual_player.info.firstname = parse_info.firstname
            actual_player.info.lastname = parse_info.lastname
            actual_player.info.age = parse_info.age
            actual_player.info.city = parse_info.city
            actual_player.info.save()

        except AttributeError:
            player_info = PlayerInfo.objects.create(
                firstname=parse_info.firstname,
                lastname=parse_info.lastname,
                age=parse_info.age,
                city=parse_info.city
            )
            actual_player.info = player_info
            actual_player.save()

    def _update_startup_config(self, game_config, parse_info):
        try:
            game_config.startup_config.startup_settings = parse_info.startup
            game_config.startup_config.save()

        except AttributeError:
            startup_config = StartUpSettings.objects.create(
                startup_settings=parse_info.startup
            )
            game_config.startup_config = startup_config
            game_config.save()


if __name__ == "__main__":
    test = CatalogUpdater()
    test.update_configs()
