from jdm_kivy import *

class CustomWidget(JDMWidget):

    def display_canvas(self):
        with self.canvas:
            Color(rgb=GetColor('ffffff'))
            self.li = Line(rectangle=[*self.pos, *self.size])
            self.col = Color(rgb=GetColor(self.color))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.change, size=self.change)

    def change(self, *_):
        self.li.rectangle=[*self.pos, *self.size]
        self.rect.size = self.size
        self.rect.pos = self.pos

class CustomButton(CustomWidget):
    
    def __init__(self, name, color='555555', func_bind=lambda : None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.clicked = False
        self.hover = False
        self.color = color
        self.func_bind = func_bind
        self.func_click = lambda : None
        self.display_canvas()
        self.main_label = JDMLabel(text=name, size=self.size, pos=self.pos)
        self.add_widget(self.main_label)
        self.bind(size=self.change, pos=self.change)
        Window.bind(mouse_pos=self.motion_check)

    def motion_check(self, __, pos, *_):
        if self.collide_point(*self.to_widget(*pos)):
            self.col.rgb = GetColor('333333')
            Window.set_system_cursor('hand')
            self.hover = True
        else:
            self.col.rgb = GetColor(self.color)
            if self.hover:
                Window.set_system_cursor('arrow')
                self.hover = False

    def change(self, *_):
        self.main_label.size = self.size
        self.main_label.pos = self.pos
        super().change(*_)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.clicked = True
            self.col.rgb = GetColor('222222')
            self.func_click()
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.clicked:
            self.clicked = False
            self.col.rgb = GetColor('333333')
            self.func_bind()
        return super().on_touch_up(touch)

class CustomLabel(CustomWidget):
    
    def __init__(self, name, color='555555', **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.color = color
        self.display_canvas()
        self.col.rgba = GetColor(self.color)
        self.main_label = JDMLabel(text=name, size=self.size, pos=self.pos)
        self.add_widget(self.main_label)
        self.bind(size=self.change, pos=self.change)

    def change(self, *_):
        self.main_label.size = self.size
        self.main_label.pos = self.pos
        super().change(*_)

class NewCustomImage(JDMWidget):

    all_tile_location = ListProperty([])
    all_tile_location2 = ListProperty([])
    all_tile_location3 = ListProperty([])

    def __init__(self, numtile, **kwargs):
        super().__init__(**kwargs)
        main = self.root.main.main
        all_tile_location = main.block_config.get('Map').get(str(numtile))
        self.all_tile_location = all_tile_location.get('BlockCombination')
        self.all_tile_location2 = all_tile_location.get('BlockCombination2')
        self.all_tile_location3 = all_tile_location.get('BlockCombination3')

        with self.canvas:
            self.im0 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location[0]).texture)
            self.im1 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location[1]).texture)
            self.im2 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location[2]).texture)
            self.im3 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location[3]).texture)
            self.im02 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location2[0]).texture)
            self.im12 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location2[1]).texture)
            self.im22 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location2[2]).texture)
            self.im32 = Rectangle(texture=main.all_raw_map.get(self.all_tile_location2[3]).texture)
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