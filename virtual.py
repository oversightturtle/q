# Designed to create a virtual g/t when physically not connected

class grbl:
    def __init__(self):
        pass
    def write(self, a ):
        pass
grbl = grbl()

class tlc:
    def __init__(self):
        pass
    def write(self, a):
        pass
    def reset_input_buffer(self):
        pass
    def read(self, a):
        return "11111" # virtual response for paper pickup sensor reading

tlc = tlc()