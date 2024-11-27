import numpy as np
from random import randint
from constants import BASE_ENERGY_LEVEL

creatures = []

def create_creature():
    creature = np.uint32(randint(0, 2**32 - 1))
    stamina = get_stamina(creature)
    creature = set_energy(creature, stamina)
    creatures.append(creature)

def get_max_energy(creature):
    return BASE_ENERGY_LEVEL*get_stamina(creature)

def get_speed(creature):
    return (creature >> 30) & (0b11) + 1

def get_eyesight(creature):
    return (creature >> 27) & (0b111)

def get_aggression(creature):
    return (creature >> 24) & (0b111)

def get_strength(creature):
    return (creature >> 20) & (0b1111) + 1

def get_stamina(creature):
    return (creature >> 16) & (0b1111) + 1

def get_energy(creature):
    pass

def set_energy(creature, new_energy):
    pass

# fight and
def fight(creature, other_creature):
    pass

def reproduce_if_possible(creature):
    pass

def mutate_speed(creature):
    pass

def mutate_eyesight(creature):
    pass

def mutate_aggression(creature):
    pass

def mutate_strength(creature):
    pass

def mutate_stamina(creature):
    pass

def eat_food(creature):
    pass

def eat_creature(creature, other_creature):
    pass
