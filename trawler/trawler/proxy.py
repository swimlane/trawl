import requests, random
from lxml.html import fromstring


class Proxy(object):

    URL = 'https://free-proxy-list.net/'

    def all(self):
        return_list = []
        try:
            response = requests.get(self.URL)
            parser = fromstring(response.text)
            for i in parser.xpath('//tbody/tr'):
                if i.xpath('.//td[7][contains(text(),"yes")]'):
                    return_list.append('{ip}:{port}'.format(
                        ip=i.xpath('.//td[1]/text()')[0],
                        port=i.xpath('.//td[2]/text()')[0]
                    ))
        except:
            pass
        return return_list

    def get(self):
        return_list = []
        try:
            response = requests.get(self.URL)
            parser = fromstring(response.text)
            for i in parser.xpath('//tbody/tr'):
                if i.xpath('.//td[7][contains(text(),"yes")]'):
                    return_list.append('{ip}:{port}'.format(
                        ip=i.xpath('.//td[1]/text()')[0],
                        port=i.xpath('.//td[2]/text()')[0]
                    ))
        except:
            pass
        return random.choice(return_list)