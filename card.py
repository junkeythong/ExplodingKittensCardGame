class Card:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name
