import jds
import json
from jdm_kivy import *
from .all_text import All_Text_Texture
from .entity.entities import Entity, EntityAnimation, Player, RPGMap, NPC, BackGroundMap
from .entity.behavior import EntityBehavior
from .message.message_box import MessageBox
from kivy.animation import Animation
from .all_command import RPGCommand
from .itemslot import ItemSlot
from kivy.core.image import Image as CoreImage

JDMConfig.activate_root_clock()
JDMConfig.activate_display_fps()

class MainScreen(JDMScreen):

    def update(self):
        super().update()
        self.main.update()

    def keyboard_down(self, window, scancode=None, key=None, keyAscii=None, *args):
        keycode = JDMKeyboard.keycode_to_string(key).lower()
        if keycode == 'add':
            self.main.game_zoom *= 1.02
            self.main.update_size()

        elif keycode == 'min':
            self.main.game_zoom *= 0.98
            self.main.update_size()

        elif self.main.in_script is False:
            if   keycode == 'w' and self.main.player.move_s is False: self.main.player.move_w = True
            elif keycode == 's' and self.main.player.move_w is False: self.main.player.move_s = True
            if   keycode == 'a' and self.main.player.move_d is False: self.main.player.move_a = True
            elif keycode == 'd' and self.main.player.move_a is False: self.main.player.move_d = True            
        return super().keyboard_down(window, scancode, key, keyAscii, *args)

    def keyboard_up(self, window, scancode=None, key=None, keyAscii=None, *args):
        keycode = JDMKeyboard.keycode_to_string(key).lower()
        if self.main.in_script is False:
            if keycode == 'w': self.main.player.move_w = False # W
            if keycode == 's': self.main.player.move_s = False # S
            if keycode == 'a': self.main.player.move_a = False # A
            if keycode == 'd': self.main.player.move_d = False # D
            if keycode == 'space': self.main.player.interact() # Space
        elif self.main.in_script and self.main.in_script_select:
            if keycode == 'space': self.main.interact_script() # Space
        elif self.main.in_script and self.main.key_script_interact:
            if keycode == 'w': self.main.player.up_key_script() # W
            if keycode == 's': self.main.player.down_key_script() # S
            if keycode == 'a': self.main.player.left_key_script() # A
            if keycode == 'd': self.main.player.right_key_script() # D
        return super().keyboard_up(window, scancode, key, keyAscii, *args)

