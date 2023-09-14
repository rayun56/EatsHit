import datetime

import requests


class DOC:
    def __init__(self, site):
        self.url = "https://api.dineoncampus.com/v1"
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) Version/16.5 Safari/605.1.15'
        }
        self.site = None
        self.site_id = None
        self.last_request_time = 0
        self._get_site_id(site)

    def get(self, path, params=None):
        r = requests.get(self.url + path, headers=self.headers, params=params)
        if r.status_code == 200:
            j = r.json()
            self.last_request_time = j['request_time']
            return r.json()
        else:
            raise Exception(f'Error {r.status_code}: {r.text}')

    def _get_site_id(self, site):
        self.site = site
        self.site_id = self.get(f'/sites/{site}/info')['site']['id']

    def get_info(self):
        return self.get(f'/sites/{self.site}/info')['site']

    def get_upcoming_events(self):
        return self.get(f'/events/upcoming_events', params={
            'site_id': self.site_id
        })['events']

    def get_locations(self, for_menus=True, with_address=False, with_buildings=False):
        return self.get(f'/locations/all_locations', params={
            'site_id': self.site_id,
            'for_menus': for_menus,
            'with_address': with_address,
            'with_buildings': with_buildings
        })['locations']

    def get_locations_status(self):
        return self.get(f'/locations/status', params={
            'site_id': self.site_id
        })['locations']

    def get_locations_name(self):
        return self.get(f'/locations/all_locations_name', params={
            'site_id': self.site_id
        })['locations']

    def get_menu_periods(self, location_id: str, date: datetime.date):
        date_str = date.strftime('%Y-%m-%d')
        return self.get(f'/location/{location_id}/periods', params={
            'date': date_str,
            'platform': '0'
        })['periods']

    def get_menu(self, location_id, period_id, date: datetime.date):
        date_str = date.strftime('%Y-%m-%d')
        return self.get(f'/location/{location_id}/periods/{period_id}', params={
            'date': date_str,
            'platform': '0'
        })['menu']['periods']

    def get_weekly_schedule(self, date: datetime.date):
        date_str = date.isoformat()
        return self.get('/locations/weekly_schedule', params={
            'site_id': self.site_id,
            'date': date_str
        })['the_locations']
