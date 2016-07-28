import logging
import os

HOME_DIR = os.getenv('HOME_DIR', '/home/')

logging.basicConfig(filename=__name__ + '.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PersistenceManager(object):
    """docstring for PersistenceManager"""
    def __init__(self, controller):
        self.__controller = controller
        self.__clients_saved = []

    def __isAlreadySaved(self, node_id):
        return len([elt for elt in self.__clients_saved if elt == node_id]) > 0

    def __getSaveClientsNbr(self):
        return len(self.__clients_saved)

    def saveResults(self, node_id, results):
        if not self.__isAlreadySaved(node_id):
            file = open(HOME_DIR + str(node_id) + '_results.txt', 'w')
            file.write(results)
            file.close()
            self.__clients_saved.append(node_id)

            if(self.__getSaveClientsNbr() >=
               self.__controller.getReadyCollabsNmbr()):
                self.__exp_ended = True
