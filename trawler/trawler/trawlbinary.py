import hashlib, os, yaml

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse



__CONFIG__ = ''

with(open('./trawler/config.yml', 'r')) as ymlfile:
    __CONFIG__ = yaml.load(ymlfile, Loader=yaml.BaseLoader)

class BinaryTrawl(object):

    def __init__(self, url, network):
        self.network = network
        self.file_name = url.split('/')[-1] 
        self.netloc = urlparse(url).netloc
        self.download_location = '{}/{}'.format(__CONFIG__['download']['folder'], self.netloc.replace('.', '_'))
        self.url = url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def download(self):
        response = None
        if not os.path.exists(self.download_location):
            os.makedirs(self.download_location)
        try:
            response = self.network.head(self.url)
        except:
            print('File does not exist: {}'.format(self.url))
            return None
        try:
            print('Downloading File from {}'.format(self.url))
            download_location = '{}/{}'.format(self.download_location, self.file_name)
            return self.network.download(self.url, download_location)
        except:
            print('Unable to download binary: {}'.format(self.url))
            pass

    @property
    def md5(self):
        self.binary.seek(0)
        hash_object = hashlib.md5()
        for chunk in iter(lambda: self.binary.read(65536), b""):
            hash_object.update(chunk)

        return hash_object.hexdigest()

    @property
    def sha1(self):
        self.binary.seek(0)
        hash_object = hashlib.sha1()
        for chunk in iter(lambda: self.binary.read(65536), b""):
            hash_object.update(chunk)
            
        return hash_object.hexdigest()

    @property
    def sha256(self):
        self.binary.seek(0)
        hash_object = hashlib.sha256()
        for chunk in iter(lambda: self.binary.read(65536), b""):
            hash_object.update(chunk)
            
        return hash_object.hexdigest()