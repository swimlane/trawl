from ..base import Base


class OpenPhish(Base):

    URL = 'https://openphish.com/feed.txt'

    def get(self):
        response = self.session.get(self.URL, stream=True)
        self.__logger.info('In OpenPhish and getting data')
        for line in response.iter_lines():
            url = str(line, 'utf-8').rstrip()
            self.__logger.info(f'OpenPhish URL: {url}')
            self.spotted.save(
                    url=url,
                    source='openphish'
                )
            self.publisher.post(url)
