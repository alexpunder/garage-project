from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CSVLoaderDB, NewProductCSVLoader
from .utils import handle_uploaded_file, handler_upload_new_products_file


@receiver(post_save, sender=CSVLoaderDB)
def process_csv_file_after_save(sender, instance, **kwargs):
    handle_uploaded_file(instance.file)


@receiver(post_save, sender=NewProductCSVLoader)
def add_products_from_csv_file(sender, instance, **kwargs):
    handler_upload_new_products_file(instance.file)
