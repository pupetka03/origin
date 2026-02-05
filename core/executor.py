from core.variables import Variables
from core.parser import parser
from commands.advanced import commands

type_u = ["int", "str"]
variables = {}

def test(tokens):
    for i, line in enumerate(tokens):
        print(i, line)

def create_variables(instr):
    var = {
        "type":'',
        "name":'',
        "value":'',
    }

   
    znak = ''
    for el in instr:
        if el[1] == "int" or var["type"] == "int":
            if el[1] == "int":
                var['type'] = el[1]

            elif el[0] == "ID" and el[1] not in variables:
                var["name"] = el[1]
            
            elif (el[0] == "NUMBER") or (el[1] in variables):

                if el[1] in variables:
                    num = (variables[el[1]].const())
                else:
                    num = el[1]


                if znak:
                    value = var["value"]
                    #print((f"{value} {znak} {num}"))
                    new_value = eval(f"{value} {znak} {num}")
                    var["value"] = (new_value)
                else:
                    var["value"] = num



            elif el[0] == "OP":
                if el[1] != "=":
                    znak = el[1]
        



        if el[1] == "str" or var["type"] == "str":
            if el[1] == "str":
                var['type'] = el[1]

            elif el[0] == "ID" and el[1] not in variables:
                var["name"] = el[1]
        
            elif el[0] == "STRING" or el[1] in variables:
                if el[1] in variables:
                    string = (variables[el[1]].const())
                else:
                    string = (el[1])

                if znak:
                    if znak == "+":
                        value = (var["value"])
                        var["value"] = (value.strip('"') + string.strip('"')).strip()
                    else:
                        var["value"] = (el[1])
                else:
                    var["value"] = (el[1])

            elif el[0] == "OP":
                    if el[1] != "=":
                        znak = el[1]




    if not var["name"]:
        return None
    return var

            

def read_instruction(tokens, pos):
    i = pos
    instruc = []

    while i < (len(tokens)):
        token_type, token_value = tokens[i] 
        instruc.append((token_type, token_value))

        if token_type == "SEMICOL":
            return instruc, i + 1


        i += 1

    return instruc, i


def executor(file_name):
    result_of_terminale = ""
    tokens = parser(file_name)

    i = 0
    while(i < len(tokens)):
        instruction, i = read_instruction(tokens, i)


        if not instruction:
            continue


        if instruction[0][1] in type_u:
            variable = create_variables(instruction)

            if variable is not None:
                variables[variable["name"]] = Variables(
                    variable["type"], 
                    variable["name"], 
                    variable["value"])
                

        

        elif instruction[0][0] == "COMMAND":
            name = instruction[0][1]
            var = instruction[2][1]
            result = commands[name](var, variables)
            print(result)


            """
            if tab == "BACKSLASH":
                result_of_terminale += str(result) + "\n"
            else:
                result_of_terminale += str(result)

            """



            

        




            

            


        
    

