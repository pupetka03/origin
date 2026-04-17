from core.errors import OriginNameError, OriginRuntimeError, OriginSyntaxError
from core.runtime import memory
from variables.factory import create_variables, parse_expression_block


SAFE_EVAL_GLOBALS = {"__builtins__": {}}


def command_arguments(tokens):
    args = tokens[1:] if tokens and tokens[0][0] == "COMMAND" else list(tokens)

    if args and args[0][0] == "LPAREN":
        args = args[1:]
        if args and args[-1][0] == "SEMICOL":
            args = args[:-1]
        if args and args[-1][0] == "RPAREN":
            args = args[:-1]
        if args and args[-1][0] == "SEMICOL":
            args = args[:-1]

    return args


def normalize_value(value):
    if isinstance(value, str):
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value
    return value


def eval_condition(a, op, b):
    if op == "<":
        return a < b
    if op == ">":
        return a > b
    if op == "==":
        return a == b
    if op == "!=":
        return a != b
    if op == "<=":
        return a <= b
    if op == ">=":
        return a >= b
    raise OriginSyntaxError(f"Невідомий оператор умови: {op}")


def resolve_value(tokens):
    if not tokens:
        raise OriginSyntaxError("Порожнє значення в умові")

    first_token = tokens[0]
    token_type, token_value, *pos_info = first_token
    line = pos_info[0] if pos_info else None
    col = pos_info[1] if len(pos_info) > 1 else None

    if token_type == "LBRACE":
        value, pos = parse_expression_block(tokens, 0)
        if pos != len(tokens):
            raise OriginSyntaxError("Некоректний вираз у {}", line=line, column=col)
        return normalize_value(value)

    if len(tokens) == 1:
        if token_type == "NUMBER":
            return normalize_value(token_value)
        if token_type == "STRING":
            return token_value.strip('"')
        if token_type == "ID":
            try:
                return normalize_value(memory.get(token_value).const())
            except Exception:
                raise OriginNameError(f"Змінна '{token_value}' не знайдена", line=line, column=col)

    raise OriginSyntaxError(f"Не вдалося обчислити значення: {token_value}", line=line, column=col)


def evaluate_condition_tokens(tokens):
    brace_depth = 0
    operator_index = None
    operator_value = None
    comparison_ops = {"<", ">", "==", "!=", "<=", ">="}

    for index, token in enumerate(tokens):
        token_type, token_value, *pos_info = token
        if token_type == "LBRACE":
            brace_depth += 1
        elif token_type == "RBRACE":
            brace_depth -= 1
        elif token_type == "OP" and brace_depth == 0 and token_value in comparison_ops:
            operator_index = index
            operator_value = token_value
            break

    if operator_index is None:
        return bool(resolve_value(tokens))

    left_tokens = tokens[:operator_index]
    right_tokens = tokens[operator_index + 1:]

    if not left_tokens or not right_tokens:
        # Беремо позицію оператора для помилки
        token_type, token_value, *pos_info = tokens[operator_index] if operator_index is not None else (None, None)
        l, c = (pos_info[0], pos_info[1]) if pos_info else (None, None)
        raise OriginSyntaxError("Умова має бути у форматі left OP right", line=l, column=c)

    left = resolve_value(left_tokens)
    right = resolve_value(right_tokens)
    return eval_condition(left, operator_value, right)


def evaluate_braced_print_expression(tokens, start_index):
    value, next_pos = parse_expression_block(tokens, start_index)
    return str(value), next_pos


def type_v(var):
    args = command_arguments(var)
    if not args:
        raise OriginSyntaxError("type: очікується аргумент")

    token_type, token_value, *pos_info = args[0]
    l, c = (pos_info[0], pos_info[1]) if pos_info else (None, None)

    if token_type == "ID":
        try:
            return memory.get(token_value).print_type()
        except Exception:
            raise OriginNameError(f"Змінна '{token_value}' не знайдена", line=l, column=c)
    if token_type == "NUMBER":
        return "int"
    if token_type == "STRING":
        return "str"
    raise OriginSyntaxError("type: некоректний аргумент", line=l, column=c)


def printf(var):
    args = command_arguments(var)
    result = ""
    i = 0

    while i < len(args):
        token = args[i]
        token_type, token_value, *pos_info = token
        line = pos_info[0] if pos_info else None
        col = pos_info[1] if len(pos_info) > 1 else None

        if token_type == "SEMICOL":
            break
        if token_type == "STRING":
            result += token_value.strip('"')
            i += 1
            continue
        if token_type == "ID":
            try:
                result += str(memory.get(token_value).const()).strip('"')
            except Exception:
                raise OriginNameError(f"Змінна '{token_value}' не знайдена", line=line, column=col)
            i += 1
            continue
        if token_type == "NUMBER":
            result += token_value
            i += 1
            continue
        if token_type == "LBRACE":
            expr_value, next_pos = evaluate_braced_print_expression(args, i)
            result += expr_value
            i = next_pos
            continue
        if token_type == "BACKSLASH":
            result += " "
            i += 1
            continue
        raise OriginSyntaxError(f"print: неочікуваний токен '{token_value}'", line=line, column=col)

    print(result)
    return None


def scanf(var):
    args = command_arguments(var)
    input_type = None
    first_pos = (None, None)

    for token in args:
        token_type, token_value, *pos_info = token
        if token_type == "TYPE":
            input_type = token_value
            first_pos = (pos_info[0], pos_info[1]) if pos_info else (None, None)
            break

    if input_type == "int":
        raw = input()
        try:
            return int(raw)
        except ValueError:
            raise OriginRuntimeError(f"Неможливо перетворити '{raw}' у int", line=first_pos[0], column=first_pos[1]) from None
    if input_type == "str":
        return input()
    raise OriginSyntaxError("scan: підтримуються лише int і str", line=first_pos[0], column=first_pos[1])


