import yaml

from .UCException import *
from .UCConfig import *
from .UCModel import *
from .validators import *
from .UCChain import *

class uniformConfig:

    def __init__(self, modelPath=False, configPath=False):
        self.conf = UCConfig(configPath)
        self.model = UCModel(modelPath)

    def addModel(self, modelPath):
        md = UCModel(modelPath)
        for prop in md.data:
            if prop in self.model.data:
                raise UCException("addModel failed, duplicate field: '%s'" % prop)
        self.model.data.update(md.data)
        return self

    def fill(self, dataPath):
        if dataPath.endswith('.yml'):
            return self.fillYaml(dataPath)
        raise UCException("unknown format file : '%s'" % dataPath) # TODO better error there

    def fillYaml(self, dataPath):
        loadData = yaml.load(open(dataPath, 'r'))
        return self.setRecursive(loadData)

    def has(self, key):
        chain = self.__toChain(key)
        return self.model.has(chain)

    def get(self, key):
        chain = self.__toChain(key)
        return self.model.get(chain)

    def set(self, key, value):
        chain = self.__toChain(key)
        self.model.set(chain, value)

    def setRecursive(self, values, chain=UCChain('')):
        if isinstance(values, dict):
            for prop in values:
                self.setRecursive(values[prop], chain.add(prop))
        else:
            self.set(chain, values)

    def export(self):
        data = self.model.export()
        return yaml.dump(data, default_flow_style=False)

    def exportFile(self, filePath):
        data = self.model.export()
        fd = open(filePath, 'w')
        yaml.dump(data, fd, default_flow_style=False)

    def __toChain(self, key):
        if not isinstance(key, UCChain):
            return UCChain(key)
        return key
