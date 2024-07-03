from django.apps import AppConfig
from django.core.signals import setting_changed


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'Панель товаров'

    def ready(self):
        from .signals import (
            process_csv_file_after_save, add_products_from_csv_file
        )
        setting_changed.connect(process_csv_file_after_save)
        setting_changed.connect(add_products_from_csv_file)
