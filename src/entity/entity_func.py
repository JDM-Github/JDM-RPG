import math
from kivy.core.window import Window

def get_npc_direction(first, second):
    x_diff = first[0] - second[0]
    y_diff = first[1] - second[1]
    if abs(x_diff) > abs(y_diff):
        if x_diff > 0: return "right"
        else: return "left"
    else:
        if y_diff > 0: return "up"
        else: return "down"

def what_move_to_target(entity, target_pos, who_will_move, direction, position):
    # Calculate the distance between the entities at the current position

    current_dist = math.sqrt((who_will_move[0] - target_pos[0])**2 + (who_will_move[1] - target_pos[1])**2)
    if current_dist <= 1: return 'n'

    if position == 'back':
        if direction.endswith('up'): target_pos = target_pos[0], target_pos[1]-1
        elif direction.endswith('down'): target_pos = target_pos[0], target_pos[1]+1
        elif direction.endswith('left'): target_pos = target_pos[0]+1, target_pos[1]
        elif direction.endswith('right'): target_pos = target_pos[0]-1, target_pos[1]
    elif position == 'front':
        if direction.endswith('up'): target_pos = target_pos[0], target_pos[1]+1
        elif direction.endswith('down'): target_pos = target_pos[0], target_pos[1]-1
        elif direction.endswith('left'): target_pos = target_pos[0]-1, target_pos[1]
        elif direction.endswith('right'): target_pos = target_pos[0]+1, target_pos[1]
    elif position == 'left':
        if direction.endswith('up'): target_pos = target_pos[0]-1, target_pos[1]
        elif direction.endswith('down'): target_pos = target_pos[0]+1, target_pos[1]
        elif direction.endswith('left'): target_pos = target_pos[0], target_pos[1]-1
        elif direction.endswith('right'): target_pos = target_pos[0], target_pos[1]+1
    elif position == 'right':
        if direction.endswith('up'): target_pos = target_pos[0]+1, target_pos[1]
        elif direction.endswith('down'): target_pos = target_pos[0]-1, target_pos[1]
        elif direction.endswith('left'): target_pos = target_pos[0], target_pos[1]+1
        elif direction.endswith('right'): target_pos = target_pos[0], target_pos[1]-1
    if who_will_move == target_pos: return 'n'

    up_dist = 999
    down_dist = 999
    left_dist = 999
    right_dist = 999

    # Calculate the distance to the other entity after each possible move
    if find_entity_in_position(entity, who_will_move[0], who_will_move[1]+1) is None:
        up_dist = math.sqrt((who_will_move[0] - target_pos[0])**2 + (who_will_move[1] - target_pos[1] + 1)**2)

    if find_entity_in_position(entity, who_will_move[0], who_will_move[1]-1) is None:
        down_dist = math.sqrt((who_will_move[0] - target_pos[0])**2 + (who_will_move[1] - target_pos[1] - 1)**2)
    
    if find_entity_in_position(entity, who_will_move[0]-1, who_will_move[1]) is None:
        left_dist = math.sqrt((who_will_move[0] - target_pos[0] - 1)**2 + (who_will_move[1] - target_pos[1])**2)
    
    if find_entity_in_position(entity, who_will_move[0]+1, who_will_move[1]) is None:
        right_dist = math.sqrt((who_will_move[0] - target_pos[0] + 1)**2 + (who_will_move[1] - target_pos[1])**2)
    
    min_dist = min(up_dist, down_dist, left_dist, right_dist)
    if left_dist == min_dist: return 'a'
    if right_dist == min_dist: return 'd'
    if up_dist == min_dist: return 'w'
    if down_dist == min_dist: return 's'

def find_entity_in_position(entity, x, y):
    from .entities import Entity
    for rect in entity.main.all_entities.children:
        if (isinstance(rect, Entity)
        and rect.pos[0] >= -rect.size[0] and rect.pos[0] < Window.width
        and rect.pos[1] >= -rect.size[1] and rect.pos[1] < Window.height):
            if rect.x_position == x and rect.y_position == y:
                return rect
    return None
