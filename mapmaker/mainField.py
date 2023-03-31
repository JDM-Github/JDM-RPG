import json
from jdm_kivy import *
from .custom import CustomWidget
from .mapnav import MapNavWidget
from .mapevent import MapEvent
from .mapmodifier import ModifierWidget
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from .editor import MapEditor
from PIL import Image

class MapScreen(JDMScreen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.control = False

    def keyboard_down(self, window, scancode=None, key=None, keyAscii=None, *args):
        if key == 224:
            self.control = True

        if self.control:
            if keyAscii == 's':
                self.main.main_map.children[0].save_map_gif()

        return super().keyboard_down(window, scancode, key, keyAscii, *args)

    def keyboard_up(self, window, scancode=None, key=None, keyAscii=None, *args):
        if key == 244: self.control = False
        if key == 19:
            self.main.preview = not self.main.preview
            if self.main.preview:
                self.main.open_preview()
        return super().keyboard_up(window, scancode, key, keyAscii, *args)

class ToolWidget(CustomWidget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = '888888'
        self.size = (Window.width, Window.height*0.1)
        self.pos = (0, Window.height*0.9-dp(10))
        self.display_canvas()

class MapMaker(JDMWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_frame = 30
        self.max_anim_loop = 1

        self._frame_number = 1
        self._loop_number = 0
        self.saving = False
        self.preview = False
        
        self.background_frame = list()
        self.first_layer_frame = list()
        self.second_layer_frame = list()
        self.third_layer_frame = list()

        self.display_design()
        self.display_raw_map()

    def display_raw_map(self):
        self.index = 0
        self.all_raw_map : dict[int, JDMImage] = dict()
        for index, con in enumerate(self.block_config.get('Raw')):
            conf = self.block_config.get('Raw').get(con)
            self.all_raw_map[index] = JDMImage(
                allow_stretch=True,
                anim_delay=-1, anim_loop=0,
                source=conf.get('Source'),
                color=conf.get('Alt-Color'))

    def save_map_gif(self):
        if self.main_map.children:
            self.background_frame.clear()
            self.first_layer_frame.clear()
            self.second_layer_frame.clear()
            self.third_layer_frame.clear()
            self._frame_number = 1
            self._loop_number = 0
            self.saving = True
            self.locbg = self.main_map.children[0].locbg
            self.loc1 = self.main_map.children[0].loc1
            self.loc2 = self.main_map.children[0].loc2
            self.loc3 = self.main_map.children[0].loc3
            
            if hasattr(self, 'clock1'): self.clock1.cancel()
            if hasattr(self, 'clock2'): self.clock2.cancel()

            for index in self.all_raw_map:
                self.all_raw_map.get(index)._coreimage._anim_index = 0
                self.all_raw_map.get(index).texture = self.all_raw_map.get(index)._coreimage.image.textures[0]
            self.update_all_texture()

            self.add_frames()
            self.clock_next_frame()

    def open_preview(self):
        self._frame_number = 1
        self._loop_number = 0
        self.clock_next_frame()

    def clock_next_frame(self, *_):
        changed = False
        for index in self.all_raw_map:
            if ((self._frame_number % self.max_frame) % (self.max_frame // len(self.all_raw_map.get(index)._coreimage.image.textures))) == 0:
                self.all_raw_map.get(index)._coreimage._anim_index = (
                    self.all_raw_map.get(index)._coreimage._anim_index + 1) % (len(self.all_raw_map.get(index)._coreimage.image.textures))
                self.all_raw_map.get(index).texture = self.all_raw_map.get(index)._coreimage.image.textures[
                    self.all_raw_map.get(index)._coreimage._anim_index]
                changed = True
        self.update_all_texture()

        self._frame_number += 1
        if self._frame_number >= self.max_frame:
            self._frame_number = 1
            self.clock1 = Clock.schedule_once(self.revert_texture_to_first, 0.02)
        else:
            if self.saving and changed:  self.add_frames()
            self.clock2 = Clock.schedule_once(self.clock_next_frame, 0.02)

    def add_frames(self):
        widget = self.main_map.children[0]
        self.background_frame.append(self.get_image_frame(self.editor.map_background.export_as_image()))
        self.first_layer_frame.append(self.get_image_frame(widget.first_layer.export_as_image()))
        self.second_layer_frame.append(self.get_image_frame(widget.second_layer.export_as_image()))
        self.third_layer_frame.append(self.get_image_frame(widget.third_layer.export_as_image()))

    def get_image_frame(self, coreimage):
        coreimage.texture.mag_filter = 'nearest'
        return Image.frombytes(mode='RGBA', size=coreimage.texture.size, data=bytes(coreimage.texture.pixels))

    def save_gif(self, filename, frames):

        lenght = len(frames)
        filename = filename
        duration = 1 / lenght
        images = frames

        images[1].save(
            filename,
            format='GIF',
            save_all=True,
            append_images=images[2:],
            duration=int(duration*1000),
            loop=0,
            disposal=2)

    def revert_texture_to_first(self, *_):
        for index in self.all_raw_map:
            self.all_raw_map.get(index).texture = self.all_raw_map.get(index)._coreimage.image.textures[0]
        self.update_all_texture()

        if self.preview is False or self.saving: self._loop_number += 1
        if self._loop_number >= self.max_anim_loop:
            self._loop_number = self.max_anim_loop
            if self.saving:
                self.save_gif(self.locbg, self.background_frame)
                self.save_gif(self.loc1, self.first_layer_frame)
                self.save_gif(self.loc2, self.second_layer_frame)
                self.save_gif(self.loc3, self.third_layer_frame)
                self.saving = False

                if self.preview: self.open_preview()
        else:
            if self.saving: self.add_frames()
            self.clock1 = Clock.schedule_once(self.clock_next_frame, 0.02)

    def update_all_texture(self, *_):
        if self.main_map.children:
            main = self.main_map.children[0].all_map
            for widget_list in main:
                for widget in widget_list:
                    main_widget = widget.new_map_
                    main_widget.change_tile()

            for child in self.editor.map_background.children:
                child.change_tile()

    def display_design(self):
        with open('jsons/all_maps.json') as f:
            self.map_config = json.load(f)
        with open('jsons/block_config.json') as f:
            self.block_config = json.load(f)
        self.event_config = json_obj('jsons/events_map.json')
        
        self.current_map = 'Map01'
        self.current_map_number = '00'
        
        
        self.all_widget()

    def all_widget(self):
        self.tool_widget = ToolWidget()
        self.map_event = MapEvent()
        self.map_nav = MapNavWidget()
        self.modifier = ModifierWidget()
        self.editor = MapEditor()
        self.main_map = JDMWidget()
        
        self.add_widget(self.main_map)
        self.add_widget(self.map_nav)
        self.add_widget(self.modifier)

        self.add_widget(self.tool_widget)
        self.add_widget(self.editor)
        self.add_widget(self.map_event)

        Clock.schedule_once(lambda *_:
            self.map_nav.add_map(self.current_map, self.current_map_number,
                                 self.map_config.get(self.current_map).get(self.current_map_number)), 0)
