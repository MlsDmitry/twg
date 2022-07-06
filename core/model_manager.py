from os import getcwd
from os.path import exists, join

from core import Singleton


class ModelManager(metaclass=Singleton):
    def __init__(self, loader=None):
        self.models = {}
        self.loader = loader


    def load(self, name, file_path):
        assert name not in self.models, 'This model name is already used.'
        assert exists(join(getcwd(), file_path)), 'Model file does not exists. File path: ' + join(getcwd(), file_path)

        model = self.loader.loadModel(file_path)
        self.models[name] = model
        
        return model

    def get(self, name):
        assert name in self.models, 'Model with this name does not exists.'

        return self.models[name]
