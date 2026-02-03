from core.variables import Variables
from core.parser import parser
from commands.advanced import commands

type_u = ["int", "str"]
variables = {}



def test(tokens):
    for line in tokens:
        print(line)

def executor(file_name):

    result_of_terminale = ""
    tokens = parser(file_name)



    
    i = 0
    while i < len(tokens):
        token_type, token_val = tokens[i]


        # Створення/оновлення змінної
        if token_type == "ID" and token_val in type_u:
            var_type = token_val
            var_name = tokens[i + 1][1]
            # tokens[i + 2] це "="
            
            # Перевіряємо що справа від "="
            right_token_type = tokens[i + 3][0]
            right_token_val = tokens[i + 3][1]
            
            # Якщо це команда типу type(x)
            if right_token_type == "COMMAND":
                cmd_name = right_token_val
                cmd_arg = tokens[i + 5][1]  # токен всередині дужок
                var_value = commands[cmd_name](cmd_arg, variables)
                i += 7  # тип, назва, =, команда, (, аргумент, )
            # Якщо це просте значення
            else:
                var_value = right_token_val
                
                # Конвертація типу
                try:
                    if var_type == 'int':
                        var_value = int(var_value)
                    elif var_type == 'str':
                        var_value = str(var_value)
                except ValueError:
                    print(f"Origin invalid type error {var_type} is not {var_value}")
                    return True
                
                i += 4  # тип, назва, =, значення
            
            # Створення/оновлення змінної
            variables[var_name] = Variables(var_type, var_name, var_value)
        
        # Виклик команди без присвоєння (print, тощо)
        elif token_type == "COMMAND":
            name = token_val
            var = tokens[i + 2][1]

            try:
                tab = tokens[i + 4][1]
            except:
                tab = 0


            result = commands[name](var, variables)

            if tab:
                result_of_terminale += str(result) + "\n"
            else:
                result_of_terminale += str(result)

            

            i += 4  # команда, (, аргумент, )
        
        else:
            i += 1

    print(result_of_terminale)