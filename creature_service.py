import numpy as np
from math import ceil, floor, sqrt
from random import randint, random, choice
from constants import (BASE_ENERGY_LEVEL, NUMBER_OF_CHILDREN_PER_REPRODUCTION,
                       PROBABILITY_OF_INDIVIDUAL_GENOME_MUTATION, ENERGY_RATIO_REQUIRED_TO_REPRODUCE,
                       ENERGY_RATIO_SPENT_TO_REPRODUCE, ENERGY_GAINED_FROM_EATING_FOOD,
                       ENERGY_GAINED_FROM_EATING_CREATURE)

creatures = []

def create_creature():
    creature = randint(0, 2**32 - 1)
    creature = set_energy(creature, get_max_energy(creature))
    creatures.append(creature)

def create_offspring(parent_creature):
    offspring = randint(0, 2**32 - 1)
    offspring = (offspring & 0b00000000000000001111111111111111) | (get_gene(parent_creature) << 16)
    return offspring

def get_max_energy(creature):
    return BASE_ENERGY_LEVEL + get_stamina(creature)

def get_gene(creature):
    return (creature >> 16) & 0b1111111111111111

def get_speed(creature):
    return ((creature >> 30) & 0b11) + 1

def set_speed(creature, new_speed):
    return (creature & 0b00111111111111111111111111111111) | ((new_speed - 1) << 30)

def get_eyesight(creature):
    return (creature >> 27) & 0b111

def set_eyesight(creature, new_eyesight):
    return (creature & 0b11000111111111111111111111111111) | (new_eyesight << 27)

def get_aggression(creature):
    return (creature >> 24) & 0b111

def set_aggression(creature, new_aggression):
    return (creature & 0b11111000111111111111111111111111) | (new_aggression << 24)

def get_strength(creature):
    return ((creature >> 20) & 0b1111) + 1

def set_strength(creature, new_strength):
    return (creature & 0b11111111000011111111111111111111) | ((new_strength - 1) << 20)

def get_stamina(creature):
    return int((creature >> 16) & 0b1111) - 7

def set_stamina(creature, new_stamina):
    return (creature & 0b11111111111100001111111111111111) | ((new_stamina + 7) << 16)

def get_energy(creature):
    return creature & 0b1111

def set_energy(creature, new_energy):
    return (creature & 0b11111111111111111111111111110000) | max(new_energy, 0)

def is_creature_fighting(creature):
    p = get_aggression(creature) / 7
    return random() <= p

def fight(creature, other_creature, creatures_to_remove):
    strength = get_strength(creature)
    other_strength = get_strength(other_creature)
    total_strength = strength + other_strength
    outcome = randint(1, total_strength)
    if outcome <= strength:
        creatures_to_remove.append(other_creature)
        creature = calculate_and_set_new_energy(creature, 0)
        creature = eat_creature(creature)
        return creature
    else:
        creatures_to_remove.append(creature)
        other_creature = calculate_and_set_new_energy(other_creature, 0)
        other_creature = eat_creature(other_creature)
        return other_creature

def reproduce_if_possible(creature):
    if get_energy(creature) < int(get_max_energy(creature) * ENERGY_RATIO_REQUIRED_TO_REPRODUCE):
        return []
    offsprings = []
    number_of_offsprings = NUMBER_OF_CHILDREN_PER_REPRODUCTION
    while number_of_offsprings > 0:
        offspring = create_offspring(creature)
        offspring = try_mutating_speed(offspring)
        offspring = try_mutating_eyesight(offspring)
        offspring = try_mutating_aggression(offspring)
        offspring = try_mutating_strength(offspring)
        offspring = try_mutating_stamina(offspring)
        offspring = set_energy(offspring, get_max_energy(offspring))
        offsprings.append(offspring)
        number_of_offsprings -= 1
    new_energy = int(get_energy(creature) - int(get_max_energy(creature) * ENERGY_RATIO_SPENT_TO_REPRODUCE))
    creature = set_energy(creature, new_energy)
    return creature, offsprings

def try_mutating_speed(creature):
    if random() <= PROBABILITY_OF_INDIVIDUAL_GENOME_MUTATION:
        mutation = choice([-1, 1])
        speed = get_speed(creature)
        if speed == 1 and mutation == -1:
            speed = 1
        elif speed == 4 and mutation == 1:
            speed = 4
        else:
            speed += mutation
        creature = set_speed(creature, speed)
    return creature

def try_mutating_eyesight(creature):
    if random() <= PROBABILITY_OF_INDIVIDUAL_GENOME_MUTATION:
        mutation = choice([-1, 1])
        eyesight = get_eyesight(creature)
        if eyesight == 0 and mutation == -1:
            eyesight = 0
        elif eyesight == 7 and mutation == 1:
            eyesight = 7
        else:
            eyesight += mutation
        creature = set_eyesight(creature, eyesight)
    return creature

def try_mutating_aggression(creature):
    if random() <= PROBABILITY_OF_INDIVIDUAL_GENOME_MUTATION:
        mutation = choice([-1, 1])
        aggression = get_aggression(creature)
        if aggression == 0 and mutation == -1:
            aggression = 0
        elif aggression == 7 and mutation == 1:
            aggression = 7
        else:
            aggression += mutation
        creature = set_aggression(creature, aggression)
    return creature

def try_mutating_strength(creature):
    if random() <= PROBABILITY_OF_INDIVIDUAL_GENOME_MUTATION:
        mutation = choice([-1, 1])
        strength = get_strength(creature)
        if strength == 1 and mutation == -1:
            strength = 1
        elif strength == 16 and mutation == 1:
            strength = 16
        else:
            strength += mutation
        creature = set_strength(creature, strength)
    return creature

def try_mutating_stamina(creature):
    if random() <= PROBABILITY_OF_INDIVIDUAL_GENOME_MUTATION:
        mutation = choice([-1, 1])
        stamina = get_stamina(creature)
        if stamina == -7 and mutation == -1:
            stamina = -7
        elif stamina == 8 and mutation == 1:
            stamina = 8
        else:
            stamina += mutation
        creature = set_stamina(creature, stamina)
    return creature

def eat_food(creature):
    new_energy = min(get_energy(creature) + ENERGY_GAINED_FROM_EATING_FOOD, get_max_energy(creature))
    creature = set_energy(creature, new_energy)
    return creature

def eat_creature(creature):
    new_energy = min(get_energy(creature) + ENERGY_GAINED_FROM_EATING_CREATURE, get_max_energy(creature))
    creature = set_energy(creature, new_energy)
    return creature

def calculate_and_set_new_energy(creature, number_of_steps):
    current_energy = get_energy(creature)
    energy_loss = (number_of_steps + ceil(get_eyesight(creature) / 3) +
                   floor(get_aggression(creature) / 5) + floor(sqrt(get_strength(creature))) +
                   floor((get_stamina(creature) / 7) + 1))
    new_energy = current_energy - energy_loss
    return set_energy(creature, new_energy)

