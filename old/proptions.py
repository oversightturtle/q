import time



class proption:
    pront_instances = []
    def __init__ (self, inputs, name, function):
        self.name = name
        self.func = function
        self.inputs = inputs
        
        proption.pront_instances.append(self)

