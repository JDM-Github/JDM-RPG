import json
import os
from plyer import filechooser
from jdm_kivy import *
from .custom import CustomWidget, CustomLabel, CustomButton

class NewCustomImage(JDMWidget):

    all_tile_location = ListProperty([])
    def __init__(self, tilenum, config, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.tilenum = tilenum
        self.hover = False

        self.all_tile_location = config.get('BlockCombination')
        self.all_tile_location2 = config.get('BlockCombination2')
        self.all_tile_location3 = config.get('BlockCombination3')

        with self.canvas:
            self.im0 = Rectangle()
            self.im1 = Rectangle()
            self.im2 = Rectangle()
            self.im3 = Rectangle()
            self.im02 = Rectangle()
            self.im12 = Rectangle()
            self.im22 = Rectangle()
            self.im32 = Rectangle()
            self.im03 = Rectangle()
            self.im13 = Rectangle()
            self.im23 = Rectangle()
            self.im33 = Rectangle()

        self.bind(pos=self.change, size=self.change)
        self.bind(all_tile_location=self.change_tile)
        Window.bind(mouse_pos=self.motion_check)
        Clock.schedule_once(self.change_tile, 0)

    def motion_check(self, __, pos, *_):
        if self.parent.parent.parent:
            if self.collide_point(*self.to_widget(*pos)):
                Window.set_system_cursor('hand')
                self.hover = True
            elif self.hover:
                Window.set_system_cursor('arrow')
                self.hover = False
        else: Window.unbind(mouse_pos=self.motion_check)

    def on_touch_down(self, touch):
        mode = self.root.main.main.modifier.mode
        if self.collide_point(*touch.pos):
            if mode == 'Map':
                self.root.main.main.editor.map_current = self.tilenum
                texture = self.export_as_image().texture
                texture.flip_vertical()
                texture.mag_filter = 'nearest'

                self.root.main.main.editor.current.texture = texture
                self.root.main.main.editor.current.texture.mag_filter = 'nearest'

        return super().on_touch_down(touch)

    def change_tile(self, *_):
        main = self.root.main.main 
        self.im0.texture = main.all_raw_map.get(self.all_tile_location[0]).texture
        self.im0.texture.mag_filter = 'nearest'
        self.im1.texture = main.all_raw_map.get(self.all_tile_location[1]).texture
        self.im1.texture.mag_filter = 'nearest'
        self.im2.texture = main.all_raw_map.get(self.all_tile_location[2]).texture
        self.im2.texture.mag_filter = 'nearest'
        self.im3.texture = main.all_raw_map.get(self.all_tile_location[3]).texture
        self.im3.texture.mag_filter = 'nearest'

        self.im02.texture = main.all_raw_map.get(self.all_tile_location2[0]).texture
        self.im02.texture.mag_filter = 'nearest'
        self.im12.texture = main.all_raw_map.get(self.all_tile_location2[1]).texture
        self.im12.texture.mag_filter = 'nearest'
        self.im22.texture = main.all_raw_map.get(self.all_tile_location2[2]).texture
        self.im22.texture.mag_filter = 'nearest'
        self.im32.texture = main.all_raw_map.get(self.all_tile_location2[3]).texture
        self.im32.texture.mag_filter = 'nearest'

        self.im03.texture = main.all_raw_map.get(self.all_tile_location3[0]).texture
        self.im03.texture.mag_filter = 'nearest'
        self.im13.texture = main.all_raw_map.get(self.all_tile_location3[1]).texture
        self.im13.texture.mag_filter = 'nearest'
        self.im23.texture = main.all_raw_map.get(self.all_tile_location3[2]).texture
        self.im23.texture.mag_filter = 'nearest'
        self.im33.texture = main.all_raw_map.get(self.all_tile_location3[3]).texture
        self.im33.texture.mag_filter = 'nearest'
    
    def re_position(self, m0, m1, m2, m3):
        m0.size = (self.width/2, self.height/2)
        m1.size = (self.width/2, self.height/2)
        m2.size = (self.width/2, self.height/2)
        m3.size = (self.width/2, self.height/2)

        m0.pos = (self.x, self.y+m0.size[1])
        m1.pos = (self.x+m1.size[0], self.y+m1.size[1])
        m2.pos = (self.x, self.y)
        m3.pos = (self.x+m3.size[0], self.y)

    def change(self, *_):
        self.height = self.width
        self.re_position(self.im0, self.im1, self.im2, self.im3)
        self.re_position(self.im02, self.im12, self.im22, self.im32)
        self.re_position(self.im03, self.im13, self.im23, self.im33)

class Tile(CustomLabel):

    def __init__(self, tilenum, config, **kwargs):
        self.config = config
        name = self.config.get('Name') if self.config.get('Name') else ''

        super().__init__(name, **kwargs)
        self.tilenum = tilenum
        self.size_hint_y = None
        self.col.rgb = GetColor('ffffff')
        self.hover = False

        self.li.width = dp(1.4)
        if config.get('Source') and os.path.exists(config.get('Source')):
            self.rect.source = config.get('Source')
        else: self.col.rgba = GetColor(config.get('Alt-Color'))
        Window.bind(mouse_pos=self.motion_check)

    def motion_check(self, __, pos, *_):
        if self.parent.parent.parent:
            if self.collide_point(*self.to_widget(*pos)):
                Window.set_system_cursor('hand')
                self.hover = True
            elif self.hover:
                Window.set_system_cursor('arrow')
                self.hover = False
        else: Window.unbind(mouse_pos=self.motion_check)

    def on_touch_down(self, touch):
        mode = self.root.main.main.modifier.mode
        if self.collide_point(*touch.pos):
            if mode == 'HitBox':
                self.root.main.main.editor.hitbox_current = self.tilenum
            elif mode == 'Behavior':
                self.root.main.main.editor.behavior_current = self.tilenum
        return super().on_touch_down(touch)

    def change(self, *_):
        self.height = self.width
        super().change(*_)

class NPCObject(JDMImage):

    def __init__(self, position, number, sprite, script, behavior, npc_id, **kwargs):
        super().__init__(**kwargs)
        self.npc_id = npc_id
        self.behavior = behavior
        self.number = number
        self.script = script

        self.block = dp(16)*2
        self.moving = False

        self.position = position
        
        self.size = (self.block, self.block)
        self.mx, self.my = self.root.main.main.main_map.children[0].pos
        self.pos = (self.mx + (position[0]*self.block), self.my + (position[1]*self.block))
        self.manage_sprite(sprite)

    def manage_sprite(self, sprite):
        self.allow_stretch = True
        self.sprite = sprite
        self.source = f'rasset/npc/{sprite}/look_down.png'
        self.texture.mag_filter = 'nearest'
        size = get_image_size(os.path.abspath(f'rasset/npc/{sprite}/look_down.png'))
        self.size = (dp(size[0])*2, dp(size[1])*2)
        self.x -= ((dp(size[0]*2) - self.block)/2)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.moving = True
            self.grab_x = touch.x - self.x
            self.grab_y = touch.y - self.y
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.moving:
            x, y = self.root.main.main.main_map.children[0].pos
            width, height = self.root.main.main.main_map.children[0].size
            if x <= touch.x <= x+width and y <= touch.y <= y+height:
                self.x = touch.x - self.grab_x
                self.y = touch.y - self.grab_y
            else:
                self.moving = False
                self.calculate_position()
                self.save_position()
                self.parent.parent.objecteditor.open_npc_editor(self)
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.moving:
            self.moving = False
            self.calculate_position()
            self.save_position()
            self.parent.parent.objecteditor.open_npc_editor(self)
        return super().on_touch_up(touch)

    def calculate_position(self):
        cols = self.root.main.main.main_map.children[0].curr_cols
        rows = self.root.main.main.main_map.children[0].curr_rows
        x, y = self.root.main.main.main_map.children[0].pos
        cx = round((self.x - x) / self.block)
        cy = round((self.y - y) / self.block)
        if cx < 0: cx = 0
        elif cx >= cols: cx = cols-1

        if cy < 0: cy = 0
        elif cy >= rows: cy = rows-1
        self.pos = (x + (cx*self.block), y + (cy*self.block))
        self.position = (cx, cy)
        
        objecte = self.parent.parent.objecteditor
        if objecte.opened:
            objecte.personx.text_value.text = str(cx)
            objecte.persony.text_value.text = str(cy)

    def update_position(self):
        objecte = self.parent.parent.objecteditor
        if objecte.opened:
            x = int(objecte.personx.text_value.text)
            y = int(objecte.persony.text_value.text)
        self.position = (x, y)
        self.pos = (self.mx + (x*self.block), self.my + (y*self.block))
        self.save_position()

    def update_sprite(self):
        objecte = self.parent.parent.objecteditor
        self.manage_sprite(objecte.all_sprites[int(objecte.personsprite.text_value.text)])
        self.save_position()

    def save_position(self):
        main = self.root.main.main
        event = main.event_config.get(main.current_map).get(main.current_map_number).get('NPC').get(self.number)
        event['position'] = self.position
        event['sprite'] = self.sprite
        event['script'] = self.script
        event['behavior'] = self.behavior

class CusTextInput(JDMTextInput):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.func_bin = lambda : None
        self.input_filter = 'int'
        self.write_tab = False
        self.multiline = False

        self.cursor_blink = False
        self.cursor_color = 'ffffff'
        self.background_color = '222222'
        self.foreground_color = 'ffffff'
        self.font_size = dp(14)
    
    def on_text_validate(self):
        self.func_bin()
        return super().on_text_validate()


class ChangeableWidget(CustomWidget):
    
    def __init__(self, npc, text, value, min_, max_, **kwargs):
        super().__init__(**kwargs)
        self.curr_npc = npc
        self.minimum = min_
        self.maximum = max_
        self.color = '444444'
        self.size_hint_y = None
        self.height = dp(40)
        self.text = text
        self.value = value
        self.display_canvas()
        self.display_label()
    
    def display_label(self):
        self.main_label = JDMLabel(text=self.text, halign='left')

        self.min_wid = CustomButton('<', size = (dp(30), dp(30)))        
        self.text_value = CusTextInput(text=str(self.value), size = (dp(60), dp(30)))
        self.text_value.func_bin = self.after_effects

        self.add_wid = CustomButton('>', size = (dp(30), dp(30)))

        self.min_wid.func_click = self.add_value
        self.add_wid.func_click = self.min_value

        self.add_widget(self.main_label)
        self.add_widget(self.min_wid)
        self.add_widget(self.text_value)
        self.add_widget(self.add_wid)

    def add_value(self):
        self.text_value.text = str(int(self.text_value.text)-1)
        self.after_effects()

    def min_value(self):
        self.text_value.text = str(int(self.text_value.text)+1)
        self.after_effects()

    def after_effects(self):
        self.text_value.text = str(max(self.minimum, int(self.text_value.text)))
        if self.maximum: self.text_value.text = str(min(self.maximum, int(self.text_value.text)))
        self.curr_npc.update_position()
        self.curr_npc.update_sprite()

    def change(self, *_):
        self.main_label.size = self.size
        self.main_label.pos = self.pos
        self.main_label.x += dp(10)
        
        self.add_wid.pos = (self.x+self.width)-dp(40), self.y+dp(5)
        self.text_value.pos = self.add_wid.x-dp(70), self.y+dp(5)
        self.min_wid.pos = self.text_value.x-dp(40), self.y+dp(5)
        return super().change(*_)

class ChooseableWidget(CustomWidget):
    
    def __init__(self, text, text2, **kwargs):
        super().__init__(**kwargs)
        self.color = '333333'
        self.size_hint_y = None
        self.height = dp(70)
        self.text = text
        self.text2 = text2
        self.display_canvas()
        self.display_label()

    def display_label(self):
        self.main_label = JDMLabel(font_size=dp(12), text=(self.text)[:28])
        self.main_func = CustomButton(self.text2)
        self.add_widget(self.main_label)
        self.add_widget(self.main_func)

    def change(self, *_):
        self.main_label.size = self.width-dp(20), dp(30)
        self.main_label.text_size = self.width-dp(20), dp(30)
        self.main_label.pos = self.x+dp(10), self.y+dp(35)
        self.main_func.size = self.width-dp(20), dp(30)
        self.main_func.pos = self.x, self.y+dp(5)
        self.main_func.x += dp(10)
        return super().change(*_)

class ObjectEditor(JDMWidget):
    
    def __init__(self, size, pos, all_sprites, **kwargs):
        super().__init__(**kwargs)
        self.all_sprites : list = all_sprites
        self.size = size
        self.pos = pos
        self.opened = False

    def open_npc_editor(self, npc: NPCObject):
        if self.opened: return
        self.clear_widgets()

        self.current_npc = npc
        widget = JDMWidget()
        scroll = JDMScrollView(size=(self.width-dp(10), self.height-dp(50)), pos=(self.x+dp(5), self.y+dp(10)))
        self.npc_grid = JDMGridLayout(cols=1, padding=dp(10), spacing=dp(10), size_hint_y=None)
        self.npc_grid.bind(minimum_height=self.npc_grid.setter('height'))

        with self.canvas:
            Color(rgb=GetColor('ffffff'))
            Line(rectangle=[*scroll.pos, *scroll.size])

        widget.add_widget(CustomLabel("Person Event", color='666666', size=(self.width-dp(10), dp(30)), pos=(self.x+dp(5), self.top-dp(35))))
        self.npc_grid.add_widget(CustomButton("Delete Event", size_hint_y=None, height=dp(30)))
        self.personid =       ChangeableWidget(npc, "Person ID", npc.npc_id, 0, None)
        self.personsprite =   ChangeableWidget(npc, "Sprite ID", self.all_sprites.index(npc.sprite), 0, len(self.all_sprites)-1)

        cols = self.root.main.main.main_map.children[0].curr_cols
        rows = self.root.main.main.main_map.children[0].curr_rows
        self.personx =        ChangeableWidget(npc, "Position X", npc.position[0], 0, cols-1)
        self.persony =        ChangeableWidget(npc, "Position Y", npc.position[1], 0, rows-1)
        self.personbehavior = ChooseableWidget(npc.behavior, "Choose Behavior")
        self.personscript =   ChooseableWidget(npc.script, "Choose Script")
        
        self.personbehavior.main_func.func_bind = self.display_behaviors
        self.personscript.main_func.func_bind = self.change_script

        self.npc_grid.add_widget(self.personid)
        self.npc_grid.add_widget(self.personsprite)
        self.npc_grid.add_widget(self.personx)
        self.npc_grid.add_widget(self.persony)
        self.npc_grid.add_widget(self.personbehavior)
        self.npc_grid.add_widget(self.personscript)

        self.npc_grid.add_widget(JDMLabel(text="", size_hint_y=None, height=dp(30)))
        self.npc_grid.add_widget(CustomButton("Add Person Event", size_hint_y=None, height=dp(30)))
        self.npc_grid.add_widget(CustomButton("Add Sign Event", size_hint_y=None, height=dp(30)))
        self.npc_grid.add_widget(CustomButton("Add Warp Event", size_hint_y=None, height=dp(30)))
        self.npc_grid.add_widget(CustomButton("Add Script Event", size_hint_y=None, height=dp(30)))

        scroll.add_widget(self.npc_grid)
        self.add_widget(scroll)
        self.add_widget(widget)
        self.opened = True

    def change_script(self):
        orig_dir = os.getcwd()
        result = filechooser.open_file(multiple=False, filters=['*.jds'])[0]
        self.current_npc.script = result
        self.personscript.main_label.text = result[:28]
        self.current_npc.save_position()
        os.chdir(orig_dir)

    def display_behaviors(self):
        self.npc_grid.disabled = True
        if not hasattr(self, 'behave_grid'):
            self.behave_grid = self.get_grid((Window.width*0.3, Window.height*0.25), (Window.width*0.4, Window.height*0.5))
            self.behave_grid.cols = 1
            all_behavior = ['none', 'look_around', 'walk_around', 'look_down', 'look_up', 'look_left', 'look_right', 'hidden']

            for behave in all_behavior:
                self.behave_grid.add_widget(but:=CustomButton(behave, height=dp(30), size_hint_y=None))
                but.func_bind = lambda text=behave : self.change_behavior(text)
        self.remove_widget(self.behave_grid.parent)
        self.add_widget(self.behave_grid.parent)

    def change_behavior(self, text):
        self.personbehavior.main_label.text = text
        self.current_npc.behavior = text
        self.npc_grid.disabled = False
        self.current_npc.save_position()
        self.remove_widget(self.behave_grid.parent)

    def get_grid(self, pos, size):
        scroll = JDMScrollView(pos=pos, size=size)
        grid = JDMGridLayout(padding=dp(5), spacing=dp(4), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        with scroll.canvas.before:
            Color(rgb=GetColor('111111'))
            Rectangle(pos=scroll.pos, size=scroll.size)
            Color(rgb=GetColor('ffffff'))
            Line(rectangle=[*scroll.pos, *scroll.size])
           
        
        scroll.add_widget(grid)
        self.add_widget(scroll)
        
        return grid

class ModifierWidget(CustomWidget):

    mode = StringProperty('Map')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = '111111'
        self.size = (Window.width*0.3, Window.height*0.9-dp(40))
        self.pos = (Window.width*0.7, dp(10))
        self.display_canvas()
        with open('jsons/block_config.json') as f:
            self.tiles_config = json.load(f)

        self.all_tilesb = JDMScrollView()
        self.all_behave = JDMScrollView()
        self.all_hitbox = JDMScrollView()
        self.npc_widget = JDMWidget()
        
        self.all_sprites_avail = os.listdir('rasset/npc')
        self.all_sprites_avail.remove('player')
        new_list = os.listdir('rasset/npc/player')
        self.all_sprites_avail += ['player/'+l for l in new_list]
        self.objecteditor = ObjectEditor(self.size, self.pos, self.all_sprites_avail)
        self.change_mode()
        self.bind(mode=self.change_mode)

    def change_mode(self, *_):
        self.clear_widgets()
        if   self.mode == 'Map': self.display_tiles('Map', self.all_tilesb)
        elif self.mode == 'Behavior': self.display_tiles('Behavior', self.all_behave)
        elif self.mode == 'HitBox': self.display_tiles('HitBox', self.all_hitbox)
        elif self.mode == 'Event': self.display_events()

    def display_events(self):
        main = self.root.main.main
        self.npc_widget.clear_widgets()
        event = main.event_config.get(main.current_map).get(main.current_map_number)
        for npc in event.get('NPC'):
            self.npc_widget.add_widget(NPCObject(
                event.get('NPC').get(npc).get('position'), npc,
                event.get('NPC').get(npc).get('sprite'),
                event.get('NPC').get(npc).get('script'),
                event.get('NPC').get(npc).get('behavior'),
                event.get('NPC').get(npc).get('id'),
            ))
        self.add_widget(self.npc_widget)
        self.add_widget(self.objecteditor)

    def display_tiles(self, text, scroll):
        if scroll.children:
            self.add_widget(scroll)
            return

        all_tiles = JDMGridLayout(cols=8, padding=dp(5), spacing=dp(4), size_hint_y=None)
        all_tiles.bind(minimum_height=all_tiles.setter('height'))
        scroll = JDMScrollView(pos=(self.x+dp(9.5), self.y+dp(9.5)), size=(self.width-dp(19), self.height-dp(19)))

        with self.canvas:
            Color(rgb=GetColor('ffffff'))
            Line(rectangle=[*scroll.pos, *scroll.size])

        for tile in self.tiles_config.get(text):
            if text == 'Map':
                all_tiles.add_widget(NewCustomImage(tile, self.tiles_config.get(text).get(tile)))
            else: all_tiles.add_widget(Tile(tile, self.tiles_config.get(text).get(tile)))

        scroll.add_widget(all_tiles)
        self.add_widget(scroll)
