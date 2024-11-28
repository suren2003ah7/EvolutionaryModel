from constants import NUMBER_OF_STEPS
from drawer import animate_simulation
from creature_service import creatures
from food_service import foods
from simulation_service import initialize, simulate_step

initialize()

simulation_data = []

step = 0
while step < NUMBER_OF_STEPS:
    print(step)
    simulate_step()
    simulation_data.append((creatures.copy(), foods.copy()))
    step += 1

animate_simulation(simulation_data)
