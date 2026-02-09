from core.runtime import memory


def parse_value(tokens, start_pos):
    """
    Парсить значення (вираз справа від =)
    Повертає: (value, next_position)
    """
    pos = start_pos

    if tokens[pos][0] == "LBRACE":
        return parse_expression_block(tokens, pos)

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
            result = commands[command_name](arg)
            return result, pos
    
    # Якщо це просте число
    elif tokens[pos][0] == "NUMBER":
        return tokens[pos][1], pos + 1
    
    # Якщо це рядок
    elif tokens[pos][0] == "STRING":
        return tokens[pos][1], pos + 1
    
    # Якщо це змінна
    elif tokens[pos][0] == "ID" and tokens[pos][1] in memory.variables:
        return memory.variables[tokens[pos][1]].const(), pos + 1
    
    return None, pos

def parse_expression_block(tokens, start_pos):
    pos = start_pos
    
    # Пропускаємо {
    if tokens[pos][0] == "LBRACE":
        pos += 1
    
    expr_parts = []  # Збираємо вираз для eval
    
    while tokens[pos][0] != "RBRACE":
        token_type, token_value = tokens[pos]
        
        # Якщо це вкладений виклик команди (scan(int))
        if token_type == "LPAREN" and pos + 1 < len(tokens) and tokens[pos + 1][0] == "COMMAND":
            # Парсимо вкладену команду
            value, new_pos = parse_value(tokens, pos)
            expr_parts.append(str(value))
            pos = new_pos
            continue
        
        # Якщо це число
        elif token_type == "NUMBER":
            expr_parts.append(token_value)
        
        # Якщо це змінна
        elif token_type == "ID":
            if token_value in memory.variables:
                expr_parts.append(str(memory.variables[token_value].const()))
            else:
                raise NameError(f"Змінна '{token_value}' не існує")
        
        # Якщо це оператор
        elif token_type == "OP":
            expr_parts.append(token_value)
        
        # Пропускаємо дужки (вони вже оброблені)
        elif token_type in ["LPAREN", "RPAREN"]:
            pass
        
        pos += 1
    
    # Пропускаємо }
    if tokens[pos][0] == "RBRACE":
        pos += 1
    
    # Обчислюємо вираз
    expression = " ".join(expr_parts)
    
    try:
        result = eval(expression)
        return result, pos
    except Exception as e:
        raise SyntaxError(f"Помилка в обчисленні '{expression}': {e}")

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

        if el[0] == "SPACE":
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
                    return TypeError
            
            var["value"] = value
            i = next_pos
            continue
        
        i += 1
    
    if not var["name"]:
        return None
    
    return var         
