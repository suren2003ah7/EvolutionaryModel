from creature_service import creatures
from food_service import foods
from numpy import random

def get_position(creature):
    x = (creature & (0b111111 << 10)) >> 10
    y = (creature & (0b111111 << 4)) >> 4
    return [x, y]

def get_position_as_12_bit_number(creature):
    return (creature & (0b111111111111 << 4)) >> 4

def get_neighbours(creature):
    neighbours = []
    for other_creature in creatures:
        if other_creature == creature:
            continue
        if get_position(other_creature) == get_position(creature):
            neighbours.append(other_creature)
    return neighbours

def get_foods_in_eyesight(eyesight):
    foods_in_eyesight = []
    viewable_cells = get_viewable_cells(eyesight)
    for viewable_cell in viewable_cells:
        if viewable_cell in foods:
            foods_in_eyesight.append(viewable_cell)
    return foods_in_eyesight

def move(creature):
    pass

def move_towards_food(creature, food) -> bool:
    creature_x, creature_y = get_position(creature)
    food_x = (food & (0b111111 << 6)) >> 6
    food_y = food & 0b111111

    if food_x > creature_x and creature_x < 63:
        creature_x += 1
    elif food_x < creature_x and creature_x > 0:
        creature_x -= 1

    if food_y > creature_y and creature_y < 63:
        creature_y += 1
    elif food_y < creature_y and creature_y > 0:
        creature_y -= 1

    creature = (creature & ~(0b111111 << 10)) | (creature_x << 10)
    creature = (creature & ~(0b111111 << 4)) | (creature_y << 4)

    return True

def get_viewable_cells(eyesight):
    pass

def move_random(creature) -> bool:
    # when you can't move to a good food source.

    x, y = get_position(creature)
    direction = random.choice(['up', 'down', 'left', 'right'])

    if direction == 'up' and y < 63:
        y += 1
    elif direction == 'down' and y > 0:
        y -= 1
    elif direction == 'left' and x > 0:
        x -= 1
    elif direction == 'right' and x < 63:
        x += 1

    creature = (creature & ~(0b111111 << 10)) | (x << 10)
    creature = (creature & ~(0b111111 << 4)) | (y << 4)

    return True
