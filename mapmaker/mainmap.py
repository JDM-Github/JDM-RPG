import json
from jdm_kivy import *
from .custom import CustomLabel

class NewCustomImage(JDMWidget):
    
    all_tile_location = ListProperty([])
    all_tile_location2 = ListProperty([])
    all_tile_location3 = ListProperty([])

    def __init__(self, f, s, t, all_tile_location, **kwargs):
        super().__init__(**kwargs)
        main = self.root.main.main 
        self.all_tile_location = all_tile_location.get('BlockCombination')
        self.all_tile_location2 = all_tile_location.get('BlockCombination2')
        self.all_tile_location3 = all_tile_location.get('BlockCombination3')

        with f.canvas:
            self.im0 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location[0]).texture)
            self.im1 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location[1]).texture)
            self.im2 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location[2]).texture)
            self.im3 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location[3]).texture)

        with s.canvas:
            self.im02 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location2[0]).texture)
            self.im12 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location2[1]).texture)
            self.im22 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location2[2]).texture)
            self.im32 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location2[3]).texture)

        with t.canvas:
            self.im03 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location3[0]).texture)
            self.im13 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location3[1]).texture)
            self.im23 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location3[2]).texture)
            self.im33 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location3[3]).texture)

        self.bind(pos=self.change, size=self.change)
        self.bind(all_tile_location=self.change_loc1)
        self.bind(all_tile_location2=self.change_loc2)
        self.bind(all_tile_location3=self.change_loc3)

    def change_loc1(self, *_):
        main = self.root.main.main
        self.im0.texture = main.all_raw_map.get(self.all_tile_location[0]).texture
        self.im0.texture.mag_filter = 'nearest'
        self.im1.texture = main.all_raw_map.get(self.all_tile_location[1]).texture
        self.im1.texture.mag_filter = 'nearest'
        self.im2.texture = main.all_raw_map.get(self.all_tile_location[2]).texture
        self.im2.texture.mag_filter = 'nearest'
        self.im3.texture = main.all_raw_map.get(self.all_tile_location[3]).texture
        self.im3.texture.mag_filter = 'nearest'

    def change_loc2(self, *_):
        main = self.root.main.main
        self.im02.texture = main.all_raw_map.get(self.all_tile_location2[0]).texture
        self.im02.texture.mag_filter = 'nearest'
        self.im12.texture = main.all_raw_map.get(self.all_tile_location2[1]).texture
        self.im12.texture.mag_filter = 'nearest'
        self.im22.texture = main.all_raw_map.get(self.all_tile_location2[2]).texture
        self.im22.texture.mag_filter = 'nearest'
        self.im32.texture = main.all_raw_map.get(self.all_tile_location2[3]).texture
        self.im32.texture.mag_filter = 'nearest'

    def change_loc3(self, *_):
        main = self.root.main.main
        self.im03.texture = main.all_raw_map.get(self.all_tile_location3[0]).texture
        self.im03.texture.mag_filter = 'nearest'
        self.im13.texture = main.all_raw_map.get(self.all_tile_location3[1]).texture
        self.im13.texture.mag_filter = 'nearest'
        self.im23.texture = main.all_raw_map.get(self.all_tile_location3[2]).texture
        self.im23.texture.mag_filter = 'nearest'
        self.im33.texture = main.all_raw_map.get(self.all_tile_location3[3]).texture
        self.im33.texture.mag_filter = 'nearest'

    def change_tile(self, *_):
        self.change_loc1()
        self.change_loc2()
        self.change_loc3()

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
        self.re_position(self.im0, self.im1, self.im2, self.im3)
        self.re_position(self.im02, self.im12, self.im22, self.im32)
        self.re_position(self.im03, self.im13, self.im23, self.im33)

class Tile(JDMWidget):

    def __init__(self, f, s, t, mn, hn, bn, cmap, hitbox, behavior, **kwargs):
        super().__init__(**kwargs)
        self.current_mode = 'Map'
        self.map_config = cmap
        self.hitbox_config = hitbox
        self.behavior_config = behavior
        
        self.first = f
        self.second = s
        self.third = t

        self.mn = mn
        self.hn = hn
        self.bn = bn

        self.display_all()
        self.check_mode(self.root.main.main.modifier.mode)
        self.bind(pos=self.change, size=self.change)
        Window.bind(mouse_pos=self.check_mouse)

    def check_mouse(self, __, pos, *_):
        if self.collide_point(*self.to_widget(*pos)):
            self.main_col.a = 1
        else: self.main_col.a = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.change_tile()
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.change_tile()
        return super().on_touch_move(touch)

    def change_tile(self):
        if self.current_mode == 'Map':
            self.new_map_.all_tile_location2 = self.root.main.main.editor.current.all_tile_location2
            self.new_map_.all_tile_location3 = self.root.main.main.editor.current.all_tile_location3
            self.new_map_.all_tile_location = self.root.main.main.editor.current.all_tile_location
            self.mn = self.root.main.main.editor.current_number

        elif self.current_mode == 'HitBox':
            self.hitbox_.col.rgba = self.root.main.main.editor.current.color
            self.hitbox_.main_label.text = self.root.main.main.editor.curr_label.text
            self.hn = self.root.main.main.editor.current_number
            
        elif self.current_mode == 'Behavior':
            self.behavior_.col.rgba = self.root.main.main.editor.current.color
            self.behavior_.main_label.text = self.root.main.main.editor.curr_label.text
            self.bn = self.root.main.main.editor.current_number

    def display_all(self):
        self.original_hitbox_opacity = 1
        self.original_behavior_opacity = 1

        self.new_map_ = NewCustomImage(self.first, self.second, self.third, all_tile_location=self.map_config)
        self.hitbox_ = CustomLabel(
            name=self.hitbox_config.get('Name'),
            color=self.hitbox_config.get('Alt-Color'),
            opacity=0
        )
        self.behavior_ = CustomLabel(
            name=self.behavior_config.get('Name'),
            color=self.behavior_config.get('Alt-Color'),
            opacity=0,
        )
        self.add_widget(self.new_map_)
        self.add_widget(self.hitbox_)
        self.add_widget(self.behavior_)

    def change(self, *_):
        if not hasattr(self, 'main_col'):
            with self.parent.parent.all_lines.canvas:
                self.main_col = Color(rgb=GetColor('ff0000'), a=0)
                self.main_line = Line(width=dp(2))

        self.new_map_.size = self.size
        self.new_map_.pos = self.pos
        self.hitbox_.pos = self.pos
        self.hitbox_.size = self.size
        self.behavior_.pos = self.pos
        self.behavior_.size = self.size
        self.main_line.rectangle = [*self.pos, *self.size]

    def check_mode(self, text):
        self.current_mode = text
        self.hitbox_.opacity = 0
        self.behavior_.opacity = 0

        if text == 'HitBox': self.hitbox_.opacity = self.original_hitbox_opacity
        elif text == 'Behavior': self.behavior_.opacity = self.original_behavior_opacity            

