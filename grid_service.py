from food_service import foods
from numpy import random

def get_creature_position(creature):
    x = (creature & (0b111111 << 10)) >> 10
    y = (creature & (0b111111 << 4)) >> 4
    return [x, y]

def set_creature_position(creature, x, y):
    creature = (creature & ~(0b111111 << 10)) | (x << 10)
    creature = (creature & ~(0b111111 << 4)) | (y << 4)
    return creature

def get_food_position(food):
    x = (food & (0b111111 << 6)) >> 6
    y = food & 0b111111
    return [x, y]

def get_position_as_12_bit_number(creature):
    return (creature & 0b00000000000000001111111111110000) >> 4

def get_neighbours(creature, creatures):
    neighbours = []
    creature_pos = get_creature_position(creature)
    for other_creature in creatures:
        if other_creature == creature:
            continue
        if get_creature_position(other_creature) == creature_pos:
            neighbours.append(other_creature)
    return neighbours

def get_foods_in_eyesight(creature, eyesight):
    foods_in_eyesight = []
    food_positions = []
    for food in foods:
        food_positions.append(get_food_position(food))
    viewable_cells = get_viewable_cells(get_creature_position(creature), eyesight)
    for viewable_cell in viewable_cells:
        if viewable_cell in food_positions:
            food_index = food_positions.index(viewable_cell)
            foods_in_eyesight.append(foods[food_index])
    return foods_in_eyesight

def move_towards_food(creature, food, number_of_moves):
    creature_x, creature_y = get_creature_position(creature)
    food_x, food_y = get_food_position(food)
    while number_of_moves > 0:
        if food_x == creature_x and food_y == creature_y:
            break
        if food_x > creature_x:
            creature_x += 1
        elif food_x < creature_x:
            creature_x -= 1
        if food_y > creature_y:
            creature_y += 1
        elif food_y < creature_y:
            creature_y -= 1
        number_of_moves -= 1
    creature = set_creature_position(creature, creature_x, creature_y)
    return creature

def get_viewable_cells(position, eyesight):
    x0, y0 = position[0], position[1]
    viewable_cells = []
    for dx in range(-eyesight, eyesight + 1):
        x = x0 + dx
        if x < 0 or x > 63:
            continue
        for dy in range(-eyesight + abs(dx), eyesight - abs(dx) + 1):
            y = y0 + dy
            if 0 <= y <= 63:
                viewable_cells.append([x, y])
    return viewable_cells

def move_random(creature, number_of_moves):
    x, y = get_creature_position(creature)
    while number_of_moves > 0:
        directions = get_possible_movement_directions(x, y)
        direction = random.choice(directions)
        if direction == 'up':
            y += 1
        elif direction == 'down':
            y -= 1
        elif direction == 'left':
            x -= 1
        elif direction == 'right':
            x += 1
        number_of_moves -= 1
    creature = set_creature_position(creature, x, y)
    return creature

def get_possible_movement_directions(x, y):
    directions = ['up', 'down', 'left', 'right']
    if y == 63:
        directions.remove('up')
    if y == 0:
        directions.remove('down')
    if x == 0:
        directions.remove('left')
    if x == 63:
        directions.remove('right')
    return directions
