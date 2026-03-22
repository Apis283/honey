import tensorflow as tf
import numpy as np
import json
import os
import random
import time

# CONFIG --- Change these to experiment!
GRID_SIZE = 5                   # GRID SIZE
EPISODES = 5000                 # NUMBER OF "LIVES"/EPISODES TO RUN
MAX_STEPS_PER_EPISODE = 200     # PREVENTS INFINATE LOOPS
LEARNING_RATE = 0.001           # HOW FAST NURAL NET LEARNS, SLOWER MEANS MORE STABLE
GAMMA = 0.95                    # HOW MUCH FUTURE REWARDS MATTER
EPSILON_START = 1.0             # STARTS AT 100% RANDOM, (EXPLORATION)
EPSILON_END = 0.05              # ENDS AT 5% RANDOM
EPSILON_DECAY = 0.995           # HOW FAST EXPLORATION DECAYS
