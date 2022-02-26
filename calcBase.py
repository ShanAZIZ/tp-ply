# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------

from generateTreeGraphviz import printTreeGraph

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'print' : 'PRINT',
    'T' : 'TRUE',
    'F': 'FALSE',
}

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'INF', 'SUPP'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    #('right','UMINUS'),
)

tokens = [
    'NUMBER','MINUS',
    'PLUS', 'PLUSPLUS','TIMES', 'MINUSMINUS','DIVIDE',
    'PLUSEQUALS',
    'MINUSEQUALS',
    'SUPPEQUALS',
    'INFEQUALS',
    'LPAREN','RPAREN', 'AND', 'OR', 'SEMICOLON', 'NAME',
    'EQUALS', 'SUPP', 'INF', 'LBRACE', 'RBRACE'
 ] + list(reserved.values())

# Tokens
t_PLUS    = r'\+'
t_PLUSPLUS = r'\+\+'
t_PLUSEQUALS = r'\+='
t_MINUS   = r'-'
t_MINUSMINUS = r'\-\-'
t_MINUSEQUALS = r'\-='
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_OR = r'\|'
t_AND = r'&'
t_TRUE  = r'TRUE'
t_FALSE = r'FALSE'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_SUPP = r'<'
t_SUPPEQUALS = r'<='
t_INF = r'>'
t_INFEQUALS = r'<='

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t
    
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

var = {}

def p_start(p):
    'START : bloc'
    p[0] = ('start', p[1])
    eval_inst(p[0])
    # printTreeGraph(p[0])
    print(p[0])

def p_bloc(p): #A|Ab|b
    '''bloc : bloc statement SEMICOLON 
    | statement SEMICOLON '''
    if len(p) == 4 :
        p[0] = ('bloc', p[1], p[2])
    else :
        p[0] = ('bloc', p[1],  'empty')

def p_statement_print(p):
    'statement : PRINT LPAREN expression RPAREN'
    p[0] = ('print', p[3])
    # print(p[3])

def p_statement_variable(p):
    'statement : NAME EQUALS expression'
    p[0] = ('assign', p[1], p[3])
    # print(var)

def p_statement_incr_parse(p):
    '''
    statement : NAME PLUSPLUS
    '''
    p[0] = ('increase', p[1])


def p_statement_plus_equal_parse(p):
    '''
    statement : NAME PLUSEQUALS NUMBER
    '''
    p[0] = ('add', p[1], p[3])

def p_statement_minus_equal_parse(p):
    '''
    statement : NAME MINUSEQUALS NUMBER
    '''
    p[0] = ('substract', p[1], p[3])

def p_statement_decr_parse(p):
    '''
    statement : NAME MINUSMINUS
    '''
    p[0] = ('decrease', p[1])

def p_statement_if(p):
    '''statement : IF LPAREN expression RPAREN LBRACE bloc RBRACE
            |      IF LPAREN expression RPAREN LBRACE bloc RBRACE ELSE LBRACE bloc RBRACE'''

    if len(p) == 8: p[0] = ('if', p[3], p[6])
    else : p[0] = ('if', p[3], p[6], p[10])

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LBRACE bloc RBRACE'
    p[0] = ('while', p[3], p[6])

def p_statement_for(p):
    'statement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN LBRACE bloc RBRACE'
    p[0] = ('for', p[3], p[5], p[7], p[10])


def p_expression_parse(p):
    '''
    expression : expression PLUS expression
                |   expression TIMES expression
                |   expression MINUS expression
                |   expression DIVIDE expression
                |   expression AND expression
                |   expression OR expression
                |   expression SUPP expression
                |   expression INF expression
                |   expression SUPPEQUALS expression
                |   expression INFEQUALS expression
    '''
    p[0] = (p[2], p[1], p[3])

    
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_true(p):
    'expression : TRUE'
    p[0] = True

def p_expression_false(p):
    'expression : FALSE'
    p[0] = False

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_name(p):
    'expression : NAME'
    p[0] = p[1]

# def p_expression_string(p):
#     'expression : MESSAGE'
#     p[0] = p[1]

def p_error(p):
    print(f"Syntax error at {p.value}")

def eval_expr(t):
    #print('eval de ',t)
    if type(t) == int : return t
    if type(t) == str: return var.get(t)
    if type(t) == bool: return t
    if type(t) == tuple : 
        if t[0] == '+' : return eval_expr(t[1])+eval_expr(t[2])
        if t[0] == '-' : return eval_expr(t[1])-eval_expr(t[2])
        if t[0] == '*' : return eval_expr(t[1])*eval_expr(t[2])
        if t[0] == '/' : return eval_expr(t[1])//eval_expr(t[2])
        if t[0] == '&' : return bool(eval_expr(t[1])) and bool(eval_expr(t[2]))
        if t[0] == '|' : return bool(eval_expr(t[1])) or bool(eval_expr(t[2]))
        if t[0] == '>' : return (eval_expr(t[1]) > eval_expr(t[2]))
        if t[0] == '>=' : return (eval_expr(t[1]) >= eval_expr(t[2]))
        if t[0] == '<' : return (eval_expr(t[1]) < eval_expr(t[2]))
        if t[0] == '<=' : return (eval_expr(t[1]) <= eval_expr(t[2]))
        
    return 'unknown'
     

def eval_inst(t):
    if type(t) is not tuple : 
        #print('tree not tuple', t)
        return 
    if t[0] == 'start' : eval_inst(t[1])
    if t[0] == 'bloc' : 
            eval_inst(t[1])
            eval_inst(t[2])
    if t[0] == 'assign' :
        var[t[1]] = eval_expr(t[2])
        pass #TODO

    if t[0] == 'increase':
        var[t[1]] = eval_expr(t[1]) + 1

    if t[0] == 'decrease':
        var[t[1]] = eval_expr(t[1]) - 1

    if t[0] == 'add':
        var[t[1]] = eval_expr(t[1]) + eval_expr(t[2])

    if t[0] == 'substract':
        var[t[1]] = eval_expr(t[1]) - eval_expr(t[2])

    if t[0] == 'empty':
        return 

    if t[0] == 'if':
        if len(t) == 2 :
            if eval_expr(t[1]) == True:
                eval_inst(t[2])
        else :
            if eval_expr(t[1]) == True:
                eval_inst(t[2])
            else :
                eval_inst(t[3])

    if t[0] == 'while':
        while eval_expr(t[1]):
            eval_inst(t[2])

    if t[0] == 'for':
        eval_inst(t[1])
        while eval_expr(t[2]):
            eval_inst(t[4])
            eval_inst(t[3])

    if t[0] == 'print':
        print(eval_expr(t[1]))
    
import ply.yacc as yacc
yacc.yacc()

data = ""
with open ("code.txt", "r") as myfile:
    data = myfile.read()

# s = input('calc > ')
yacc.parse(data)

    
