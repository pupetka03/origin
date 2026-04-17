from commands.advanced import commands
from core.errors import OriginSyntaxError
from core.parser import parser
from core.runtime import memory
from variables.factory import create_variables


type_u = ["int", "str"]


def read_block_instruction(tokens, pos):
    i = pos
    instruc = []
    depth = 0
    block_commands = {"for", "if", "while", "func"}

    while i < len(tokens):
        token = tokens[i]
        token_type, token_value, *pos_info = token
        instruc.append(token)

        if token_type == "COMMAND" and token_value in block_commands:
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

    if depth > 0:
        # Беремо позицію першого токена блоку для помилки
        l, c = (instruc[0][2], instruc[0][3]) if len(instruc) > 0 and len(instruc[0]) > 3 else (None, None)
        raise OriginSyntaxError(f"Незавершений блок '{instruc[0][1]}': очікується 'end;'", line=l, column=c)

    return instruc, i


def read_instruction(tokens, pos):
    i = pos
    instruc = []

    if i < len(tokens) and tokens[i][0] == "COMMAND":
        command_name = tokens[i][1]
        if command_name in ["for", "if", "while", "func"]:
            return read_block_instruction(tokens, pos)

    while i < len(tokens):
        token = tokens[i]
        token_type, token_value, *pos_info = token
        instruc.append(token)
        if token_type == "SEMICOL":
            return instruc, i + 1
        i += 1

    if instruc:
        # Отримуємо позицію останнього токена інструкції
        last_token = instruc[-1]
        l, c = (last_token[2], last_token[3]) if len(last_token) > 3 else (None, None)
        raise OriginSyntaxError("Очікується ';' у кінці інструкції", line=l, column=c)

    return instruc, i


def execute_tokens(tokens):
    i = 0
    while i < len(tokens):
        instruction, i = read_instruction(tokens, i)

        if not instruction:
            continue

        first_token = instruction[0]
        first_type, first_value, *first_pos = first_token
        line = first_pos[0] if first_pos else None
        col = first_pos[1] if len(first_pos) > 1 else None

        if first_type == "TYPE" and first_value in type_u:
            variable = create_variables(instruction)
            memory.declare(variable["type"], variable["name"], variable["value"])
            continue

        if first_type == "COMMAND":
            if first_value not in commands:
                raise OriginSyntaxError(f"Команда '{first_value}' ще не підтримується", line=line, column=col)
            commands[first_value](instruction)
            continue

        raise OriginSyntaxError(f"Некоректна інструкція: {first_value}", line=line, column=col)


def executor(file_name):
    tokens = parser(file_name)
    execute_tokens(tokens)