class MainMap(JDMWidget):

    def __init__(self, name, num, config, **kwargs):
        super().__init__(**kwargs)
        self.all_lines = JDMWidget()
        self.name = name
        self.num = num

        self.root.main.main.current_map = name
        self.root.main.main.current_map_number = num

        self.locbg = f'rasset/Maps/{self.name[3:]}/MBG-{self.num}.gif'
        self.loc1 = f'rasset/Maps/{self.name[3:]}/M1-{self.num}.gif'
        self.loc2 = f'rasset/Maps/{self.name[3:]}/M2-{self.num}.gif'
        self.loc3 = f'rasset/Maps/{self.name[3:]}/M3-{self.num}.gif'

        self.saving_map = False
        self.config = config
        self.curr_cols = self.config.get('Cols')
        self.curr_rows = self.config.get('Rows')
        self.width = self.config.get('Cols') * (dp(16) * 2)
        self.height = self.config.get('Rows') * (dp(16) * 2)
        self.pos = Window.width*0.2+dp(2), Window.height*0.9-dp(32) - self.height

        self.first_layer = JDMWidget(size=self.size, pos=self.pos)
        self.second_layer = JDMWidget(size=self.size, pos=self.pos)
        self.third_layer = JDMWidget(size=self.size, pos=self.pos)

        self.display_map()
        self.add_widget(self.all_lines)

    def remove_map(self):
        for child in self.grid.children: Window.unbind(mouse_pos=child.check_mouse)
        self.parent.remove_widget(self)

    def add_map(self, widget):
        for child in self.grid.children: Window.bind(mouse_pos=child.check_mouse)
        self.root.main.main.current_map = self.name
        self.root.main.main.current_map_number = self.num
        widget.add_widget(self)

    def save_map_gif(self):
        bg_list = list()
        map_list = list()
        hitbox_list = list()
        behavior_list = list()

        self.saving_map = True
        for r, li in enumerate(self.all_map):
            map_list.append(list())
            hitbox_list.append(list())
            behavior_list.append(list())
            for child in li:
                map_list[r].append(int(child.mn))
                hitbox_list[r].append(int(child.hn))
                behavior_list[r].append(int(child.bn))

        main = self.root.main.main
        main.save_map_gif()
        
        for child in main.editor.map_background.children:
            bg_list.append(int(child.numtile))

        config = json_obj('jsons/all_maps.json')
        config.get(self.name).get(self.num)['Map'] = map_list
        config.get(self.name).get(self.num)['HitBox'] = hitbox_list
        config.get(self.name).get(self.num)['Behavior'] = behavior_list
        config.get(self.name).get(self.num)['Background'] = bg_list
        config.get(self.name).get(self.num)['BGLocation'] = self.locbg
        config.get(self.name).get(self.num)['Location'] = self.loc1
        config.get(self.name).get(self.num)['Location2'] = self.loc2
        config.get(self.name).get(self.num)['Location3'] = self.loc3
        pprint_save_json(config, 'jsons/all_maps.json')
        save_json(main.event_config, 'jsons/events_map.json')

    def display_map(self):
        main_block_config = json_obj('jsons/block_config.json')
        map_config = main_block_config.get('Map')
        hitbox_config = main_block_config.get('HitBox')
        behavior_config = main_block_config.get('Behavior')

        self.grid = JDMGridLayout(
            cols=self.config.get('Cols'),
            rows=self.config.get('Rows'),
            size=self.size,
            pos=self.pos)

        with self.canvas:
            Color(rgb=GetColor('ffffff'))
            Rectangle(size=(self.width+dp(2), self.height+dp(2)), pos=(self.x-dp(1), self.y-dp(1)))

        self.add_widget(self.first_layer)
        self.add_widget(self.second_layer)
        self.add_widget(self.third_layer)

        self.all_map : list[list[Tile]] = list()
        for r in range(self.config.get('Rows')):
            self.all_map.append(list())
            for c in range(self.config.get('Cols')):

                self.all_map[r].append(Tile(
                    self.first_layer,
                    self.second_layer,
                    self.third_layer,
                    str(self.config.get('Map')[r][c]),
                    str(self.config.get('HitBox')[r][c]),
                    str(self.config.get('Behavior')[r][c]),
                    map_config.get(str(self.config.get('Map')[r][c])),
                    hitbox_config.get(str(self.config.get('HitBox')[r][c])),
                    behavior_config.get(str(self.config.get('Behavior')[r][c]))))
                self.grid.add_widget(self.all_map[r][-1])

        self.add_widget(self.grid)

