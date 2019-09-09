try:
    from urllib.parse import urlparse, urlencode
except ImportError:
    from urlparse import urlparse

class Skin(object):

    def url(self, value):
        url = value.strip()
        url = url.replace('_','')
        
        print(url)
        if url[0:7] == 'http://' or url[0:8] == 'https://':
            url = url.replace('[','')
            url = url.replace(']','')

            if url.endswith('//'):
                url = url[:-2]
            
            if not url.endswith('/'):
                url = '{}/'.format(url)
            print(url)
            return url
        if url[0:7] != 'http://':
            if url.startswith('/'):
                url = value.replace('/', 'http://', 1)
            if url.startswith('hxxp') or url.startswith('hXXp'):
                url = url.replace('hxxp', 'http').replace('hXXp', 'http')
        elif url[0:8] != 'https://':
            if url.startswith('hxxps') or url.startswith('hXXps'):
                url = url.replace('hxxps', 'https').replace('hXXps', 'https')
        else:
            url = 'http://{}'.format(url)
        
        print(url)
        url = url.replace('[','')
        url = url.replace(']','')

        if url.endswith('//'):
            url = url[:-2]
        
        if not url.endswith('/'):
            url = '{}/'.format(url)
        return url