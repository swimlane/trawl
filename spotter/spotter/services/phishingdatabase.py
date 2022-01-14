from ..base import Base


class PhishingDatabase(Base):

    ACTIVE_URL = 'https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt'
    NEW_LAST_HOUR_URL = 'https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-NEW-last-hour.txt'
    NEW_TODAY_URL = 'https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-ACTIVE-TODAY.txt'

    def get(self, active=True, last_hour=False, today=False):
        list_type = ''
        self.__logger.info('In PhishingDatabase and getting data')
        if active:
            response = self.session.get(self.ACTIVE_URL)
            list_type = 'active'
        elif last_hour:
            response = self.session.get(self.NEW_LAST_HOUR_URL)
            list_type = 'new_last_hour'
        elif today:
            response = self.session.get(self.NEW_TODAY_URL)
            list_type = 'new_today'
        
        content = response.content
        for line in content.splitlines():
            self.spotted.save(
                    url=line,
                    source='phishingdatabase'
                )
            self.publisher.post(line)
