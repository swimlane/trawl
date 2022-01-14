# This file is part of StalkPhish - see https://github.com/t4d/StalkPhish

import pendulum, re, requests
from bones import Spotted, Sounder
from ..base import Base


class UrlScan(Base):

    URL = 'https://urlscan.io/api/v1/search/'
    session = requests.Session()
    
    def __init__(self, search_string = '*'):
        super(UrlScan, self).__init__()
        self.search_string = search_string
    
    def run(self):
        self.__logger.info('In UrlScan and getting data')
        urlscan = self.sounder.get(service='urlscan')
        if urlscan:
            self._save_service_config('urlscan')
        self.session.headers.update({
            'Content-Type': 'application/json',
            'API-Key': None
        })
        response = self.session.get(
            url='{url}?q={search_string}'.format(url=self.URL, search_string=self.search_string),
            allow_redirects=True,
            timeout=(5, 12)
        ).json()
        for item in response['results']:
            if pendulum.parse(item['task']['time']) >= pendulum.now().subtract(
                days=self.config['urlscan']['check-interval']['days'],
                hours=self.config['urlscan']['check-interval']['hours']
            ):
                self.spotted.save(
                    url=item.get('page').get('url'),
                    parsed_url=item.get('page').get('url'),
                    ipv4_address=item.get('page').get('ip'),
                    country=item.get('page').get('country'),
                    domain=item.get('page').get('domain'),
                    source=['urlscan', item.get('task').get('source')]
                )
                self.publisher.post(item.get('page').get('url'))
            else:
                break