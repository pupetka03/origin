def type_v(var, variablese):
    if var[0][1] in variablese:
        var_z = variablese[var[0][1]]
        return var_z.print_type()
    else:
        try:
            if int(var[0][1]):
                return int
        except:
            return str

def printf(var, variablese):
    result = ""
    i = 0

    while i < len(var):
        token_type, token_value = var[i]

        if token_type == "SEMICOL":
            break

        # звичайний string
        if token_type == "STRING":
            result += token_value.strip('"')

        # змінна
        elif token_type == "ID":
            if token_value in variablese:
                result += (str(variablese[token_value].const()).strip('"'))
            else:
                result += token_value

        # число
        elif token_type == "NUMBER":
            result += token_value

        # вираз у фігурних дужках { x + 5 }
        elif token_type == "LBRACE":
            expr = ""
            i += 1
            while var[i][0] != "RBRACE":
                t_type, t_val = var[i]
                if t_type == "ID" and t_val in variablese:
                    expr += str(variablese[t_val].const())
                else:
                    expr += t_val
                i += 1

            try:
                result += str(eval(expr))
            except Exception:
                result += "<expr error>"

        elif token_type == "COMMA":
            result += " "

        i += 1

    print(result)
    return None

def scanf(var, variablese):
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
    
        

commands =  {
    'type': type_v,
    'print': printf, 
    'scan': scanf,
}