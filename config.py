"""
Configuration constants for the Honey Agent.
Change these to experiment with different learning behaviors.
"""

# === ENVIRONMENT ===
GRID_SIZE = 5                   # Size of the training grid (5x5 = 25 cells)

# === TRAINING ===
EPISODES = 100000               # Total training episodes (full runs through the world)
MAX_STEPS_PER_EPISODE = 200     # Max steps per episode (prevents infinite loops)
LEARNING_RATE = 0.001           # How fast the neural network learns (lower = more stable)
GAMMA = 0.95                    # Discount factor (how much future rewards matter: 0-1)

# === EXPLORATION ===
EPSILON_START = 1.0             # Start at 100% random (full exploration)
EPSILON_END = 0.05              # End at 5% random (mostly exploitation)
EPSILON_DECAY = 0.995           # Decay rate per episode (how fast we shift from explore to exploit)

# === LOGGING ===
PROGRESS_PRINT_EVERY = 10       # Print heartbeat/progress every N episodes
CHECKPOINT_EVERY = 200          # Save model every N episodes

# === ACTIONS ===
# Format: (dx, dy) where x is horizontal (0-4 left to right), y is vertical (0-4 top to bottom)
ACTIONS = [
    (0, -1),  # 0: up
    (0, 1),   # 1: down
    (-1, 0),  # 2: left
    (1, 0),   # 3: right
    (0, 0)    # 4: stay
]
NUM_ACTIONS = len(ACTIONS)

# === STATE ENCODING ===
# State consists of:
# - Flattened grid (GRID_SIZE * GRID_SIZE = 25 values)
# - 4-direction vision (north, south, west, east = 4 values)
STATE_SIZE = GRID_SIZE * GRID_SIZE + 4

# === REWARD STRUCTURE ===
REWARD_FOOD = 1.0              # Reward for eating food (positive terminal reward)
REWARD_POISON = -1.0           # Penalty for eating poison (negative terminal reward)
REWARD_WALL = -0.2             # Penalty for hitting wall (negative terminal reward)
REWARD_LIVING = -0.01          # Small living cost per step (encourages shorter paths)
