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
    pass

def get_speed(creature):
    pass

def get_eyesight(creature):
    pass

def get_aggression(creature):
    pass

def get_strength(creature):
    pass

def get_stamina(creature):
    pass

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