from django.core.management.base import BaseCommand
from ...utils.catalog_updater import CatalogUpdater
from ...utils.parsers.csgopedia_parser import CsgoPediaParser


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = CatalogUpdater()
        updater.update_configs()
        updater.update_info()
        updater.update_age_and_stats()
