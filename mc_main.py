import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from simulation_service import initialize, initialize_from_gene, simulate_step
from creature_service import creatures, get_eyesight, get_aggression, get_speed, get_strength, get_stamina
import time

# Monte Carlo Parameters
NUM_SIMULATIONS = 100  # Number of Monte Carlo simulations
NUM_STEPS = 20  # Number of steps in each simulation


def visualize_results1(simulation_data):
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


def visualize_results2(simulation_data):
    mean_population = np.mean(simulation_data, axis=0)
    pct003 = np.percentile(simulation_data, 0.03, axis=0)
    pct5 = np.percentile(simulation_data, 5, axis=0)
    pct32 = np.percentile(simulation_data, 32, axis=0)
    pct68 = np.percentile(simulation_data, 68, axis=0)
    pct95 = np.percentile(simulation_data, 95, axis=0)
    pct997 = np.percentile(simulation_data, 99.7, axis=0)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(mean_population, label="Mean", color="black", linewidth=2)
    plt.fill_between(range(NUM_STEPS), pct003, pct997, color="blue", alpha=0.2, label="Pct0.03-Pct99.7")
    plt.fill_between(range(NUM_STEPS), pct5, pct95, color="blue", alpha=0.3, label="Pct5-Pct95")
    plt.fill_between(range(NUM_STEPS), pct32, pct68, color="blue", alpha=0.5, label="Pct32-Pct68")
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
            print(f"Time Elapsed: {time_elapsed:.2f} seconds")
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


def classify_survival(trait_data):
    """
    Dummy classifier based on a simple rule.
    For illustration purposes, let's assume creatures with speed > median_speed survive.
    """
    df = pd.DataFrame(trait_data)
    median_speed = df['speed'].median()

    # Actual labels: Let's assume all creatures in the simulation survived (1)
    # Modify this according to your simulation's logic
    y_true = np.ones(len(df))  # Replace with actual survival data if available

    # Predicted labels based on speed
    y_pred = (df['speed'] > median_speed).astype(int)

    return y_true, y_pred


def plot_confusion_matrix_plot(y_true, y_pred, classes=['Survived', 'Did Not Survive']):
    """
    Plots the confusion matrix using sklearn's ConfusionMatrixDisplay.
    """
    cm = confusion_matrix(y_true, y_pred)
    cm_display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)

    fig, ax = plt.subplots(figsize=(6, 6))
    cm_display.plot(cmap='Blues', ax=ax)
    plt.title("Confusion Matrix: Survival Classification")
    plt.show()


def bin_traits(trait_data):
    """
    Bins numerical traits into categorical bins.
    """
    df = pd.DataFrame(trait_data)

    # Example: Binning 'eyesight' into 'Low', 'Medium', 'High'
    df['eyesight_bin'] = pd.cut(df['eyesight'], bins=3, labels=['Low', 'Medium', 'High'])

    # Similarly, bin 'aggression' into categories
    df['aggression_bin'] = pd.cut(df['aggression'], bins=3, labels=['Low', 'Medium', 'High'])

    return df


def plot_trait_confusion_matrix(df, trait1, trait2):
    """
    Plots a confusion matrix-like cross-tabulation between two categorical traits.
    """
    cm = pd.crosstab(df[trait1], df[trait2])

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f"Confusion Matrix between {trait1} and {trait2}")
    plt.xlabel(trait2)
    plt.ylabel(trait1)
    plt.show()


def perform_correlation_analysis(trait_data):
    """
    Perform correlation analysis on the trait data and visualize the correlation matrix.

    Parameters:
    - trait_data (dict): Dictionary containing lists of trait values.

    Returns:
    - corr_matrix (pd.DataFrame): DataFrame containing the correlation coefficients.
    """
    df = pd.DataFrame(trait_data)

    # Compute Pearson correlation matrix
    corr_matrix = df.corr(method='pearson')

    # Plot the correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=.5)
    plt.title("Correlation Matrix of Creature Traits", fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

    return corr_matrix


simulation_data, trait_data, time_arr = monte_carlo_simulation_with_traits(NUM_SIMULATIONS, NUM_STEPS)

print(f"Average Running Time: {np.mean(time_arr):.2f} seconds")
print(f"Running Time Variance: {np.var(time_arr):.2f} seconds²")

visualize_results2(simulation_data)
visualize_relative_frequencies(trait_data)

df_binned = bin_traits(trait_data)
plot_trait_confusion_matrix(df_binned, 'eyesight_bin', 'aggression_bin')

correlation_matrix = perform_correlation_analysis(trait_data)
correlation_matrix.to_csv("trait_correlation_matrix.csv", index=True)
