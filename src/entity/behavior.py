import random
from .entities import Entity
from .entity_func import what_move_to_target

class EntityBehavior:

    @staticmethod
    def look_around(entity: Entity):
        move = random.choice(['left', 'right', 'down', 'up'])
        entity.set_look_npc('look_'+move)
        entity.behavior_duration = 2

    @staticmethod
    def walk_around(entity: Entity):
        x, y = entity.position
        x1, y1 = entity.original_position
        move_choices = ['a', 'd', 's', 'w']

        if x-x1 < -5: move_choices.remove('a')
        elif x-x1 > 5: move_choices.remove('d')

        if y-y1 < -5: move_choices.remove('s')
        elif y-y1 > 5: move_choices.remove('w')

        move = random.choice(move_choices)
        entity.set_move_npc(move)
        entity.behavior_duration = 2

    @staticmethod
    def walk_towards_player_front(entity: Entity):
        if entity._moving is False:
            move = what_move_to_target(
                entity,
                entity.main.player.position,
                entity.position,
                entity.main.player.current_anim,
                'front'
            )
            if move == 'n':
                entity.set_look_on_player(entity.main.player)
                entity.behavior_duration = 0
                return

            entity.set_move_npc(move)
            entity.behavior_duration = 0
    
    @staticmethod
    def walk_towards_player(entity: Entity):
        if entity._moving is False:
            move = what_move_to_target(
                entity,
                entity.main.player.position,
                entity.position,
                entity.main.player.current_anim,
                'none'
            )
            if move == 'n':
                entity.set_look_on_player(entity.main.player)
                entity.behavior_duration = 0
                return

            entity.set_move_npc(move)
            entity.behavior_duration = 0

    @staticmethod
    def walk_towards_player_back(entity: Entity):
        if entity._moving is False:
            move = what_move_to_target(
                entity,
                entity.main.player.position,
                entity.position,
                entity.main.player.current_anim,
                'back'
            )
            if move == 'n':
                entity.set_look_on_player(entity.main.player)
                entity.behavior_duration = 0
                return

            entity.set_move_npc(move)
            entity.behavior_duration = 0
    
    @staticmethod
    def walk_towards_player_left(entity: Entity):
        if entity._moving is False:
            move = what_move_to_target(
                entity,
                entity.main.player.position,
                entity.position,
                entity.main.player.current_anim,
                'left'
            )
            if move == 'n':
                entity.set_look_on_player(entity.main.player)
                entity.behavior_duration = 0
                return

            entity.set_move_npc(move)
            entity.behavior_duration = 0

    @staticmethod
    def walk_towards_player_right(entity: Entity):
        if entity._moving is False:
            move = what_move_to_target(
                entity,
                entity.main.player.position,
                entity.position,
                entity.main.player.current_anim,
                'right'
            )
            if move == 'n':
                entity.set_look_on_player(entity.main.player)
                entity.behavior_duration = 0
                return

            entity.set_move_npc(move)
            entity.behavior_duration = 0

    @staticmethod
    def none(entity: Entity): ...

    @staticmethod
    def look_down(entity: Entity):
        entity.current_anim = 'down'
        entity.load_texture()

    @staticmethod
    def look_up(entity: Entity):
        entity.current_anim = 'up'
        entity.load_texture()

    @staticmethod
    def look_left(entity: Entity):
        entity.current_anim = 'left'
        entity.load_texture()

    @staticmethod
    def look_right(entity: Entity):
        entity.current_anim = 'right'
        entity.load_texture()

    @staticmethod
    def hidden(entity: Entity):
        entity.set_npc_hide(0)
