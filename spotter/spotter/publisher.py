from .base import Base
import pika


class Publisher(Base):

    EXCHANGE = 'exchange'
    ROUTING_KEY = 'chum.bucket'

    def __init__(self, duration=None):
        self.duration = duration

    def post(self, value):
        parameters = pika.URLParameters(self.PUBLISHER_URL)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        result = channel.queue_declare(queue='chum', durable=True)
        
        self.__logger.debug('Publishing spotted URL: {}'.format(value))
        channel.basic_publish(
            exchange=self.EXCHANGE,
            routing_key=self.ROUTING_KEY,
            body='Publishing spotted URL: {}'.format(value),
            properties=pika.BasicProperties(
                delivery_mode = 2, # make message persistent
            )
        )
        connection.close()
