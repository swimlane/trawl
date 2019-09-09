try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from bs4 import BeautifulSoup
import yaml

__CONFIG__ = ''

with(open('./trawler/config.yml', 'r')) as ymlfile:
    __CONFIG__ = yaml.load(ymlfile, Loader=yaml.BaseLoader)


class Generator(object):

    def __init__(self, url):
        self.url_list = []
        self._kit_url_subdirectories(url)

    def _add_to_path(self, path, add):
        return '{path}/{add}'.format(path=path, add=add)

    def _kit_url_subdirectories(self, url):
        old_part = None
        new_path = None
        temp_url = '{scheme}://{netloc}/{part}'
        parsed_url = urlparse(url)
        for part in parsed_url.path.split('/'):
            if part:
                if new_path:
                    if old_part:
                        old_part = self._add_to_path(old_part, part)
                    else:
                        old_part = '{new_url}/{part}'.format(new_url=new_path, part=part)
                    if not old_part.endswith('.zip'):
                        new_part = '{}.zip'.format(old_part)
                    else:
                        new_part = old_part
                    new_url = temp_url.format(
                        scheme=parsed_url.scheme,
                        netloc=parsed_url.netloc,
                        part=new_part
                    )
                    if new_url not in self.url_list:
                        self.url_list.append(new_url)
                else:
                    new_part = '{}.zip'.format(part)
                    new_url = temp_url.format(
                        scheme=parsed_url.scheme,
                        netloc=parsed_url.netloc,
                        part=new_part
                    )
                    new_path = part
                    if new_url not in self.url_list:
                        self.url_list.append(new_url)