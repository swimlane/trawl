import pendulum
from ..base import Base


class PhishTank(Base):

    URL = 'http://data.phishtank.com/data/online-valid.json'
    
    def get(self):
        return_list = []
        response = self.request('GET', self.URL, **{'stream': True})
        self.__logger.info('In PhishTank and getting data')
        for item in response.json():
            self.__logger.info(f"Item is {item}")
            if pendulum.parse(item['submission_time']) >= pendulum.now().subtract(
                days=self.config['phishtank']['check-interval']['days'],
                hours=self.config['phishtank']['check-interval']['hours']):
                self.__logger.info('about to save to spotted')
                self.spotted.save(
                    url=item['url'],
                    source='phishtank',
                    ipv4_address=item['details'][0]['ip_address'],
                    country=item['details'][0]['country'],
                    registrar=item['details'][0]['rir']
                )
                self.publisher.post(item['url'])
            else:
                break
