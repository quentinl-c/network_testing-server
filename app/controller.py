from config_loader import ConfigLoader
from clients_manager import ClientsManager
from rmq_communication import RMQCommunication
from persistence_manager import PersistenceManager
import sys
import os
import json
import time
import logging


logging.basicConfig(filename=__name__ + '.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Controller(object):
    """docstring for Manager"""
    def __init__(self):
        self.__exp_sarted = False
        self.__exp_ended = False
        self.ready = False
        self.__beginning_time = 'Not yet started'
        self.__persistence_manager = PersistenceManager(self)

    def readConfig(self, env_var, path):
        self.__config_loader = ConfigLoader(path)
        self.ready = False
        if env_var:
            self.ready = self.__config_loader.readFromEnv()
        else:
            self.ready = self.__config_loader.readFromFile()

        writers = self.__config_loader.writers
        readers = self.__config_loader.readers
        initial_collabs = self.__config_loader.initial_collabs
        typing_speed = self.__config_loader.typing_speed

        self.__clients_manager = ClientsManager(self,
                                                readers,
                                                writers,
                                                initial_collabs,
                                                typing_speed)

        return self.ready

    def addNode(self, node_id):
        return self.__clients_manager.addNode(node_id)

    def acknowledgeRegistration(self, node_id):
        self.__clients_manager.acknowledgeRegistration(node_id)

    def saveResults(self, node_id, results):
        self.__persistence_manager.saveResults(node_id, results)

    def startExp(self):
        logger.debug("=== Experience will start NOW ===")
        self.__exp_sarted = True
        self.__beginning_time = time.strftime("%H:%M:%S")
        self.__rmq_communication = RMQCommunication(self)
        self.__rmq_communication.broadcastStartSignal()

    def getReadyCollabsNmbr(self):
        return self.__clients_manager.getReadyCollabsNmbr()

    def getNoAckCollabsNmbr(self):
        return self.__clients_manager.getNoAckCollabsNmbr()

    def getStatus(self):
        return {
            'ready': self.getReadyCollabsNmbr(),
            'no_ack': self.getNoAckCollabsNmbr(),
            'is_exp_started': self.__exp_sarted,
            'is_exp_ended': self.__exp_ended,
            'beginning_time': self.__beginning_time,
            }

    def getConfig(self):
        return self.__config_loader.getJSONConfig()
