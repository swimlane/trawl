import yaml, os, pendulum, requests

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


from entrails import Spotted, Sounder
from publisher import Publisher

class Spotter(object):

    def __init__(self, config='spotter.yml'):
        self.config = config
        self.session = requests.Session()
        self.sounder = Sounder()
        self.spotted = Spotted()
        self.publisher = Publisher()
        
    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        try:
            with(open('%s/%s' % (os.getcwd(), value), 'r')) as ymlfile:
                self._config = yaml.load(ymlfile, Loader=yaml.BaseLoader)
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            raise Exception('Spotter.yml cannot be found!')
        except AssertionError as error:
            print(error)
            raise AssertionError('Unable to retrieve configuration from yaml file')


    def _get_check_interval_from_service_config(self, value):
        return_dict = {}
        if 'check-interval' in value:
            if 'days' in value['check-interval']:
                return_dict['days'] = value['check-interval']['days']
            else:
                return_dict['days'] = 0
            if 'hours' in value['check-interval']:
                return_dict['hours'] = value['check-interval']['hours']
            else:
                return_dict['days'] = 0
        else:
            return_dict['days'] = 0
            return_dict['hours'] = 0
        return return_dict

    def _save_service_config(self):
        for service, value in self._config.iteritems():
            if 'twitter' == service:
                if 'consumer_key' and 'consumer_secret' and 'access_token_key' and 'access_token_secret' and 'hashtags' in value:
                    interval = self._get_check_interval_from_service_config(value)
                    self.sounder.save(service=service, day_interval=interval['days'], hour_interval=interval['hours'])
                else:
                    raise AttributeError('Please provide a consumer_key, consumer_secret, access_token_key, access_token_secret, and hashtags for {} in spotter.yml'.format(service))
            if service in ('urlscan', 'openphish', 'phishtank', 'whoisds', 'webanalyzer'):
                if 'url' in value:
                    interval = self._get_check_interval_from_service_config(value)
                    self.sounder.save(service=service, day_interval=interval['days'], hour_interval=interval['hours'])
                else:
                    raise AttributeError('Please provide a url for {} in spotter.yml'.format(service))

    def run(self):
        while True:
            try:
                services = self.sounder.get()
                if not services:
                    self._save_service_config()
                else:
                    for service in services:
                        time_interval = pendulum.now().subtract(days=service.day_interval, hours=service.hour_interval)
                        if time_interval >= pendulum.parse(service.last_checked):
                            # RUN SERVICE
                            if service == 'openphish':
                                from openphish import OpenPhish
                                for finding in OpenPhish().get():
                                    self.spotted.save(
                                        url=finding,
                                        source=service
                                    )
                                    self.publisher.post(finding)
                            if service == 'phishingdatabase':
                                from phishingdatabase import PhishingDatabase
                                for finding in PhishingDatabase().get(today=True):
                                    self.spotted.save(
                                        url=finding,
                                        source=service
                                    )
                                    self.publisher.post(finding)
                            if service == 'phishtank':
                                from phishtank import PhishTank
                                for finding in PhishTank().get():
                                    self.spotted.save(
                                        url=finding['url'],
                                        source=service,
                                        ipv4_address=finding['ip'],
                                        country=finding['country'],
                                        registrar=finding['registrar']
                                    )
                                    self.publisher.post(finding['url'])
                            if service == 'twitter':
                                count = 0
                                last_id = self.sounder.get(service=service)['last_id']
                                if not last_id:
                                    last_id = None
                                from twitterscraper import TwitterScraper
                                for finding in TwitterScraper().get(since_id=last_id):
                                    if not last_id and count == 0:
                                        self.sounder.save(
                                            service=service,
                                            last_id=finding['id']
                                        )
                                        count += 1
                                    self.spotted.save(
                                        tweet_extracted_urls=finding['extracted_urls'],
                                        tweet_urls=finding['urls'],
                                        tweet_hash_tags=finding['tags'],
                                        tweet_text=finding['text'],
                                        tweet_id=finding['id'],
                                        source=service
                                    )
                                    self.publisher.post(finding['extracted_urls'])
                            if service == 'urlscan':
                                from urlscan import UrlScan
                                for finding in UrlScan().get():
                                    self.spotted.save(
                                        url=finding['url'],
                                        parsed_ur=finding['parsed_url'],
                                        ipv4_address=finding['ip'],
                                        country=finding['country'],
                                        domain=finding['domain'],
                                        source=finding['source']
                                    )
                                    self.publisher.post(finding['url'])
                            if service == 'webanalyzer':
                                from webanalyzer import WebAnalyzer
                                for finding in WebAnalyzer().get():
                                    self.spotted.save(
                                        url=finding,
                                        source=service
                                    )
                                    self.publisher.post(finding)
                            if service == 'whoisds':
                                from whoisds import WhoisDs
                                for finding in WhoisDs().get():
                                    self.spotted.save(
                                        url=finding,
                                        source=service
                                    )
                                    self.publisher.post(finding)
            except:
                print('ERROR: Error when calling spotter.run: {}'.format(sys.exc_info()[0]))
                pass

            
     
spot = Spotter()
print(spot.run())