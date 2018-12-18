#import inspect
from graphviz import Graph
from collections import defaultdict
#inspect.getouterframes(inspect.currentframe(), 2)[1][3]


class Node:
    def __init__(self, parent, level, text):
        self.parent = parent
        self.level = level
        self.text = text

    def __str__(self):
        return self.text


def match(token):
    global i
    global tokens
    if i >= len(tokens):
        return 0
    if tokens[i][1] == token:
        i += 1
        # print(token)
        return 1
    raise ValueError('token mismatch')


def program():
    stmt_sequence(-1, 0)
    print('compiled successfully')


def stmt_sequence(parent, level):
    global i
    global tokens
    # level += 1
    x = statement(parent, level)
    y = x
    while i < len(tokens) and tokens[i][1] == ';':
        match(';')
        x = statement(x, level)
    # level -= 1
    return y


def statement(parent, level):
    global i
    global tokens

    # if tokens[i][1] != 'identifier':
    #    print(tokens[i][1], ' level:', level)
    # else:
    #    print('assign', ' level:', level)

    if tokens[i][1] == 'if':
        return if_stmt(parent, level)
    elif tokens[i][1] == 'repeat':
        return repeat_stmt(parent, level)
    elif tokens[i][1] == 'identifier':
        return assign_stmt(parent, level)
    elif tokens[i][1] == 'read':
        return read_stmt(parent, level)
    elif tokens[i][1] == 'write':
        return write_stmt(parent, level)
    else:
        raise ValueError('token mismatch')


def if_stmt(parent, level):
    global i
    global tokens
    nodes.append(Node(parent, level, 'if'))
    level += 1
    x = len(nodes) - 1
    match('if')
    exp(x, level)
    match('then')
    stmt_sequence(x, level)
    if i < len(tokens) and tokens[i][1] == 'else':
        nodes.append(Node(parent, level, 'else'))
        y = len(nodes) - 1
        match('else')
        stmt_sequence(y, level)
    match('end')
    return x


def repeat_stmt(parent, level):
    global i
    global tokens
    nodes.append(Node(parent, level, 'repeat'))
    level += 1
    match('repeat')
    x = len(nodes) - 1
    stmt_sequence(x, level)
    match('until')
    exp(x, level)
    return x


def assign_stmt(parent, level):
    global i
    global tokens
    nodes.append(Node(parent, level, f'assign ({tokens[i][0]})'))
    x = len(nodes) - 1
    match('identifier')
    match(':=')
    exp(x, level + 1)
    return x


def read_stmt(parent, level):
    global i
    global tokens
    match('read')
    nodes.append(Node(parent, level, f'read ({tokens[i][0]})'))
    match('identifier')
    x = len(nodes) - 1
    return x


def write_stmt(parent, level):
    global i
    global tokens
    match('write')
    nodes.append(Node(parent, level, 'write'))
    x = len(nodes) - 1
    exp(x, level + 1)
    return x


def exp(parent, level):
    global i
    global tokens
    x = simple_exp(parent, level)
    if i < len(tokens) and (tokens[i][1] == '<' or tokens[i][1] == '='):
        nodes.append(Node(parent, level, f'op ({tokens[i][0]})'))
        nodes[x].parent = len(nodes) - 1
        nodes[x].level = level + 1
        x = len(nodes) - 1
        comparison_op()
        simple_exp(x, level + 1)
    return x


def comparison_op():
    match(tokens[i][1])


def simple_exp(parent, level):
    global i
    global tokens
    x = term(parent, level)
    while i < len(tokens) and (tokens[i][1] == '+' or tokens[i][1] == '-'):
        nodes.append(Node(parent, level, f'op ({tokens[i][0]})'))
        nodes[x].parent = len(nodes) - 1
        nodes[x].level = level + 1
        x = len(nodes) - 1
        addop()
        term(x, level + 1)
    return x


def addop():
    match(tokens[i][1])


def term(parent, level):
    global i
    global tokens
    x = factor(parent, level)
    while i < len(tokens) and (tokens[i][1] == '*' or tokens[i][1] == '/'):
        nodes.append(Node(parent, level, f'op ({tokens[i][0]})'))
        nodes[x].parent = len(nodes) - 1
        nodes[x].level = level + 1
        x = len(nodes) - 1
        mulop()
        addop()
        factor(x, level + 1)
    return x


def mulop():
    match(tokens[i][1])


def factor(parent, level):
    global i
    global tokens
    if tokens[i][1] == '(':
        match('(')
        x = exp(parent, level)
        match(')')
        return x
    elif tokens[i][1] == 'number':
        nodes.append(Node(parent, level, f'const ({tokens[i][0]})'))
        match('number')
    elif tokens[i][1] == 'identifier':
        nodes.append(Node(parent, level, f'id ({tokens[i][0]})'))
        match('identifier')
    return len(nodes) - 1


def get_shape(label):
    label = label.split(' ',1)[0]
    if label in ['read', 'assign', 'if', 'repeat', 'write']:
        return 'rectangle'
    return ''

def draw(nodes):
    nodes_clustered = defaultdict(list)
    for i, node in enumerate(nodes):
        nodes_clustered[node.level].append((i,node))

    g = Graph('tree', format = 'png')

    for level, node_list in sorted(nodes_clustered.items()):
        # print(level)
        # for node in node_list:
        #     print(node)
        with g.subgraph() as s:
            s.attr(rank = 'same')
            for data in node_list: s.node(str(data[0]),data[1].text,shape=get_shape(data[1].text))

    for i, node in enumerate(nodes):
        if i == 0: continue
        g.edge(str(node.parent), str(i))
    g.view()