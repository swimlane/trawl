#!/usr/bin/env python
import os
import pika

class Consumer(object):

    EXCHANGE = 'exchange'
    ROUTING_KEY = 'chum.bucket'
    CONSUMER_URL = os.environ['AMQP_URL']

    def __init__(self, duration=None):
        self.duration = duration

    def get(self):
        parameters = pika.URLParameters(self.CONSUMER_URL)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        result = channel.queue_declare(queue='chum', durable=True)
       
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='chum',
                      on_message_callback=self.callback)

       
        print(f'Retrieving spotted URL:', flush=True)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body, flush=True)
        from trawler.trawler import Trawler
        trawl = Trawler().trawl(body)
        print(trawl)
        # We do stuff here before acknowledging delivery

        ch.basic_ack(delivery_tag=method.delivery_tag)

publisher = Consumer().get()