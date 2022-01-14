import os, yaml
from bs4 import BeautifulSoup

from .trawlbinary import BinaryTrawl
from .generator import Generator
from .parser import Parser
from .motor import Motor
from .skin import Skin

__CONFIG__ = ''

with(open('./trawler/config.yml', 'r')) as ymlfile:
    __CONFIG__ = yaml.load(ymlfile, Loader=yaml.BaseLoader)


class Trawler(object):

    def __init__(self, user_agent=False, proxy=False):
        self.skin = Skin()
        if user_agent and proxy:
            self.network = Motor(user_agent=True, proxy=True)
        elif user_agent:
            self.network = Motor(user_agent=True)
        elif proxy:
            self.network = Motor(proxy=True)
        else:
            self.network = Motor()

        if not os.path.exists('./{}'.format(__CONFIG__['download']['folder'])):
            os.mkdir('./{}'.format(__CONFIG__['download']['folder']))

    def trawl(self, url):
        # making sure url is formatted correctly (aka skinning)
        skinned_url = self.skin.url(url)
        return_dict = {}
        return_dict[skinned_url] = None
        # Determining if the site is up
        url_info = self.is_site_up(skinned_url)
        if url_info:
            
            # Generating a url list based on previously identified patterns with phish kits
            
            attempt_to_download_list = []
            # Trying our generated kit locations to see if files are present
            for url in Generator(skinned_url).url_list:
                print('generated item: %s' % url)
                generated_parsed_files = Parser(url, self.network).parsed_files
                if generated_parsed_files:
                    for item in generated_parsed_files:
                        attempt_to_download_list.append(item)
                attempt_to_download_list.append(url)
    
            for url in Parser(skinned_url, self.network).parsed_files:
                generated_files = Generator(url).url_list
                if generated_files:
                    for item in generated_files:
                        attempt_to_download_list.append(item)
                attempt_to_download_list.append(url)

        return_dict[skinned_url] = self._download_from_url_list(attempt_to_download_list)
        return return_dict
        

    def _download_from_url_list(self, url_list):
        return_list = []
        if isinstance(url_list, list):
            for url in url_list:
                try:
                    print('parsed item: %s' % url)
                    bin_trawl = BinaryTrawl(url,self.network)
                    bin_trawl.download()
                    return_list.append(bin_trawl.file_name)
                except:
                    print('Unable to access kit based on the following path: {}'.format(url))
                    pass
            return return_list

    def is_site_up(self, value):
        url = value.replace(" ","%20")
        response = self.network.get(url)
        return response