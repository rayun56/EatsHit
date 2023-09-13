import datetime
import threading
import hashlib

from .models import MenuItem, MenuPeriod, DiningLocation, Menu, Change
from .doc_wrapper import DOC


def _collect_menu_worker(date: datetime.date):
    doc = DOC('MTU')
    print(f"Collecting menu for {date.strftime('%Y-%m-%d')}")
    locations = doc.get_locations_status()
    for location in locations:
        DiningLocation.objects.get_or_create(location_id=location['id'], defaults={
            'name': location['name']
        })
    for location in DiningLocation.objects.all():
        if location.menus.filter(date=date).exists():
            continue
        location.menus.create(date=date)
    for menu in Menu.objects.all().filter(date=date):
        menu_location = DiningLocation.objects.get(menus=menu)
        print(f"  Collecting menu for {menu_location.name}")
        periods = doc.get_menu_periods(menu_location.location_id, date)
        for period in periods:
            menu.periods.get_or_create(period_id=period['id'], name=period['name'])
        for period in menu.periods.all():
            print(f"    Collecting menu for {period.name}")
            menu_categories = doc.get_menu(menu_location.location_id, period.period_id, date)['categories']
            for category in menu_categories:
                cat, _ = period.categories.get_or_create(name=category['name'])
                for item in category['items']:
                    if type(item['calories']) == float:
                        item['calories'] = str(round(item['calories']))
                    if '+' in item['calories']:
                        item['calories'] = item['calories'].split('+')[0]
                    item['calories'] = int(item['calories'])
                    item['name'] = item['name'].strip()
                    h = hashlib.md5(f"{item['name']}{item['portion']}".encode()).hexdigest()[:16]
                    menu_item, _ = MenuItem.objects.get_or_create(hash=h, defaults={
                        'name': item['name'],
                        'portion': item['portion'],
                        'calories': item['calories']
                    })
                    cat.items.add(menu_item)
        print(f"  Done!")
    print(f"Done!")


def _collect_menu(through_date):
    for i in range((through_date - datetime.date.today()).days + 1):
        date = datetime.date.today() + datetime.timedelta(days=i)
        _collect_menu_worker(date)


def collect_menu(through_date=datetime.date.today()):
    # Get database up to date through through_date
    t = threading.Thread(target=_collect_menu, args=(through_date,))
    t.start()
