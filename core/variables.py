class Variables:
    def __init__(self, type, name, contents):
        self.type = type
        self.name = name
        self.contents = contents


    def __repr__(self):
        return f"Variables({self.type, self.name, self.contents})"



    def print_value(self):
        return (self.contents)
    
    def print_type(self):
        return self.type



