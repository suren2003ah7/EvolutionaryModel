import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from grid_service import get_creature_position, get_food_position
from constants import GRID_SIZE

def animate_simulation(simulation_data):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(0, GRID_SIZE)
    ax.set_ylim(0, GRID_SIZE)
    scat_creatures = ax.scatter([], [], c='blue', s=20, label='Creatures')
    scat_foods = ax.scatter([], [], c='green', s=10, label='Foods')
    ax.legend()
    ax.set_title('Simulation Over Time')
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.grid(True)

    def update(frame):
        creatures, foods = simulation_data[frame]
        x_creatures = []
        y_creatures = []
        for creature in creatures:
            x, y = get_creature_position(creature)
            x_creatures.append(x)
            y_creatures.append(y)
        x_foods = []
        y_foods = []
        for food in foods:
            x, y = get_food_position(food)
            x_foods.append(x)
            y_foods.append(y)
        scat_creatures.set_offsets(list(zip(x_creatures, y_creatures)))
        scat_foods.set_offsets(list(zip(x_foods, y_foods)))
        ax.set_title(f'Simulation at Step {frame+1}')
        return scat_creatures, scat_foods

    ani = FuncAnimation(fig, update, frames=len(simulation_data), blit=True, interval=50)
    plt.show()
