import os
import sys
import json
from pprint import pprint, pformat

if __name__ == "__main__": from src import *
else: from .src import *

class JDS:
    
    def __init__(self) -> None:
        self.compiler = JDSCompiler()
        self.all_compiled_script = dict()

    def set_script(self, filename: str | None= None):
        if self.all_compiled_script.get(filename) is None:
            self.parse(filename)
        return filename

    def run(self, filename: str | None= None, save=True):
        if self.all_compiled_script.get(filename) is None:
            self.parse(filename)

        return self.compiler.compile(self.all_compiled_script.get(filename), self.start, self.import_file, self.main_config, save)

    def parse(self, filename: str|None = None):
        self.lexer = JDSLexer()
        if filename is None:
            self.lexer.input("@START: test\n"
                    "@JDS test\n"
                    "   faceplayer owner\n"
                    "   exit\n"
                    "@end")
        else:
            if os.path.exists(filename):
                with open(filename) as f:
                    self.lexer.input(f.read())
            else:
                print(f"[{'JDS'.center(10)}] -> WARNING: {filename} not Found")
                self.lexer.input("@START: test\n"
                    "@JDS test\n"
                    "   faceplayer owner\n"
                    "   exit\n"
                    "@end")

        self.current_line = 0
        self.current_func = None
        self.all_variables_created = []
        self.all_variables_global = []

        self.all_func_lexes : list[list[LexesValue]]= {}

        self.import_file = None
        self.import_name = 'game'
        self.main_config = {}
        self.tok = self.lexer.token()
        if not self.tok: return

        if self.tok.type == 'IMPORT':
            self.current_line = self.tok.lineno
            self.tok = self.lexer.token()
            if not self.tok or self.tok.type != 'STRING' or self.current_line < self.tok.lineno: raise SyntaxError(f"Expected 'STRING' in import on line {self.tok.lineno}")
            if os.path.exists(os.path.abspath(self.tok.value[1:-1])) and self.tok.value[1:-1].endswith('.json'):
                with open(self.tok.value[1:-1]) as f:
                    self.import_file = self.tok.value[1:-1]
                    self.main_config = json.load(f)

                self.tok = self.lexer.token()
                if not self.tok or self.tok.value != 'as': raise SyntaxError(f"Expected 'as' on line {self.tok.lineno}")
                self.tok = self.lexer.token()
                if not self.tok or self.tok.type != 'ID': raise SyntaxError(f"Expected 'ID' on line {self.tok.lineno}")
                self.import_name =self.tok.value

                self.tok = self.lexer.token()
                if not self.tok or self.current_line == self.tok.lineno: raise SyntaxError(f"Expected START on line {self.tok.lineno}")
            else: raise FileNotFoundError(f"{os.path.abspath(self.tok.value[1:-1])} not Found or not Valid")

        if self.tok.type != 'START':
            raise SyntaxError(f"First Command is not START")
        self.tok = self.lexer.token()
        if self.tok.type != 'ID':
            raise SyntaxError(f"Expected Identifier on line {self.tok.lineno}")
        self.start = self.tok.value

        self.resurvely_call()
        self.all_compiled_script[filename] = self.all_func_lexes

    def resurvely_call(self):
        while True:
            self.tok = self.lexer.token()
            if not self.tok: break

            if self.tok.type == 'REGISTER':
                self.all_variables_created.clear()
                self.current_line = self.tok.lineno
                self.tok = self.lexer.token()
                if self.tok.lineno == self.current_line and self.tok.type == 'ID':
                    if self.tok.value in self.all_func_lexes.keys():
                        raise SyntaxError(f"{self.tok.value} already defined.")

                    self.all_func_lexes[self.tok.value] = [[]]
                    self.current_func = self.tok.value
                    if self.current_func in list(command.values()):
                        raise SyntaxError(f"REGISTER name is a reserved words")
                else: raise SyntaxError(f"Expected Identifier on line {self.tok.lineno}")

                self.tok = self.lexer.token()
                if self.tok.lineno == self.current_line: raise SyntaxError(f"Found {self.tok.value}, on Line {self.tok.lineno}")
                self.current_line = self.tok.lineno

                while True:
                    if self.current_line < self.tok.lineno:
                        self.current_line = self.tok.lineno
                        self.all_func_lexes.get(self.current_func).append([])

                    if self.tok.type == 'END':
                        if self.all_func_lexes.get(self.current_func)[-1]:
                            raise SyntaxError(f"Found {self.tok.value}, on Line {self.tok.lineno}")
                        self.all_func_lexes[self.current_func] = self.all_func_lexes.get(self.current_func)[:-1]
                        break

                    elif self.tok.type == 'IF': self.if_else_current(self.all_func_lexes.get(self.current_func))
                    elif self.tok.type in ['ELIF', 'ELSE']: raise SyntaxError(f"Did you mean if?, line {self.tok.lineno}")
                    elif self.tok.type == 'ENDIF': raise SyntaxError(f"Please use if statements like a normal human being. line {self.tok.lineno}")

                    elif self.check_function(self.all_func_lexes.get(self.current_func)) != 'None': pass
                    else: raise SyntaxError(f"{self.tok.type} not in {list(command.values()) + ['ID', 'NUMBER', 'STRING']}, line {self.tok.lineno}")

                    self.tok = self.lexer.token()
                    if not self.tok: raise SyntaxError(f"Expected @end, line {self.tok.lineno}")
                    elif self.current_line == self.tok.lineno: raise SyntaxError(f"Found {self.tok.value}, on Line {self.tok.lineno}")
            else: raise SyntaxError("NO REGISTER FOUND")

    def check_function(self, current_list):
        if self.tok.type == 'BACKGROUND': self.background_func(current_list)
        elif self.tok.type == 'MESSAGE': self.message_func(current_list)
        elif self.tok.type == 'PRINT': self.print_func(current_list)
        elif self.tok.type == 'FOR': self.for_func(current_list)
        elif self.tok.type == 'WHILE': self.while_func(current_list)
        elif self.tok.type in ['EXIT', 'WAIT_ANIM', 'HELP', 'BACK', 'WAITMSG']: current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        elif self.tok.type == 'PAUSE': self.func_pause(current_list)
        elif self.tok.type == 'CALL': self.func_call(current_list)
        elif self.tok.type == 'FACEPLAYER': self.face_player(current_list)
        elif self.tok.type in ['MOVE', 'LOOK']: self.move_look(current_list)
        elif self.tok.type == 'SET': self.set_game_variable(current_list)
        elif self.tok.type in ['VAR', 'GLOBVAR']: self.set_variable(current_list)
        else: return 'None'

    def message_func(self, current_list):
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        self.create_expression(current_list)
        self.current_line = self.tok.lineno
        self.function_get(
            current_list,
            lambda tok, target=list(message_type.values()): tok.type not in target,
            f"Expected Message Type")

    def function_get(self, current_list, rule, details):
        self.tok = self.lexer.token()
        if not self.tok or self.current_line < self.tok.lineno: raise SyntaxError(details)
        if rule(self.tok): raise SyntaxError(details)
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=(self.tok.value[1:-1] if self.tok.type == 'STRING' else self.tok.value)))
    
    def background_func(self, current_list):
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        self.function_get(
            current_list,
            lambda tok, target='STRING': tok.type != target,
            f"Expected STRING: Color")
        self.function_get(
            current_list,
            lambda tok, target='NUMBER': tok.type != target,
            f"Expected NUMBER: Duration")

    def func_call(self, current_list):
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        self.function_get(
            current_list,
            lambda tok, target='ID': tok.type != target,
            f"Expected Target")

    def func_pause(self, current_list):
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        self.create_expression(current_list)
        self.current_line = self.tok.lineno

    def print_func(self, current_list):
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        self.create_expression(current_list)
        self.current_line = self.tok.lineno

    def face_player(self, current_list):
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        self.function_get(
            current_list,
            lambda tok, target=list(all_target.values())+['NUMBER']: tok.type not in target,
            f"Expected Target")

    def move_look(self, current_list):
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        self.function_get(
            current_list,
            lambda tok, target=list(all_target.values())+['NUMBER']: tok.type not in target,
            f"Expected Target")

        self.tok = self.lexer.token()
        if not self.tok or self.current_line < self.tok.lineno: raise SyntaxError(f"Expected Direction")
        if self.tok.type == 'ID':
            if self.tok.value in self.all_variables_global:
                current_list[-1].append(LexesValue(identifier='GLOBVAR', value=self.tok.value))
            elif self.tok.value in self.all_variables_created:
                current_list[-1].append(LexesValue(identifier='VAR', value=self.tok.value))
            elif self.tok.type in 'ID' and self.tok.value.startswith(self.import_name):
                self.tok = self.lexer.token()
                if not self.tok or self.current_line < self.tok.lineno or self.tok.type != 'DOT': raise SyntaxError(f"Expected '.'")
                self.tok = self.lexer.token()
                if not self.tok or self.current_line < self.tok.lineno or self.tok.type != 'ID': raise SyntaxError(f"Expected 'SET'")
                current_list[-1].append(LexesValue(identifier='SET', value=self.tok.value))
        elif self.tok.type in list(all_movements.values())+['NUMBER']: current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        else: raise SyntaxError(f"Expected Direction")

    def create_expression(self, current_list):
        new_list = []
        is_paren = False
        self.tok = self.lexer.token()
        if not self.tok or self.current_line < self.tok.lineno:
            raise SyntaxError(f"Expected Value {['STRING', 'NUMBER', 'NONE', 'TRUE', 'FALSE']+self.all_variables_created+self.all_variables_global}")
        elif self.tok.type == 'LPAREN':
            new_list.append(LexesValue(identifier=self.tok.type, value=self.tok.value))
            is_paren = True
        elif self.tok.type in ['STRING', 'NUMBER', 'NONE', 'TRUE', 'FALSE']:
            new_list.append(LexesValue(identifier=self.tok.type, value=(self.tok.value[1:-1] if self.tok.type == 'STRING' else self.tok.value)))
        elif self.tok.value in self.all_variables_global:
            new_list.append(LexesValue(identifier='GLOBVAR', value=self.tok.value))
        elif self.tok.value in self.all_variables_created:
            new_list.append(LexesValue(identifier='VAR', value=self.tok.value))
        elif self.tok.type in 'ID' and self.tok.value.startswith(self.import_name):
            self.tok = self.lexer.token()
            if not self.tok or self.current_line < self.tok.lineno or self.tok.type != 'DOT': raise SyntaxError(f"Expected '.'")
            self.tok = self.lexer.token()
            if not self.tok or self.current_line < self.tok.lineno or self.tok.type != 'ID': raise SyntaxError(f"Expected 'SET'")
            new_list.append(LexesValue(identifier='SET', value=self.tok.value))
        else: raise SyntaxError(f"Expected Value {['STRING', 'NUMBER', 'NONE', 'TRUE', 'FALSE']+self.all_variables_created+self.all_variables_global}")

        if is_paren: self.paren_loop(new_list)
        current_list[-1].append(new_list)

    def paren_loop(self, new_list):
        is_number = True
        self.tok = self.lexer.token()
        if not self.tok: raise SyntaxError(f'Expected END')
        while self.tok.type != 'RPAREN':
            if is_number:
                if self.tok.type == 'LPAREN':
                    new_list.append(LexesValue(identifier=self.tok.type, value=self.tok.value))
                    self.paren_loop(new_list)
                    is_number = False
                elif self.tok.type == 'NOT':
                    new_list.append(LexesValue(identifier=self.tok.type, value=self.tok.value))
                elif self.tok.type in ['STRING', 'NUMBER', 'NONE', 'TRUE', 'FALSE']:
                    new_list.append(LexesValue(identifier=self.tok.type, value=(self.tok.value[1:-1] if self.tok.type == 'STRING' else self.tok.value)))
                    is_number = False
                elif self.tok.value in self.all_variables_global:
                    new_list.append(LexesValue(identifier='GLOBVAR', value=self.tok.value))
                    is_number = False
                elif self.tok.value in self.all_variables_created:
                    new_list.append(LexesValue(identifier='VAR', value=self.tok.value))
                    is_number = False
                elif self.tok.type in 'ID' and self.tok.value.startswith(self.import_name):
                    self.tok = self.lexer.token()
                    if not self.tok or self.tok.type != 'DOT': raise SyntaxError(f"Expected '.'")
                    self.tok = self.lexer.token()
                    if not self.tok or self.tok.type != 'ID': raise SyntaxError(f"Expected 'SET'")
                    new_list.append(LexesValue(identifier='SET', value=self.tok.value))
                    is_number = False
                else: raise SyntaxError(f"Expected Value {['STRING', 'NUMBER', 'NONE', 'TRUE', 'FALSE']+self.all_variables_created+self.all_variables_global}")

            else:
                if self.tok.type in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE']:
                    new_list.append(LexesValue(identifier=self.tok.type, value=self.tok.value))
                    is_number = True                    
                elif self.tok.type == 'STRING':
                    new_list.append(LexesValue(identifier=self.tok.type, value=(self.tok.value[1:-1])))
                elif self.tok.type in list(all_comparison.values()) + all_comparison_:
                    new_list.append(LexesValue(identifier=self.tok.type, value=self.tok.value))
                    is_number = True
                else: raise SyntaxError(f"Expected Value {['PLUS', 'MINUS', 'TIMES', 'DIVIDE']}")

            self.tok = self.lexer.token()
            if not self.tok: raise SyntaxError(f"Expected ')'")

        if is_number: raise SyntaxError(f"Expected 'Value'")
        new_list.append(LexesValue(identifier=self.tok.type, value=self.tok.value))

    def set_game_variable(self, current_list):
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        self.tok = self.lexer.token()
        if not self.tok or self.current_line < self.tok.lineno: raise SyntaxError(f"Expected Flag Name")
        if self.tok.type != 'ID': raise SyntaxError(f"Expected Flag Name")
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))

        self.tok = self.lexer.token()
        if not self.tok or self.current_line < self.tok.lineno: raise SyntaxError(f"Expected '='")
        if self.tok.type != 'EQUALS': raise SyntaxError(f"Expected '='")
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        self.create_expression(current_list)
        self.current_line = self.tok.lineno

    def set_variable(self, current_list):
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        if_glob_var = (self.tok.type == 'GLOBVAR')
        self.tok = self.lexer.token()
        if not self.tok or self.current_line < self.tok.lineno: raise SyntaxError(f"Expected Variable Name")
        if self.tok.type != 'ID': raise SyntaxError(f"Expected Variable Name")

        if self.tok.value in list(self.all_func_lexes.keys()):
            raise SyntaxError(f'{self.tok.value} is a JDS Function')
        elif self.tok.value in self.all_variables_global and not if_glob_var:
            raise SyntaxError(f'{self.tok.value} already defined as GLOBVAR')
        elif self.tok.value in self.all_variables_created and if_glob_var:
            raise SyntaxError(f'{self.tok.value} already defined as VAR')

        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        var_name = self.tok.value
        if var_name in list(command.values()): raise SyntaxError(f"{var_name} is a reserved words")
        if var_name == self.import_name: raise SyntaxError(f"{var_name} already defined as import {self.import_file}")

        self.tok = self.lexer.token()
        if not self.tok or self.current_line < self.tok.lineno: raise SyntaxError(f"Expected '='")
        if self.tok.type != 'EQUALS': raise SyntaxError(f"Expected '='")
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        self.create_expression(current_list)
        self.current_line = self.tok.lineno

        if if_glob_var:
            if not (var_name in self.all_variables_global):
                self.all_variables_global.append(var_name)
        else:
            if not (var_name in self.all_variables_created):
                self.all_variables_created.append(var_name)

    def if_else_current(self, current_list, is_else=False):
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        if is_else is False: self.create_expression(current_list)
        self.current_line = self.tok.lineno

        self.tok = self.lexer.token()
        if self.tok.lineno == self.current_line: raise SyntaxError(f"Found {self.tok.value}, on Line {self.tok.lineno}")
        self.current_line = self.tok.lineno
        self.loop_if_current(current_list, is_else)

    def while_func(self, current_list):
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))

        self.create_expression(current_list)
        self.current_line = self.tok.lineno
        self.tok = self.lexer.token()
        if self.tok.lineno == self.current_line: raise SyntaxError(f"Found {self.tok.value}, on Line {self.tok.lineno}")
        self.current_line = self.tok.lineno
        
        self.while_for_loop(current_list, 'ENDWHILE')

    def for_func(self, current_list):
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))
        self.tok = self.lexer.token()
        if not self.tok or self.current_line < self.tok.lineno: raise SyntaxError(f"Expected Variable")
        elif self.tok.value in self.all_variables_global:
            current_list[-1].append(LexesValue(identifier='GLOBVAR', value=self.tok.value))
        elif self.tok.value in self.all_variables_created:
            current_list[-1].append(LexesValue(identifier='VAR', value=self.tok.value))
        elif self.tok.type in 'ID' and self.tok.value.startswith(self.import_name):
            self.tok = self.lexer.token()
            if not self.tok or self.current_line < self.tok.lineno or self.tok.type != 'DOT': raise SyntaxError(f"Expected '.'")
            self.tok = self.lexer.token()
            if not self.tok or self.current_line < self.tok.lineno or self.tok.type != 'ID': raise SyntaxError(f"Expected 'SET'")
            current_list[-1].append(LexesValue(identifier='SET', value=self.tok.value))
        else: raise SyntaxError(f"Expected Variable")

        self.tok = self.lexer.token()
        if not self.tok or self.current_line < self.tok.lineno or self.tok.type != 'TO': raise SyntaxError(f"Expected 'TO'")
        current_list[-1].append(LexesValue(identifier=self.tok.type, value=self.tok.value))

        self.create_expression(current_list)
        self.current_line = self.tok.lineno
        self.tok = self.lexer.token()
        if self.tok.lineno == self.current_line: raise SyntaxError(f"Found {self.tok.value}, on Line {self.tok.lineno}")
        self.current_line = self.tok.lineno
        self.while_for_loop(current_list, 'ENDFOR')

    def while_for_loop(self, current_list, rule):
        new_list = [[]]
        while True:
            if self.current_line < self.tok.lineno:
                self.current_line = self.tok.lineno
                new_list.append([])

            if self.tok.type == rule:
                if new_list[-1]: raise SyntaxError(f"Found {self.tok.value}, on Line {self.tok.lineno}")
                new_list = new_list[:-1]
                break

            elif self.tok.type == 'IF': self.if_else_current(new_list)
            elif self.tok.type in ['ELIF', 'ELSE']: raise SyntaxError(f"Did you mean if?, line {self.tok.lineno}")
            elif self.tok.type == 'ENDIF': raise SyntaxError(f"Please use if statements like a normal human being. line {self.tok.lineno}")

            elif self.check_function(new_list) != 'None': pass
            elif self.tok.type == 'END': raise SyntaxError(f"Expected '{rule}'")
            else: raise SyntaxError(f"{self.tok.type} not in {list(command.values()) + ['ID', 'NUMBER', 'STRING']}")

            self.tok = self.lexer.token()
            if not self.tok: raise SyntaxError(f"Expected 'endif'")
        current_list[-1].append(new_list)

    def loop_if_current(self, current_list, is_else=False):
        new_list = [[]]
        while True:
            if self.current_line < self.tok.lineno:
                self.current_line = self.tok.lineno
                new_list.append([])
            if self.tok.type == 'ENDIF':
                if new_list[-1]: raise SyntaxError(f"Found {self.tok.value}, on Line {self.tok.lineno}")
                new_list = new_list[:-1]
                break

            elif self.tok.type in 'IF':
                if is_else: raise SyntaxError(f"Please use if statements like a normal human being.")
                self.if_else_current(new_list)
            elif self.tok.type in ['ELIF', 'ELSE']:
                if is_else: raise SyntaxError(f"Please use if statements like a normal human being.")
                if new_list[-1]: raise SyntaxError(f"Found {self.tok.value}, on Line {self.tok.lineno}")
                new_list = new_list[:-1]
                current_list[-1].append(new_list)
                current_list.append([])
                self.if_else_current(current_list, True if self.tok.type == 'ELSE' else False)
                return

            elif self.check_function(new_list) != 'None': pass
            elif self.tok.type == 'END': raise SyntaxError(f"Expected 'endif'")
            else: raise SyntaxError(f"{self.tok.type} not in {list(command.values()) + ['ID', 'NUMBER', 'STRING']}")

            self.tok = self.lexer.token()
            if not self.tok: raise SyntaxError(f"Expected 'endif'")
        current_list[-1].append(new_list)

if __name__ == "__main__":
    jds = JDS()
    if len(sys.argv) < 2: result = jds.run()
    else:
        result = jds.run(sys.argv[1], False)
        pprint(result)