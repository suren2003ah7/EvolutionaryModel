from random import choice
from constants import INITIAL_NUMBER_OF_CREATURES
from creature_service import creatures, create_creature, eat_food, get_eyesight, reproduce_if_possible, is_creature_fighting, fight, get_speed
from food_service import foods, create_food
from grid_service import (get_position_as_12_bit_number, get_neighbours,
                          get_foods_in_eyesight, move_random, move_towards_food)

creatures_already_fought_in_current_round = []

def initialize():
    creatures.clear()
    foods.clear()
    for _ in range(INITIAL_NUMBER_OF_CREATURES):
        create_creature()
    simulate_food()

def simulate_step():
    creatures_already_fought_in_current_round.clear()
    creatures_to_remove = []
    creatures_to_add = []
    for i in range(len(creatures)):
        creature = creatures[i]
        if creature in creatures_already_fought_in_current_round:
            continue
        updated_creature, new_offsprings = simulate_individual_creature_step(creature, creatures_to_remove)
        creatures[i] = updated_creature
        if new_offsprings:
            creatures_to_add.extend(new_offsprings)
    # Update creatures list
    for creature in creatures_to_remove:
        if creature in creatures:
            creatures.remove(creature)
    creatures.extend(creatures_to_add)
    simulate_food()

def simulate_individual_creature_step(creature, creatures_to_remove):
    creatures_to_add = []
    neighbours = get_neighbours(creature, creatures)
    if len(neighbours) != 0 and is_creature_fighting(creature):
        target_neighbour = choice(neighbours)
        winner = fight(creature, target_neighbour, creatures_to_remove)
        creatures_already_fought_in_current_round.append(winner)
        offspring = reproduce_if_possible(winner)
        if offspring:
            creatures_to_add.extend(offspring)
        return winner, creatures_to_add
    position = get_position_as_12_bit_number(creature)
    if position in foods:
        foods.remove(position)
        creature = eat_food(creature)
        offspring = reproduce_if_possible(creature)
        if offspring:
            creatures_to_add.extend(offspring)
        return creature, creatures_to_add
    eyesight = get_eyesight(creature)
    foods_in_eyesight = get_foods_in_eyesight(creature, eyesight)
    if len(foods_in_eyesight) != 0:
        target_food = choice(foods_in_eyesight)
        number_of_moves = get_speed(creature)
        creature = move_towards_food(creature, target_food, number_of_moves)
    else:
        number_of_moves = get_speed(creature)
        creature = move_random(creature, number_of_moves)
    return creature, creatures_to_add

def simulate_food():
    from constants import FOOD_CAP
    amount_of_food_to_generate = max(0, FOOD_CAP - len(foods))
    while amount_of_food_to_generate > 0:
        create_food()
        amount_of_food_to_generate -= 1
