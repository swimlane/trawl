import os
import time
import requests

import yaml

from .logging import LoggingBase
from bones import Spotted, Sounder


class Base(metaclass=LoggingBase):

    __config = None
    __config_path = os.path.abspath('./spotter.yml')
    PUBLISHER_URL = os.environ['AMQP_URL']

    def __init__(self):
        self.spotted = Spotted()
        self.sounder = Sounder()
        from .publisher import Publisher
        self.publisher = Publisher()
        self.session = requests.Session()

    def request(self, method, url, **kwargs):
        try:
            response = self.session.request(method, url, **kwargs)
            if response.status_code == 429:
                self.__logger.warning("Retry Error occurred")
                self.__logger.info(f"Waiting for {response.headers.get('Retry-After')} seconds")
                time.sleep(int(response.headers.get('Retry-After')))
                self.request(method=method, url=url, kwargs=kwargs)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as errc:
            self.__logger.warning("An Error Connecting to the API occurred:" + repr(errc))
        except requests.exceptions.Timeout as errt:
            self.__logger.warning("A Timeout Error occurred:" + repr(errt))
        except requests.exceptions.HTTPError as errh:
            self.__logger.warning("An Http Error occurred:" + repr(errh))
        except requests.exceptions.RequestException as err:
            self.__logger.warning("An Unknown Error occurred" + repr(err))

    @property
    def config(self):
        if not self.__config:
            try:
                print(self.__config_path, flush=True)
                with open(self.__config_path, 'r') as ymlfile:
                    self.__config = yaml.load(ymlfile, Loader=yaml.BaseLoader)
            except FileNotFoundError as fnf_error:
                print(fnf_error)
                raise Exception('Spotter.yml cannot be found!')
            except AssertionError as error:
                print(error)
                raise AssertionError('Unable to retrieve configuration from yaml file')
        return self.__config
        