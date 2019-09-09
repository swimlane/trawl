from bs4 import BeautifulSoup
import yaml

__CONFIG__ = ''

with(open('./trawler/config.yml', 'r')) as ymlfile:
    __CONFIG__ = yaml.load(ymlfile, Loader=yaml.BaseLoader)


class Parser(object):

    def __init__(self, url, network):
        self.network = network
        self.url = url
        self.url_list = []
        self.url_file_list = []
        self.searched_url_list = []
        if isinstance(url, list):
            self.parse_links(url)
        else:
            self.parse_links([url])

    @property
    def parsed_urls(self):
        return_url_list = []
        if self.url_list:
            for url in self.url_list:
                return_url_list.append(url)
        return return_url_list

    @property
    def parsed_files(self):
        return_url_list = []
        if self.url_file_list:
            for url in self.url_file_list:
                return_url_list.append(url)
        return return_url_list

    def parse_links(self, url):
        url_list = []
        if isinstance(url, list):
            for link in url:
                print('parsing link: %s' % link)
                if link not in self.searched_url_list:
                    if link.endswith('/'):
                       # print('link endswith /')
                        content = ''
                        self.searched_url_list.append(link)
                        response = self.network.get(link)
                        #print(response)
                        if response:
                            try:
                                content = response['content'].decode('utf-8')
                            except:
                                continue
                        soup = BeautifulSoup(content, 'html.parser')
                        index_of = self.parse_indexof(soup, link)
                        if index_of:
                            for item in index_of:
                                print('item in index_of is %s' % item)
                                if item not in self.searched_url_list:
                                    url_list.append(item)
                        else:
                            for item in self.parse_href_links(soup):
                                new_url = '{}/{}'.format(link, item)
                                print('new url is %s' % new_url)
                                if new_url not in self.searched_url_list:
                                    url_list.append(new_url)
                    else:
                        for extension in __CONFIG__['download']['extensions']:
                            if link.endswith(extension):
                                if link not in self.searched_url_list:
                                    self.url_file_list.append(link)
        if url_list:
            for item in url_list:
                self.url_list.append(item)
            self.parse_links(self.url_list)


    def parse_indexof(self, soup, url):
        return_list = []
        try:
            if 'index of' in (soup.title.string).lower():
                for link in self.parse_href_links(soup):
                    new_link_path = '{}/{}'.format(url.rstrip('/'), link)
                    if new_link_path.endswith('//'):
                        new_link_path = new_link_path[:-1]
                    return_list.append(new_link_path)
                return return_list
        except:
            pass
    
    def parse_href_links(self, soup):
        return_list = []
        for link in soup.find_all('a'):
            return_list.append(link.get('href'))
        return return_list