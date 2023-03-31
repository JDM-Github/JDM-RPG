from jdm_kivy import *
from kivy.core.image import Image as CoreImage

class MessageBox(Canvas):

    def __init__(self, root, zoom, texture_list) -> None:
        super().__init__()
        self.main = root
        self.root = self.main.root
        self.zoom = zoom
        self.text_speed = 0
        self.text_max_speed = 0.03

        self.all_texture_text : list[list[Rectangle]] = []
        self.texture_list = texture_list
        self.all_variables()
        self.display_message_box()

    def all_variables(self):
        self.all_color_main = []
        self.all_color_shadow = []
        self.original_color = '404040'
        self.original_shadow_color = 'd8d8c0'
        self.all_mode = []
        self.all_mode_index = 0
        self.start_message = False

        self.up_position = (dp(10)*self.zoom) + (dp(32)*self.zoom)
        self.mid_position = (dp(10)*self.zoom) + (dp(16)*self.zoom)
        self.down_position = (dp(10)*self.zoom)

    def display_message_box(self):
        self.text_box1 = Canvas()
        self.text_box2 = Canvas()
        self.text_box3 = Canvas()
        self.box_color = Color(rgba=GetColor('ffffffff'))
        self.displaying = False

        size = get_image_size('rasset/messagebox/orig.png')
        self.size = (dp(size[0])*self.zoom, (dp(16)*self.zoom)*4)
        self.pos = Window.width/2-self.size[0]/2, dp(8)
        self.margin = dp(16)*self.zoom
        self.max_width = self.size[0]-(self.margin*2)-(dp(16)*self.zoom*3)

        self.message_box = Rectangle(size=self.size, pos=self.pos)        
        self.message_box.texture = CoreImage('rasset/messagebox/orig.png').texture
        self.message_box.texture.mag_filter = 'nearest'

    def remove_all(self):
        if self.mugshot_canvas in self.children: self.remove(self.mugshot_canvas)
        if self.box_color in self.children: self.remove(self.box_color)
        if self.message_box in self.children: self.remove(self.message_box)
        if self.text_box1 in self.children: self.remove(self.text_box1)
        if self.text_box2 in self.children: self.remove(self.text_box2)
        if self.text_box3 in self.children: self.remove(self.text_box3)

    def add_all(self):
        self.add(self.box_color)
        self.add(self.message_box)
        self.add(self.text_box1)
        self.add(self.text_box2)
        self.add(self.text_box3)
        self.add(self.mugshot_canvas)

    def manage_text(self, text):
        self.all_mode_index = 0
        self.all_mode.clear()
        self.all_texture_text.clear()
        self.all_texture_text.append(list())

        self.all_color_main.clear()
        self.all_color_shadow.clear()

        current_width = 0
        have_single = False
        have_double = False
        escape_check = False

        activate_color_main = False
        act_main = False
        act_shad = False
        color_activate_list = []
        curr_type = 'main'

        current_color_main = self.original_color
        current_color_shadow = self.original_shadow_color

        for  t in text:
            if escape_check:
                escape_check = False
                if t in ('l', 'n'):
                    current_width = 0
                    self.all_mode.append(t)
                    self.all_texture_text.append(list())
                    continue
                elif t == 'c':
                    if (act_main):
                        current_color_main = self.original_color
                        color_activate_list.clear()
                    else:
                        act_main = True
                        activate_color_main = True
                        curr_type = 'main'
                    continue
                elif t == 's':
                    if (act_shad):
                        current_color_shadow = self.original_shadow_color
                        color_activate_list.clear()
                    else:
                        act_shad = True
                        activate_color_main = True
                        curr_type = 'shad'
                        color_activate_list.clear()
                    continue   

            if activate_color_main:
                res = self.get_color(color_activate_list, t, curr_type)
                if res[0] or res[1]:
                    activate_color_main = False
                    current_color_main = res[0] if res[0] is not None else current_color_main
                    current_color_shadow = res[1] if res[1] is not None else current_color_shadow
                continue

            if t in ('"', "'"):
                if have_single and t == "'":
                    t = "''"
                    have_single = False
                elif have_double and t == '"':
                    t = '""'
                    have_double = False
                elif not have_single and not have_double:
                    if t == "'": have_single = True
                    else: have_double = True

            elif t == '\n':
                current_width = 0
                self.all_mode.append('n')
                self.all_texture_text.append([])
                continue
            elif t == '\\':
                escape_check = True
                continue

            texture = self.texture_list.get(t)
            if texture:
                texture_width = texture.width * self.zoom
                current_width += texture_width
                if current_width >= self.max_width:
                    self.all_texture_text.append([])
                    self.all_mode.append('n')
                    current_width = 0
                if t != ' ':
                    self.all_color_main.append(current_color_main)
                    self.all_color_shadow.append(current_color_shadow)
                self.all_texture_text[-1].append([(texture_width, texture.height*self.zoom), t])

        self.all_texture_text = [sublist for sublist in self.all_texture_text if sublist]

    def get_color(self, color_activity_list, t, type_='main'):
        if not color_activity_list:
            if t != '[': raise SyntaxError(f"Invalid use of \c, Example \c[ff0000]")
            color_activity_list.append('[')
        else:
            if t == '#':
                if len(color_activity_list) != 1: raise SyntaxError(f"Invalid use of \c, Example \c[ff0000]")
                color_activity_list.append('#')
            elif len(color_activity_list) == 7:
                if t == ']': return (''.join(color_activity_list[1:]), None) if type_ == 'main' else (None, ''.join(color_activity_list[1:]))
            elif len(color_activity_list) == 9:
                if t != ']': raise SyntaxError(f"Invalid use of \c, Example \c[ff0000]")
                return (''.join(color_activity_list[1:]), None) if type_ == 'main' else (None, ''.join(color_activity_list[1:]))

            elif t.upper() in '0123456789ABCDEF':
                color_activity_list.append(t)
            else: raise SyntaxError(f"Invalid use of \c, Example \c[ff0000]")
        return (None, None)

    def display_message(self, text, type_='normal'):
        if self.start_message is False:
            self.color_index = 0
            self.start_message = True
            self.current_col = 0
            self.current_width = 0
            self.current_posstr = 'up'
            self.current_position = self.up_position
            self.texture_index = 0

            self.text_box1.clear()
            self.text_box2.clear()
            self.text_box3.clear()
            self.manage_text(text)
            self.show_mugshot()

        self.continue_display()

    def show_mugshot(self):
        self.mugshot_canvas = Rectangle(
            source='rasset/mugshot/JD.png',
            size=(dp(48)*self.zoom, dp(48)*self.zoom),
            pos=(self.max_width+(dp(47)*self.zoom), dp(10)*self.zoom))
        self.mugshot_canvas.texture.mag_filter = 'nearest'

    def continue_display(self):
        if self.displaying is False:
            self.remove_all()
            if self.texture_index < len(self.all_texture_text):
                self.add_all()
                self.check_changes()
                self.displaying = True
            else: self.start_message = False

    def reset_message(self):
        self.text_speed = self.text_max_speed
        self.start_message = False
        self.displaying = False

    def update(self):
        if self.text_speed <= 0 and self.displaying:
            self.text_speed = self.text_max_speed
            if self.texture_index < len(self.all_texture_text) and self.current_col < len(self.all_texture_text[self.texture_index]):
                texture = self.all_texture_text[self.texture_index][self.current_col]
                if texture[1] == ' ':
                    self.current_col += 1
                    self.current_width += texture[0][0]
                    self.text_speed -= self.root.elapseTime
                    return

                col = Color(rgb=GetColor(self.all_color_main[self.color_index]))
                rect = Rectangle(
                    pos=(self.pos[0]+self.margin+(self.current_width),
                         self.current_position),
                    size=texture[0],
                    texture=self.texture_list.get(texture[1]))
                rect.texture.mag_filter = 'nearest'

                s_col = Color(rgb=GetColor(self.all_color_shadow[self.color_index]))
                s_rect = Rectangle(
                    pos=(self.pos[0]+self.margin+(self.current_width),
                         self.current_position),
                    size=texture[0],
                    texture=self.texture_list.get('s_'+texture[1]))
                s_rect.texture.mag_filter = 'nearest'

                self.current_width += texture[0][0]
                self.color_index += 1

                if self.current_posstr == 'up':
                    self.text_box1.add(col)
                    self.text_box1.add(rect)
                    self.text_box1.add(s_col)
                    self.text_box1.add(s_rect)

                elif self.current_posstr == 'mid':
                    self.text_box2.add(col)
                    self.text_box2.add(rect)
                    self.text_box2.add(s_col)
                    self.text_box2.add(s_rect)

                else:
                    self.text_box3.add(col)
                    self.text_box3.add(rect)
                    self.text_box3.add(s_col)
                    self.text_box3.add(s_rect)
                self.current_col += 1

            else:
                self.texture_index += 1
                self.current_width = 0
                self.current_col = 0
                if self.texture_index < len(self.all_texture_text):
                    if self.current_posstr == 'up':
                        self.current_posstr = 'mid'
                        self.current_position = self.mid_position
                        self.all_mode_index += 1

                    elif self.current_posstr == 'mid':
                        self.current_posstr = 'down'
                        self.current_position = self.down_position
                        self.all_mode_index += 1

                    else: self.displaying = False

                else: self.displaying = False
        self.text_speed -= self.root.elapseTime

    def check_changes(self):
        if self.current_posstr == 'down':
            if self.all_mode[self.all_mode_index] == 'n':
                self.current_posstr = 'up'
                self.current_position = self.up_position
                self.text_box1.clear()
                self.text_box2.clear()
                self.text_box3.clear()
            else:
                self.text_box1.clear()
                all_texture = self.text_box2.children
                for text in all_texture:
                    if isinstance(text, Rectangle):
                        text.pos = [text.pos[0], self.up_position]
                        self.text_box1.add(text)
                    elif isinstance(text, Color):
                        self.text_box1.add(text)

                self.text_box2.clear()
                all_texture = self.text_box3.children
                for text in all_texture:
                    if isinstance(text, Rectangle):
                        text.pos = [text.pos[0], self.mid_position]
                        self.text_box2.add(text)
                    elif isinstance(text, Color):
                        self.text_box2.add(text)

                self.text_box3.clear()
            self.all_mode_index += 1