def iff(var):
    from core.executor import execute_tokens

    start_index = None
    depth = 0

    for index in range(1, len(var)):
        token_type, token_value, *pos_info = var[index]

        if token_type == "COMMAND" and token_value in {"if", "for", "while", "func"}:
            depth += 1
        elif token_type == "COMMAND" and token_value == "end":
            if depth > 0:
                depth -= 1
        elif token_type == "COMMAND" and token_value == "start" and depth == 0:
            start_index = index
            break

    if start_index is None:
        l, c = (var[0][2], var[0][3]) if len(var[0]) > 3 else (None, None)
        raise OriginSyntaxError("if: очікується ключове слово start", line=l, column=c)

    condition_tokens = var[1:start_index]
    block_tokens = var[start_index + 1:]

    if block_tokens and block_tokens[-1][0] == "SEMICOL":
        block_tokens = block_tokens[:-1]

    if not block_tokens or block_tokens[-1][:2] != ("COMMAND", "end"):
        l, c = (var[0][2], var[0][3]) if len(var[0]) > 3 else (None, None)
        raise OriginSyntaxError("if: очікується завершення через end;", line=l, column=c)

    block_tokens = block_tokens[:-1]

    true_branch = []
    false_branch = []
    current_branch = true_branch
    nested_depth = 0

    for token in block_tokens:
        token_type, token_value, *pos_info = token

        if token_type == "COMMAND" and token_value in {"if", "for", "while", "func"}:
            nested_depth += 1
            current_branch.append(token)
            continue
        if token_type == "COMMAND" and token_value == "end":
            if nested_depth > 0:
                nested_depth -= 1
            current_branch.append(token)
            continue
        if token_type == "COMMAND" and token_value == "else" and nested_depth == 0:
            current_branch = false_branch
            continue

        current_branch.append(token)

    if evaluate_condition_tokens(condition_tokens):
        memory.push_scope()
        try:
            execute_tokens(true_branch)
        finally:
            memory.pop_scope()
    elif false_branch:
        memory.push_scope()
        try:
            execute_tokens(false_branch)
        finally:
            memory.pop_scope()


def forf(var):
    from core.executor import execute_tokens

    def split_for_sections(tokens):
        sections = []
        current = []
        depth_brace = 0
        depth_block = 0
        block_commands = {"for", "if", "while", "func"}

        i = 0
        if tokens and tokens[0][:2] == ("COMMAND", "for"):
            i = 1

        while i < len(tokens):
            token = tokens[i]
            tok_type, tok_val, *pos_info = token

            if tok_type == "LBRACE":
                depth_brace += 1
            elif tok_type == "RBRACE":
                depth_brace -= 1

            if tok_type == "COMMAND" and tok_val in block_commands:
                depth_block += 1
            elif tok_type == "COMMAND" and tok_val == "end":
                if depth_block > 0:
                    depth_block -= 1
                else:
                    sections.append(current)
                    current = []
                    break

            if tok_type == "COMMA" and depth_brace == 0 and depth_block == 0 and len(sections) < 3:
                sections.append(current)
                current = []
                i += 1
                continue

            current.append(token)
            i += 1

        if current:
            sections.append(current)

        return sections

    def get_condition_value(token):
        tok_type, tok_val, *pos_info = token
        l, c = (pos_info[0], pos_info[1]) if pos_info else (None, None)
        if tok_type == "ID":
            try:
                return int(memory.get(tok_val).const())
            except Exception:
                raise OriginNameError(f"Змінна '{tok_val}' не знайдена", line=l, column=c)
        if tok_type == "NUMBER":
            return int(tok_val)
        raise OriginSyntaxError(f"Невідомий токен в умові: {tok_val}", line=l, column=c)

    sections = split_for_sections(var)
    if len(sections) < 4:
        l, c = (var[0][2], var[0][3]) if len(var[0]) > 3 else (None, None)
        raise OriginSyntaxError(f"for: очікується 4 секції, отримано {len(sections)}", line=l, column=c)

    init_tokens = sections[0]
    condition_tokens = sections[1]
    update_tokens = sections[2]
    body_tokens = sections[3]

    # Створюємо нову область видимості для всього циклу
    memory.push_scope()
    try:
        obj = create_variables(init_tokens)
        memory.declare(obj["type"], obj["name"], obj["value"])

        if len(condition_tokens) < 3:
            l, c = (condition_tokens[0][2], condition_tokens[0][3]) if condition_tokens and len(condition_tokens[0]) > 3 else (None, None)
            raise OriginSyntaxError("for: некоректна умова", line=l, column=c)

        cond_left_tok = condition_tokens[0]
        cond_op = condition_tokens[1][1]
        cond_right_tok = condition_tokens[2]

        def check_condition():
            left = get_condition_value(cond_left_tok)
            right = get_condition_value(cond_right_tok)
            return eval_condition(left, cond_op, right)

        def update_var():
            var_data = create_variables(update_tokens)
            memory.declare(var_data["type"], var_data["name"], var_data["value"])

        while check_condition():
            # Всередині тіла циклу можна було б робити ще один push_scope, 
            # але зазвичай достатньо одного на весь цикл (разом з лічильником)
            execute_tokens(body_tokens)
            update_var()
    finally:
        memory.pop_scope()


commands = {
    "type": type_v,
    "print": printf,
    "scan": scanf,
    "if": iff,
    "for": forf,
}
