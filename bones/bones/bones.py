import os, datetime
from mongoengine import connect
import yaml


class Bones(object):

    def __init__(self):
        self.client = connect(
            os.environ.get('MONGO_INITDB_NAME', 'entrails'),
            username=os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'root'),
            password=os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'example'),
            authentication_source='admin',
            host='entrails',
            port=int(os.environ.get('MONGO_INITDB_PORT', 27017)))
