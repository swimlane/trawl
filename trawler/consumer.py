#!/usr/bin/env python
import pika, logging, os

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

# Example Value in docker-compose.yml - 'amqp://trawl:spotter@rabbitmq/phish-tank?connection_attempts=5&retry_delay=5'
__CONSUMER_URL__ = os.environ['AMQP_URL']


class Consumer(object):

    def __init__(self, duration=None):
        self.duration = duration

    def get(self):
        parameters = pika.URLParameters(__CONSUMER_URL__)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        result = channel.queue_declare(queue='chum', durable=True)
       
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='chum',
                      on_message_callback=self.callback)

       
        LOGGER.debug('Retrieving spotted URL:')
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        from trawler import Trawler
        trawl = Trawler().trawl(body)
        print(trawl)
        # We do stuff here before acknowledging delivery

        ch.basic_ack(delivery_tag=method.delivery_tag)

publisher = Consumer().get()