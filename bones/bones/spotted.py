from mongoengine import connect
import datetime
from .models import SpottedModel
from .bones import Bones


class Spotted(Bones):
     
    def save(self, url=None, parsed_url=None, ipv4_address=None, ipv6_address=None, country=None, registrar=None, 
        domain=None, source=None, received=None, tweet_extracted_urls=None, tweet_urls=None, tweet_hash_tags=None,
        tweet_text=None, tweet_id=None):
        spotted = SpottedModel(
            url=url,
            parsed_url=parsed_url,
            ipv4_address=ipv4_address,
            ipv6_address=ipv6_address,
            country=country,
            domain=domain,
            source=source,
            registrar=registrar,
            received=datetime.datetime.utcnow() if received is None else received,
            tweet_extracted_urls=tweet_extracted_urls,
            tweet_urls=tweet_urls,
            tweet_hash_tags=tweet_hash_tags,
            tweet_text=tweet_text,
            tweet_id=tweet_id
        ).save()

    def get(self, url):
        try:
            if SpottedModel.objects(url=url):
                return SpottedModel.objects(url=url)
            else:
                return False
        except:
            return False
            