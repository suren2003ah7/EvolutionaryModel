import numpy as np
import grid_service

def should_set_creature_position():
    creature = 0b00011101010110011011111110111010
    x = 47
    y = 58
    new_creature = grid_service.set_creature_position(creature, x, y)
    assert new_creature == 0b00011101010110011011111110101010

should_set_creature_position()