import os
from jdm_kivy import *
from .entity_func import get_npc_direction

class MainBackGround(Rectangle):

    def __init__(self, root, location, **kwargs):
        super().__init__(**kwargs)
        self.location = location
        self.main = root
        self.started = False

    def on_start(self):
        self.set_map_config()
        self.configure_map()
        self.started = True

    def set_map_config(self):
        self.map_config = self.main.main_map_config

    def configure_map(self):
        main_map = self.main.all_maps_config.get(
            f"Map{self.map_config.get('CurrentMap')}").get(
            f"{self.map_config.get('CurrentIndex')}")

        self.map_list = main_map.get('Map')
        self.set_size_and_pos()

        self.original_pos = self.pos
        self.x, self.y = self.pos
        self._main_image = JDMImage(
            anim_delay=1/get_gif_frames(main_map.get(self.location)),
            source=main_map.get(self.location)
        )
        self._main_image.bind(texture=self.update_texture)
        self.update_texture()

    def set_size_and_pos(self): ...
    def set_size(self): ...
    def update_texture(self, *_): ...

    def update(self):
        if self.started is False:
            self.on_start()
            return

        self.pos = (
            self.x - self.main.camera_x,
            self.y - self.main.camera_y
        )

class BackGroundMap(MainBackGround):
    
    def set_size(self):
        self.size = (
            (self.main.block_size*40),
            (self.main.block_size*40)
        )

    def set_size_and_pos(self):
        self.set_size()
        self.pos = (
            self.main.player.pos[0] - self.main.block_size*20 - self.main.block_size*self.main.player.x_position,
            self.main.player.pos[1] - self.main.block_size*20 - self.main.block_size*self.main.player.y_position
        )
        self.original_pos = self.pos
        self.x, self.y = self.pos
        self.pos = (
            self.x - self.main.camera_x,
            self.y - self.main.camera_y
        )

    def update_texture(self, *_):
        self._main_image.texture.wrap = 'repeat'
        self._main_image.texture.uvsize = (20, 20)
        self._main_image.texture.mag_filter = 'nearest'
        self._main_image.texture.flip_vertical()
        self.texture = self._main_image.texture
    
class RPGMap(MainBackGround):

    def set_size(self):
        self.size = (
            self.main.block_size*len(self.map_list[0]),
            self.main.block_size*len(self.map_list)
        )

    def set_size_and_pos(self):
        self.set_size()
        self.pos = (
            self.main.player.pos[0] - self.main.block_size*self.main.player.x_position,
            self.main.player.pos[1] - self.main.block_size*self.main.player.y_position
        )
        self.original_pos = self.pos
        self.x, self.y = self.pos
        self.pos = (
            self.x - self.main.camera_x,
            self.y - self.main.camera_y
        )

    def update_texture(self, *_):
        self._main_image.texture.mag_filter = 'nearest'
        self.texture = self._main_image.texture
        self.texture.mag_filter = 'nearest'

