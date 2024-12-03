import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.widgets import Button
from constants import GRID_SIZE
from grid_service import get_creature_position, get_food_position


def animate_simulation(simulation_data, interval=200):
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.subplots_adjust(bottom=0.2)
    ax.set_xlim(0, GRID_SIZE)
    ax.set_ylim(0, GRID_SIZE)
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.grid(True)

    # Initialize scatter plots
    scat_creatures = ax.scatter([], [], c='blue', s=20, label='Creatures')
    scat_foods = ax.scatter([], [], c='green', s=10, label='Food')
    ax.legend(loc='upper right')

    is_paused = False

    def init():
        scat_creatures.set_offsets(np.empty((0, 2)))
        scat_foods.set_offsets(np.empty((0, 2)))
        return scat_creatures, scat_foods

    def update_frame(frame):
        creatures, foods_list = simulation_data[frame]

        # Extract creature positions
        x_creatures = [get_creature_position(creature)[0] for creature in creatures]
        y_creatures = [get_creature_position(creature)[1] for creature in creatures]

        # Extract food positions
        x_foods = [get_food_position(food)[0] for food in foods_list]
        y_foods = [get_food_position(food)[1] for food in foods_list]

        # Prepare offsets for creatures
        if x_creatures and y_creatures:
            creature_offsets = np.column_stack((x_creatures, y_creatures))
        else:
            creature_offsets = np.empty((0, 2))

        # Prepare offsets for foods
        if x_foods and y_foods:
            food_offsets = np.column_stack((x_foods, y_foods))
        else:
            food_offsets = np.empty((0, 2))

        # Update scatter plots
        scat_creatures.set_offsets(creature_offsets)
        scat_foods.set_offsets(food_offsets)

        return scat_creatures, scat_foods

    ani = animation.FuncAnimation(
        fig,
        update_frame,
        frames=len(simulation_data),
        init_func=init,
        blit=True,
        interval=interval,
        repeat=False
    )

    def on_pause(event):
        nonlocal is_paused
        if is_paused:
            ani.event_source.start()
            pause_button.label.set_text('Pause')
        else:
            ani.event_source.stop()
            pause_button.label.set_text('Play')
        is_paused = not is_paused

    def on_restart(event):
        ani.event_source.stop()
        ani.frame_seq = ani.new_frame_seq()
        ani.event_source.start()
        if is_paused:
            on_pause(event)

    # Pause Button
    ax_pause = plt.axes([0.3, 0.05, 0.1, 0.075])
    pause_button = Button(ax_pause, 'Pause')
    pause_button.on_clicked(on_pause)

    # Restart Button
    ax_restart = plt.axes([0.6, 0.05, 0.1, 0.075])
    restart_button = Button(ax_restart, 'Restart')
    restart_button.on_clicked(on_restart)

    plt.show()
