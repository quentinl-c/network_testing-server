import logging
import string
import random

logging.basicConfig(filename=__name__ + '.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ClientsManager(object):
    """docstring for ClientsManager"""
    def __init__(self, controller, readers, writers, initial_collabs,
                 typing_speed):
        self.__controller = controller
        self.__collaborators = dict()  # Stores all collaborators
        self.__collaborators['ready'] = list()  # collaborators which are ready
        self.__collaborators['waiting_signal'] = list()
        self.__collaborators['no_ack'] = list()
        self.__readers = readers
        self.__writers = writers
        self.__initial_collabs = initial_collabs
        self.typing_speed = typing_speed
        self.words = []  # words given to each collaborator

    """
    Private methods
    """
    def __isAlreadyRegistered(self, node_id):
        return len(
            [t for t in self.__collaborators['no_ack'] if t[0] == node_id]) > 0

    def __genUniqWord(self):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        l = int(self.typing_speed)

        if l <= 2:
            l = 3

        word = None
        while word is None or word in self.words:
            word = ''.join(
                random.SystemRandom().choice(chars) for _ in range(l - 1))
        self.words.append(word)

        return word

    def __getWaitingMessage(self):
        msg = {
            'config': self.__controller.getConfig(),
            'waiting': True,
            'word': '',
            'error': False,
            'error_msg': ''
        }

        return msg

    def __getConfigMessage(self, node_id, role):
        msg = {
            'config': self.__controller.getConfig(),
            'waiting': False,
            'word': '',
            'error': False,
            'error_msg': ''
        }

        if role[0] == 'w':
            msg['word'] = self.__genUniqWord()

        return msg

    def __getErrorMessage(self):
        msg = {
            'config': '',
            'waiting': False,
            'word': '',
            'error': True,
            'error_msg': ''
        }
        return msg

    """
    Public methods
    """
    def addNode(self, node_id):
        if self.__controller.ready and not self.__isAlreadyRegistered(node_id):
            if self.__initial_collabs > 0:
                if self.__readers > 0:
                    role = 'r'
                    self.__readers -= 1
                elif self.__writers > 0:
                    role = 'w'
                    self.__writers -= 1
                else:
                    logger.warning("=== UNKNOWN ERROR ===")
                    return self.__getErrorMessage('Error : initial_collabs is greater\
                                         than collaborators number')
            elif self.__readers > 0 and self.__writers > 0:
                self.__collaborators['no_ack'].append((node_id, role))
                return self.__getWaitingMessage()
            else:
                logger.warning("=== UNKNOWN ERROR ===")
                return self.__getErrorMessage('Error : unknown error')

            self.__initial_collabs -= 1
            self.__collaborators['no_ack'].append((node_id, role))
            logger.debug("=== New node has been added, node_id : %s ===" %
                         node_id)
            logger.debug("=== Remaining writers : %s ===" % self.__writers)
            logger.debug("=== Remaining readers : %s ===" % self.__readers)

            return self.__getConfigMessage(node_id, role)
        else:
            logger.debug("=== Node can't be added, node_id : %s ===" % node_id)
            return self.__getErrorMessage('exceeded quota or node already\
                                          registrated')

    def acknowledgeRegistration(self, node_id):
        if self.__controller.ready and self.__isAlreadyRegistered(node_id):
            logger.debug("=== Acknowledgement has been received from node_id  \
                         %s ===" % node_id)
            if self.__initial_collabs <= 0:
                self.__controller.startExp()

    def getReadyCollabsNmbr(self):
        return len(self.__collaborators['ready'])

    def getNoAckCollabsNmbr(self):
        return len(self.__collaborators['no_ack'])
