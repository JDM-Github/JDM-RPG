import ply.lex as lex
from .jdsalltoken import *

def JDSLexer():
    t_START = r'\@' + r'START:\s'
    t_STRING = r'("[^"]*")|(\'[^\']*\')'
    t_REGISTER = r'\@' + r'JDS\s'
    t_END = r'\@end'

    t_DOT = r'\.'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_EQUALS = r'\='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    t_ignore = ' \t'
    
    t_EQUALS_TO = r'\=\='
    t_NOT_EQUALS = r'\!\='
    t_LESS_THAN = r'\<'
    t_GREATER_THAN = r'\>'
    t_LESS_THAN_EQUALS = r'\<\='
    t_GREATER_THAN_EQUALS = r'\>\='

    @lex.TOKEN(r'\#.*')
    def t_COMMENT(t):
        r'\#.*'
        pass

    @lex.TOKEN(identifier)
    def t_ID(t):
        t.type = command.get(t.value,'ID')
        return t

    @lex.TOKEN(r'\d+')
    def t_NUMBER(t):
        t.value = int(t.value)
        return t

    @lex.TOKEN(r'\n+')
    def t_newline(t):
        t.lexer.lineno += len(t.value)

    def t_error(t):
        raise Exception(f"Illegal character '{t.value[0]}' at line {t.lineno}")

    return lex.lex()

