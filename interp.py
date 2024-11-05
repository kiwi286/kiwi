import sys # allow randNum inside expr
import ast
import operator
import random

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
        if word == '@d':
            variable = words[index + 1][1:-1]
            if not (words[index + 1][0] == '|' and words[index + 1][-1] == '|') or words[index + 2] != '=':
                raise SyntaxError("Invalid variable declaration!")
            if variable in variables:
                raise SyntaxError("Variable already declared!")
            value = words[index + 3]
            if value == '@randNum':
                try:
                    if '.' in words[index + 4] or '.' in words[index + 5]:
                        raise SyntaxError("Function '@randNum' only takes integers as valid boundaries")
                    value = random.randint(int(words[index + 4]), int(words[index + 5]))
                except ValueError:
                    raise SyntaxError("Function '@randNum' only takes integers as valid boundaries")
            elif value == '@gl':
                if words[index + 4].startswith('#v-'):
                    value = len(str(variables[words[index + 4][3:]]))
                else:
                    value = len(str(words[index + 4]))
            elif value in ('[bin', '[den', '[hex'):
                if words[index + 4] != '->':
                    raise SyntaxError("Converter missing!")
            
                if value == '[bin':
                    if words[index + 5] == 'den]':
                        if words[index + 6].startswith('#v-'):
                            value = int(str(variables[words[index + 6][3:]]), 2)
                        else:
                            value = int(str(words[index + 6]), 2)
                    elif words[index + 5] == 'hex]':
                        if words[index + 6].startswith('#v-'):
                            value = hex(int(str(variables[words[index + 6][3:]]), 2))[2:].upper()
                        else:
                            value = hex(int(str(words[index + 6]), 2))[2:].upper()
                    else:
                        raise SyntaxError("Invalid conversion target for binary")

                elif value == '[den':
                    if words[index + 5] == 'bin]':
                        if words[index + 6].startswith('#v-'):
                            value = bin(int(variables[words[index + 6][3:]]))[2:]
                        elif words[index + 6] == 'expr':
                            value = bin(int(evaluate_expression(str(''.join([variables[item[3:]] if item.startswith('#v-') else item for item in words[7:]])))))[2:]
                        else:
                            value = bin(int(words[index + 6]))[2:]
                    elif words[index + 5] == 'hex]':
                        if words[index + 6].startswith('#v-'):
                            value = hex(int(variables[words[index + 6][3:]]))[2:]
                        elif words[index + 6] == 'expr':
                            value = hex(int(evaluate_expression(str(''.join([variables[item[3:]] if item.startswith('#v-') else item for item in words[7:]])))))[2:]
                        else:
                            value = hex(int(words[index + 6]))[2:]
                    else:
                        raise SyntaxError("Invalid conversion target for decimal")

                elif value == '[hex':
                    if words[index + 5] == 'bin]':
                        if words[index + 6].startswith('#v-'):
                            value = bin(int(str(variables[words[index + 6][3:]]), 16))[2:]
                        else:
                            value = bin(int(words[index + 6], 16))[2:]
                    elif words[index + 5] == 'den]':
                        if words[index + 6].startswith('#v-'):
                            value = int(str(variables[words[index + 6][3:]]), 16)[2:]
                        else:
                            value = int(words[index + 6], 16)[2:]
                    else:
                        raise SyntaxError("Invalid conversion target for hexadecimal")
            elif value == 'expr':
                value = evaluate_expression(str(''.join([variables[item[3:]] if item.startswith('#v-') else item for item in words[(index + 4):]])))
            elif value == 'true':
                value = True
            elif value == 'false':
                value = False
            elif value == 'null':
                value = None
            elif value == '@type':
                newVal = words[index + 4]
                if newVal == 'true':
                    newVal = True
                if newVal == 'false':
                    newVal = False
                if newVal == 'null':
                    newVal = None
                if newVal == 'expr':
                    newVal = 0
                if newVal.startswith('#v-'):
                    newVal = newVal[3:]
                value = eval_type(newVal)
            else:
                value = ' '.join(words[index + 3:])
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except Exception:
                ...
            variables[variable] = value

        elif word == '@a':
            if words[index + 1] == '@randNum':
                try:
                    if '.' in words[index + 2] or '.' in words[index + 3]:
                        raise SyntaxError("Function '@randNum' only takes integers as valid boundaries")
                    print(random.randint(int(words[index + 2]), int(words[index + 3])))
                except ValueError:
                    raise SyntaxError("Funcion '@randNum' only takes integers as valid boundaries")
            elif words[index + 1].startswith('#v-'):
                try:
                    var = variables[words[index + 1][3:]]
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
            elif words[index + 1] == '@gl':
                if words[index + 2].startswith('#v-'):
                    print(len(str(variables[words[index + 2][3:]])))
                else:
                    print(len(str(words[index + 2])))
            elif words[index + 1] == '@type':
                if words[index + 2].startswith('#v-'):
                    if words[index + 4] != '?':
                        raise SyntaxError("@type call must end with '?'")
                    else:
                        print(variables[words[index + 2][3:]])
                else:
                    cms = [word for word in words if not word.startswith('@a') and not word.startswith('@type') and not word.startswith('?')]
                    if len(cms) > 1:
                        print('str')
                    else:
                        print(eval_type(cms[0]))
            elif words[index + 1] == 'expr':
                if words[index + 2] == '..i':
                    print(int(evaluate_expression(str(''.join([variables[item[3:]] if item.startswith('#v-') else item for item in words[3:]])))))
                else:
                    print(evaluate_expression(str(''.join([variables[item[3:]] if item.startswith('#v-') else item for item in words[2:]]))))
            else:
                text = [variables[item[3:]] if item.startswith('#v-') else item for item in [word for word in words if not word.startswith('@a')]]
                print(' '.join(map(str, text)))

        elif word == '@i':
            variable = words[index + 1][1:-1]
            text = [word for word in words if not word.startswith('@i') and not word.startswith('|') and not word.startswith('~')]
            input_text = [variables[item[3:]] if item.startswith('#v-') else item for item in text]
            text = ' '.join(map(str, input_text))
            response = input(text + ' ')
            response = response.strip()
            try:
                new_res = float(response)
                if new_res.is_integer():
                    new_res = int(new_res)
            except ValueError:
                new_res = str(response)
            variables[variable] = new_res


def eval_type(var):
    value = str(type(var))
    if value == "<class 'float'>":
        return 'float'
    elif value == "<class 'int'>":
        return 'int'
    elif value == "<class 'bool'>":
        return 'bool'
    elif value == "<class 'list'>":
        return 'array'
    else:
        return 'str'

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}

def evaluate_expression(expression):
    try:
        # Parse the expression into an AST
        tree = ast.parse(expression, mode='eval')
        return _evaluate_ast(tree.body)
    except Exception as e:
        print(expression)
        raise ValueError("Invalid expression") from e

def _evaluate_ast(node):
    if isinstance(node, ast.BinOp):  # Binary operations (e.g., 2 + 3)
        left = _evaluate_ast(node.left)
        right = _evaluate_ast(node.right)
        return operators[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _evaluate_ast(node.operand)
        return operators[type(node.op)](operand)
    elif isinstance(node, ast.Constant):
        return node.n
    elif isinstance(node, ast.Expression):
        return _evaluate_ast(node.body)
    else:
        raise TypeError("Unsupported type")

def main():
    if len(sys.argv) == 2:
        init(sys.argv[1])
    else:
        print('Pass 1 file name after initialising.')

if __name__ == "__main__":
    main()
