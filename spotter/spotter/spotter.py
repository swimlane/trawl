import yaml, os, pendulum, requests, sys

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from .base import Base
from .services import (
    OpenPhish,
    PhishingDatabase,
    PhishTank,
    TwitterScraper,
    UrlScan,
    WebAnalyzer,
    WhoisDs
)


class Spotter(Base):

    def run(self, service):
        if service == 'openphish':
            OpenPhish().get()
        if service == 'phishingdatabase':
            PhishingDatabase().get(today=True)
        if service == 'phishtank':
            PhishTank().get()
        if service == 'twitter':
            count = 0
            last_id = self.sounder.get(service=service.service)['last_id']
            if not last_id:
                last_id = None
            for finding in TwitterScraper().get(since_id=last_id):
                if not last_id and count == 0:
                    self.sounder.save(
                        service=service.service,
                        last_id=finding['id']
                    )
                    count += 1
                self.spotted.save(
                    tweet_extracted_urls=finding['extracted_urls'],
                    tweet_urls=finding['urls'],
                    tweet_hash_tags=finding['tags'],
                    tweet_text=finding['text'],
                    tweet_id=finding['id'],
                    source=service.service
                )
                self.publisher.post(finding['extracted_urls'])
