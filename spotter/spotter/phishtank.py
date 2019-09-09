import pendulum
from spotter import Spotter


class PhishTank(Spotter):

    URL = 'http://data.phishtank.com/data/online-valid.json'
    
    def get(self):
        return_list = []
        response = self.session.get(self.URL, stream=True)
        for item in response.json():
            if pendulum.parse(item['submission_time']) >= pendulum.now().subtract(
                days=self.config['phishtank']['check-interval']['days'],
                hours=self.config['phishtank']['check-interval']['hours']):

                return_list.append({
                    'phish_id': item['phish_id'],
                    'url': item['url'],
                    'ip': item['details'][0]['ip_address'],
                    'registrar': item['details'][0]['rir'],
                    'country': item['details'][0]['country']
                })
            else:
                break
        return return_list