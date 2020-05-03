from django.core.management.base import BaseCommand, CommandError
from ...utils.catalog_updater import CatalogUpdater
from ...utils.parsers.prosettings_parser import CsProSettingsParser


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = CatalogUpdater()
        updater.update_configs()
        # parser = CsProSettingsParser()
        # print(parser.parse_all_csgo_players())
