import json
from jdm_kivy import *
from .custom import CustomWidget, CustomButton, CustomLabel
from .mainmap import MainMap

class MapNavWidget(CustomWidget):

    class MapList(JDMWidget):

        def __init__(self, name, config, **kwargs):
            super().__init__(**kwargs)
            self.name = name
            self.height = dp(20)
            self.button = CustomButton(name=config.get('Name') if config else 'None')
            self.add_widget(self.button)

            self.config: list = config
            self.opened = False
            self.size_hint_y = None
            self.real_height = 0
            self.button.func_bind = self.open_close
            self.display_all_map()
            self.bind(size=self.change, pos=self.change)

        def change(self, *_):
            self.button.size = self.width, dp(20)
            self.button.pos = self.x, self.top-dp(20)
            if hasattr(self, 'grid'):
                self.grid.pos = self.pos

        def open_close(self):
            if self.opened is False:
                self.opened = True
                self.grid.width = self.width
                self.add_widget(self.grid)
                self.height = self.grid.height + dp(20)
            else:
                self.opened = False
                self.remove_widget(self.grid)
                self.height = dp(20)
            self.change()

        def display_all_map(self):
            self.grid = JDMGridLayout(cols=1,
                pos=self.pos,
                size_hint_y=None, width=self.width,
                padding=dp(5), spacing=dp(5))
            self.grid.bind(minimum_height=self.grid.setter('height'))

            if self.config:
                for con in self.config:
                    if con != 'Name': self.grid.add_widget(
                        CustomButton(
                            self.config.get(con).get('Name'),
                            color='444444',
                            size_hint_y=None,
                            height=dp(15),
                            func_bind=lambda con=con, config=self.config.get(con): self.root.main.main.map_nav.add_map(self.name, con, config)))
            self.grid.add_widget(CustomLabel('END', color='222222', size_hint_y=None, height=dp(15)))

    def add_map(self, name, num, config):
        if not self.all_map_widget.get(config.get('Name')):
            if self.current_map:
                self.all_map_widget.get(self.current_map).remove_map()

            new_map = MainMap(name, num, config)            
            self.all_map_widget[config.get('Name')] = new_map    
            self.parent.main_map.add_widget(new_map)
            self.current_map = config.get('Name')
            self.root.main.main.editor.change_background(config)

        elif self.current_map != config.get('Name'):
            self.all_map_widget.get(self.current_map).remove_map()
            self.all_map_widget.get(config.get('Name')).add_map(self.parent.main_map)
            self.current_map = config.get('Name')
            self.root.main.main.editor.change_background(config)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_map = None
        self.all_map_widget = dict()

        self.color = '111111'
        self.size = (Window.width*0.2, Window.height*0.9-dp(20))
        self.pos = (0, dp(10))
        self.display_canvas()
        self.set_config()
        self.display_all_map()

    def set_config(self):
        with open('jsons/all_maps.json') as f:
            self.config = json.load(f)

    def display_all_map(self):
        self.grid = JDMGridLayout(cols=1, size_hint_y=None, padding=dp(5), spacing=dp(5))
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll = JDMScrollView(size=self.size, pos=self.pos)

        for config in self.config:
            if config.startswith('Map'):
                self.grid.add_widget(MapNavWidget.MapList(config, config=self.config.get(config)))

        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)
