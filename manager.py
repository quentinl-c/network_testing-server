from config_reader import ConfigReader
import json
import pika

# RabbitMQ Server
# HOST = '40.117.234.24'
HOST = '127.0.0.1'
PORT = 5672
EXCHANGE = 'broker'


class Manager(object):
    """docstring for Manager"""
    def __init__(self):
        self.collaborators = []
        self.ready = False
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
            HOST, PORT))
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(
            exchange='msg', type='fanout')

    def readConfig(self, path):
        self.config_reader = ConfigReader(path)
        output = self.config_reader.readFromFile()
        self.registered_nodes = self.config_reader.nodes_nbr
        self.acknowledged_nodes = self.config_reader.nodes_nbr
        return output

    def addNode(self, node_id):
        if self.registered_nodes > 0 and node_id not in self.collaborators:
            self.collaborators.append(node_id)
            self.registered_nodes -= 1
            print("=== New node has been added, node_id : %s ===" % node_id)
            return True
        else:
            print("=== Node can't be added, node_id : %s ===" % node_id)
            return False

    def acknowledgeRegistration(self, node_id):
        if node_id in self.collaborators:
            self.acknowledged_nodes -= 1
            print("=== Acknowledgement has been received from node_id %s ==="
                  % node_id)
            if self.acknowledged_nodes <= 0:
                print("=== Experience will start NOW ===")
                self.__sendStartSignal()

    def getConfig(self):
        return self.config_reader.getJSONConfig()

    def __sendStartSignal(self):
        msg = json.dumps({
            'recipient': 'all',
            'body': 'start'
            })
        self.__channel.basic_publish(exchange=EXCHANGE, routing_key='',
                                     body=msg)
