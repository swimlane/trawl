import requests

from spotter import Spotter

class OpenPhish(Spotter):

    URL = 'https://openphish.com/feed.txt'

    def get(self):
        latest_list = []
        response = self.session.get(self.URL, stream=True)
        
        for line in response.iter_lines():
            latest_list.append(str(line, 'utf-8').rstrip())

        return latest_list

#openphish = OpenPhish()
#print(openphish.latest)