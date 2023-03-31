import copy
import json
from .jdsalltoken import *

class JDSCompiler:

    all_command_key = {
        'move' : {
            'left' : 'move_left',
            'right' : 'move_right',
            'up' : 'move_up',
            'down' : 'move_down',
        },
        'look' : {
            'left' : 'look_left',
            'right' : 'look_right',
            'up' : 'look_up',
            'down' : 'look_down',
        }
    }
    number_where = {
        1: 'up',
        2: 'down',
        3: 'left',
        4: 'right',
    }
    def compile_move(self, args): return self.compile_move_look(args)
    def compile_look(self, args): return self.compile_move_look(args)
    def compile_move_look(self, args: list[LexesValue]):
        """
        TARGET: (NUMBER|PLAYER) WHERE: (LEFT|RIGHT|DOWN|UP) 
        """
        target = args[1].value
        if args[2].identifier == 'NUMBER':
            if args[2].value in [1, 2, 3, 4]: 
                where = self.number_where.get(args[2].value)
            else: raise RuntimeError(f"{args[2].value} not in [1, 2, 3, 4]")

        elif args[2].identifier == 'VAR':
            if self.all_local_variable.get(self.current_name).get(args[2].value) is not None:
                where = self.all_local_variable.get(self.current_name).get(args[2].value)
                if type(where) is not int: raise RuntimeError(F"This function only accept Integer[1, 2, 3, 4] and Direction")
                if where not in [1, 2, 3, 4]: raise RuntimeError(f"{args[2].value} not in [1, 2, 3, 4]")

            else: raise RuntimeError(F"Variable {args[2].value} not defined.")
        elif args[2].identifier == 'GLOBVAR':
            if self.all_global_variable.get(args[2].value) is not None:
                where = self.all_global_variable.get(args[2].value)
                if type(where) is not int: raise RuntimeError(F"This function only accept Integer[1, 2, 3, 4] and Direction")
                if where not in [1, 2, 3, 4]: raise RuntimeError(f"{args[2].value} not in [1, 2, 3, 4]")

            else: raise RuntimeError(F"Global Variable {args[2].value} not defined.")
        elif args[2].identifier == 'SET':
            if self.main_config.get(args[2].value) is None:
                self.compile_set([None, LexesValue(identifier='ID', value=args[2].value), None, [LexesValue(identifier='NUMBER', value='0')]])
                where = 0
            else: where = self.main_config.get(args[2].value)
            if type(where) is not int: raise RuntimeError(F"This function only accept Integer[1, 2, 3, 4] and Direction")
            if where not in [1, 2, 3, 4]: raise RuntimeError(f"{args[2].value} not in [1, 2, 3, 4]")

        else: where = args[2].value
        if type(where) is int: where = self.number_where.get(where)
        return [[self.all_command_key.get(args[0].value).get(where), target]]

    def compile_exit(self, *_):
        return [['end_script']]

    def compile_faceplayer(self, args: list[LexesValue]):
        return [[args[0].value, args[1].value]]

    def compile_waitanim(self, *_):
        return [['wait_animation']]

    def compile_pause(self, args: list[LexesValue]):
        result = self.evaluate_expression(args[1])
        if type(result) is not int: raise RuntimeError(f"Pause function only accept Integer")
        return [['pause_event', result/100]]

    def compile_call(self, args: list[LexesValue], lexes):
        if args[1].value in list(lexes.keys()):
            return self.set_compile(args[1].value)
        else: raise SyntaxError(f"{args[1].value} is not a defined register")

    def compile_help(self, *_):
        commands = "\n".join([f" - {_com} : {_val}" for _com, _val in command.items()])
        print(commands)
        return None

    def compile_set(self, args: list[LexesValue]):
        self.main_config[args[1].value] = self.evaluate_expression(args[3], True)

    def compile_globvar(self, args: list[LexesValue]):
        self.all_global_variable[args[1].value] = self.evaluate_expression(args[3], True)

    def compile_var(self, args: list[LexesValue]):
        self.all_local_variable.get(self.current_name)[args[1].value] = self.evaluate_expression(args[3], True)

    def evaluate_expression(self, args, is_set=False):
        all_str = ""
        is_string = False
        for arg in args:
            if arg.identifier == 'VAR':
                if self.all_local_variable.get(self.current_name).get(arg.value) is not None:
                    all_str += str(self.all_local_variable.get(self.current_name).get(arg.value))+' '
                else: raise RuntimeError(F"Variable {arg.value} not defined.")
            elif arg.identifier == 'GLOBVAR':
                if self.all_global_variable.get(arg.value) is not None:
                    all_str += str(self.all_global_variable.get(arg.value))+' '
                else: raise RuntimeError(F"Global Variable {arg.value} not defined.")
            elif arg.identifier == 'SET':
                if self.main_config.get(arg.value) is None:
                    self.compile_set([None, LexesValue(identifier='ID', value=arg.value), None, [LexesValue(identifier='NUMBER', value='0')]])
                    all_str += '0 '
                else: all_str += str(self.main_config.get(arg.value))+' '

            elif arg.identifier == 'TRUE':
                all_str += '1 '
            elif arg.identifier == 'FALSE':
                all_str += '0 '
            elif arg.identifier == 'NONE':
                all_str += '0 '
            elif arg.identifier == 'STRING':
                is_string = True
                all_str += f"'{arg.value}' "
            else: all_str += str(arg.value)+' '

        try: result = eval(all_str)
        except: raise RuntimeError(F"Wrong Expression")
        if is_set and is_string: return f"'{result}'"
        return result

    def is_valid_color(self, color_str):
        try:
            color_int = int(color_str, 16)
            return 0 <= color_int <= 0xffffff or 0 <= color_int <= 0xffffffff
        except ValueError:
            return False

    def compile_background(self, args: list[LexesValue]):
        if (self.is_valid_color(args[1].value)):
            return [['background', args[1].value, args[2].value/100]]
        raise RuntimeError(f"Invalid String Color")

    def compile_if(self, args: list[LexesValue]):
        if (self.evaluate_expression(args[1])):
            return self.compile_all(args[2]), True
        return None, False

    def compile_elif(self, args: list[LexesValue]):
        if (self.evaluate_expression(args[1])):
            return self.compile_all(args[2]), True
        return None, False

    def compile_else(self, args: list[LexesValue]):
        return self.compile_all(args[1])

    def compile_while(self, args: list[LexesValue]):
        new_list = []
        while (self.evaluate_expression(args[1])):
            new_list.extend(self.compile_all(args[2]))
        return new_list

    def compile_for(self, args: list[LexesValue]):
        var_name = None
        current_dict = None
        if args[1].identifier == 'VAR':
            if self.all_local_variable.get(self.current_name).get(args[1].value) is not None:
                var_name = self.all_local_variable.get(self.current_name).get(args[1].value)
                if type(var_name) is not int: raise RuntimeError(F"For loop variable only accept Integer")
                current_dict = self.all_local_variable.get(self.current_name)
            else: raise RuntimeError(F"Variable {args[1].value} not defined.")
        elif args[1].identifier == 'GLOBVAR':
            if self.all_global_variable.get(args[1].value) is not None:
                var_name = self.all_global_variable.get(args[1].value)
                if type(var_name) is not int: raise RuntimeError(F"For loop variable only accept Integer")
                current_dict = self.all_global_variable
            else: raise RuntimeError(F"Global Variable {args[1].value} not defined.")
        elif args[1].identifier == 'SET':
            if self.main_config.get(args[1].value) is None:
                self.compile_set([None, LexesValue(identifier='ID', value=args[1].value), None, [LexesValue(identifier='NUMBER', value='0')]])
                var_name = '0'
            else: var_name = self.main_config.get(args[1].value)
            if type(var_name) is not int: raise RuntimeError(F"For loop variable only accept Integer")
            current_dict = self.main_config

        else: raise RuntimeError(F"Variable {args[1].value} not defined.")

        range_ = self.evaluate_expression(args[3])
        if type(range_) is not int: raise RuntimeError(F"For loop variable only accept Integer")

        new_list = []
        for i in range(var_name, range_):
            new_list.extend(self.compile_all(args[4]))
            var_name += 1
            current_dict[args[1].value] = var_name
        return new_list

    def compile_print(self, args: list[LexesValue]):
        result = self.evaluate_expression(args[1])
        print(result, end='')

    def compile_message(self, args: list[LexesValue]):
        return [['message_box', str(self.evaluate_expression(args[1])), args[2].value]]

    def compile_waitmsg(self, *_):
        return [['wait_message']]

    def compile_all(self, arg_list=None):
        condition = False
        main_script = []

        if arg_list is None: arg_list = self.lexes.get(self.current_name)
        for command in arg_list:
            main_command = command[0]
            if main_command.value in all_parsable:
                if main_command.identifier == 'CALL':
                    orig_dict = copy.copy(self.all_local_variable[self.current_name])
                    orig_name = self.current_name
                    result = self.compile_call(command, self.lexes)
                    self.compiled_script[command[1].value] = result
                    main_script.extend(result)
                    self.current_name = orig_name
                    self.all_local_variable[self.current_name] = orig_dict
                elif main_command.identifier == 'IF':
                    result, check = getattr(self, 'compile_'+main_command.value)(command)
                    if result: main_script.extend(result)
                    if check: condition = True
                elif main_command.identifier == 'ELIF':
                    if condition is False:
                        result, check = getattr(self, 'compile_'+main_command.value)(command)
                        if result: main_script.extend(result)
                        if check: condition = True
                elif main_command.identifier == 'ELSE':
                    if condition is False:
                        result = getattr(self, 'compile_'+main_command.value)(command)
                        if result: main_script.extend(result)
                    condition = False
                else:
                    condition = False
                    result = getattr(self, 'compile_'+main_command.value)(command)
                    if result: main_script.extend(result)
            elif main_command.value == 'back': break
            else: raise RuntimeError(f"{main_command.identifier} is not a parsable function")
        return main_script

    def set_compile(self, start):
        self.current_name = start
        self.all_local_variable[self.current_name] = {}
        return self.compile_all()

    def compile(self, lexes, start, filename, main_config, save=True):
        self.lexes = lexes
        self.main_config = main_config
        self.all_local_variable = {}
        self.all_global_variable = {}
        self.compiled_script = {}
        result = self.set_compile(start)
        if filename and save:
            with open(filename, 'w') as fp: json.dump(self.main_config, fp)

        return result
