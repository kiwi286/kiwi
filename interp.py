import sys

class InitialiseError(Exception):
    pass

variables = {}

def init(filename):
    with open(filename) as file:
        line = file.readline().strip()
        if line != "init kiwi~":
            raise InitialiseError("First line must initialise kiwi!")
        else:
            interpret(filename)

def interpret(filename):
    with open(filename) as file:
        file_contents = file.readlines()
    
    for line in file_contents[1:]:
        line = line.strip()
        if line:
            evaluate(line)

def evaluate(line):
    words = line.split()

    for index, word in enumerate(words):
        if word == 'expr' and words[index + 1] == '..i':
            return int(eval_expr(float(words[index + 2]), words[index + 3], value2 = float(words[index + 4])))
    
        elif word == 'expr':
            return eval_expr(float(words[index + 1]), words[index + 2], value2 = float(words[index + 3]))

        elif word == '@d':
            variable = words[index + 1][1:-1]
            if not (words[index + 1][0] == '|' and words[index + 1][-1] == '|') or words[index + 2] != '=':
                raise SyntaxError("Invalid variable declaration!")
            if variable in variables:
                raise SyntaxError("Variable already declared!")
            value = words[index + 3]
            if value == '@gl':
                if words[index + 4] == '#v':
                    value = len(str(variables[words[index + 5]]))
                else:
                    value = len(str(words[index + 4]))
            if value in ('[bin', '[den', '[hex'):
                if words[index + 4] != '->':
                    raise SyntaxError("Converter missing!")
            
                if value == '[bin':
                    if words[index + 5] == 'den]':
                        if words[index + 6] == '#v':
                            value = int(str(variables[words[index + 7]]), 2)
                        elif words[index + 6] == 'expr':
                            value = eval_expr(words[index + 7], words[index + 8], words[index + 9])
                        else:
                            value = int(str(words[index + 6]), 2)
                    elif words[index + 5] == 'hex]':
                        if words[index + 6] == '#v':
                            value = hex(int(str(variables[words[index + 7]]), 2))[2:].upper()
                        elif words[index + 6] == 'expr':
                            value = eval_expr(words[index + 7], words[index + 8], words[index + 9])
                        else:
                            value = hex(int(str(words[index + 6]), 2))[2:].upper()
                    else:
                        raise SyntaxError("Invalid conversion target for binary")

                elif value == '[den':
                    if words[index + 5] == 'bin]':
                        if words[index + 6] == '#v':
                            value = bin(int(variables[words[index + 7]]))[2:]
                        elif words[index + 6] == 'expr':
                            value = bin(int(eval_expr(words[index + 7], words[index + 8], words[index + 9])))[2:]
                        else:
                            value = bin(int(words[index + 6]))[2:]
                    elif words[index + 5] == 'hex]':
                        if words[index + 6] == '#v':
                            value = hex(int(variables[words[index + 7]]))[2:]
                        elif words[index + 6] == 'expr':
                            value = hex(int(eval_expr(words[index + 7], words[index + 8], words[index + 9])))[2:]
                        else:
                            value = hex(int(words[index + 6]))[2:]
                    else:
                        raise SyntaxError("Invalid conversion target for decimal")

                elif value == '[hex':
                    if words[index + 5] == 'bin]':
                        if words[index + 6] == '#v':
                            value = bin(int(str(variables[words[index + 7]]), 16))[2:]
                        elif words[index + 6] == 'expr':
                            value = bin(int(eval_expr(words[index + 7], words[index + 8], words[index + 9]), 16))[2:]
                        else:
                            value = bin(int(words[index + 6], 16))[2:]
                    elif words[index + 5] == 'den]':
                        if words[index + 6] == '#v':
                            value = int(str(variables[words[index + 7]]), 16)[2:]
                        elif words[index + 6] == 'expr':
                            value = int(eval_expr(words[index + 7], words[index + 8], words[index + 9]), 16)[2:]
                    else:
                        raise SyntaxError("Invalid conversion target for hexadecimal")
            if value == 'expr':
                value = eval_expr(float(words[index + 4]), words[index + 5], float(words[index + 6]))
            if value == 'true':
                value = True
            if value == 'false':
                value = False
            if value == 'null':
                value = None
            if value == '@type':
                newVal = words[index + 4]
                if newVal == 'true':
                    newVal = True
                if newVal == 'false':
                    newVal = False
                if newVal == 'null':
                    newVal = None
                if newVal == 'expr':
                    if words[index + 5] == '..i':
                        if words[index + 9] != '?':
                            raise SyntaxError("@type call must end with '?'")
                        else:
                            newVal = int(eval_expr(float(words[index + 6]), words[index + 7], float(words[index + 8])))
                    else:
                        if words[index + 8] != '?':
                            raise SyntaxError("@type call must end with '?'")
                        else:
                            newVal = eval_expr(float(words[index + 5]), words[index + 6], float(words[index + 7]))
                if newVal == '#v':
                    newVal = variables[words[index + 5]]
                value = eval_type(newVal)
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except Exception:
                ...
            variables[variable] = value

        elif word == '@a':
            if words[index + 1] == '#v':
                try:
                    var = variables[words[index + 2]]
                    if var == None:
                        print('null')
                    elif var == True:
                        print('true')
                    elif var == False:
                        print('false')
                    else:
                        print(var)
                except KeyError:
                    raise SyntaxError('Variable does not exist!')
            elif words[index + 2] == '@gl':
                if words[index + 3] == '#v':
                    print(len(str(variables[words[index + 4]])))
                else:
                    print(len(str(words[index + 4])))
            elif words[index + 1] == '@type':
                if words[index + 2] == '#v':
                    if words[index + 4] != '?':
                        raise SyntaxError("@type call must end with '?'")
                    else:
                        print(variables[words[index + 3]])
                else:
                    cms = [word for word in words if not word.startswith('@a') and not word.startswith('@type') and not word.startswith('?')]
                    if len(cms) > 1:
                        print('str')
                    else:
                        if cms[0] in ('true', 'false', 'null'):
                            print('bool')
                        else:
                            try:
                                cmsn = int(cms[0])
                                if '.' in cms[0]:
                                    print('float')
                                else:
                                    print('int')
                            except ValueError:
                                print('str')
            elif words[index + 1] == 'expr':
                if words[index + 2] == '..i':
                    print(int(eval_expr(words[index + 3], words[index + 4], words[index + 5])))
                else:
                    print(eval_expr(words[index + 2], words[index + 3], words[index + 4]))
            elif words[index + 1] == '..i':
                if words[index + 2] == '#v':
                    print(int(variables[words[index + 3]]))
                if words[index + 2] == 'expr':
                    print(int(eval_expr(words[index + 3], words[index + 4], words[index + 5])))
            elif words[index + 1] == '@d':
                raise SyntaxError("Cannot define variable inside 'aloud' statement.")
            else:
                print(' '.join([word for word in words if not word.startswith('@a')]))

        elif word == '@type':
            if words[index + 1] == '#v':
                try:
                    eval_type(variables[words[index + 2]])
                except KeyError:
                    raise SyntaxError('No such variable defined!')
            else:
                eval_type(' '.join([word for word in words if not word.startswith('@type')]))

        elif word == '@i':
            variable = words[index + 1][1:-1]
            text = ' '.join([word for word in words if not word.startswith('@i') and not word.startswith('|') and not word.startswith('~')])
            response = input(text + ' ')
            response = response.strip()
            try:
                new_res = float(response)
                if new_res.is_integer():
                    new_res = int(new_res)
            except ValueError:
                new_res = str(response)
            variables[variable] = new_res
        
        elif word == "%aft%":
            all_text = ' '.join([word for word in words if not word.startswith('%aft%')])

            for var in all_text.split():
                if var.startswith('#i-'):
                    key = var[3:]
                    if key in variables:
                        all_text = all_text.replace(var, str(variables[key]))

            print(all_text)


def eval_type(var):
    value = str(type(var))
    if value == "<class 'float'>":
        return 'float'
    elif value == "<class 'int'>":
        return 'int'
    elif value == "<class 'bool'>":
        return 'bool'
    else:
        return 'str'

def eval_expr(value1, operation, value2):
    value1 = float(value1)
    value2 = float(value2)

    try:
        if operation == '+':
            return value1 + value2
        elif operation == '-':
            return value1 - value2
        elif operation == '*':
            return value1 * value2
        elif operation == '/':
            return value1 / value2
        else:
            raise SyntaxError("Invalid operation!")
    except ValueError:
        raise SyntaxError("Values must be numbers!")

def main():
    if len(sys.argv) == 2:
        init(sys.argv[1])
    else:
        print('Pass 1 file name after initialising.')

if __name__ == "__main__":
    main()