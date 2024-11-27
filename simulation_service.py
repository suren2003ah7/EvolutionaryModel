from random import randint, choice
from constants import INITIAL_NUMBER_OF_CREATURES, FOOD_CAP
from creature_service import creatures, create_creature, eat_food, get_eyesight, reproduce_if_possible, is_creature_fighting, fight
from food_service import foods, create_food
from grid_service import get_position_as_12_bit_number, get_neighbours, get_foods_in_eyesight, move_random, move_towards_food

creatures_already_fought_in_current_round = []

def initialize():
    creatures.clear()
    foods.clear()
    for i in range(INITIAL_NUMBER_OF_CREATURES):
        create_creature()
    simulate_food()

def simulate_step():
    creatures_already_fought_in_current_round.clear()
    for creature in creatures:
        if creature in creatures_already_fought_in_current_round:
            continue
        simulate_individual_creature_step(creature)
    simulate_food()

def simulate_individual_creature_step(creature):
    neighbours = get_neighbours(creature)
    if len(neighbours) != 0 and is_creature_fighting(creature):
        target_neighbour = choice(neighbours)
        winner = fight(creature, target_neighbour)
        creatures_already_fought_in_current_round.append(winner)
        reproduce_if_possible(winner)
        return
    if get_position_as_12_bit_number(creature) in foods:
        eat_food(creature)
        foods.remove(get_position_as_12_bit_number(creature))
        reproduce_if_possible(creature)
        return
    foods_in_eyesight = get_foods_in_eyesight(creature, get_eyesight(creature))
    if len(foods_in_eyesight) != 0:
        target_food = foods_in_eyesight[randint(0, len(foods_in_eyesight) - 1)]
        move_towards_food(creature, target_food)
        return
    move_random(creature)

def simulate_food():
    amount_of_food_to_generate = max(0, FOOD_CAP - len(foods))
    while amount_of_food_to_generate > 0:
        create_food()
        amount_of_food_to_generate -= 1