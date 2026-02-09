from variables.variables import Variables

class Memory:
    def __init__(self):
        self.variables = {}

    def declare(self, var_type, name, value):
        self.variables[name] = Variables(var_type, name, value)

    def get(self, name):
        if name not in self.variables:
            raise NameError(f"Змінна '{name}' не існує")
        return self.variables[name]

    def set(self, name, value):
        if name not in self.variables:
            raise NameError(f"Змінна '{name}' не існує")
        self.variables[name].set(value)