class MainField(JDMWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = self.root.size
        self.set_main_game_config()
        self.all_variables()

        self.display_some_canvas()
        self.display_entities()
        self.display_player()
        self.display_background()
        self.display_all_item_slot()
        self.set_arrow()

    def set_arrow(self):
        Window.show_cursor = False
        with self.canvas:
            txt = CoreImage('rasset/arrow.png').texture
            txt.mag_filter = 'nearest'
            self.rect_cursor = Rectangle(size=(dp(32), dp(32)), texture=txt)
            Window.bind(mouse_pos=lambda _, pos, *__: setattr(self.rect_cursor, 'pos', (pos[0], pos[1]-dp(32))))

    def set_main_game_config(self):
        self.main_config = json_obj('jsons/game_config.json')
        self.all_maps_config = json_obj('jsons/all_maps.json')
        self.main_map_config : dict = self.main_config.get('MapConfig')

        self.event_map = json_obj('jsons/events_map.json')

    def all_variables(self):
        self.game_start = False
        self.in_script = False
        self.in_script_select = False
        self.key_script_interact = False
        self.camera_x = self.camera_y = 0

        self.game_zoom = self.main_config.get('GameZoom')
        self.block_size = dp(self.main_config.get('BlockSize')) * self.game_zoom
        self.block2_size = [self.block_size, self.block_size]

        self.all_text = All_Text_Texture
        self.script_runner = RPGCommand(self.root)
        self.all_behavior = EntityBehavior()
        self.jds_compiler = jds.JDS()

    def display_some_canvas(self):
        self.background_map = BackGroundMap(self, 'BGLocation')
        self.main_map = RPGMap(self, 'Location')
        self.second_layer_map = RPGMap(self, 'Location2')
        self.third_layer_map = RPGMap(self, 'Location3')        
        self.message_box = MessageBox(self, self.game_zoom, self.all_text)
        self.third_layer_canvas = Canvas()

        self.canvas.add(self.background_map)
        self.canvas.add(self.main_map)
        self.canvas.add(self.second_layer_map)
        self.third_layer_canvas.add(self.third_layer_map)

    def display_entities(self):
        self.npc_id = {}
        self.all_entities = Canvas()
        self.all_entity_anim_color = []
        self.event_current_config = self.event_map.get(
            'Map'+self.main_map_config.get('CurrentMap')).get(
                self.main_map_config.get('CurrentIndex'))

        for npc_ in self.event_current_config.get('NPC'):
            npc = self.event_current_config.get('NPC').get(npc_)
            size = get_image_size('rasset/npc/'+npc.get('sprite')+'/look_down.png')

            self.npc_id[npc.get('id')] = NPC(
                root=self,
                position=npc.get('position'),
                size_=size,
                path_anim='rasset/npc/'+npc.get('sprite'),
                current_behavior=npc.get('behavior'),
                npc_id=npc.get('id'),
                script=self.jds_compiler.set_script(npc.get('script')))

        for npc in self.npc_id:
            self.all_entities.add(self.npc_id.get(npc).color)
            self.all_entities.add(self.npc_id.get(npc))

        self.canvas.add(self.all_entities)
        self.canvas.add(self.third_layer_canvas)

    def display_player(self):
        config = self.main_config.get('NPC')
        self.player = Player(
            root=self,
            size_=(config.get('Width'), config.get('Height')),
            pos=(self.width/2-self.block_size/2, self.height/2-self.block_size),
            path_anim='rasset/npc/player/original'
        )
        size = get_image_size('rasset/npc/dog/look_down.png')
        self.dog = NPC(
            root=self,
            size_=size,
            position=(4, 4),
            path_anim='rasset/npc/dog',
            current_behavior='walk_towards_player_back',
            npc_id=99,
            script=None
        )
        self.all_entities.add(self.player.color)
        self.all_entities.add(self.player)
        self.all_entities.add(self.dog.color)
        self.all_entities.add(self.dog)

###############################################################################
# ITEM SLOT
###############################################################################

    def display_all_item_slot(self):
        with self.canvas:
            self.slot0 = ItemSlot(0, 1)
            self.slot1 = ItemSlot(1, 2)
            self.slot2 = ItemSlot(2, 3)
            self.slot3 = ItemSlot(3)
            self.slot4 = ItemSlot(4)
            self.slot5 = ItemSlot(5)
            self.slot6 = ItemSlot(6)
            self.slot7 = ItemSlot(7)

###############################################################################

###############################################################################
# BACKGROUND
###############################################################################

    def all_time_color(self):
        self.current_time = 5
        self.sec_on_hours = 3
        self.current_timer = 0

        self.background_time_color = {
            0: '000000DD',
            1: '000000CC',
            2: '000000BB',
            3: '000000AA',
            4: '00000099',
            5: '00000066',
            6: '00000044',
            7: '00000022',
            8: '00000000',
            15: '00000022',
            16: '00000022',
            17: '00000033',
            18: '00000044',
            19: '00000066',
            20: '00000077',
            21: '00000088',
            22: '000000AA',
            23: '000000BB',
            24: '000000CC',
        }

    def display_background(self):
        self.all_time_color()
        self.background_anim = False
        self.background_original_color = self.background_time_color.get(self.current_time, 0)

        with self.canvas:
            self.background_canvas_color = Color(rgba=GetColor(self.background_original_color))
            self.background_canvas = Rectangle(size=self.root.size)
            Color(rgb=GetColor('ffffff'))
        self.canvas.add(self.message_box)
    
    def update_original_background(self):
        if self.in_script is False:
            self.current_timer += self.root.elapseTime
            if self.current_timer >= self.sec_on_hours:
                self.current_timer = 0
                self.current_time = (self.current_time + 1) % 24
                self.background_original_color = self.background_time_color.get(self.current_time, '00000000')
                self.animate_background(None, self.sec_on_hours-1)

    def animate_background(self, color, duration):
        if self.background_anim is False:
            self.background_anim = True
            if color is None: color = self.background_original_color
            anim = Animation(rgba=GetColor(color), d=duration)
            anim.bind(on_complete=self.on_complete_anim)
            anim.start(self.background_canvas_color)

    def on_complete_anim(self, *_):
        self.background_anim = False

###############################################################################

    def order_visible_rectangles_by_position(self, canvas):
        screen_width, screen_height = self.root.size
        children = canvas.children

        visible_rectangles = [
            c for c in children
            if (isinstance(c, Entity) or isinstance(c, EntityAnimation))
            and c.pos[0] >= -c.size[0] and c.pos[0] < screen_width
            and c.pos[1] >= -c.size[1] and c.pos[1] < screen_height]

        visible_rectangles.sort(key=lambda r: (-r.pos[1], not isinstance(r, Entity)))
        for child in visible_rectangles:
            canvas.remove(child.color)
            canvas.remove(child)

            canvas.add(child.color)
            canvas.add(child)

    def update_size(self):
        self.camera_x = 0
        self.camera_y = 0

        self.block_size = dp(self.main_config.get('BlockSize')) * self.game_zoom
        old_player_size = self.player.size
        self.player.set_size()
        self.player.x, self.player.y = (
            self.player.x-(self.player.size[0]-old_player_size[0])/2,
            self.player.y-(self.player.size[1]-old_player_size[1])/2
        )
        self.player.pos = self.player.x, self.player.y

        self.background_map.set_size_and_pos()
        self.main_map.set_size_and_pos()
        self.second_layer_map.set_size_and_pos()
        self.third_layer_map.set_size_and_pos()

        for entity in self.all_entities.children:
            if (isinstance(entity, Entity)):
                if isinstance(entity, Player): continue
                entity.set_position()
            elif isinstance(entity, EntityAnimation): entity.set_position()

    def update(self):
        self.background_map.update()
        self.main_map.update()
        self.second_layer_map.update()
        self.third_layer_map.update()

        self.player.update()
        for rect in self.all_entities.children:
            if (isinstance(rect, Entity)):
                if isinstance(rect, Player): continue
                rect.update()

            elif isinstance(rect, EntityAnimation): rect.update()
        self.order_visible_rectangles_by_position(self.all_entities)
        self.message_box.update()
        self.update_original_background()

###############################################################################
# SCRIPT
###############################################################################

    def variable_for_script(self):
        self.continue_message_display = False

    def handle_script_update(self, owner):
        self.in_script = True
        self.script_index = 0
        self.current_owner = owner
        self.script = self.jds_compiler.run(owner.script)
        self.script_runner.start_script(owner)
        self.current_owner.current_in_script = True

        self.clock_script = Clock.schedule_interval(
            lambda *_: self.run_script(), 1/60)

    def interact_script(self):
        if self.in_script_select:
            if self.continue_message_display:
                self.message_box.continue_display()

    def run_script(self):
        if self.script_index >= len(self.script) or self.script_runner._script_ended:
            self.in_script = False
            self.in_script_select = False
            self.key_script_interact = False
            self.current_owner.current_in_script = False
            self.clock_script.cancel()
            return

        self.script_runner.check_command(self.script[self.script_index][0], *self.script[self.script_index][1:])

###############################################################################