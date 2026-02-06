from core.variables import Variables
from core.parser import parser
from commands.advanced import commands

type_u = ["int", "str"]
variables = {}

def test(tokens):
    for i in (tokens):
        print(i)

def parse_value(tokens, start_pos):
    """
    Парсить значення (вираз справа від =)
    Повертає: (value, next_position)
    """
    pos = start_pos


    # Перевіряємо чи це функція/команда
    if tokens[pos][0] == "LPAREN":
        # Пропускаємо (
        pos += 1
        
        if tokens[pos][0] == "COMMAND":
            command_name = tokens[pos][1]
            pos += 1
            
            # Пропускаємо (
            if tokens[pos][0] == "LPAREN":
                pos += 1
            
            # Отримуємо аргумент
            arg = []
            while tokens[pos][0] != "RPAREN":
                line = tokens[pos]
                arg.append(line)
                pos += 1
            
            # Пропускаємо )
            if tokens[pos][0] == "RPAREN":
                pos += 1
            
            # Пропускаємо зовнішню )
            if tokens[pos][0] == "RPAREN":
                pos += 1
            
            # Виконуємо команду
            from commands.advanced import commands
            result = commands[command_name](arg, variables)
            return result, pos
    
    # Якщо це просте число
    elif tokens[pos][0] == "NUMBER":
        return tokens[pos][1], pos + 1
    
    # Якщо це рядок
    elif tokens[pos][0] == "STRING":
        return tokens[pos][1], pos + 1
    
    # Якщо це змінна
    elif tokens[pos][0] == "ID" and tokens[pos][1] in variables:
        return variables[tokens[pos][1]].const(), pos + 1
    
    return None, pos


def create_variables(instr):
    var = {
        "type": '', 
        "name": '', 
        "value": '',
        }
    
    i = 0
    while i < len(instr):
        el = instr[i]
        
        # Отримуємо тип
        if el[0] == "TYPE":
            var['type'] = el[1]
            i += 1
            continue
        
        # Отримуємо ім'я
        if el[0] == "ID" and not var["name"]:
            var["name"] = el[1]
            i += 1
            continue
        
        # Знак =
        if el[0] == "OP" and el[1] == "=":
            i += 1
            # тут логіка AI
            value, next_pos = parse_value(instr, i)


            if var["type"] == "int":
                try:
                    int(value) == int
                except:
                    TypeError
            
            var["value"] = value
            i = next_pos
            continue
        
        i += 1
    
    if not var["name"]:
        return None
    
    return var         

def read_instruction(tokens, pos):
    i = pos
    instruc = []

    while i < (len(tokens)):
        token_type, token_value = tokens[i] 
        instruc.append((token_type, token_value))

        if token_type == "SEMICOL":
            return instruc, i + 1


        i += 1

    return instruc, i


def executor(file_name):
    tokens = parser(file_name)

    i = 0
    while(i < len(tokens)):
        instruction, i = read_instruction(tokens, i)

        #test(instruction)

        if not instruction:
            continue


        if instruction[0][1] in type_u:
            variable = create_variables(instruction)

            if variable is not None:
                variables[variable["name"]] = Variables(
                    variable["type"], 
                    variable["name"], 
                    variable["value"])
                

        

        elif instruction[0][0] == "COMMAND":
            name = instruction[0][1]
            result = commands[name](instruction, variables)
            



