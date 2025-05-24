OPERATORS = set("|*+?.()")

def is_symbol(c):
    return c.isalnum();

def is_operator(c):
    return c in OPERATORS

def add_concat_operator(regex):
    result = ""
    prev = ""
    for curr in regex:
        if prev:
            if((prev.isalnum() or prev in ")*+?") and (curr.isalnum() or curr == "(")):
                result += "."
        result += curr
        prev = curr
    return result
    
def peek(stack):
    return stack[-1] if stack else None

def greater_precedence(op1, op2):
    precedences = {'+' : 3, '*' : 3, '?' : 3, '.' : 2, '|' : 1}
    right_associative = {'*', '+', '?'}
    if precedences[op1] > precedences[op2]:
        return True
    elif precedences[op1] < precedences[op2]:
        return False
    else:
        return op1 not in right_associative

def parse_to_rpn(regex):

    regex = add_concat_operator(regex);
    output, operators = [], []
    
    for c in regex:
        if is_symbol(c):
            output.append(c)
        elif c == '(':
            operators.append(c)
        elif c == ')':
            while peek(operators) and peek(operators) != '(':
                output.append(operators.pop())
            if not operators:
                raise ValueError("Mismatched parentheses")
            operators.pop()
        elif is_operator(c):
            while (peek(operators) and peek(operators) != '(' and greater_precedence(peek(operators), c)):
                output.append(operators.pop())
            operators.append(c)
        else:
            raise ValueError(f"Symbol not allowed in the expression: '{c}'")
        
    while operators:
        if peek(operators) in ('(' , ')'):
            raise ValueError("Mismatched parentheses - unclosed parenthesis found")
        output.append(operators.pop())

    return ''.join(output)
