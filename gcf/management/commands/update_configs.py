from django.core.management.base import BaseCommand
from ...utils.catalog_updater import CatalogUpdater


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = CatalogUpdater()
        updater.update_configs()
        updater.update_info()
