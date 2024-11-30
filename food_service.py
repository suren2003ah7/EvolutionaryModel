from random import randint

foods = []

def create_food():
    food = randint(0, 2**12 - 1)
    foods.append(food)
