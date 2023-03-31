import json
from jdm_kivy import *
from .custom import CustomWidget, NewCustomImage

class Tile(NewCustomImage):

    def __init__(self, numtile, **kwargs):
        super().__init__(numtile, **kwargs)
        self.numtile = numtile
        self.bind(pos=self.change, size=self.change)
        Window.bind(mouse_pos=self.check_mouse)

    def check_mouse(self, __, pos, *_):
        if self.collide_point(*self.to_widget(*pos)):
            self.main_col.a = 1
        else:
            self.main_col.a = 0

    def change(self, *_):
        if not hasattr(self, 'main_col'):
            with self.parent.parent.all_lines.canvas:
                self.main_col = Color(rgb=GetColor('ff0000'), a=0)
                self.main_line = Line(width=dp(2))
        self.main_line.rectangle = [*self.pos, *self.size]
        super().change(*_)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.parent.parent.current_mode == 'Map':
                self.numtile = self.parent.parent.current_number
                self.all_tile_location = self.parent.parent.current.all_tile_location
                self.all_tile_location2 = self.parent.parent.current.all_tile_location2
                self.all_tile_location3 = self.parent.parent.current.all_tile_location3
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if self.parent.parent.current_mode == 'Map':
                self.numtile = self.parent.parent.current_number
                self.all_tile_location = self.parent.parent.current.all_tile_location
                self.all_tile_location2 = self.parent.parent.current.all_tile_location2
                self.all_tile_location3 = self.parent.parent.current.all_tile_location3
        return super().on_touch_move(touch)

class MapEditor(CustomWidget):

    current_mode = StringProperty('Map')
    map_current = StringProperty('0')
    hitbox_current = StringProperty('0')
    behavior_current = StringProperty('0')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = '333333'
        self.size = (Window.width*0.5-dp(20), dp(64)+dp(20))
        self.pos = (Window.width*0.2+dp(10), dp(10))
        self.display_canvas()
        self.display_tools()

    def display_tools(self):
        with open('jsons/block_config.json') as f:
            self.main_block = json.load(f)
            self.map_block = self.main_block.get('Map')
        self.display_background()
        self.display_currentblock()

    def display_background(self):
        self.all_lines = JDMWidget()
        self.map_background = JDMGridLayout(
            cols=2, rows=2,
            size=(self.height-dp(20), self.height-dp(20)),
            pos=(self.x+dp(10), self.y+dp(10)))

        with self.canvas:
            Color(rgb=GetColor('ffffff'))
            Line(rectangle=[*self.map_background.pos, *self.map_background.size])

        self.add_widget(self.map_background)
        self.add_widget(self.all_lines)

    def display_currentblock(self):
        self.current_number = '0'
        self.current = JDMImage(
            allow_stretch=True,
            pos=(self.x+dp(20)+(self.height-dp(20)), self.y+dp(10)+((self.height-dp(20))/4)),
            size=((self.height-dp(20))/2, (self.height-dp(20))/2),
        )
        self.current.texture = JDMImage(source='rasset/tileset/forest/1.png').texture
        self.current.all_tile_location = self.map_block.get(self.map_current).get('BlockCombination')
        self.current.all_tile_location2 = self.map_block.get(self.map_current).get('BlockCombination2')
        self.current.all_tile_location3 = self.map_block.get(self.map_current).get('BlockCombination3')
        self.current.anim_delay = 1 / get_gif_frames(self.current.source)

        self.current.bind(source=lambda *_: setattr(self.current, 'anim_delay', 1 / get_gif_frames(self.current.source)))
        self.curr_label = JDMLabel(
            size=self.current.size, pos=self.current.pos, text='')
        self.current.add_widget(self.curr_label)
        with self.canvas:
            Color(rgb=GetColor('ffffff'))
            Line(rectangle=[*self.current.pos, *self.current.size])

        self.add_widget(self.current)

        self.bind(
            current_mode=self.change_mode,
            map_current=self.change_mode,
            hitbox_current=self.change_mode,
            behavior_current=self.change_mode,
        )

    def change_mode(self, *_):
        number = self.map_current if self.current_mode == 'Map' else (
            self.hitbox_current if self.current_mode == 'HitBox' else (
                self.behavior_current if self.current_mode == 'Behavior' else '0'
            ))
        self.current_number = number
        if self.current_mode == 'Map':
            self.curr_label.text = ''
            self.current.color = GetColor('ffffff')
            self.current.all_tile_location = self.main_block.get(self.current_mode).get(number).get('BlockCombination')
            self.current.all_tile_location2 = self.main_block.get(self.current_mode).get(number).get('BlockCombination2')
            self.current.all_tile_location3 = self.main_block.get(self.current_mode).get(number).get('BlockCombination3')
            return

        self.curr_label.text = self.main_block.get(self.current_mode).get(number).get('Name') \
            if self.main_block.get(self.current_mode).get(number).get('Name') else ''
        self.current.color=GetColor('ffffff') if self.main_block.get(self.current_mode).get(number).get('Source') \
            else GetColor(self.main_block.get(self.current_mode).get(number).get('Alt-Color'))

    def change_background(self, config):
        self.config = config
        self.map_background.clear_widgets()
        for child in self.all_lines.children:
            Window.unbind(mouse_pos=child.check_mouse)

        for tile in self.config.get('Background'):
            self.map_background.add_widget(Tile(tile))
