ops = ('+', '-', '/', '*', '^', 'sqrt', '(', ')')

def split(exp):
    for op in ops:
        exp = exp.replace(op, f' {op} ')
    exp = exp.split()

    return exp

def is_op(op):
    return op in ops

def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`, 
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True

def setsign(exp):

    i = 0
    try:
        while i < len(exp):
        
            if exp[i] == '+' or exp[i] == '-':
                if not is_number(exp[i - 1]) or i == 0:
                    exp[i + 1] = float(exp[i] + str(exp[i + 1]))
                    del exp[i]
                    i = -1
            i += 1
    except ValueError:
        exit(f'Bad usage of \'{exp[i]}\' operator')

    return exp

def lexer(exp):
    if not exp:
        exit('No expression')

    exp = split(exp)

    # check exp for valid syntax
    for op in exp:
        if not is_number(op) and not is_op(op):
            exit(f'Invalid operator/operand: \'{op}\'')

    for i in range(0, len(exp)):
        if is_number(exp[i]):
            exp[i] = float(exp[i])

    return exp

def parser(exp):

    exp = setsign(exp)

    try:
        
        for level in range(1, 4):
        
            i = 0

            while i < len(exp):
                if is_op(exp[i]):

                    if i == 0 and exp[i] != 'sqrt': # Handle a bug with -1 list posiition
                        exit(f'Bad usage of \'{exp[i]}\' operator')

                    if level == 1: # First level, ^

                        if exp[i] == '^':
                            exp[i - 1] = pow(exp[i - 1], exp[i + 1])
                            del exp[i] # deleting unnecessary elements
                            del exp[i]
                            i = -1
                        elif exp[i] == 'sqrt':
                            if exp[i + 1] < 0:
                                exit('Complex numbers are not supported')
                            exp[i] = pow(exp[i + 1], float(1 / 2))
                            del exp[i + 1]
                            i = -1

                    elif level == 2: # Second level, * and /

                        if exp[i] == '*':
                            exp[i - 1] = exp[i - 1] * exp[i + 1]
                            del exp[i]
                            del exp[i]
                            i = -1
                        elif exp[i] == '/':
                            exp[i - 1] = exp[i - 1] / exp[i + 1]
                            del exp[i]
                            del exp[i]
                            i = -1

                    elif level == 3: # Third level, + and -

                        if exp[i] == '+':
                            exp[i - 1] = exp[i - 1] + exp[i + 1]
                            del exp[i]
                            del exp[i]
                            i = -1
                        elif exp[i] == '-':
                            exp[i - 1] = exp[i - 1] - exp[i + 1]
                            del exp[i]
                            del exp[i]
                            i = -1

                i += 1

    except TypeError:
        exit(f'Invalid arithmetic expression: \'{" ".join(str(x) for x in exp)}\'')
    except IndexError:
        exit(f'Bad usage of \'{exp[i]}\' operator')
    except ZeroDivisionError:
        exit('You can\'t divide by zero')

    return exp

def calc(exp):

    if '\\' in exp:

        slashes = exp.count('\\')

        for _ in range(0, slashes):
            extra_exp = input('...')
            exp = exp.replace('\\', extra_exp, 1)

    exp = lexer(exp)

    opar = -1 # position of open parentheses
    cpar = -1 # position of close parentheses

    i = 0 # counter

    while i < len(exp):

        if exp[i] == '(':
            opar = i
        elif exp[i] == ')':
            if opar == -1:
                exit('Unmatched \')\'')
            cpar = i
            try:
                exp[opar] = parser(exp[opar + 1:cpar])[0] # replacing open parenthesis with the result
                del exp[opar + 1:cpar + 1] # Deleting garbage
            except IndexError:
                exit('You should have something inside parentheses')
            i = -1
            opar = -1
            cpar = -1

        i += 1

    if opar != -1 and cpar == -1:
        exit('Unmatched \'(\'')

    exp = parser(exp)

    for i in range(0, len(exp)):

        if exp[i] == int(exp[i]):
            exp[i] = int(exp[i])
        else:
            continue

    if len(exp) != 1:

        for i in range(0, len(exp)):
            exp[i] = str(exp[i])

        return ' | '.join(exp)

    else:
        return exp[0]
