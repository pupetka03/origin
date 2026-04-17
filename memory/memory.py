from core.errors import OriginNameError
from variables.variables import Variables


class Memory:
    def __init__(self):
        # Стек областей видимості. Початкова - глобальна.
        self.scopes = [{}]

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def declare(self, var_type, name, value):
        # Оголошення завжди відбувається в поточній (найглибшій) області
        current_scope = self.scopes[-1]
        
        if name in current_scope:
            # Якщо змінна вже є в ЦЬОМУ скоупі, оновлюємо її
            current_scope[name].type = var_type
            current_scope[name].set(value)
        else:
            # Якщо немає - створюємо нову
            current_scope[name] = Variables(var_type, name, value)

    def get(self, name):
        # Шукаємо від найглибшого скоупу до глобального
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise OriginNameError(f"Змінна '{name}' не існує")

    def set(self, name, value):
        # Оновлення шукає існуючу змінну в усіх доступних скоупах
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name].set(value)
                return
        raise OriginNameError(f"Змінна '{name}' не існує")
