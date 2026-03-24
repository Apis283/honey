import tensorflow as tf
import numpy as np
import json
import os
import random
import time
import sys

# CONFIG --- Change these to experiment!
GRID_SIZE = 5                   # GRID SIZE
EPISODES = 100000                 # NUMBER OF "LIVES"/EPISODES TO RUN
MAX_STEPS_PER_EPISODE = 200     # PREVENTS INFINATE LOOPS
LEARNING_RATE = 0.001           # HOW FAST NURAL NET LEARNS, SLOWER MEANS MORE STABLE
GAMMA = 0.95                    # HOW MUCH FUTURE REWARDS MATTER
EPSILON_START = 1.0             # STARTS AT 100% RANDOM, (EXPLORATION)
EPSILON_END = 0.05              # ENDS AT 5% RANDOM
EPSILON_DECAY = 0.995           # HOW FAST EXPLORATION DECAYS
PROGRESS_PRINT_EVERY = 10       # PRINT HEARTBEAT EVERY N EPISODES


# ACTIONS! 0=up 1=down 2=left 3=right 4=stay
ACTIONS = [(0,-1),(0,1),(-1,0),(1,0),(0,0)]
NUM_ACTIONS = len(ACTIONS)

# STATE! flattened grid (25 cells) + simple 4-direction vision
STATE_SIZE = GRID_SIZE * GRID_SIZE +4

# Global world variables (will be saved/loaded)
agent_pos = None
food_pos = None
poison_pos = None

