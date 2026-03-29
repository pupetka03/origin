from core.errors import OriginNameError, OriginSyntaxError, OriginTypeError
from core.runtime import memory


SAFE_EVAL_GLOBALS = {"__builtins__": {}}


def safe_eval(expression):
    try:
        return eval(expression, SAFE_EVAL_GLOBALS, {})
    except Exception as exc:
        raise OriginSyntaxError(f"Помилка в обчисленні '{expression}': {exc}") from None


def parse_value(tokens, start_pos):
    pos = start_pos

    if pos >= len(tokens):
        raise OriginSyntaxError("Очікується значення після '='")

    if tokens[pos][0] == "LBRACE":
        return parse_expression_block(tokens, pos)

    if tokens[pos][0] == "LPAREN":
        pos += 1
        if pos >= len(tokens) or tokens[pos][0] != "COMMAND":
            raise OriginSyntaxError("Очікується виклик команди у дужках")

        command_name = tokens[pos][1]
        pos += 1

        if pos >= len(tokens) or tokens[pos][0] != "LPAREN":
            raise OriginSyntaxError(f"Команда '{command_name}' має бути викликана як {command_name}(...) ")
        pos += 1

        arg = []
        while pos < len(tokens) and tokens[pos][0] != "RPAREN":
            arg.append(tokens[pos])
            pos += 1

        if pos >= len(tokens) or tokens[pos][0] != "RPAREN":
            raise OriginSyntaxError(f"Не закрито виклик команди '{command_name}'")
        pos += 1

        if pos >= len(tokens) or tokens[pos][0] != "RPAREN":
            raise OriginSyntaxError("Не закрито зовнішні дужки виклику")
        pos += 1

        from commands.advanced import commands

        if command_name not in commands:
            raise OriginSyntaxError(f"Невідома команда '{command_name}'")

        result = commands[command_name](arg)
        return result, pos

    if tokens[pos][0] == "NUMBER":
        return tokens[pos][1], pos + 1

    if tokens[pos][0] == "STRING":
        return tokens[pos][1], pos + 1

    if tokens[pos][0] == "ID":
        return memory.get(tokens[pos][1]).const(), pos + 1

    raise OriginSyntaxError(f"Некоректне значення: {tokens[pos]}")


def parse_expression_block(tokens, start_pos):
    pos = start_pos

    if pos >= len(tokens) or tokens[pos][0] != "LBRACE":
        raise OriginSyntaxError("Очікується '{' на початку виразу")
    pos += 1

    expr_parts = []

    while pos < len(tokens) and tokens[pos][0] != "RBRACE":
        token_type, token_value = tokens[pos]

        if token_type == "LPAREN" and pos + 1 < len(tokens) and tokens[pos + 1][0] == "COMMAND":
            value, new_pos = parse_value(tokens, pos)
            expr_parts.append(str(value))
            pos = new_pos
            continue
        if token_type == "NUMBER":
            expr_parts.append(token_value)
        elif token_type == "ID":
            expr_parts.append(str(memory.get(token_value).const()))
        elif token_type == "OP":
            expr_parts.append(token_value)
        elif token_type in ["LPAREN", "RPAREN"]:
            expr_parts.append(token_value)
        else:
            raise OriginSyntaxError(f"Некоректний токен у виразі: {token_value}")

        pos += 1

    if pos >= len(tokens) or tokens[pos][0] != "RBRACE":
        raise OriginSyntaxError("Не закрито вираз у {}")
    pos += 1

    expression = " ".join(expr_parts)
    result = safe_eval(expression)
    return result, pos


def create_variables(instr):
    var = {
        "type": "",
        "name": "",
        "value": "",
    }

    i = 0
    while i < len(instr):
        token_type, token_value = instr[i]

        if token_type == "TYPE":
            var["type"] = token_value
            i += 1
            continue

        if token_type == "ID" and not var["name"]:
            var["name"] = token_value
            i += 1
            continue

        if token_type == "OP" and token_value == "=":
            i += 1
            value, next_pos = parse_value(instr, i)

            if var["type"] == "int":
                try:
                    value = int(value)
                except (TypeError, ValueError):
                    raise OriginTypeError(f"Змінна '{var['name']}' має тип int") from None
            elif var["type"] == "str":
                if not isinstance(value, str):
                    value = str(value)

            var["value"] = value
            i = next_pos
            continue

        i += 1

    if not var["name"]:
        raise OriginSyntaxError("Очікується ім'я змінної")
    if not var["type"]:
        raise OriginSyntaxError(f"Для змінної '{var['name']}' не вказано тип")

    return var
