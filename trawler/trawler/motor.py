import requests, shutil
from .useragent import UserAgent
from .proxy import Proxy



class Motor(object):

    def __init__(self, user_agent=False, proxy=False):
        self.proxy = {}
        self.session = requests.Session()
        if user_agent:
            self.session.headers.update({'User-agent', '{}'.format(UserAgent().get())})
        if proxy:
            ip = Proxy().get()
            self.proxy['http'] = 'http://{}'.format(ip)
            self.proxy['https'] = 'https://{}'.format(ip)

    def head(self, url):
        try:
            response = self.session.head(url, proxies=self.proxy)
            return response.headers
        except:
            return False

    def get(self, url):
        try:
            response = self.session.get(url, proxies=self.proxy)
            return {
                'content': response.content,
                'headers': response.headers,
                'status': response.status_code
            }
        except:
            return False

    def download(self, url, path):
        try:
            with requests.get(url, stream=True) as content:
                with open(path, 'wb') as download:
                    shutil.copyfileobj(content.raw, download)
            return path
        except:
            return False    