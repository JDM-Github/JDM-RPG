import json
import zipfile
import os
import pprint
from .Jwidget import JDMWidget, JDMLabel
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Rectangle, Color
from kivy.graphics.texture import Texture
from PIL import Image

def JDM_getColor(string: str) -> str:
    with open("jsons/all_color.json", 'r') as f:
        main : dict = json.load(f)
        color : str = main.get(string.title())
    return color if color else "#ffffff"

def JDM_addTitle(widget: JDMWidget, text: str, height: float,
             background_color: str, foreground_color: str, font_size: int or str):
    widget._main_title = JDMLabel(text=text, font_size=font_size, color=GetColor(foreground_color),
                                  size=(widget.width, height), pos=(widget.x, widget.top-height))
    with widget.canvas:
        widget._main_title_color = Color(rgba=GetColor(background_color))
        widget._main_title_rect = Rectangle(size=(widget.width, height), pos=(widget.y, widget.top-height))
    widget.add_widget(widget._main_title)

def get_image_size(filepath):
    with Image.open(filepath) as img:
        size = img.size
        return size

def get_gif_frames(filename: str):
    if filename and filename.endswith('zip') and os.path.exists(filename):
        return get_zip_frames(filename)

    if (not filename or not filename.endswith('gif')
        or not os.path.exists(filename)): return -1

    with Image.open(filename) as im:
        durations = []
        for frame in range(im.n_frames):
            im.seek(frame)
            durations.append(im.info['duration'] / 1000)
        num_frames = len(durations)
    return num_frames

def get_zip_frames(filename: str):
    with zipfile.ZipFile(filename, 'r') as zip_file:
        num_files = len(zip_file.namelist())
    return num_files

def json_obj(filename:str) -> dict:
    if os.path.exists(filename):
        try:
            with open(filename) as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    else: return {}

def pprint_save_json(obj:object,
              filename:str='data.json',
              depth:int|None=None,
              width:int=80,
              indent:int=1,
              sort_dicts:bool=False,
              underscore_numbers:bool=False,
              compact:bool=False):

    json_str = pprint.pformat(
        obj,
        depth=depth,
        width=width,
        indent=indent,
        sort_dicts=sort_dicts,
        compact=compact,
        underscore_numbers=underscore_numbers
    )
    json_str = json_str.replace("'", "\"")
    json_str = json_str.replace("None", "null")
    with open(filename, "w") as f: f.write(json_str)

def save_json(obj: object,
              filename: str,
              indent=4):
    with open(filename, 'w') as f:
        json.dump(obj, f, indent=indent)

def get_texture_on_four_texture(w1, w2, w3, w4):
    gif1 = w1.texture
    gif2 = w2.texture
    gif3 = w3.texture
    gif4 = w4.texture

    # determine the size of the new texture based on the sizes of the input textures
    new_width = max(gif1.width + gif2.width, gif3.width + gif4.width)
    new_height = max(gif1.height + gif3.height, gif2.height + gif4.height)

    texture = Texture.create(size=(new_width, new_height))
    
    # calculate the position of each input texture based on its size
    pos1 = (0, 0)
    pos2 = (new_width - gif2.width, 0)
    pos3 = (0, new_height - gif3.height)
    pos4 = (new_width - gif4.width, new_height - gif4.height)
    
    texture.blit_buffer(gif1.pixels, colorfmt=gif1.colorfmt, bufferfmt=gif1.bufferfmt, pos=pos1, size=gif1.size)
    texture.blit_buffer(gif2.pixels, colorfmt=gif2.colorfmt, bufferfmt=gif2.bufferfmt, pos=pos2, size=gif2.size)
    texture.blit_buffer(gif3.pixels, colorfmt=gif3.colorfmt, bufferfmt=gif3.bufferfmt, pos=pos3, size=gif3.size)
    texture.blit_buffer(gif4.pixels, colorfmt=gif4.colorfmt, bufferfmt=gif4.bufferfmt, pos=pos4, size=gif4.size)
    
    texture.flip_vertical()

    return texture