class EntityAnimation(Rectangle):

    def __init__(
            self,
            root,
            position: tuple = (0, 0),
            speed: float = 0.4,
            behavior: int = 1,
            path_anim: str = 'None',
            animate: bool = True,
            max_loops: int = 1,
            **kwargs
        ):
        super().__init__(**kwargs)

        self.main = root
        self.x, self.y = self.pos
        self.color = Color(rgb=GetColor('ffffff'))

        self.max_loops = max_loops
        self.animate = animate
        self.speed = speed
        self.behavior = behavior
        self.position = position
        self.path_anim = path_anim

        self.set_animation()
        self.set_position()
        self.load_texture()

    def set_animation(self):
        self.loops = 0
        self.size_ = get_image_size( 'rasset/animation/' + self.path_anim)
        self.main_animation = 'rasset/animation/' + self.path_anim

    def set_size(self):
        self.size = (
            self.size_[0]*self.main.game_zoom,
            self.size_[1]*self.main.game_zoom
        )

    def set_position(self):
        self.set_size()
        self.x_position, self.y_position = self.position
        self.pos = (
            self.main.main_map.original_pos[0] + self.main.block_size*self.x_position,
            self.main.main_map.original_pos[1] + self.main.block_size*self.y_position
        )
        self.x, self.y = self.pos
        self.pos = (
            self.x - self.main.camera_x,
            self.y - self.main.camera_y
        )

    def update(self):
        if ((self.loops > 0 and self.loops >= self.max_loops) or self.animate is False):
            if self.behavior == 1:
                for rect in self.main.all_entities.children:
                    if isinstance(rect, Entity):
                        if rect.x_position == self.x_position and rect.y_position == self.y_position:
                            break
                else:
                    self.remove_from_entities()
                    return
            else:
                self.remove_from_entities()
                return

        self.pos = (
            self.x - self.main.camera_x,
            self.y - self.main.camera_y
        )

    def remove_from_entities(self):
        self.main.all_entities.remove(self.color)
        self.main.all_entities.remove(self)

    def load_texture(self, look=False):
        texture = self.main_animation
        if os.path.exists(texture):
            if hasattr(self, '__image'):
                self.__image.unbind(texture=self.update_texture)
                del self.__image

            self.__image = JDMImage(opacity=0,
                source=texture,
                anim_delay=-1 if self.animate is False else (self.speed / (4 if look else 1))/get_gif_frames(texture),
                anim_loop=self.max_loops)

            if self.animate is False and self.__image._coreimage.image.textures:
                self.__image.texture = self.__image._coreimage.image.textures[-1]

            self.__image.bind(texture=self.update_texture)
            self.update_texture()

    def update_texture(self, *_):
        self.texture = self.__image.texture
        self.texture.mag_filter = 'nearest'
        if self.__image._coreimage._anim_index + 1 == len(self.__image._coreimage.image.textures):
            self.loops += 1

