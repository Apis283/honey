"""
Environment module: Handles the world grid, entity positions, and game mechanics.
"""

import random
import numpy as np
from config import GRID_SIZE, ACTIONS, NUM_ACTIONS, REWARD_FOOD, REWARD_POISON, REWARD_WALL, REWARD_LIVING

# Global state variables
agent_pos = None        # [x, y] - agent position
food_pos = None         # [x, y] - food position (goal)
poison_pos = None       # [x, y] - poison position (hazard)


def reset_world(silent=False):
    """
    Generate a fresh episode with random positions for agent, food, and poison.
    Ensures no overlaps.
    
    Args:
        silent (bool): If True, don't print position information
    """
    global agent_pos, food_pos, poison_pos
    
    # Random agent position
    agent_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
    
    # Random food position (must differ from agent)
    food_pos = agent_pos[:]
    while food_pos == agent_pos:
        food_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
    
    # Random poison position (must differ from agent and food)
    poison_pos = agent_pos[:]
    while poison_pos in (agent_pos, food_pos):
        poison_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
    
    if not silent:
        print(f"New world → Agent@{agent_pos} | Food@{food_pos} | Poison@{poison_pos}")


def get_state():
    """
    Encode the current world state as a neural network input vector.
    
    Returns:
        numpy array of shape (1, STATE_SIZE) where STATE_SIZE = 25 + 4
        - First 25 values: flattened grid (1=food, -1=poison, 0=empty)
        - Last 4 values: vision of adjacent cells (north, south, west, east)
    """
    # Build flattened grid representation
    grid = np.zeros((GRID_SIZE, GRID_SIZE))
    grid[food_pos[1], food_pos[0]] = 1      # Mark food with 1
    grid[poison_pos[1], poison_pos[0]] = -1 # Mark poison with -1
    
    flat_grid = grid.flatten()
    
    # Build 4-direction vision (what's directly adjacent to agent)
    x, y = agent_pos
    vision = [
        grid[y - 1, x] if y > 0 else -2,              # north: -2 means out-of-bounds
        grid[y + 1, x] if y < GRID_SIZE - 1 else -2, # south
        grid[y, x - 1] if x > 0 else -2,              # west
        grid[y, x + 1] if x < GRID_SIZE - 1 else -2   # east
    ]
    
    # Concatenate and reshape for model input (1, STATE_SIZE)
    return np.concatenate([flat_grid, vision]).reshape(1, -1)


def step(action_idx):
    """
    Execute one game step: move agent based on action and compute reward.
    
    Args:
        action_idx (int): Index into ACTIONS list (0-4)
    
    Returns:
        (reward, done): 
            reward (float): Immediate reward for this step
            done (bool): Whether episode ended (terminal state)
    """
    global agent_pos
    
    dx, dy = ACTIONS[action_idx]
    new_x = agent_pos[0] + dx
    new_y = agent_pos[1] + dy
    
    reward = REWARD_LIVING  # Base cost of living
    done = False
    
    # Check boundary collision
    if not (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE):
        reward = REWARD_WALL  # Wall collision penalty
        done = True
        # Agent does NOT move (stays in place)
    else:
        # Valid move
        agent_pos = [new_x, new_y]
        
        # Check food collision
        if agent_pos == food_pos:
            reward = REWARD_FOOD
            done = True
            print("Ate food! Yum!")
        
        # Check poison collision
        elif agent_pos == poison_pos:
            reward = REWARD_POISON
            done = True
            print("Ate poison... ouch!")
    
    return reward, done
