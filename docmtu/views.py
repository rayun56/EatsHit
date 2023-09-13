import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from .models import DiningLocation, Menu


def index(request):
    dates = []
    today = timezone.now().astimezone(tz=timezone.get_current_timezone()).date()
    for men in Menu.objects.all().filter(visible=True).order_by('date'):
        menu_date = {
            'str': men.date.strftime('%a, %b %d, %Y') + (" (Today)" if men.date == today else ""),
            'id': men.date.strftime('%Y-%m-%d')
        }
        if menu_date not in dates and men.date >= today:
            dates.append(menu_date)
    return render(request, 'docmtu/index.html', {
        'locations': DiningLocation.objects.all(),
        'dates': dates
    })


def dropdown(request):
    base = """<button id="dropdown-main" class="btn btn-secondary dropdown-toggle {id}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                   {str}
              </button>"""
    location_id = request.headers['HX-Trigger'].split('-')[1]
    response = base.format(id=f"selected-location-{location_id}", str=DiningLocation.objects.get(location_id=location_id).name)
    return HttpResponse(response, headers={'HX-Trigger-After-Settle': 'loadDate'})


def location(request, date=None):
    today = timezone.now().astimezone(tz=timezone.get_current_timezone()).date()
    if date is None:
        date = today
    else:
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    location_id = request.headers['HX-Trigger'].split("-")[1]
    loc = DiningLocation.objects.get(location_id=location_id)
    menu = loc.menus.get(date=date).to_dict()
    date_info = {
        'str': date.strftime('%b %d, %Y') if date != today else "Today",
        'id': date.strftime('%Y-%m-%d')
    }
    response = render(request, 'docmtu/main.html', {
        'location': loc,
        'menu': menu,
        'date': date_info,
        'empty': False if menu['periods'] else True
    })
    response.headers['HX-Trigger-After-Settle'] = 'updateInfo'
    return response


def date(request):
    info = request.headers['HX-Trigger'].split('-')
    date = "-".join(info[3:])
    return location(request, date=date)


def about(request):
    return render(request, 'docmtu/about.html')
