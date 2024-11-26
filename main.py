from constants import NUMBER_OF_STEPS
from drawer import draw
from creature_service import creatures
from simulation_service import initialize, simulate_step

initialize()

step = 0
while step < NUMBER_OF_STEPS:
    simulate_step()
    step += 1

draw(creatures)