class Entity(Rectangle):

    def __init__(
            self,
            root,
            size_,
            position: tuple = (0, 0),
            speed: float = 0.4,
            path_anim: str = 'None',
            current_behavior = 'look_down',
            **kwargs
        ):
        super().__init__(**kwargs)

        self.size_ = size_
        self.color = Color(rgba=GetColor('ffffff'))
        self.behave_placeholder = current_behavior
        self.current_behavior = lambda : None

        self.speed = speed
        self.main = root
        self.root = self.main.root

        self.current_anim = 'down'
        self.x, self.y = self.pos
        self.original_position = position
        self.position = position
        self.path_anim = path_anim

        self.all_variables()
        self.all_animations()
        self.load_texture()

    def all_animations(self):
        self.hidden_anim = 'rasset/transparent.png'
        self.look_down = self.path_anim + '/look_down.png'
        self.look_up = self.path_anim + '/look_up.png'
        self.look_left = self.path_anim + '/look_left.png'
        self.look_right = self.path_anim + '/look_right.png'

        self.look_down_anim = self.path_anim + '/look_down.zip'
        self.look_up_anim = self.path_anim + '/look_up.zip'
        self.look_left_anim = self.path_anim + '/look_left.zip'
        self.look_right_anim = self.path_anim + '/look_right.zip'

        self.walk_down_animation = self.path_anim + '/walk_down.zip'
        self.walk_up_animation = self.path_anim + '/walk_up.zip'
        self.walk_left_animation = self.path_anim + '/walk_left.zip'
        self.walk_right_animation = self.path_anim + '/walk_right.zip'

        self._all_anim_ = {
            'hidden': self.hidden_anim,
            'down': self.look_down,
            'up': self.look_up,
            'left': self.look_left,
            'right': self.look_right,
            
            'look_down': self.look_down_anim,
            'look_up': self.look_up_anim,
            'look_left': self.look_left_anim,
            'look_right': self.look_right_anim,
            
            'anim_down': self.walk_down_animation,
            'anim_up': self.walk_up_animation,
            'anim_left': self.walk_left_animation,
            'anim_right': self.walk_right_animation
        }

    def load_texture(self, look=False):
        texture = self._all_anim_.get(self.current_anim, self.hidden_anim)
        if os.path.exists(texture):
            if hasattr(self, '__image'):
                self.__image.unbind(texture=self.update_texture)
                del self.__image

            self.__image = JDMImage(
                opacity=0,
                source=texture,
                anim_delay=(self.speed / (4 if look else 1))/get_gif_frames(texture),
                anim_loop=1
            )
            self.__image.bind(texture=self.update_texture)
            self.texture = self.__image.texture
            self.texture.mag_filter = 'nearest'

    def update_texture(self, *_):
        self.texture = self.__image.texture
        self.texture.mag_filter = 'nearest'

    def all_variables(self):
        self.all_actions = []
        self.add_animation = True
        self.current_in_script = False

        self.finished_actions = True
        self.behavior_duration = 0

        self.started = False
        self._look_timeout = 0.1
        self._moving = False
        self.move_a = False
        self.move_d = False
        self.move_w = False
        self.move_s = False

        self.x_position = 0
        self.y_position = 0

    def on_start(self):
        self.set_behavior(self.behave_placeholder)

        self.map_config = self.main.main_map_config
        self.main_map = self.main.all_maps_config.get(
            f"Map{self.map_config.get('CurrentMap')}").get(
                f"{self.map_config.get('CurrentIndex')}")

        self.map_behavior = list(reversed(self.main_map.get('Behavior')))
        self.map_hitbox = list(reversed(self.main_map.get('HitBox')))
        self.set_position()
        self.checked_if_currently_on_behavior()
        self.started = True

    def set_behavior(self, behavior):
        behave = getattr(self.main.all_behavior, behavior)
        if self.behave_placeholder in ['look_down', 'look_left', 'look_up', 'look_right', 'none', 'hidden']:
            behave(self)

        else: self.current_behavior = lambda : behave(self)

    def set_position(self):
        self.set_size()
        self.x_position, self.y_position = self.position
        self.pos = (
            self.main.main_map.original_pos[0] + self.main.block_size*self.x_position - ((self.size[0]-self.main.block_size)/2),
            self.main.main_map.original_pos[1] + self.main.block_size*self.y_position
        )
        self.x, self.y = self.pos
        self.pos = (
            self.x - self.main.camera_x,
            self.y - self.main.camera_y
        )
    
    def set_size(self):
        self.size = (
            self.size_[0]*self.main.game_zoom,
            self.size_[1]*self.main.game_zoom
        )

    def update(self):
        if self.started is False:
            self.on_start()
            return

        self.pos = (
            self.x - self.main.camera_x,
            self.y - self.main.camera_y
        )
        self.check_timeout()
        self.check_behavior()
        self.check_actions()

    def check_if_possible_move(self, x: int = 0, y: int = 0):
        if self.y_position+y >= len(self.map_hitbox) or self.y_position+y < 0: return False
        if self.x_position+x >= len(self.map_hitbox) or self.x_position+x < 0: return False

        for rect in self.main.all_entities.children:
            if (isinstance(rect, Entity)
            and rect.pos[0] >= -rect.size[0] and rect.pos[0] < Window.width
            and rect.pos[1] >= -rect.size[1] and rect.pos[1] < Window.height):
                if rect.x_position == self.x_position+x and rect.y_position == self.y_position+y:
                    return False

        tiles = self.map_hitbox[self.y_position+y][self.x_position+x]
        if tiles == 0:
            if self.map_behavior[self.y_position+y][self.x_position+x] == 1:
                self.add_animation = True
            else: self.add_animation = False
            return True
        else: return False

    def check_timeout(self):
        if self._moving is False:
            self._look_timeout -= self.root.elapseTime
        else: self._look_timeout = 0.08

    def check_behavior(self):
        if self.current_in_script is False:
            if self.behavior_duration <= 0:
                self.current_behavior()
            self.behavior_duration -= self.root.elapseTime

    def check_actions(self):
        if self.all_actions != [] and self.finished_actions:
            self.finished_actions = False
            getattr(self, self.all_actions[0][0])(*self.all_actions[0][1])

    def move_animation(self, x: int = 0, y: int = 0):
        self._moving = True
        if x != 0: self.x_position += 1 if x > 0 else -1
        if y != 0: self.y_position += 1 if y > 0 else -1
        self.position = self.x_position, self.y_position
        anim = Animation(
            x=self.x + x,
            y=self.y + y,
            d=(self.speed)
        )
        anim.bind(on_complete=self.on_complete_anim)
        anim.bind(on_progress=self.checked_progress)
        anim.start(self)

    def checked_if_currently_on_behavior(self):
        if self.map_behavior[self.y_position][self.x_position] == 1:
            self.main.all_entities.add(
                EntityAnimation(self.main, (self.x_position, self.y_position), 0.5, 1, 'GrassAnimation.gif', False))

    def checked_progress(self, _, __, progress):
        if progress * 100 >= (90 if self.current_anim.endswith('up') else 60) and self.add_animation:
            self.add_animation = False
            if self.map_behavior[self.y_position][self.x_position] == 1:
                self.main.all_entities.add(
                    EntityAnimation(self.main, (self.x_position, self.y_position), 0.5, 1, 'GrassAnimation.gif'))

    def on_complete_anim(self, *_):
        if self.current_anim.endswith('down'): self.current_anim = 'down'
        elif self.current_anim.endswith('up'): self.current_anim = 'up'
        elif self.current_anim.endswith('left'): self.current_anim = 'left'
        elif self.current_anim.endswith('right'): self.current_anim = 'right'
        else: self.current_anim = 'down'
        self.set_anim_complete()
    
    def no_move_complete(self):
        if self.move_s: self.set_look_npc('look_down')
        elif self.move_w: self.set_look_npc('look_up')
        elif self.move_a: self.set_look_npc('look_left')
        elif self.move_d: self.set_look_npc('look_right')
        self.set_anim_complete()
    
    def set_anim_complete(self):
        self.load_texture()
        self._moving = False
        self.finished_actions = True
        if self.all_actions != []: self.all_actions = self.all_actions[1:]

    def set_npc_hide(self, duration=0):
        anim = Animation(a=0, duration=duration)
        anim.start(self.color)

    def set_npc_show(self, duration=0):
        anim = Animation(a=1, duration=duration)
        anim.start(self.color)

    def set_npc_color(self, color, duration=0):
        anim = Animation(rgba=GetColor(color), duration=duration)
        anim.start(self.color)

    def set_move_npc(self, move: str): 
        if self._moving: return
        self._look_timeout = 0.08
        if   move == 'w' and self.move_s is False:
            self.move_w = True
            self.move_entity()
            self.move_w = False
        elif move == 's' and self.move_w is False:
            self.move_s = True
            self.move_entity()
            self.move_s = False
        if   move == 'a' and self.move_d is False:
            self.move_a = True
            self.move_entity()
            self.move_a = False
        elif move == 'd' and self.move_a is False:
            self.move_d = True
            self.move_entity()
            self.move_d = False

    def set_look_npc(self, move: str):
        if move == self.current_anim or move[5:] == self.current_anim:
            self.on_complete_anim()
            return

        self._moving = True
        self.current_anim = move
        self.load_texture(True)
        Clock.schedule_once(self.on_complete_anim, self.speed/4)

    def set_look_on_player(self, entity):
        if self._moving is False:
            move = get_npc_direction(entity.pos, self.pos)
            self.set_look_npc('look_'+move)

    def handle_look_anim(self, anim_type):
        self._moving = True
        self.current_anim = anim_type
        self.load_texture(True)
        Clock.schedule_once(self.on_complete_anim, self.speed/4)

    def handle_move_anim(self, anim_type, **kwargs):
        self.current_anim = anim_type
        self.load_texture()
        self.move_animation(**kwargs)

    def move_entity(self):
        if self._moving is False:
            # Looking Animation
            if self._look_timeout <= 0 and self.move_w and not self.current_anim == 'up':
                self.handle_look_anim('look_up')
            elif self._look_timeout <= 0 and self.move_s and not self.current_anim == 'down':
                self.handle_look_anim('look_down')
            elif self._look_timeout <= 0 and self.move_d and not self.current_anim == 'right':
                self.handle_look_anim('look_right')
            elif self._look_timeout <= 0 and self.move_a and not self.current_anim == 'left':
                self.handle_look_anim('look_left')

            # Walking Animation
            elif self.move_w and self.check_if_possible_move(y= 1):
                self.handle_move_anim('anim_up', y =  self.root.main.main.block_size)
            elif self.move_s and self.check_if_possible_move(y=-1):
                self.handle_move_anim('anim_down', y = -self.root.main.main.block_size)
            elif self.move_d and self.check_if_possible_move(x= 1):
                self.handle_move_anim('anim_right', x =  self.root.main.main.block_size)
            elif self.move_a and self.check_if_possible_move(x=-1):
                self.handle_move_anim('anim_left', x = -self.root.main.main.block_size)
            else: self.no_move_complete()

    def find_entity_in_position(self, x, y):
        for rect in self.main.all_entities.children:
            if (isinstance(rect, Entity)
            and rect.pos[0] >= -rect.size[0] and rect.pos[0] < Window.width
            and rect.pos[1] >= -rect.size[1] and rect.pos[1] < Window.height):
                if rect.x_position == x and rect.y_position == y:
                    return rect
        return None

