from constants import NUMBER_OF_STEPS
from drawer import draw
from grid_service import generate, simulate_step

grid = generate()

step = 0
while step < NUMBER_OF_STEPS:
    simulate_step(grid)
    step += 1

draw(grid)