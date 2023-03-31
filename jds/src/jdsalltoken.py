digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
identifier       = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'

all_func = {
    'import': 'IMPORT', # CHECK
    'move' : 'MOVE', # CHECK
    'look' : 'LOOK', # CHECK
    'exit' : 'EXIT', # CHECK
    'faceplayer': 'FACEPLAYER', # CHECK
    'waitanim' : 'WAIT_ANIM', # CHECK
    'pause' : 'PAUSE', # CHECK
    'call' : 'CALL', # CHECK
    'help': 'HELP', # CHECK
    'print': 'PRINT',
    'background': 'BACKGROUND',
    'back': 'BACK',
    'message': 'MESSAGE',
    'waitmsg': 'WAITMSG'
}
message_type = {
    'normal': 'NORMAL',
    'yesorno': 'YESORNO'
}
all_target = {
    'player': 'PLAYER', # CHECK
    'owner': 'OWNER' # CHECK
}
all_movements = {
    'left': 'LEFT', # CHECK
    'right': 'RIGHT', # CHECK
    'up': 'UP', # CHECK
    'down': 'DOWN', # CHECK
}
all_keyword = {
    'set' : 'SET', # CHECK
    'var' : 'VAR',  # CHECK
    'globvar': 'GLOBVAR',  # CHECK
    'null' : 'NONE',  # CHECK
    'true': 'TRUE', # CHECK
    'false': 'FALSE', # CHECK
    'not' : 'NOT', # CHECK
}
all_control = {
    'for': 'FOR', # CHECK
    'to': 'TO', # CHECK
    'endfor': 'ENDFOR', # CHECK

    'while' : 'WHILE', # CHECK
    'endwhile' : 'ENDWHILE', # CHECK

    'if' : 'IF', # CHECK
    'elif' : 'ELIF', # CHECK
    'else' : 'ELSE', # CHECK
    'endif': 'ENDIF' # CHECK
}
all_comparison = {
    'and' : 'AND',
    'or' : 'OR'
}

all_comparison_ = [
    'EQUALS_TO', # CHECK
    'NOT_EQUALS', # CHECK
    'LESS_THAN', # CHECK
    'GREATER_THAN', # CHECK
    'LESS_THAN_EQUALS', # CHECK
    'GREATER_THAN_EQUALS', # CHECK
]

all_parsable = [
    'move', 'look', 'exit', 'faceplayer', 'waitanim', 'background', 'print', 'message', 'waitmsg',
    'pause', 'call', 'help', 'set', 'globvar', 'var', 'for', 'if', 'elif', 'else', 'while'
]

command = {**all_func, **all_target, **all_movements, **all_keyword, **all_control, **all_comparison, **message_type}
tokens = all_comparison_ + [
    'DOT', # CHECK
    'NUMBER', # CHECK
    'PLUS', # CHECK
    'MINUS', # CHECK
    'TIMES', # CHECK
    'DIVIDE', # CHECK
    'EQUALS', # CHECK
    'LPAREN', # CHECK
    'RPAREN', # CHECK
    'COMMENT', # CHECK
    'START', # CHECK
    'ID', # CHECK
    'REGISTER', # CHECK
    'END', # CHECK
    'STRING', # CHECK
] + list(command.values())

class LexesValue:
    def __init__(self, identifier, value=None) -> None:
        self.identifier : str = identifier
        self.value : str | int = value

    def __repr__(self) -> str:
        if self.value: return f"{self.identifier}: {self.value}"
        else: return f"{self.identifier}"