class NPC(Entity):

    def __init__(
            self,         
            root,
            size_,
            position: tuple = (0, 0),
            speed: float = 0.4,
            path_anim: str = 'None',
            current_behavior = 'look_down',
            npc_id : int = 0,
            script: str = '',
            **kwargs
        ):
        super().__init__(root, size_, position, speed, path_anim, current_behavior, **kwargs)
        self.npc_id = npc_id
        self.script = script

class Player(Entity):

    def __init__(
            self,
            root,
            size_,
            position: tuple = (0, 0),
            speed: float = 0.4,
            path_anim: str = 'None',
            **kwargs
        ):
        super().__init__(root, size_, position, speed, path_anim, 'look_down', **kwargs)

    def all_variables(self):
        super().all_variables()
        self.using_camera = True
        self.move_camera = False
        self.set_position()

    def set_position(self):
        self.set_size()
        self.map_config = self.main.main_map_config
        self.x_position = self.map_config.get('CurrentPlayerX')
        self.y_position = self.map_config.get('CurrentPlayerY')
        self.position = self.x_position, self.y_position

    def interact(self):
        entity = None
        if   self.current_anim == 'up'   : entity = self.find_entity_in_position(self.x_position, self.y_position+1)
        elif self.current_anim == 'down' : entity = self.find_entity_in_position(self.x_position, self.y_position-1)
        elif self.current_anim == 'left' : entity = self.find_entity_in_position(self.x_position-1, self.y_position)
        elif self.current_anim == 'right': entity = self.find_entity_in_position(self.x_position+1, self.y_position)

        if entity and entity.current_anim in ['up', 'down', 'left', 'right']:
            if isinstance(entity, NPC): self.main.handle_script_update(entity)

    def move_animation(self, x: int = 0, y: int = 0):
        self._moving = True
        if self.using_camera:
            if x != 0: self.x_position += 1 if x > 0 else -1
            if y != 0: self.y_position += 1 if y > 0 else -1
            self.position = self.x_position, self.y_position
            anim = Animation(
                camera_x=self.main.camera_x + x,
                camera_y=self.main.camera_y + y,
                d=(self.speed)
            )
            anim.bind(on_complete=self.on_complete_anim)
            anim.bind(on_progress=self.checked_progress)
            anim.start(self.main)
        else: super().move_animation(x, y)

    def check_if_possible_move(self, x: int = 0, y: int = 0):
        if self.y_position+y >= len(self.map_hitbox) or self.y_position+y < 0: return False
        if self.x_position+x >= len(self.map_hitbox) or self.x_position+x < 0: return False

        for rect in self.main.all_entities.children:
            if (isinstance(rect, Entity)
            and rect.pos[0] >= -rect.size[0] and rect.pos[0] < Window.width
            and rect.pos[1] >= -rect.size[1] and rect.pos[1] < Window.height):
                if rect.x_position == self.x_position+x and rect.y_position == self.y_position+y:
                    if rect == self.main.dog: break
                    return False

        tiles = self.map_hitbox[self.y_position+y][self.x_position+x]
        if tiles == 0:
            if self.map_behavior[self.y_position+y][self.x_position+x] == 1:
                self.add_animation = True
            else: self.add_animation = False
            return True
        else: return False

    def update(self):
        if self.started is False:
            self.on_start()
            return

        if self.main.script_runner._script_ended:
            self.move_entity()
            if self.move_camera is False: self.pos = self.x, self.y
            else: self.pos = (
                self.x - self.main.camera_x,
                self.y - self.main.camera_y
            )
            self.check_timeout()
        else: self.check_actions()
