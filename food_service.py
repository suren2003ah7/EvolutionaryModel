from random import randint
from constants import GRID_SIZE

foods = []

def create_food():
    x = randint(0, GRID_SIZE - 1)
    y = randint(0, GRID_SIZE - 1)
    food = (x << 6) | y
    foods.append(food)
