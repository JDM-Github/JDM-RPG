from jdm_kivy import *
from .custom import CustomWidget, CustomButton

class MapEvent(CustomWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = '333333'
        self.size = (Window.width*0.8, dp(20))
        self.pos = (Window.width*0.2, Window.height*0.9-dp(30))
        self.display_canvas()
        self.display_widgets()

    def change_mode(self, widget, text):
        for child in self.children:
            if child is widget:
                child.main_label.outline_color = GetColor('aaccff')
                child.main_label.outline_width = dp(1)
            else:
                child.main_label.outline_color = GetColor('ffffff')
                child.main_label.outline_width = 0

        if self.parent:
            if text == 'Event': self.parent.remove_widget(self.parent.editor)
            else:
                self.parent.remove_widget(self.parent.editor)
                self.parent.add_widget(self.parent.editor)
                self.parent.editor.current_mode = text

            self.parent.modifier.mode = text
            if self.parent.main_map.children:
                for child in self.parent.main_map.children[0].grid.children: child.check_mode(text)

    def display_widgets(self):
        self.add_widget(but1 := CustomButton("Map",
            size=(dp(100), self.height-dp(4)),
            pos=(self.x+dp(2), self.y+dp(2))))
        but1.func_bind = lambda : self.change_mode(but1, 'Map')
        
        self.add_widget(but2 := CustomButton("Behavior",
            size=(dp(100), self.height-dp(4)),
            pos=(but1.right+dp(2), self.y+dp(2))))
        but2.func_bind = lambda : self.change_mode(but2, 'Behavior')
        
        self.add_widget(but3 := CustomButton("HitBox",
            size=(dp(100), self.height-dp(4)),
            pos=(but2.right+dp(2), self.y+dp(2))))
        but3.func_bind = lambda : self.change_mode(but3, 'HitBox')
        
        self.add_widget(but4 := CustomButton("Event",
            size=(dp(100), self.height-dp(4)),
            pos=(but3.right+dp(2), self.y+dp(2))))
        but4.func_bind = lambda : self.change_mode(but4, 'Event')
        
        self.change_mode(but1, 'Map')
