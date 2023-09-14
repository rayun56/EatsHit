import datetime
import hashlib
import time

from .models import MenuItem, DiningLocation, Menu
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
        location.menus.create(date=date, visible=False)
    week = doc.get_weekly_schedule(date)
    for menu in Menu.objects.all().filter(date=date):
        menu_location = DiningLocation.objects.get(menus=menu)
        print(f"  Collecting menu for {menu_location.name}")
        for weekly in week:
            if weekly['id'] == menu_location.location_id:
                for day in weekly['week']:
                    if day['date'] == date.strftime('%Y-%m-%d'):
                        if day['closed']:
                            print(f"    {menu_location.name} is closed on {date.strftime('%Y-%m-%d')}")
                            menu.closed = True
                            menu.save()
                            break
                        menu.opening_time = datetime.time(hour=day['hours'][0]['start_hour'], minute=day['hours'][0]['start_minutes'])
                        menu.closing_time = datetime.time(hour=day['hours'][0]['end_hour'], minute=day['hours'][0]['end_minutes'])
                        menu.save()
                        break
        if menu.closed:
            continue
        periods = doc.get_menu_periods(menu_location.location_id, date)
        for period in periods:
            menu.periods.get_or_create(period_id=period['id'], name=period['name'])
        for period in menu.periods.all():
            print(f"    Collecting menu for {period.name}")
            menu_categories = doc.get_menu(menu_location.location_id, period.period_id, date)['categories']
            for category in menu_categories:
                cat, _ = period.categories.get_or_create(name=category['name'], category_id=category['id'])
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
        menu.visible = True
        menu.save()
        print(f"  Done!")
    print(f"Done!")


def collect_menu(through_date):
    start_time = time.perf_counter()
    i = 0
    for i in range((through_date - datetime.date.today()).days + 1):
        date = datetime.date.today() + datetime.timedelta(days=i)
        _collect_menu_worker(date)
    end_time = time.perf_counter()
    print(f"Updated {i + 1} menu dates in {end_time - start_time:.02f} seconds.")
