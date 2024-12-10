import os
import sys
import importlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time
from simulation_service import initialize, initialize_from_gene, simulate_step
from creature_service import creatures, get_eyesight, get_aggression, get_speed, get_strength, get_stamina
import constants  # Import the constants module
import logging

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("simulation.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Monte Carlo Parameters
NUM_SIMULATIONS = 100  # Number of Monte Carlo simulations per constants set
NUM_STEPS = 60        # Number of steps in each simulation

# Define Food and Creature Percentages
FOOD_PERCENTAGES = [0.01, 0.03, 0.05, 0.1, 0.2]      # 10%
CREATURE_PERCENTAGES = [0.01, 0.03, 0.05]  # 1%, 10%

# Backup Original Constants
ORIGINAL_CONSTANTS = {
    'GRID_SIZE': constants.GRID_SIZE,
    'FOOD_CAP': constants.FOOD_CAP,
    'INITIAL_NUMBER_OF_CREATURES': constants.INITIAL_NUMBER_OF_CREATURES,
    'NUMBER_OF_STEPS': constants.NUMBER_OF_STEPS,
    'BASE_ENERGY_LEVEL': constants.BASE_ENERGY_LEVEL,
    'ENERGY_GAINED_FROM_EATING_FOOD': constants.ENERGY_GAINED_FROM_EATING_FOOD,
    'ENERGY_GAINED_FROM_EATING_CREATURE': constants.ENERGY_GAINED_FROM_EATING_CREATURE,
    'ENERGY_LOSS_PER_MOVE': constants.ENERGY_LOSS_PER_MOVE,
    'ENERGY_RATIO_REQUIRED_TO_REPRODUCE': constants.ENERGY_RATIO_REQUIRED_TO_REPRODUCE,
    'ENERGY_RATIO_SPENT_TO_REPRODUCE': constants.ENERGY_RATIO_SPENT_TO_REPRODUCE,
    'NUMBER_OF_CHILDREN_PER_REPRODUCTION': constants.NUMBER_OF_CHILDREN_PER_REPRODUCTION,
    'PROBABILITY_OF_INDIVIDUAL_GENOME_MUTATION': constants.PROBABILITY_OF_INDIVIDUAL_GENOME_MUTATION,
    'GENOME_BIT_SIZE': constants.GENOME_BIT_SIZE,
    'ENERGY_LOSS_COEFFICIENT': constants.ENERGY_LOSS_COEFFICIENT,
}

def set_constants(food_pct, creature_pct):
    """
    Dynamically update the constants in constants.py based on the given percentages.

    Parameters:
    - food_pct (float): Percentage for FOOD_CAP (e.g., 0.01 for 1%)
    - creature_pct (float): Percentage for INITIAL_NUMBER_OF_CREATURES (e.g., 0.05 for 5%)
    """
    constants.FOOD_CAP = int(constants.GRID_SIZE ** 2 * food_pct)
    constants.INITIAL_NUMBER_OF_CREATURES = int(constants.GRID_SIZE ** 2 * creature_pct)
    # Update NUMBER_OF_STEPS if it varies per set; currently fixed at 5
    # constants.NUMBER_OF_STEPS = 5  # Uncomment if needed

def reset_constants():
    """
    Reset the constants in constants.py to their original values.
    """
    for key, value in ORIGINAL_CONSTANTS.items():
        setattr(constants, key, value)
    # Reload the constants module to ensure all references are updated
    importlib.reload(constants)

def visualize_results2(simulation_data, save_path):
    """
    Visualizes the population dynamics over time using multiple percentiles.
    Saves the plot to the specified path.
    """
    mean_population = np.mean(simulation_data, axis=0)
    pct003 = np.percentile(simulation_data, 0.3, axis=0)
    pct5 = np.percentile(simulation_data, 5, axis=0)
    pct32 = np.percentile(simulation_data, 32, axis=0)
    pct68 = np.percentile(simulation_data, 68, axis=0)
    pct95 = np.percentile(simulation_data, 95, axis=0)
    pct997 = np.percentile(simulation_data, 99.7, axis=0)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(mean_population, label="Mean", color="black", linewidth=2)
    plt.fill_between(range(NUM_STEPS), pct003, pct997, color="blue", alpha=0.2, label="Pct0.3-Pct99.7")
    plt.fill_between(range(NUM_STEPS), pct5, pct95, color="blue", alpha=0.3, label="Pct5-Pct95")
    plt.fill_between(range(NUM_STEPS), pct32, pct68, color="blue", alpha=0.5, label="Pct32-Pct68")
    plt.xlabel("Steps")
    plt.ylabel("Population")
    plt.title("Population Dynamics Over Time (Monte Carlo Simulations)")
    plt.legend()
    plt.grid(True)

    # Save the plot
    plt.savefig(os.path.join(save_path, "population_dynamics.png"))
    plt.close()

def visualize_relative_frequencies(trait_data, save_path):
    """
    Visualizes the relative frequencies of each trait using bar plots.
    Saves the plots to the specified path.
    """
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

        # Save the plot
        plt.tight_layout()
        plt.savefig(os.path.join(save_path, f"relative_frequency_{trait}.png"))
        plt.close()

def normalize_traits(trait_data):
    """
    Normalizes trait values to a [0, 1] range using Min-Max scaling.

    Parameters:
    - trait_data (dict): Dictionary containing lists of trait values.

    Returns:
    - normalized_df (pd.DataFrame): DataFrame with normalized trait values.
    """
    df = pd.DataFrame(trait_data)
    normalized_df = (df - df.min()) / (df.max() - df.min())
    return normalized_df

def perform_correlation_analysis(normalized_df, save_path):
    """
    Performs correlation analysis on the normalized trait data and visualizes the correlation matrix.
    Saves the plot to the specified path.

    Parameters:
    - normalized_df (pd.DataFrame): DataFrame containing normalized trait values.

    Returns:
    - corr_matrix (pd.DataFrame): DataFrame containing the correlation coefficients.
    """
    # Compute Pearson correlation matrix
    corr_matrix = normalized_df.corr(method='pearson')

    # Plot the correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=.5)
    plt.title("Correlation Matrix of Normalized Creature Traits", fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    # Save the plot
    plt.savefig(os.path.join(save_path, "correlation_matrix.png"))
    plt.close()

    return corr_matrix

def bin_traits(normalized_df):
    """
    Bins numerical traits into categorical bins ('Low', 'Medium', 'High') based on quantiles.

    Binning Logic:
    - 'Low': Below 33rd percentile
    - 'Medium': Between 33rd and 66th percentile
    - 'High': Above 66th percentile

    Parameters:
    - normalized_df (pd.DataFrame): DataFrame containing normalized trait values.

    Returns:
    - df_binned (pd.DataFrame): DataFrame with binned categorical traits.
    """
    df = normalized_df.copy()

    # Define bin edges based on quantiles
    bins = [0, 0.33, 0.66, 1.0]
    labels = ['Low', 'Medium', 'High']

    # Binning each trait
    for trait in normalized_df.columns:
        df[f'{trait}_bin'] = pd.cut(df[trait], bins=bins, labels=labels, include_lowest=True)

    return df

def plot_top_confusion_matrices(normalized_df, df_binned, save_path, threshold=0.3, top_n=5, scale=0.8):
    """
    Plots confusion matrices for the top N trait pairs where at least one cell in the matrix
    exceeds the specified threshold (in ratio format).

    Parameters:
    - normalized_df (pd.DataFrame): DataFrame containing normalized trait values.
    - df_binned (pd.DataFrame): DataFrame with binned categorical traits.
    - save_path (str): Directory to save the confusion matrix plots.
    - threshold (float): Ratio threshold for inclusion.
    - top_n (int): Number of top pairs to display.
    - scale (float): Scaling factor for individual plots (default is 0.8).
    """
    traits = normalized_df.columns
    high_proportion_pairs = []

    # Iterate through all unique trait pairs
    for i in range(len(traits)):
        for j in range(i + 1, len(traits)):
            trait1 = traits[i]
            trait2 = traits[j]

            # Create a confusion matrix (crosstab)
            cm = pd.crosstab(df_binned[f'{trait1}_bin'], df_binned[f'{trait2}_bin'])

            # Calculate ratios
            cm_ratio = cm / cm.sum().sum()

            # Check if any cell's ratio exceeds the threshold
            if (abs(cm_ratio) > threshold).any().any():
                max_ratio = cm_ratio.max().max()
                high_proportion_pairs.append((trait1, trait2, cm_ratio, max_ratio))

    if not high_proportion_pairs:
        logging.info(f"No trait pairs have any cell ratio exceeding {threshold}.")
        return

    # Sort by max ratio and select the top N pairs
    high_proportion_pairs = sorted(high_proportion_pairs, key=lambda x: x[3], reverse=True)[:top_n]

    # Determine the layout for subplots
    num_pairs = len(high_proportion_pairs)
    cols = 2
    rows = (num_pairs + cols - 1) // cols  # Ceiling division

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4 * scale, rows * 4 * scale))

    # Flatten axes to 1D list
    if num_pairs == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for idx, (trait1, trait2, cm_ratio, max_ratio) in enumerate(high_proportion_pairs):
        ax = axes[idx]
        sns.heatmap(
            cm_ratio,
            annot=True,
            fmt=".2f",  # Display ratios
            cmap="coolwarm",  # Heatmap color scheme
            ax=ax,
            cbar=False,
            annot_kws={"size": 8 * scale},  # Adjust annotation font size
        )
        ax.set_title(f"{trait1.capitalize()} vs {trait2.capitalize()}", fontsize=10 * scale)
        ax.set_xlabel(trait2.capitalize(), fontsize=9 * scale)
        ax.set_ylabel(trait1.capitalize(), fontsize=9 * scale)

        # Scale axis labels and ticks
        ax.tick_params(axis="both", labelsize=8 * scale)

    # Remove any empty subplots
    for idx in range(len(high_proportion_pairs), len(axes)):
        fig.delaxes(axes[idx])

    # Adjust layout and save the plot
    plt.tight_layout(pad=2.0 * scale)
    plt.savefig(os.path.join(save_path, "confusion_matrices.png"))
    plt.close()

