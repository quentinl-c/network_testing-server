import pika
import logging
import os
import json

EXCHANGE = 'broker'

# RabbitMQ Server
HOST = os.getenv('RABBITMQ_ADDRESS', '127.0.0.1')
PORT = os.getenv('RABBITMQ_PORT', 5672)


logging.basicConfig(filename=__name__ + '.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RMQCommunication(object):
    """docstring for RMQCommunication"""
    def __init__(self, controller):
        self.controller = controller
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
            HOST, PORT))
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(
            exchange=EXCHANGE, type='fanout')

    def broadcastStartSignal(self):
        msg = json.dumps({
            'recipient': 'all',
            'body': 'start'
            })
        self.__channel.basic_publish(exchange=EXCHANGE, routing_key='',
                                     body=msg)
