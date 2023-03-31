from jdm_kivy import *
from .entity.entities import Entity

class RPGCommand:

    _wait_animation = False
    _wait_time = 0
    _script_ended = True
    _entity_script : Entity = None
    
    __all_command__ = [
        'move_down',
        'move_up',
        'move_left',
        'move_right',
        
        'look_down',
        'look_up',
        'look_left',
        'look_right',
        
        'faceplayer',
        'wait_animation',
        'pause_event'
        'end_script',
        
    ]
    def __init__(self, root) -> None:
        self.root = root

    def move_down(self, target: int | Entity = None):
        target = self._get_target(target)

        target.all_actions.append(['set_move_npc', ['s']])

    def move_up(self, target: int | Entity = None):
        target = self._get_target(target)

        target.all_actions.append(['set_move_npc', ['w']])

    def move_left(self, target: int | Entity = None):
        target = self._get_target(target)

        target.all_actions.append(['set_move_npc', ['a']])

    def move_right(self, target: int | Entity = None):
        target = self._get_target(target)

        target.all_actions.append(['set_move_npc', ['d']])

    def look_down(self, target: int | Entity = None):
        target = self._get_target(target)

        target.all_actions.append(['set_look_npc', ['look_down']])
    def look_up(self, target: int | Entity = None):
        target = self._get_target(target)

        target.all_actions.append(['set_look_npc', ['look_up']])
    def look_left(self, target: int | Entity = None):
        target = self._get_target(target)

        target.all_actions.append(['set_look_npc', ['look_right']])
    def look_right(self, target: int | Entity = None):
        target = self._get_target(target)

        target.all_actions.append(['set_look_npc', ['look_left']])

    def faceplayer(self, target: int | Entity = None):
        target = self._get_target(target)
        if target is not self.main.player:
            target.all_actions.append(['set_look_on_player', [self.main.player]])

    def background(self, color, duration):
        self.main.animate_background(color, duration)
    
    def retbackground(self, duration):
        self.main.animate_background(None, duration)

    def message_box(self, text, type_='normal'):
        self.main.message_box.reset_message()
        self.main.message_box.display_message(text, type_)

    def _get_target(self, target):
        if target is None: target = self._entity_script
        elif type(target) == int: target = self.main.npc_id.get(target)
        elif target == 'player': target = self.main.player
        elif target == 'owner': target = self._entity_script

        if not target: raise('NO TARGET')
        else: return target

    def end_script(self):
        self._script_ended = True
        self._wait_animation = False
        self._wait_msg = False
        self._wait_time = 0
        self._entity_script = None

    def wait_animation(self): self._wait_animation = True
    def wait_message(self):
        self._wait_msg = True
        self.main.in_script_select = True
        self.main.continue_message_display = True

    def pause_event(self, time: float = 0.4): self._wait_time = time
    def start_script(self, entity):
        self._wait_animation = False
        self._wait_msg = False
        self._wait_time = 0
        self._script_ended = False
        self._entity_script = entity

    def check_command(self, command: str, *args):
        if not hasattr(self, 'main'): self.main = self.root.main.main

        if self._wait_time > 0:
            self._wait_time -= self.root.elapseTime
            return

        if self._wait_animation:
            for rect in self.main.all_entities.children:
                if (isinstance(rect, Entity)):
                    if rect.all_actions != []:
                        return
            if self.main.background_anim: return

        if self._wait_msg and self.main.message_box.start_message: return
        self.main.in_script_select = False
        self.main.continue_message_display = False

        self._wait_animation = False
        self._wait_msg = False
        self.main.script_index += 1
        if hasattr(self, command): getattr(self, command)(*args)