def monte_carlo_simulation_with_traits(num_simulations, num_steps):
    """
    Runs Monte Carlo simulations, collects population counts and trait data.

    Parameters:
    - num_simulations (int): Number of simulation runs.
    - num_steps (int): Number of steps per simulation.

    Returns:
    - all_simulations (np.ndarray): Population counts across simulations.
    - last_step_trait_data (dict): Collected trait data at the last step.
    - time_arr (np.ndarray): Execution time for each simulation.
    """
    all_simulations = []
    time_arr = []
    last_step_trait_data = {"eyesight": [], "aggression": [], "speed": [], "strength": [], "stamina": []}

    try:
        for sim in range(num_simulations):
            start = time.time()
            logging.info(f"Running Simulation {sim + 1}/{num_simulations}")
            initialize()
            # initialize_from_gene(0b0101101110001000)  # Reset simulation for each run
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
            logging.info(f"Time Elapsed: {time_elapsed:.2f} seconds")
    except KeyboardInterrupt:
        logging.warning("Keyboard Interrupted, Saving Completed Simulation Sets Only.")
        raise  # Re-raise to handle in the outer loop

    return np.array(all_simulations), last_step_trait_data, np.array(time_arr)

def run_simulation_set(set_index, food_pct, creature_pct, base_output_dir):
    """
    Runs a single simulation set with specified food and creature percentages.

    Parameters:
    - set_index (int): Index of the simulation set (for directory naming).
    - food_pct (float): Percentage for FOOD_CAP.
    - creature_pct (float): Percentage for INITIAL_NUMBER_OF_CREATURES.
    - base_output_dir (str): Base directory to save simulation results.
    """
    # Define the simulation set directory with descriptive naming
    simulation_set_dir = os.path.join(
        base_output_dir,
        f"simulation_set_{set_index}_food_{int(food_pct * 100)}%_creature_{int(creature_pct * 100)}%"
    )
    os.makedirs(simulation_set_dir, exist_ok=True)

    try:
        # Update constants
        set_constants(food_pct, creature_pct)

        # Run Monte Carlo simulations
        simulation_data, trait_data, time_arr = monte_carlo_simulation_with_traits(NUM_SIMULATIONS, NUM_STEPS)

        # Save running time statistics
        with open(os.path.join(simulation_set_dir, "running_time.txt"), "w") as f:
            f.write(f"Average Running Time: {np.mean(time_arr):.2f} seconds\n")
            f.write(f"Running Time Variance: {np.var(time_arr):.2f} seconds²\n")

        # Visualize and save the population dynamics
        visualize_results2(simulation_data, simulation_set_dir)

        # Visualize and save the trait distributions
        visualize_relative_frequencies(trait_data, simulation_set_dir)

        # Normalize traits
        normalized_df = normalize_traits(trait_data)

        # Perform Correlation Analysis and save the plot
        perform_correlation_analysis(normalized_df, simulation_set_dir)

        # Save the correlation matrix to a CSV file for further analysis
        correlation_matrix = normalized_df.corr(method='pearson')
        correlation_matrix.to_csv(os.path.join(simulation_set_dir, "trait_correlation_matrix.csv"), index=True)

        # Bin the normalized traits into 'Low', 'Medium', 'High'
        df_binned = bin_traits(normalized_df)

        # Plot confusion matrices for trait pairs with any cell proportion > threshold
        plot_top_confusion_matrices(normalized_df, df_binned, simulation_set_dir, threshold=0.3, top_n=6)

        # Save the binned data for future use
        df_binned.to_csv(os.path.join(simulation_set_dir, "binned_traits.csv"), index=False)

        # Save the constants used in this simulation set after successful completion
        constants_file = os.path.join(simulation_set_dir, "constants.txt")
        with open(constants_file, "w") as f:
            for key, value in ORIGINAL_CONSTANTS.items():
                current_value = getattr(constants, key)
                f.write(f"{key} = {current_value}\n")

        logging.info(
            f"Completed Simulation Set {set_index}: Food {int(food_pct * 100)}%, Creature {int(creature_pct * 100)}%")
    except KeyboardInterrupt:
        logging.warning(f"Simulation Set {set_index} interrupted and not saved.")
        # Attempt to remove the partially created directory to avoid incomplete data
        try:
            import shutil
            shutil.rmtree(simulation_set_dir)
            logging.info(f"Removed incomplete simulation directory: {simulation_set_dir}")
        except Exception as e:
            logging.error(f"Could not remove simulation directory ({simulation_set_dir}): {e}")
        raise  # Re-raise to stop the main loop

# Create a base directory to store all simulation results
base_output_dir = "simulation_results"
random_gene_dir = os.path.join(base_output_dir, "random_gene")
os.makedirs(random_gene_dir, exist_ok=True)  # Create 'random_gene' subdirectory

set_index = 1  # To keep track of simulation set numbering

try:
    for food_pct in FOOD_PERCENTAGES:
        for creature_pct in CREATURE_PERCENTAGES:
            logging.info(
                f"\nStarting Simulation Set {set_index}: Food {int(food_pct * 100)}%, Creature {int(creature_pct * 100)}%")
            try:
                run_simulation_set(set_index, food_pct, creature_pct, random_gene_dir)
                set_index += 1
            except KeyboardInterrupt:
                logging.warning(f"Simulation interrupted during Simulation Set {set_index}.")
                break  # Exit the loop upon interruption
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
finally:
    # Reset constants to original values after all simulations or interruption
    reset_constants()
    logging.info("Constants have been reset to original values.")
