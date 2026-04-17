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
        # Отримуємо позицію попереднього токена (ймовірно '=')
        l, c = (tokens[pos-1][2], tokens[pos-1][3]) if pos > 0 and len(tokens[pos-1]) > 3 else (None, None)
        raise OriginSyntaxError("Очікується значення після '='", line=l, column=c)

    first_token = tokens[pos]
    token_type, token_value, *pos_info = first_token
    line = pos_info[0] if pos_info else None
    col = pos_info[1] if len(pos_info) > 1 else None

    if token_type == "LBRACE":
        return parse_expression_block(tokens, pos)

    if token_type == "LPAREN":
        pos += 1
        if pos >= len(tokens):
            raise OriginSyntaxError("Очікується виклик команди у дужках", line=line, column=col)
        
        token_type, token_value, *pos_info = tokens[pos]
        if token_type != "COMMAND":
            raise OriginSyntaxError("Очікується виклик команди у дужках", line=line, column=col)

        command_name = token_value
        pos += 1

        if pos >= len(tokens) or tokens[pos][0] != "LPAREN":
            raise OriginSyntaxError(f"Команда '{command_name}' має бути викликана як {command_name}(...) ", line=line, column=col)
        pos += 1

        arg = []
        while pos < len(tokens) and tokens[pos][0] != "RPAREN":
            arg.append(tokens[pos])
            pos += 1

        if pos >= len(tokens) or tokens[pos][0] != "RPAREN":
            raise OriginSyntaxError(f"Не закрито виклик команди '{command_name}'", line=line, column=col)
        pos += 1

        if pos >= len(tokens) or tokens[pos][0] != "RPAREN":
            raise OriginSyntaxError("Не закрито зовнішні дужки виклику", line=line, column=col)
        pos += 1

        from commands.advanced import commands

        if command_name not in commands:
            raise OriginSyntaxError(f"Невідома команда '{command_name}'", line=line, column=col)

        result = commands[command_name](arg)
        return result, pos

    if token_type == "NUMBER":
        return token_value, pos + 1

    if token_type == "STRING":
        return token_value, pos + 1

    if token_type == "ID":
        try:
            return memory.get(token_value).const(), pos + 1
        except Exception:
            raise OriginNameError(f"Змінна '{token_value}' не знайдена", line=line, column=col)

    raise OriginSyntaxError(f"Некоректне значення: {token_value}", line=line, column=col)


def parse_expression_block(tokens, start_pos):
    pos = start_pos

    if pos >= len(tokens) or tokens[pos][0] != "LBRACE":
        l, c = (tokens[pos][2], tokens[pos][3]) if pos < len(tokens) and len(tokens[pos]) > 3 else (None, None)
        raise OriginSyntaxError("Очікується '{' на початку виразу", line=l, column=c)
    
    first_token = tokens[pos]
    line, col = (first_token[2], first_token[3]) if len(first_token) > 3 else (None, None)
    pos += 1

    expr_parts = []

    while pos < len(tokens) and tokens[pos][0] != "RBRACE":
        token = tokens[pos]
        token_type, token_value, *pos_info = token

        if token_type == "LPAREN" and pos + 1 < len(tokens) and tokens[pos + 1][0] == "COMMAND":
            value, new_pos = parse_value(tokens, pos)
            expr_parts.append(str(value))
            pos = new_pos
            continue
        if token_type == "NUMBER":
            expr_parts.append(token_value)
        elif token_type == "ID":
            try:
                expr_parts.append(str(memory.get(token_value).const()))
            except Exception:
                l, c = (pos_info[0], pos_info[1]) if pos_info else (None, None)
                raise OriginNameError(f"Змінна '{token_value}' не знайдена", line=l, column=c)
        elif token_type == "OP":
            expr_parts.append(token_value)
        elif token_type in ["LPAREN", "RPAREN"]:
            expr_parts.append(token_value)
        else:
            l, c = (pos_info[0], pos_info[1]) if pos_info else (None, None)
            raise OriginSyntaxError(f"Некоректний токен у виразі: {token_value}", line=l, column=c)

        pos += 1

    if pos >= len(tokens) or tokens[pos][0] != "RBRACE":
        raise OriginSyntaxError("Не закрито вираз у {}", line=line, column=col)
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
    assigned = False
    
    while i < len(instr):
        token = instr[i]
        token_type, token_value, *pos_info = token
        line, col = (pos_info[0], pos_info[1]) if pos_info else (None, None)

        if token_type == "SEMICOL":
            break

        if token_type == "TYPE":
            if var["type"]:
                raise OriginSyntaxError(f"Дублювання типу: {token_value}", line=line, column=col)
            var["type"] = token_value
            i += 1
            continue

        if token_type == "ID" and not var["name"]:
            var["name"] = token_value
            i += 1
            continue

        if token_type == "OP" and token_value == "=":
            if not var["name"]:
                raise OriginSyntaxError("Очікується ім'я змінної перед '='", line=line, column=col)
            i += 1
            value, next_pos = parse_value(instr, i)

            if var["type"] == "int":
                try:
                    value = int(float(value))
                except (TypeError, ValueError):
                    raise OriginTypeError(f"Змінна '{var['name']}' має тип int", line=line, column=col) from None
            elif var["type"] == "str":
                if not isinstance(value, str):
                    value = str(value)

            var["value"] = value
            i = next_pos
            assigned = True
            continue

        if assigned:
            # Якщо ми вже отримали значення, але інструкція не закінчилася
            raise OriginSyntaxError(f"Неочікуваний токен після значення: {token_value}", line=line, column=col)

        i += 1

    if not var["name"]:
        l, c = (instr[0][2], instr[0][3]) if len(instr[0]) > 3 else (None, None)
        raise OriginSyntaxError("Очікується ім'я змінної", line=l, column=c)
    if not var["type"]:
        l, c = (instr[0][2], instr[0][3]) if len(instr[0]) > 3 else (None, None)
        raise OriginSyntaxError(f"Для змінної '{var['name']}' не вказано тип", line=l, column=c)

    return var
