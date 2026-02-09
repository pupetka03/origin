from variables.variables import Variables
from core.parser import parser
from commands.advanced import commands
from variables.factory import create_variables
from core.runtime import memory

type_u = ["int", "str"]

def read_block_instruction(tokens, pos):
    i = pos
    instruc = []
    
    # Перевіряємо чи це for (без start/end глибини)
    if tokens[pos][1] == "for":
        while i < len(tokens):
            token_type, token_value = tokens[i]
            instruc.append((token_type, token_value))
            
            # Для for зупиняємось на end;
            if token_type == "COMMAND" and token_value == "end":
                i += 1
                if i < len(tokens) and tokens[i][0] == "SEMICOL":
                    instruc.append(tokens[i])
                    i += 1
                return instruc, i  
            i += 1
    
    # Для інших команд (if, while, func) - стара логіка з depth
    depth = 0
    while i < len(tokens):
        token_type, token_value = tokens[i]
        instruc.append((token_type, token_value))
        
        if token_type == "COMMAND" and token_value == "start":
            depth += 1
        elif token_type == "COMMAND" and token_value == "end":
            depth -= 1
            if depth == 0:
                i += 1
                if i < len(tokens) and tokens[i][0] == "SEMICOL":
                    instruc.append(tokens[i])
                    i += 1
                return instruc, i
        i += 1
    
    return instruc, i

def read_instruction(tokens, pos):
    i = pos
    instruc = []
    if i < len(tokens) and tokens[i][0] == "COMMAND":
        command_name = tokens[i][1]
        if command_name in ["for", "if", "while", "func"]:
            return read_block_instruction(tokens, pos)
    
    while i < (len(tokens)):
        token_type, token_value = tokens[i] 
        instruc.append((token_type, token_value))
        if token_type == "SEMICOL":
            return instruc, i + 1
        i += 1
    return instruc, i

def execute_tokens(tokens):
    """Виконує вже розпарсені токени"""
    i = 0
    while(i < len(tokens)):
        instruction, i = read_instruction(tokens, i)
        if not instruction:
            continue
        
        if instruction[0][1] in type_u:
            variable = create_variables(instruction)
            if variable is not None:
                memory.declare(
                    variable["type"], 
                    variable["name"], 
                    variable["value"]
                )
        elif instruction[0][0] == "COMMAND":
            name = instruction[0][1]
            result = commands[name](instruction)


def executor(file_name):
    tokens = parser(file_name)
    execute_tokens(tokens)