import inspect
#inspect.getouterframes(inspect.currentframe(), 2)[1][3]

class Node:
    def __init__(self, parent, level, text):
        self.parent = parent
        self.level = level
        self.text = text
    
    def __str__(self):
        return self.text + f' | parent: {self.parent}'
    

def match(token):
    global i
    global tokens
    if i >= len(tokens):
        return 0
    if tokens[i][1] == token:
        i += 1
        #print(token)
        return 1
    raise ValueError('token mismatch')


def program():
    stmt_sequence(-1)
    print('compiled successfully')
    
    
def stmt_sequence(parent):
    global i
    global tokens
    global level
    level += 1
    statement(parent)
    while i < len(tokens) and tokens[i][1] == ';':
        match(';')
        parent+=1
        statement(parent)
    level -= 1

        
def statement(parent):
    global i
    global tokens

    #if tokens[i][1] != 'identifier':
    #    print(tokens[i][1], ' level:', level)
    #else:
    #    print('assign', ' level:', level)

    if tokens[i][1] == 'if':
        if_stmt(parent)
    elif tokens[i][1] == 'repeat':
        repeat_stmt(parent)
    elif tokens[i][1] == 'identifier':
        assign_stmt(parent)
    elif tokens[i][1] == 'read':
        read_stmt(parent)
    elif tokens[i][1] == 'write':
        write_stmt(parent)
    else:
        raise ValueError('token mismatch')
    

def if_stmt(parent):
    global level
    global i
    global tokens
    match('if')
    exp()
    match('then')
    stmt_sequence(parent)
    if tokens[i][1] == 'else':
        match('else')
        stmt_sequence(parent)
    match('end')
  
    
def repeat_stmt(parent):
    global level
    global i
    global tokens
    match('repeat')
    stmt_sequence(parent)
    match('until')
    exp()
    
    
def assign_stmt(parent):
    global level
    global i
    global tokens
    match('identifier')
    match(':=')
    exp()
    
    
def read_stmt(parent):
    global level
    global i
    global tokens
    match('read')
    nodes.append(Node(parent, level, f'read ({tokens[i][0]})'))
    match('identifier')

    
def write_stmt(parent):
    global level
    global i
    global tokens
    match('write')
    nodes.append(Node(parent, level, 'write'))
    exp(len(nodes)-1)
    
    
def exp(parent):
    global i
    global tokens
    x = simple_exp(parent)
    if tokens[i][1] == '<' or tokens[i][1] == '=':
        nodes.append(Node(parent, level, f'op ({tokens[i][0]})'))
        nodes[x].parent = len(nodes)-1
        x = len(nodes)-1
        comparison_op()
        simple_exp(x)

        
def comparison_op():
    match(tokens[i][1])
    

def simple_exp(parent):
    global i
    global tokens
    x = term(parent)
    while tokens[i][1] == '+' or tokens[i][1] == '-':
        nodes.append(Node(parent, level, f'op ({tokens[i][0]})'))
        nodes[x].parent = len(nodes)-1
        x = len(nodes)-1
        addop()
        term(x)
    return x

        
def addop():
    match(tokens[i][1])
    

def term(parent):
    global i
    global tokens
    x = factor(parent)
    while tokens[i][1] == '*' or tokens[i][1] == '/':
        nodes.append(Node(parent, level, f'op ({tokens[i][0]})'))
        nodes[x].parent = len(nodes)-1
        x = len(nodes)-1
        mulop()
        factor(x)
    return x
        
        
def mulop():
    match(tokens[i][1])
    

def factor(parent):
    global i
    global tokens
    if tokens[i][1] == '(':
        match('(')
        x = exp(parent)
        match(')')
        return x
    elif tokens[i][1] == 'number':
        nodes.append(Node(parent, level, f'const ({tokens[i][0]})'))
        match('number')


    elif tokens[i][1] == 'identifier':
        nodes.append(Node(parent, level, f'id ({tokens[i][0]})'))
        match('identifier')
    return len(nodes)-1
