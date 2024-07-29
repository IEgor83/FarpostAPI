import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farpost_api.settings')
django.setup()

from listings.models import Listing


def import_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for entry in data:
        listing, created = Listing.objects.update_or_create(
            listing_id=entry['id'],
            defaults={
                'title': entry['title'],
                'author': entry['author'],
                'views': entry['view'],
                'position': entry['position']
            }
        )
        if created:
            print(f"Создано новое объявление: {listing}")
        else:
            print(f"Объявление обновлено: {listing}")


if __name__ == "__main__":
    import_data_from_json('ad_info.json')
