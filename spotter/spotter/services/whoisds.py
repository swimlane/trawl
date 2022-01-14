import base64
from datetime import date, datetime, timedelta
from io import BytesIO
from zipfile import ZipFile
from ..base import Base


class WhoisDs(Base):

    URL = 'https://whoisds.com//whois-database/newly-registered-domains'

    def get(self):
        latest_list = []
        past = datetime.strftime(self.now - timedelta(self.config['whoisds']['check-interval']['days']), "%Y-%m-%d")

        filename = "{}.zip".format(past)
        encoded_filename = base64.b64encode(filename.encode('utf-8'))
        self.__logger.info('In WHOISDS and getting data')
        response = self.session.get('{url}/{file_name}/nrd'.format(url=self.URL, file_name=encoded_filename.decode('ascii')))
        with BytesIO(response.content) as zip_file:
            with ZipFile(zip_file) as zip_file:
                for zip_info in zip_file.infolist():
                    with zip_file.open(zip_info) as ffile:
                        for line in ffile.readlines():
                            latest_list.append(str(line, 'utf-8').rstrip())

        return latest_list