


def type_v(var, variablese):
    if  (var[0] != '"'):

        value = variablese[var]
        return value.print_type()



def printf(var, variablese):
    if var[0] == '"':
        return (var[1:-1])
    else:
        value = variablese[var]
        return value.print_value()

        
    





commands =  {
    'type': type_v,
    'print': printf, 
}