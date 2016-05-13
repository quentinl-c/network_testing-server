import json

# Default values
DEFAULT_EXP_NAME = "Experience"
DEFAULT_NODES_NBR = 2
DEFAULT_TYPING_SPEED = 1
DEFAULT_DURATION = 60
DEFAULT_BROWSER_BY_NODE = 1

# Min threasholds
MIN_NODES_NBR = 2
MIN_TYPING_SPEED = 1
MIN_DURATION = 15
MIN_BROWSER_BY_NODE = 1


class ConfigReader(object):
    """docstring for ConfigReader"""
    def __init__(self, path):
        self.__path = path
        self.exp_name = DEFAULT_EXP_NAME
        self.nodes_nbr = DEFAULT_NODES_NBR
        self.typing_speed = DEFAULT_TYPING_SPEED
        self.duration = DEFAULT_DURATION
        self.browser_by_node = DEFAULT_BROWSER_BY_NODE

    def readFromFile(self):
        output = True
        self.__file = open(self.__path, "r")
        content = self.__file.read()

        try:
            decod_json = json.loads(content)

            if isinstance(decod_json['exp_name'], str):
                self.exp_name = decod_json['exp_name']

            if isinstance(decod_json['nodes_nbr'], int) and decod_json['nodes_nbr'] >= MIN_NODES_NBR:
                self.nodes_nbr = decod_json['nodes_nbr']

            if isinstance(decod_json['typing_speed'], int) and decod_json['typing_speed'] >= MIN_TYPING_SPEED:
                self.typing_speed = decod_json['typing_speed']

            if isinstance(decod_json['duration'], int) and decod_json['duration'] >= MIN_DURATION:
                self.duration = decod_json['duration']

            if isinstance(decod_json['browser_by_node'], int) and decod_json['browser_by_node'] >= MIN_TYPING_SPEED:
                self.browser_by_node = decod_json['browser_by_node']

        except Exception:
            output = False
        finally:
            self.__file.close()
            return output

    def getJSONConfig(self):
        return json.dumps({
            'exp_name': self.exp_name,
            'nodes_nbr': self.nodes_nbr,
            'typing_speed': self.typing_speed,
            'duration': self.duration,
            'browser_by_node': self.browser_by_node
            })
