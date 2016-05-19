import json

# Default values
DEFAULT_EXP_NAME = "Experience"
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
        self.exp_name = DEFAULT_EXP_NAME
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

            if isinstance(decod_json['exp_name'], str):
                self.exp_name = decod_json['exp_name']

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

    def getJSONConfig(self):
        return {
            'exp_name': self.exp_name,
            'writers': self.writers,
            'readers': self.readers,
            'typing_speed': self.typing_speed,
            'duration': self.duration,
            'browser_by_node': self.browser_by_node,
            'target': self.target
            }
