import json
import os

# Default values
DEFAULT_NODES_NBR = 1
DEFAULT_TYPING_SPEED = 1
DEFAULT_DURATION = 60
DEFAULT_TARGET = 'http://localhost:8080/doc/peer/test'

# Min threasholds
MIN_NODES_NBR = 1
MIN_TYPING_SPEED = 1
MIN_DURATION = 15


class ConfigReader(object):
    """docstring for ConfigReader"""
    def __init__(self, path):
        self.__path = path
        self.writers = DEFAULT_NODES_NBR
        self.readers = DEFAULT_NODES_NBR
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
                self.writers = decod_json['writers']

            if(isinstance(decod_json['readers'], int) and
               decod_json['readers'] >= MIN_NODES_NBR):
                self.readers = decod_json['readers']

            if(isinstance(decod_json['typing_speed'], int) and
               decod_json['typing_speed'] >= MIN_TYPING_SPEED):
                self.typing_speed = decod_json['typing_speed']

            if(isinstance(decod_json['duration'], int) and
               decod_json['duration'] >= MIN_DURATION):
                self.duration = decod_json['duration']

            if isinstance(decod_json['target'], str):
                self.target = decod_json['target']

        except Exception:
            output = False
        finally:
            self.__file.close()
            return output

    def readFromEnv(self):
        self.writers = os.getenv('WRITERS', 10)
        self.readers = os.getenv('READERS', 10)
        self.typing_speed = os.getenv('TYPING_SPEED', 2)
        self.duration = os.getenv('DURATION', 36000)
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
