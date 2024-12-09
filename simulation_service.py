from random import choice
import constants
from creature_service import creatures, create_creature, create_creature_from_gene, eat_food, get_eyesight, reproduce_if_possible, is_creature_fighting, fight, get_speed, get_energy, calculate_and_set_new_energy
from food_service import foods, create_food
from grid_service import (get_neighbours,
                          get_foods_in_eyesight, move_random, move_towards_food, get_position_as_12_bit_number)

creatures_already_fought_in_current_round = []

def initialize():
    creatures.clear()
    foods.clear()
    for _ in range(constants.INITIAL_NUMBER_OF_CREATURES):
        create_creature()
    simulate_food()

def initialize_from_gene(gene):
    creatures.clear()
    foods.clear()
    for _ in range(constants.INITIAL_NUMBER_OF_CREATURES):
        create_creature_from_gene(gene)
    simulate_food()

def simulate_step():
    creatures_already_fought_in_current_round.clear()
    creatures_to_remove = []
    creatures_to_add = []
    for i in range(len(creatures)):
        creature = creatures[i]
        if creature in creatures_already_fought_in_current_round or creature in creatures_to_remove:
            continue
        updated_creature, new_offsprings = simulate_individual_creature_step(creature, creatures_to_remove)
        creatures[i] = updated_creature
        if len(new_offsprings) != 0:
            creatures_to_add.extend(new_offsprings)
    for creature in creatures_to_remove:
        if creature in creatures:
            creatures.remove(creature)
    creatures.extend(creatures_to_add)
    simulate_food()

def simulate_individual_creature_step(creature, creatures_to_remove):
    creatures_to_add = []
    neighbours = get_neighbours(creature, creatures, creatures_to_remove)
    if len(neighbours) != 0 and is_creature_fighting(creature):
        target_neighbour = choice(neighbours)
        winner = fight(creature, target_neighbour, creatures_to_remove)
        winner, offsprings = reproduce_if_possible(winner)
        creatures_already_fought_in_current_round.append(winner)
        if len(offsprings) != 0:
            creatures_to_add.extend(offsprings)
        if creature not in creatures_to_remove:
            return winner, creatures_to_add
        else:
            creatures_to_remove.append(target_neighbour)
            creatures_to_add.append(winner)
            return creature, creatures_to_add
    elif get_position_as_12_bit_number(creature) in foods:
        foods.remove(get_position_as_12_bit_number(creature))
        creature = calculate_and_set_new_energy(creature, 0)
        creature = eat_food(creature)
        creature, offsprings = reproduce_if_possible(creature)
        if len(offsprings) != 0:
            creatures_to_add.extend(offsprings)
    else:
        eyesight = get_eyesight(creature)
        foods_in_eyesight = get_foods_in_eyesight(creature, eyesight)
        number_of_moves = get_speed(creature)
        if len(foods_in_eyesight) != 0:
            target_food = choice(foods_in_eyesight)
            creature, energy_loss_from_moving = move_towards_food(creature, target_food, number_of_moves)
        else:
            creature, energy_loss_from_moving = move_random(creature, number_of_moves)
        creature = calculate_and_set_new_energy(creature, energy_loss_from_moving)
    if get_energy(creature) <= 0:
        creatures_to_remove.append(creature)
    return creature, creatures_to_add

def simulate_food():
    from constants import FOOD_CAP
    amount_of_food_to_generate = int(max(0, FOOD_CAP - len(foods)))
    while amount_of_food_to_generate > 0:
        create_food()
        amount_of_food_to_generate -= 1

# TODO: OPTIMIZE USING CPYTHON, ADD CROSS FUNCTIONALITY WITH OTHER GEOMETRY TYPES.
