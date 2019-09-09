#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of StalkPhish - see https://github.com/t4d/StalkPhish

import pendulum, re

from spotter import Spotter


class UrlScan(Spotter):

    URL = 'https://urlscan.io/api/v1/search/'
    
    def __init__(self, search_string = '*'):
        super(UrlScan, self).__init__()
        self.search_string = search_string
    
    def get(self):
        latest_list = []
        response = self.session.get(
            url='{url}?q={search_string}'.format(url=self.URL, search_string=self.search_string),
            allow_redirects=True,
            timeout=(5, 12)
        ).json()

        for item in response['results']:
            if pendulum.parse(item['task']['time']) >= self.now.subtract(
                days=self.config['urlscan']['check-interval']['days'],
                hours=self.config['urlscan']['check-interval']['hours']
            ):
                latest_list.append({
                    'id': item.get('_id'),
                    'url': item.get('page').get('url'),
                    'parsed_url': self.parse_url(item.get('page').get('url')),
                    'ip': item.get('page').get('ip'),
                    #'registrar': item['details'][0]['rir'],
                    'country': item.get('page').get('country'),
                    'domain': item.get('page').get('domain'),
                    'source': ['urlscan', item.get('task').get('source')]
                })
            else:
                break
        return latest_list