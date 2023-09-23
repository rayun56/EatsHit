import datetime
import time

import requests


class DOC:
    def __init__(self, site):
        self.url = "https://doc-relay.vercel.app/v1"
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'
        }
        self.site = None
        self.site_id = None
        self.last_request_time = 0.0
        self.total_reported_request_time = 0.0
        self.total_response_time = 0.0
        self.retry_count = 0
        self._get_site_id(site)

    def get(self, path, params=None):
        st = time.perf_counter()
        r = requests.get(self.url + path, headers=self.headers, params=params)
        if r.status_code == 200:
            j = r.json()
            self.last_request_time = j['request_time']
            self.total_reported_request_time += j['request_time']
            self.total_response_time += time.perf_counter() - st
            return r.json()
        elif r.status_code == 502 or r.status_code == 504:
            self.retry_count += 1
            if self.retry_count > 16:
                raise TimeoutError(f'Too many retries: {self.retry_count}. Error 502: {r.text.strip()}')
            return self.get(path, params)
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
