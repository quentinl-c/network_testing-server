class Manager(object):
    """docstring for Manager"""
    def __init__(self):
        self.collaborators = []
        self.ready = False

    def readConfig(self, path):
        self.config_reader = ConfigReader(path)
        self.config_reader.readFromFile()
        self.remaining_nodes = self.config_reader.nodes_nbr

    def getNumbersCollabs(self):
        return len(self.collaborators)

    def getRemainingCollabs(self):
        return self.remaining_nodes

    def addNode(self, node_id):
        if self.remaining_nodes > 0 and node_id not in self.collaborators:
            self.collaborators.append(node_id)
            self.remaining_nodes -= 1
            return True
        else:
            return False

    def getConfig(self):
        return self.config_reader.getJSONConfig()
