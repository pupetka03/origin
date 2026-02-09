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

        # звичайний string
        if token_type == "STRING":
            result += token_value.strip('"')

        # змінна
        elif token_type == "ID":
            if token_value in memory.variables:
                result += (str(memory.variables[token_value].const()).strip('"'))
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

    

    def eval_condition(var, op, value):
        if op == "<":
            return var < value
        if op == ">":
            return var > value
        if op == "==":
            return var == value
    
    def read_for(instruct, i):
        pos = i
        obj = []
        while pos < len(instruct) and (instruct[pos][0] != "COMMA"):
            token_type, token_value = instruct[pos]
            if token_value == "end":
                return obj, pos
            obj.append((token_type, token_value))
            pos += 1
        return obj, pos
        
    pos = 0
    instruc_for = []
    while pos < len(var):
        obj, i = read_for(var, pos)
        instruc_for.append((obj))
        pos = i + 1

    #init
    if instruc_for[0][2][1] not in memory.variables:
        obj = create_variables(instruc_for[0])
        memory.declare(
            obj["type"],
            obj["name"],
            obj["value"],
        )


    def update_var():
        var_data = create_variables(instruc_for[2])
        memory.declare(
            var_data["type"],
            var_data["name"],
            var_data["value"],
        )

    def get_const_var_2(name):
        if name[0] == "ID":
            return memory.variables[name[1]].const()
        elif name[0] == "NUMBER":
            return name[1]

    #condition
    condition = instruc_for[1][1][1]
    const_var = instruc_for[1][0][1]

    const_var_2 = get_const_var_2(instruc_for[1][2])

    
    while (eval_condition(int(memory.variables[const_var].const()), condition, int(const_var_2))):
        execute_tokens(instruc_for[3])
        update_var()


    """""
        obj, i = read_for(var, pos)
        token_type, token_value = var[pos]

        if token_type == "COMMAND" and token_value == "for":
            pos += 1
            continue

        elif token_type == "TYPE":
            if pos + 1 < len(var) and var[pos + 1][1] not in memory.variables:
                var_data = create_variables(obj)
                memory.declare(
                    var_data["type"],
                    var_data["name"],
                    var_data["value"]
                )
                pos += i  
                continue 

    """""
        


commands =  {
    'type': type_v,
    'print': printf, 
    'scan': scanf,
    'for':forf,
}