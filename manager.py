from config_reader import ConfigReader
import os
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
            exchange=EXCHANGE, type='fanout')
        self.__ready = False

    def readConfig(self, path):
        self.config_reader = ConfigReader(path)
        output = self.config_reader.readFromFile()
        self.writers = self.config_reader.writers
        self.readers = self.config_reader.readers
        self.acknowledged_nodes = self.writers + self.readers
        self.__ready = output
        return output

    def __isAlreadyRegistered(self, node_id):
        return len([t for t in self.collaborators if t[0] == node_id]) > 0

    def addNode(self, node_id):
        if(self.__ready and (self.writers > 0 or self.readers > 0) and
           not self.__isAlreadyRegistered(node_id)):
            if self.writers > 0:
                status = 'r'
                self.writers -= 1
            elif self.readers > 0:
                status = 'w'
                self.readers -= 1
            else:
                print("=== UNKNOWN ERROR ===")
                return False

            self.collaborators.append((node_id, status))
            print("=== New node has been added, node_id : %s ===" % node_id)
            print("=== Remaining writers : %s ===" % self.writers)
            print("=== Remaining readers : %s ===" % self.readers)
            return True
        else:
            print("=== Node can't be added, node_id : %s ===" % node_id)
            return False

    def acknowledgeRegistration(self, node_id):
        if self.__ready and self.__isAlreadyRegistered(node_id):
            self.acknowledged_nodes -= 1
            print("=== Acknowledgement has been received from node_id %s ==="
                  % node_id)
            if self.acknowledged_nodes <= 0:
                print("=== Experience will start NOW ===")
                self.__sendStartSignal()

    def getConfig(self, node_id):
        role = [t[1] for t in self.collaborators if t[0] == node_id]
        msg = {
            'role': role[0],
            'config': self.config_reader.getJSONConfig()
        }
        return msg

    def saveResults(self, node_id, results):
        dirname = "./Results_" + self.config_reader.exp_name + "/"
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        file = open(dirname + str(node_id) + '_results', 'w')
        file.write(results)
        file.close()

    def __sendStartSignal(self):
        msg = json.dumps({
            'recipient': 'all',
            'body': 'start'
            })
        self.__channel.basic_publish(exchange=EXCHANGE, routing_key='',
                                     body=msg)
