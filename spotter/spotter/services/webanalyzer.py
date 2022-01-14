import pendulum, re
from bs4 import BeautifulSoup
from ..base import Base


class WebAnalyzer(Base):

    URL = 'https://wa-com.com/'

    def get(self):
        latest_list = []
        now = pendulum.now().subtract(days=2).to_date_string()
        self.__logger.info('In Web Analyzer and getting data')
        for tld in self.config['webanalyzer']['tld']:
            count = 1
            total = 15
            while count <= total:
                url = '{url}{time}/new-created-domains/{tld}/p/{count}'.format(url=self.URL, time=now, tld=tld, count=count)
                response = self.session.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                for link in soup.find_all(id='hd'):
                    latest_list.append(link.get('href').strip('/'))
                count += 1
        return latest_list