# === Create or load the neural network ===
def build_model():
    model = tf.keras.Sequential([
        tf.keras.Input(shape=(STATE_SIZE,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(NUM_ACTIONS, activation='linear')  # Q-values for each action
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
                  loss='mse')  # We use mean squared error for Q-learning updates
    return model

model = build_model()

# === Save / Load functions (makes it portable between machines) ===
def save_state():
    model.save('agent_model.keras')  # Modern Keras format, works cross-platform
    with open('world_state.json', 'w') as f:
        json.dump({
            'agent_pos': agent_pos,
            'food_pos': food_pos,
            'poison_pos': poison_pos
        }, f, indent=2)
    print("Saved agent & world.")

def load_state():
    global agent_pos, food_pos, poison_pos, model
    if os.path.exists('agent_model.keras'):
        model = tf.keras.models.load_model('agent_model.keras')
        print("Loaded existing model.")
    if os.path.exists('world_state.json'):
        with open('world_state.json') as f:
            data = json.load(f)
            agent_pos = data['agent_pos']
            food_pos = data['food_pos']
            poison_pos = data['poison_pos']
        print("Loaded existing world.")
    else:
        reset_world()

def notify_completion(message):
    # Terminal bell works on most terminals.
    print("\a", end="")
    print(message)

    # Best effort Windows popup notification.
    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, message, "Honey Training", 0x40)
        except Exception:
            pass

# === Reset world when starting new episode or no save exists ===
def reset_world():
    global agent_pos, food_pos, poison_pos
    agent_pos = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
    # Make sure food & poison aren't on agent
    food_pos = agent_pos[:]
    while food_pos == agent_pos:
        food_pos = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
    poison_pos = agent_pos[:]
    while poison_pos in (agent_pos, food_pos):
        poison_pos = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
    print(f"New world → Agent@{agent_pos} | Food@{food_pos} | Poison@{poison_pos}")

# === Get current state as a vector (for neural net) ===
def get_state():
    # Flatten grid: 0=empty, 1=food, -1=poison, 2=agent (but we don't mark agent anymore)
    grid = np.zeros((GRID_SIZE, GRID_SIZE))
    grid[food_pos[1], food_pos[0]] = 1
    grid[poison_pos[1], poison_pos[0]] = -1

    flat_grid = grid.flatten()

    # Simple 4-direction vision (what's directly adjacent)
    x, y = agent_pos
    vision = [
        grid[y-1, x] if y > 0 else -2,          # north
        grid[y+1, x] if y < GRID_SIZE-1 else -2, # south
        grid[y, x-1] if x > 0 else -2,          # west
        grid[y, x+1] if x < GRID_SIZE-1 else -2  # east
    ]
    return np.concatenate([flat_grid, vision]).reshape(1, -1)  # shape (1, state_size)

# === Execute one action, return reward & done flag ===
def step(action_idx):
    global agent_pos
    dx, dy = ACTIONS[action_idx]
    new_x = agent_pos[0] + dx
    new_y = agent_pos[1] + dy

    reward = -0.01     # Small living cost → encourages faster solutions
    done = False

    if not (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE):
        reward = -0.2  # Wall bump hurts more
        done = True    # End episode on wall hit (optional - can remove)
    else:
        agent_pos = [new_x, new_y]
        if agent_pos == food_pos:
            reward = 1.0
            done = True
            print("Ate food! Yum!")
        elif agent_pos == poison_pos:
            reward = -1.0
            done = True
            print("Ate poison... ouch!")
    
    return reward, done

# === Main training loop ===
def train(episodes=EPISODES):
    load_state()  # Try to resume if files exist

    epsilon = EPSILON_START
    start_time = time.time()
    episode_rewards = []

    completed = False
    last_episode = -1

    try:
        for episode in range(episodes):
            if episode % 50 == 0:
                print(f"\nEpisode {episode} | Epsilon: {epsilon:.3f}")

            reset_world() if episode > 0 else None  # Only reset after first load
            state = get_state()
            total_reward = 0
            step_count = 0

            for step_num in range(MAX_STEPS_PER_EPISODE):
                step_count += 1

                # Epsilon-greedy action selection
                if random.random() < epsilon:
                    action = random.randint(0, NUM_ACTIONS-1)  # Explore
                else:
                    q_values = model.predict(state, verbose=0)[0]
                    action = np.argmax(q_values)  # Exploit

                reward, done = step(action)
                total_reward += reward

                # Get next state
                next_state = get_state()

                # Simple Q-update target: reward + discounted max future reward
                if done:
                    target = reward
                else:
                    next_q = model.predict(next_state, verbose=0)[0]
                    target = reward + GAMMA * np.max(next_q)

                # Prepare targets for training (only update the chosen action)
                targets = model.predict(state, verbose=0)
                targets[0][action] = target

                # Train on this single step (online learning)
                model.fit(state, targets, epochs=1, verbose=0)

                state = next_state

                if done:
                    break

            # Decay exploration
            epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)
            last_episode = episode
            episode_rewards.append(total_reward)

            if episode % 20 == 0:
                print(f"Episode {episode} finished | Reward: {total_reward:.2f} | Steps: {step_count}")

            if (episode + 1) % 50 == 0:
                recent_rewards = episode_rewards[-50:]
                avg_recent_reward = sum(recent_rewards) / len(recent_rewards)
                print(f"Average reward (last {len(recent_rewards)} episodes): {avg_recent_reward:.3f}")

            if episode % PROGRESS_PRINT_EVERY == 0:
                elapsed = time.time() - start_time
                episodes_done = episode + 1
                avg_sec_per_episode = elapsed / episodes_done
                eta_sec = max(0, (episodes - episodes_done) * avg_sec_per_episode)
                print(f"Heartbeat | {episodes_done}/{episodes} episodes | Elapsed: {elapsed:.1f}s | ETA: {eta_sec:.1f}s")

            if episode % 200 == 0:
                save_state()

        completed = True
    finally:
        save_state()
        elapsed_total = time.time() - start_time
        if completed:
            notify_completion(f"Training complete after {episodes} episodes in {elapsed_total:.1f}s. State saved.")
        else:
            notify_completion(f"Training stopped around episode {last_episode + 1}. State saved before exit.")

    return {
        'completed': completed,
        'last_episode': last_episode,
        'episodes_ran': last_episode + 1,
        'epsilon_final': epsilon,
        'elapsed_seconds': time.time() - start_time
    }


if __name__ == '__main__':
    print("[legacy] honey.py is kept for backward compatibility.")
    print("[legacy] Please use 'python main.py' for the supported modular workflow.")
    result = train()
    sys.exit(0 if result['completed'] else 1)