from jdm_kivy import *

all_items_id = {
    0 : None,
    1 : 'Sword0',
    2 : 'Sword1',
    3 : 'Sword2',
}

class ItemSlot(Canvas):
    
    def __init__(self, slot_number=0, item_id=0) -> None:
        super().__init__()
        self.slot_number = slot_number
        self.slot_texture()      
        self.display_item(item_id)

    def slot_texture(self):
        with self:
            block = dp(32*2)
            rect = Rectangle(
                size = (block, block),
                pos = (dp(10) + ((block+dp(10))*self.slot_number), Window.height-(block+dp(10))),
                source = 'rasset/itemslot.png'
            )
            rect.texture.mag_filter = 'nearest'
            
            self.item_rect = Rectangle(
                size=(block, block),
                pos=(dp(10) + ((block+dp(10))*self.slot_number), Window.height-(block+dp(10)))
            )

    def display_item(self, item_id=0):
        if item_id <= 0 :
            self.item_rect.source = 'rasset/transparent.png'
            return
        self.item_rect.source = f'rasset/sword/{all_items_id.get(item_id)}.png'
        self.item_rect.texture.mag_filter = 'nearest'
