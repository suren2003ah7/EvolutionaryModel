from creature_service import creatures
from food_service import foods

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

def move_towards_food(creature, food):
    pass

def get_viewable_cells(eyesight):
    pass