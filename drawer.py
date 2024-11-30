import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from constants import GRID_SIZE
from grid_service import get_creature_position, get_food_position

def animate_simulation(simulation_data):
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.subplots_adjust(bottom=0.2)  # Make space for the slider
    ax.set_xlim(0, GRID_SIZE)
    ax.set_ylim(0, GRID_SIZE)
    scat_creatures = ax.scatter([], [], c='blue', s=20)
    scat_foods = ax.scatter([], [], c='green', s=10)
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.grid(True)

    # Create the slider
    ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
    slider = Slider(ax_slider, 'Step', 1, len(simulation_data), valinit=1, valstep=1)

    def update(val):
        frame = int(slider.val) - 1  # Adjust for zero-based index
        creatures, foods_list = simulation_data[frame]
        x_creatures = []
        y_creatures = []
        for creature in creatures:
            x, y = get_creature_position(creature)
            x_creatures.append(x)
            y_creatures.append(y)
        x_foods = []
        y_foods = []
        for food in foods_list:
            x, y = get_food_position(food)
            x_foods.append(x)
            y_foods.append(y)
        scat_creatures.set_offsets(list(zip(x_creatures, y_creatures)))
        scat_foods.set_offsets(list(zip(x_foods, y_foods)))
        fig.canvas.draw_idle()

    slider.on_changed(update)
    update(1)  # Initialize with the first frame
    plt.show()
