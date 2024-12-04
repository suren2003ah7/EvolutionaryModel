import time
import pickle  # For saving simulation data
from constants import NUMBER_OF_STEPS
from drawer import animate_simulation
from creature_service import creatures
from food_service import foods
from simulation_service import initialize, simulate_step

# Initialize the simulation
initialize()

simulation_data = []

step = 0
while step < NUMBER_OF_STEPS:
    start = time.time()
    simulate_step()
    # Append the current state of creatures and foods
    simulation_data.append((creatures.copy(), foods.copy()))
    step += 1
    end = time.time()
    print(f"Step {step}: Time {end - start}")

# Save the simulation data to a file
with open("simulation_data.pkl", "wb") as file:
    pickle.dump(simulation_data, file)

# Run the animation
animate_simulation(simulation_data)
