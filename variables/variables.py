class Variables:
    def __init__(self, type, name, contents):
        self.type = type
        self.name = name
        self.contents = contents

    def __repr__(self):
        return f"Variables({self.type}, {self.name}, {self.contents})"

    def print_value(self):
        return self.contents

    def print_type(self):
        if self.type == "int":
            return "<class 'int'>"
        if self.type == "str":
            return "<class 'str'>"
        if self.type == "bool":
            return "<class 'bool'>"
        if self.type == "float":
            return "<class 'float'>"
        return f"<class '{self.type}'>"

    def const(self):
        return self.contents

    def set(self, value):
        self.contents = value
