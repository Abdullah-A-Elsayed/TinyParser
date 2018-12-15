def match(token):
    global i
    global tokens
    if i >= len(tokens):
        return 0
    if tokens[i][1] == token:
        i += 1
        print(token)
        return 1
    raise ValueError('token mismatch')


def program():
    stmt_sequence()
    print('compiled successfully')
    
    
def stmt_sequence():
    global i
    global tokens
    statement()
    while i < len(tokens) and tokens[i][1] == ';':
        match(';')
        statement()

        
def statement():
    global i
    global tokens
    if tokens[i][1] == 'if':
        if_stmt()
    elif tokens[i][1] == 'repeat':
        repeat_stmt()
    elif tokens[i][1] == 'identifier':
        assign_stmt()
    elif tokens[i][1] == 'read':
        read_stmt()
    elif tokens[i][1] == 'write':
        write_stmt()
    else:
        raise ValueError('token mismatch')
    

def if_stmt():
    global i
    global tokens
    match('if')
    exp()
    match('then')
    stmt_sequence()
    if tokens[i][1] == 'else':
        match('else')
        stmt_sequence()
    match('end')
  

def repeat_stmt():
    match('repeat')
    stmt_sequence()
    match('until')
    exp()
    
    
def assign_stmt():
    match('identifier')
    match(':=')
    exp()
    
    
def read_stmt():
    match('read')
    match('identifier')

    
def write_stmt():
    match('write')
    exp()
    
    
def exp():
    global i
    global tokens
    simple_exp()
    if tokens[i][1] == '<' or tokens[i][1] == '=':
        comparison_op()
        simple_exp()

        
def comparison_op():
    match(tokens[i][1])
    

def simple_exp():
    global i
    global tokens
    term()
    while tokens[i][1] == '+' or tokens[i][1] == '-':
        addop()
        term()

        
def addop():
    match(tokens[i][1])
    

def term():
    global i
    global tokens
    factor()
    while tokens[i][1] == '*' or tokens[i][1] == '/':
        mulop()
        factor()
        
        
def mulop():
    match(tokens[i][1])
    

def factor():
    global i
    global tokens
    if tokens[i][1] == '(':
        match('(')
        exp()
        match(')')
    elif tokens[i][1] == 'number':
        match('number')
    elif tokens[i][1] == 'identifier':
        match('identifier')
