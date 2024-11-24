import numpy as np
from random import random
from constants import BASE_ENERGY_LEVEL, PROBABILITY_OF_INDIVIDUAL_GENE_MUTATION, ENERGY_GAINED_FROM_EATING_FOOD

def create_creature(gene):
    creature = [gene, BASE_ENERGY_LEVEL]
    return creature

def get_max_energy(gene):
    max_energy = BASE_ENERGY_LEVEL * get_stamina()
    return max_energy

def eat_food(creature):
    creature[2] += ENERGY_GAINED_FROM_EATING_FOOD

def eat_creature(creature, other_creature):
    pass

def get_speed(gene):
    pass

def get_eyesight(gene):
    pass

def get_aggression(gene):
    pass

def get_strength(gene):
    pass

def get_stamina(gene):
    pass

def mutate_speed(gene):
    pass

def mutate_eyesight(gene):
    pass

def mutate_aggression(gene):
    pass

def mutate_strength(gene):
    pass

def mutate_stamina(gene):
    pass

def reproduce(creature):
    new_gene = creature[0]

    new_gene = mutate_speed(new_gene)
    new_gene = mutate_eyesight(new_gene)
    new_gene = mutate_aggression(new_gene)
    new_gene = mutate_strength(new_gene)
    new_gene = mutate_stamina(new_gene)

    new_creature = [new_gene, BASE_ENERGY_LEVEL]
    return new_creature