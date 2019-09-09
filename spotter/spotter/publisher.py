#!/usr/bin/env python
import pika, logging, os

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

# Example Value in docker-compose.yml - 'amqp://trawl:spotter@rabbitmq/phish-tank?connection_attempts=5&retry_delay=5'
__PUBLISHER_URL__ = os.environ['AMQP_URL']



class Publisher(object):

    def __init__(self, duration=None):
        self.duration = duration

    def post(self, value):
        parameters = pika.URLParameters(__PUBLISHER_URL__)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        result = channel.queue_declare(queue='chum', durable=True)
        
        LOGGER.debug('Publishing spotted URL: {}'.format(value))
        channel.basic_publish(exchange='',
                      routing_key='chum.bucket',
                      body='Publishing spotted URL: {}'.format(value),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))

        connection.close()