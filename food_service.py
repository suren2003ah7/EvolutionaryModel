from random import randint

foods = []

def create_food():
    foods.append(randint(0, 2**12 - 1))