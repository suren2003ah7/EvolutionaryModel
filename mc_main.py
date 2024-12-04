import numpy as np
import matplotlib.pyplot as plt
from simulation_service import initialize, initialize_from_gene, simulate_step
from creature_service import creatures, get_eyesight, get_aggression, get_speed, get_strength, get_stamina
import time

# Monte Carlo Parameters
NUM_SIMULATIONS = 100  # Number of Monte Carlo simulations
NUM_STEPS = 60  # Number of steps in each simulation


def visualize_results(simulation_data):
    mean_population = np.mean(simulation_data, axis=0)
    pct20 = np.percentile(simulation_data, 20, axis=0)
    pct40 = np.percentile(simulation_data, 40, axis=0)
    pct60 = np.percentile(simulation_data, 60, axis=0)
    pct80 = np.percentile(simulation_data, 80, axis=0)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(mean_population, label="Mean", color="black", linewidth=2)
    plt.fill_between(range(NUM_STEPS), pct20, pct80, color="blue", alpha=0.3, label="Pct20-Pct80")
    plt.fill_between(range(NUM_STEPS), pct40, pct60, color="blue", alpha=0.5, label="Pct40-Pct60")
    plt.xlabel("Steps")
    plt.ylabel("Population")
    plt.title("Population Dynamics Over Time (Monte Carlo Simulations)")
    plt.legend()
    plt.grid(True)
    plt.show()


def monte_carlo_simulation_with_traits(num_simulations, num_steps):
    all_simulations = []
    time_arr = []
    last_step_trait_data = {"eyesight": [], "aggression": [], "speed": [], "strength": [], "stamina": []}

    try:
        for sim in range(num_simulations):
            start = time.time()
            print(f"Running Simulation {sim + 1}/{num_simulations}")
            initialize_from_gene(0b0101101110001000)  # Reset simulation for each run
            population_counts = []

            for step in range(num_steps):
                simulate_step()
                population_counts.append(len(creatures))  # Track population size

                # Collect traits at the last step of this simulation
                if step == num_steps - 1:
                    for creature in creatures:
                        last_step_trait_data["eyesight"].append(get_eyesight(creature))
                        last_step_trait_data["aggression"].append(get_aggression(creature))
                        last_step_trait_data["speed"].append(get_speed(creature))
                        last_step_trait_data["strength"].append(get_strength(creature))
                        last_step_trait_data["stamina"].append(get_stamina(creature))

            all_simulations.append(population_counts)

            end = time.time()
            time_elapsed = end - start
            time_arr.append(time_elapsed)
            print(f"Time Elapsed: {time_elapsed}")
    except KeyboardInterrupt:
        print("Keyboard Interrupted, Saving Data so far.")

    return np.array(all_simulations), last_step_trait_data, np.array(time_arr)


def visualize_relative_frequencies(trait_data):
    traits = ["eyesight", "aggression", "speed", "strength", "stamina"]

    for trait in traits:
        # Calculate absolute and relative frequencies across all simulations
        unique_values, counts = np.unique(trait_data[trait], return_counts=True)
        total_creatures = sum(counts)
        relative_freqs = counts / total_creatures

        # Create a bar plot for relative frequencies
        plt.figure(figsize=(10, 6))
        plt.bar(unique_values, relative_freqs, color="blue", alpha=0.75, edgecolor="black")
        plt.title(f"Relative Frequency of {trait.capitalize()}", fontsize=16)
        plt.xlabel(trait.capitalize(), fontsize=14)
        plt.ylabel("Relative Frequency", fontsize=14)
        plt.xticks(unique_values, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # Show the plot
        plt.tight_layout()
        plt.show()


# Run Monte Carlo simulations
simulation_data, trait_data, time_arr = monte_carlo_simulation_with_traits(NUM_SIMULATIONS, NUM_STEPS)

print(f"Average Running Time: {np.mean(time_arr)}")
print(f"Running Time Variance: {np.var(time_arr)}")

# Visualize the population dynamics
visualize_results(simulation_data)

# Visualize the trait distributions
visualize_relative_frequencies(trait_data)

# TODO: ADD 95, 5 percentiles as well
