import os
from PIL import Image
import zipfile

def split_image(image_path, folder_name):
    with Image.open(image_path) as img:
        width, height = img.size
        count = 1
        for x in range(0, width, 32):
            for y in range(0, height, 32):
                box = (x, y, x + 32, y + 32)
                tile = img.crop(box)
                tile.save(f'{folder_name}/{count}.png')
                count += 1

        with zipfile.ZipFile(f'{folder_name}.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
            for file in os.listdir(folder_name):
                zip.write(f'{folder_name}/{file}', file)

image_path = 'rasset/npc/dog/look_up_anim.png'
folder_name = 'rasset/npc/dog/look_up'

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

split_image(image_path, folder_name)
