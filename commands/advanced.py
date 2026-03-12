from core.runtime import memory
from variables.factory import create_variables


def type_v(var):
    if var[0][1] in memory.variables:
        var_z = memory.variables[var[0][1]]
        return var_z.print_type()
    else:
        try:
            if int(var[0][1]):
                return int
        except:
            return str

def printf(var):
    result = ""
    i = 0

    while i < len(var):
        token_type, token_value = var[i]

        if token_type == "SEMICOL":
            break

        if token_type == "STRING":
            result += token_value.strip('"')

        elif token_type == "ID":
            if token_value in memory.variables:
                result += (str(memory.variables[token_value].const()).strip('"'))
            else:
                result += token_value

        elif token_type == "NUMBER":
            result += token_value

        elif token_type == "LBRACE":
            expr = ""
            i += 1
            while var[i][0] != "RBRACE":
                t_type, t_val = var[i]
                if t_type == "ID" and t_val in memory.variables:
                    expr += str(memory.variables[t_val].const())
                else:
                    expr += t_val
                i += 1
            try:
                result += str(eval(expr))
            except Exception:
                result += "<expr error>"

        elif token_type == "BACKSLASH":
            result += " "

        i += 1

    print(result)
    return None

def scanf(var):
    type = None
    for t in var:
        if t[0] == "TYPE":
            type = t[1]

    if type == "int":
        try:
            return int(input())
        except ValueError:
            return SyntaxError
    elif type == "str":
        return (input())

def forf(var):
    from core.executor import execute_tokens

    def eval_condition(a, op, b):
        if op == "<":  return a < b
        if op == ">":  return a > b
        if op == "==": return a == b
        if op == "<=": return a <= b
        if op == ">=": return a >= b
        return False

    def split_for_sections(tokens):
        """
        Розбиває токени for на 4 секції по COMMA верхнього рівня:
          [0] init      — int i = 0
          [1] condition — i < 10
          [2] update    — int i = {i + 1}
          [3] body      — всі інструкції до end

        COMMA всередині {} або вкладених for ігноруються.
        """
        sections = []
        current = []
        depth_brace = 0   # глибина { }
        depth_for   = 0   # глибина вкладених for

        i = 0
        # Пропускаємо перший токен — це сам "for" COMMAND
        if tokens and tokens[0] == ("COMMAND", "for"):
            i = 1

        while i < len(tokens):
            tok_type, tok_val = tokens[i]

            # Рахуємо дужки { }
            if tok_type == "LBRACE":
                depth_brace += 1
            elif tok_type == "RBRACE":
                depth_brace -= 1

            # Рахуємо вкладені for / end
            if tok_type == "COMMAND" and tok_val == "for":
                depth_for += 1
            elif tok_type == "COMMAND" and tok_val == "end":
                if depth_for > 0:
                    depth_for -= 1
                else:
                    # Це "end" нашого for — кінець тіла
                    sections.append(current)
                    current = []
                    break

            # COMMA верхнього рівня — роздільник секцій (тільки перші 3)
            if tok_type == "COMMA" and depth_brace == 0 and depth_for == 0 and len(sections) < 3:
                sections.append(current)
                current = []
                i += 1
                continue

            current.append((tok_type, tok_val))
            i += 1

        # Якщо тіло не було закрите через end (на випадок помилки)
        if current:
            sections.append(current)

        return sections

    def get_condition_value(token):
        """Повертає числове значення токена (змінна або число)"""
        tok_type, tok_val = token
        if tok_type == "ID":
            return int(memory.variables[tok_val].const())
        elif tok_type == "NUMBER":
            return int(tok_val)
        raise ValueError(f"Невідомий токен в умові: {token}")

    # --- Розбиваємо на секції ---
    sections = split_for_sections(var)

    if len(sections) < 4:
        raise SyntaxError(f"for: очікується 4 секції, отримано {len(sections)}")

    init_tokens      = sections[0]  # int i = 0
    condition_tokens = sections[1]  # i < 10
    update_tokens    = sections[2]  # int i = {i + 1}
    body_tokens      = sections[3]  # тіло

    # --- Ініціалізація ---
    # Визначаємо ім'я змінної (3-й токен: TYPE ID OP VALUE)
    var_name = init_tokens[1][1] if len(init_tokens) > 1 else None


    obj = create_variables(init_tokens)
    memory.declare(obj["type"], obj["name"], obj["value"])

    # --- Розбираємо умову ---
    # Формат: ID/NUMBER  OP  ID/NUMBER
    if len(condition_tokens) < 3:
        raise SyntaxError("for: некоректна умова")

    cond_left_tok  = condition_tokens[0]
    cond_op        = condition_tokens[1][1]
    cond_right_tok = condition_tokens[2]

    def check_condition():
        left  = get_condition_value(cond_left_tok)
        right = get_condition_value(cond_right_tok)
        return eval_condition(left, cond_op, right)

    # --- Оновлення змінної ---
    def update_var():
        var_data = create_variables(update_tokens)
        memory.declare(var_data["type"], var_data["name"], var_data["value"])

    # --- Цикл ---
    while check_condition():
        execute_tokens(body_tokens)
        update_var()


commands = {
    'type':  type_v,
    'print': printf,
    'scan':  scanf,
    'for':   forf,
}