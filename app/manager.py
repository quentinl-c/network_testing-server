from config_reader import ConfigReader
import sys
import os
import string
import random
import json
import pika
import time

# RabbitMQ Server
# HOST = '40.117.234.24'
HOST = os.getenv('RABBITMQ_ADDRESS', '127.0.0.1')
PORT = os.getenv('RABBITMQ_PORT', 5672)
EXCHANGE = 'broker'

HOME_DIR = os.getenv('HOME_DIR', '/home/')

# Log File
log_file = open("server.log", 'w')
err_file = open("server.err", 'w')
sys.stdout = log_file
sys.stderr = err_file


class Manager(object):
    """docstring for Manager"""
    def __init__(self):
        self.collaborators = []
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
            HOST, PORT))
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(
            exchange=EXCHANGE, type='fanout')
        self.__ready = False
        self.__exp_sarted = False
        self.__exp_ended = False
        self.__beginning_time = 'Not yet started'
        self.__clients_saved = []
        self.words = []

    def readConfig(self, env_var, path):
        self.config_reader = ConfigReader(path)
        self.__ready = False
        if env_var:
            self.__ready = self.config_reader.readFromEnv()
        else:
            self.__ready = self.config_reader.readFromFile()

        self.writers = self.config_reader.writers
        self.readers = self.config_reader.readers

        self.acknowledged_nodes = self.writers + self.readers
        self.collaborators_nbr = self.acknowledged_nodes

        return self.__ready

    def __isAlreadyRegistered(self, node_id):
        return len([t for t in self.collaborators if t[0] == node_id]) > 0

    def __isAlreadySaved(self, node_id):
        return len([elt for elt in self.__clients_saved if elt == node_id]) > 0

    def addNode(self, node_id):
        if(self.__ready and (self.writers > 0 or self.readers > 0) and
           not self.__isAlreadyRegistered(node_id)):
            if self.readers > 0:
                status = 'r'
                self.readers -= 1
            elif self.writers > 0:
                status = 'w'
                self.writers -= 1
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
                self.__exp_sarted = True
                self.__beginning_time = time.strftime("%H:%M:%S")
                self.__sendStartSignal()

    def getConfig(self, node_id):
        role = [t[1] for t in self.collaborators if t[0] == node_id]
        msg = {
            'role': role[0],
            'config': self.config_reader.getJSONConfig(),
            'word': ''
        }
        if role[0] == 'w':
            msg['word'] = self.genUniqWord()
        return msg

    def genUniqWord(self):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        l = int(self.config_reader.typing_speed)

        if l <= 1:
            l = 2

        word = None
        while word is None or word in self.words:
            word = ''.join(
                random.SystemRandom().choice(chars) for _ in range(l - 1))
            word = word + '|'
        self.words.append(word)
        return word

    def saveResults(self, node_id, results):
        if not self.__isAlreadySaved(node_id):
            file = open(HOME_DIR + str(node_id) + '_results', 'w')
            file.write(results)
            file.close()
            self.__clients_saved.append(node_id)

            if len(self.__clients_saved) >= self.collaborators_nbr:
                self.exp_ended = True

    def getStatus(self):
        return {
            'writers': self.writers,
            'readers': self.readers,
            'is_exp_started': self.__exp_sarted,
            'is_exp_ended': self.__exp_ended,
            'beginning_time': self.__beginning_time,
            'waiting_acknowledgments': self.acknowledged_nodes
            }

    def __sendStartSignal(self):
        msg = json.dumps({
            'recipient': 'all',
            'body': 'start'
            })
        self.__channel.basic_publish(exchange=EXCHANGE, routing_key='',
                                     body=msg)
