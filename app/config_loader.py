import json
import os
import logging

# Default values
DEFAULT_NODES_NBR = 1
DEFAULT_TYPING_SPEED = 1
DEFAULT_DURATION = 60
DEFAULT_TARGET = 'http://localhost:8080/doc/peer/test'

# Min threasholds
MIN_NODES_NBR = 1
MIN_TYPING_SPEED = 1
MIN_DURATION = 15

logging.basicConfig(filename=__name__ + '.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ConfigLoader(object):
    """docstring for ConfigReader"""
    def __init__(self, path):
        self.__path = path
        self.writers = DEFAULT_NODES_NBR
        self.readers = DEFAULT_NODES_NBR
        self.initial_collabs = 2 * DEFAULT_NODES_NBR
        self.typing_speed = DEFAULT_TYPING_SPEED
        self.duration = DEFAULT_DURATION
        self.target = DEFAULT_TARGET

    def readFromFile(self):
        output = True
        self.__file = open(self.__path, "r")
        content = self.__file.read()

        try:
            decod_json = json.loads(content)

            if(isinstance(decod_json['writers'], int) and
               decod_json['writers'] >= MIN_NODES_NBR):
                self.writers = int(decod_json['writers'])

            if(isinstance(decod_json['readers'], int) and
               decod_json['readers'] >= MIN_NODES_NBR):
                self.readers = int(decod_json['readers'])

            if 'initial_collabs' in decod_json:
                if(isinstance(decod_json['initial_collabs'], int) and
                   decod_json['readers'] >= MIN_NODES_NBR):
                    self.initial_collabs = int(decod_json['readers'])
            else:
                self.initial_collabs = self.readers + self.writers

            if(isinstance(decod_json['typing_speed'], int) and
               decod_json['typing_speed'] >= MIN_TYPING_SPEED):
                self.typing_speed = int(decod_json['typing_speed'])

            if(isinstance(decod_json['duration'], int) and
               decod_json['duration'] >= MIN_DURATION):
                self.duration = int(decod_json['duration'])

            if isinstance(decod_json['target'], str):
                self.target = decod_json['target']

        except Exception:
            logging.exception("Format error")
            output = False
        finally:
            self.__file.close()
            return output

    def readFromEnv(self):
        self.writers = int(os.getenv('WRITERS', 10))
        self.readers = int(os.getenv('READERS', 10))
        self.initial_collabs = int(os.getenv('INITIAL_COLLABS',
                                             self.readers + self.writers))
        self.typing_speed = int(os.getenv('TYPING_SPEED', 2))
        self.duration = int(os.getenv('DURATION', 36000))
        self.target = os.getenv('TARGET', "http://localhost:8080/peer/doc/a")
        return True

    def getJSONConfig(self):
        return {
            'writers': self.writers,
            'readers': self.readers,
            'typing_speed': self.typing_speed,
            'duration': self.duration,
            'target': self.target
            }
