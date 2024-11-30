from constants import NUMBER_OF_STEPS
from drawer import animate_simulation
from creature_service import creatures
from food_service import foods
from simulation_service import initialize, simulate_step

import time

initialize()

simulation_data = []

step = 0
while step < NUMBER_OF_STEPS:
    start = time.time()
    simulate_step()
    simulation_data.append([creatures.copy(), foods.copy()])
    step += 1
    end = time.time()
    print(f"Step {step}: Time {end - start}")
    print(simulation_data[step - 1])

# animate_simulation(simulation_data)
