import numpy as np
import matplotlib.pyplot as plt

"""
    lets say 16 bit 0000000000000000
    
    Grid Environment
    Movement directions: only horizontal and vertical
    
    Bit management: Starting from the left
    1. Speed - The amount of cells that the boz can move in a single time step.
               2 bits (from 1 to 4 units per time step)
    
    2. Eyesight - The amount of cells that the boz sees at any time.
                  3 bits (from 0 to 7 units)
    
    3. Aggression - The probability that the boz will engage in a battle if possible. Two bozes can engage in a battle if they are in adjacent cells and one of them decided to do so.
                    3 bits (from 0 to 7 units, percent = (value * 100)/(2^(number of bits) - 1))
    
    4. Strength - The physical power unit each boz has.
                  4 bits (from 1 to 16 units)
                  To be discussed: the aggressor has an advantage or no? (+1 strength ??)
                  
    5. Stamina - The modifier which determines the upper bound of the energy level.
                 4 bit (from 1 to 16 units, with some mapping)
"""