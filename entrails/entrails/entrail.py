from mongoengine import connect
import os, datetime

__DB_PORT__ = 27017
__DB_NAME__ = 'entrails'


class Entrail(object):

    def __init__(self):
        self.client = connect(
            __DB_NAME__,
            username=os.environ['MONGO_INITDB_ROOT_USERNAME'],
            password=os.environ['MONGO_INITDB_ROOT_PASSWORD'],
            authentication_source='admin',
            host='entrails',
            port=__DB_PORT__)
        
        
