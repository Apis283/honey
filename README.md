# Honey Agent: Complete Learning Guide

A machine learning project where an AI agent learns to navigate a grid, find food, and avoid poison using **Deep Q-Learning**—a foundational reinforcement learning algorithm.

---

## Table of Contents

1. [What Is This Project?](#what-is-this-project)
2. [Core Concepts: Q-Learning in Plain English](#core-concepts-q-learning-in-plain-english)
3. [How the Honey Agent Works](#how-the-honey-agent-works)
4. [Project Structure](#project-structure)
5. [How to Run the Agent](#how-to-run-the-agent)
6. [Understanding the Code](#understanding-the-code)
7. [How to Modify It](#how-to-modify-it)
8. [Rebuilding From Scratch](#rebuilding-from-scratch)
9. [Next Improvements](#next-improvements)

---

## What Is This Project?

The **Honey Agent** is a small, self-contained machine learning project that trains an AI to:

- Navigate a 5×5 grid.
- Find and "eat" food (goal: +1 reward).
- Avoid and not eat poison (hazard: -1 reward).
- Learn through trial and error (reinforcement learning).

**Why is it called Honey Agent?** Because bees search for honey (food) and avoid poison—a natural metaphor for reward-seeking behavior.

The agent uses a **neural network** to predict which action (move up/down/left/right/stay) is best in any situation. Over 100,000 episodes of training, it learns to find food faster and avoid poison.

---

## Core Concepts: Q-Learning in Plain English

### The Learning Problem

Imagine you're in a maze:
- You can move up, down, left, right, or stay.
- You get +1 reward if you find treasure.
- You get -1 reward if you hit a monster.
- You get -0.01 reward for each step (time cost).

**How do you learn the best path?** Trial and error. You try random moves, remember what worked, and do more of that.

### The Q-Learning Idea

**Q-value** = estimate of "how good is action A from state S?"

Instead of memorizing every possible state (impossible for complex problems), we use a **neural network** to predict Q-values.

**Formula** (the Bellman equation):

$$
Q(s,a) \leftarrow r + \gamma \cdot \max_{a'} Q(s', a')
$$

In English:
- $r$ = immediate reward (what you got now)
- $\gamma$ (gamma) = discount factor (how much to care about future rewards: 0.95 = 95% care about future)
- $\max_{a'} Q(s', a')$ = best Q-value from the next state (estimated future reward)

**Example:**
- Current state: Agent sees food to the right.
- Action: Move right.
- Immediate reward: +1 (found food!).
- Target Q-value: $1.0 + 0.95 \cdot 0 = 1.0$
  - (Episode ends, so no future reward.)

### Exploration vs. Exploitation

The agent needs to balance two urges:

1. **Exploration**: Try random actions to discover new things.
2. **Exploitation**: Use what you already know works.

**Strategy: Epsilon-Greedy**
- 80% of the time: pick the best known action (exploit).
- 20% of the time: pick a random action (explore).

Over time, epsilon (exploration rate) decreases so the agent exploits more.

In our code: `EPSILON_START = 1.0, EPSILON_END = 0.05, EPSILON_DECAY = 0.995`
- Start at 100% random.
- Decrease by 0.5% each episode.
- End at 5% random.

---

## How the Honey Agent Works

### 1. The World (Environment)

**Grid Size:** 5×5 (25 cells)  
**Entities:**
- **Agent** (green square): starts at random position
- **Food** (blue square): goal, gives +1 reward
- **Poison** (red square): hazard, gives -1 reward

```
5 x [Food]  [ ]     [ ]     [ ]     [ ]
4 [ ]       [ ]     [ ]     [Poison][ ]
3 [ ]       [ ]     [ ]     [ ]     [ ]
2 [ ]       [Agent] [ ]     [ ]     [ ]
1 [ ]       [ ]     [ ]     [ ]     [ ]
    0       1       2       3       4
```

### 2. State Representation

The agent perceives the world as a vector of 25 + 4 = 29 numbers:

**Grid (25 numbers):**
- 1 if that cell contains food
- -1 if that cell contains poison
- 0 if that cell is empty

**Local Vision (4 numbers):**
- What's directly north of the agent
- What's directly south
- What's directly west
- What's directly east
- (-2 means out-of-bounds/wall)

```python
state = [grid_cell_0, grid_cell_1, ..., grid_cell_24, north, south, west, east]
```

### 3. Actions

5 possible actions at each step:

```
0: Move up     (0, -1)
1: Move down   (0, +1)
2: Move left   (-1, 0)
3: Move right  (+1, 0)
4: Stay        (0, 0)
```

### 4. Rewards

```
Food:     +1.0 (terminal: episode ends)
Poison:   -1.0 (terminal: episode ends)
Wall hit: -0.2 (terminal: episode ends)
Living:   -0.01 (per step, encourages faster paths)
```

### 5. Neural Network

```
Input: 29 numbers (state)
    ↓
Dense 32 (ReLU activation) — learn patterns
    ↓
Dense 16 (ReLU activation) — learn abstractions
    ↓
Output: 5 numbers (Q-values for each action)
```

The network learns to predict: "From this state, how good is each action?"

### 6. Training Loop (Simplified)

```
For each of 100,000 episodes:
  1. Reset world (random positions)
  2. Get current state
  
  For each step (up to 200 steps):
    a. Epsilon-greedy action selection
    b. Take action → get reward & next state
    c. Compute target Q-value (Bellman equation)
    d. Train network to predict target (via MSE loss)
    
  Decay epsilon (explore less, exploit more)
  Each 200 episodes: save model
```

---

## Project Structure

### Files

```
honey/
├── config.py              # All constants (grid size, learning rates, etc.)
├── environment.py         # World mechanics (reset, get_state, step)
├── model.py              # Neural network (build_model)
├── main.py               # Supported entry point
├── persistence.py        # Save/load state
├── train.py              # Training loop (train function)
├── test_honey.py         # Unit tests
├── AGENT_LEARNING_GUIDE.md  # Quick reference
└── honey-Legacy.py       # Legacy compatibility script (not recommended)
```

### Key Design Principles

1. **Modularity**: Each file has a single responsibility.
2. **Config-driven**: All hyperparameters in `config.py`.
3. **Stateless functions**: Easier to test and reason about.
4. **Global state**: `agent_pos`, `food_pos`, etc., in `environment.py` (simplified for learning).

---

## How to Run the Agent

### 1. Train the Agent

```powershell
cd c:\Users\Adam\OneDrive\Desktop\Techy\ stuff\Python\honey
c:/python313/python.exe train.py
```

**What happens:**
- Loads previous model and world state (if they exist).
- Runs training for 100,000 episodes.
- Saves checkpoint every 200 episodes.
- Prints progress every 10 episodes.
- Final save and notification on completion.

**Console output example:**
```
Episode 0 | Epsilon: 1.000
New world → Agent@[2, 1] | Food@[4, 4] | Poison@[1, 1]
Episode 5 | Epsilon: 0.975
  → Average reward (last 50 episodes): -0.234
[...]
Training complete after 100000 episodes in 1234.5s. State saved.
```

### 2. Train for Fewer Episodes (Quick Test)

Create a quick test script `train_quick.py`:

```python
#!/usr/bin/env python3
from train import train, notify_completion

result = train(episodes=100, verbose=True)
notify_completion(f"Quick train done: {result['episodes_ran']} episodes in {result['elapsed_seconds']:.1f}s")
```

Run:
```powershell
c:/python313/python.exe train_quick.py
```

### 3. Run Unit Tests

```powershell
c:/python313/python.exe -m unittest discover -v
```

Tests:
- Verify world reset produces valid positions
- Check state encoding shape and semantics
- Test reward logic for food/poison/walls
- Test neural network output shape

---

## Understanding the Code

### Layer 1: Environment (Read This First)

File: `environment.py`

**Functions:**
- `reset_world()` — Place agent, food, poison randomly (no overlaps)
- `get_state()` — Render world as 29-number vector
- `step(action_idx)` — Move agent, compute reward, check terminal conditions

**Key insight:** The environment is a pure function (ignoring global state). Given agent/food/poison positions, it deterministically produces state and rewards.

**Exercise:**
```python
from environment import reset_world, get_state, step

reset_world()
state1 = get_state()
reward, done = step(3)  # Move right
state2 = get_state()

print(state1.shape)  # Should be (1, 29)
print(reward)        # -0.01 to 1.0 depending on what happened
print(done)          # True if terminal, False otherwise
```

### Layer 2: Model (Read Next)

File: `model.py`

**Function:**
- `build_model()` — Create the neural network

**Key insight:** The model is just a function approximator. Input state, output Q-values for 5 actions.

**Questions:**
1. Why 32 and 16 hidden units? (Trial and error; could experiment)
2. Why ReLU activation? (Non-linearity to learn complex functions)
3. Why linear output? (Q-values can be any real number, not constrained to [0,1])

**Exercise:**
```python
import numpy as np
from model import build_model

model = build_model()
dummy_state = np.zeros((1, 29))
q_values = model.predict(dummy_state)

print(q_values)        # Shape (1, 5)
print(q_values.shape)  # (1, 5) = 1 batch, 5 actions
```

### Layer 3: Training (The Heart)

File: `train.py`, function `train()`

**High-level pseudo-code:**
```
initialize model and world
epsilon = 1.0

for episode in 100,000:
  reset world
  state = get current world state
  
  for step in 200:
    if random() < epsilon:
      action = random action
    else:
      q_values = model.predict(state)
      action = argmax(q_values)
    
    reward, done = step(action)
    next_state = get current world state
    
    if done:
      target = reward
    else:
      next_q_values = model.predict(next_state)
      target = reward + 0.95 * max(next_q_values)
    
    predict_targets = model.predict(state)
    predict_targets[0][action] = target
    
    model.train_on_batch(state, predict_targets)
    
    state = next_state
    if done: break
  
  epsilon = max(0.05, epsilon * 0.995)
  save every 200 episodes
```

**Key insight:** Each step is a tiny training iteration. The model learns online (one sample at a time), not batched.

### Layer 4: Persistence

File: `persistence.py`

- `save_state()` — Dump model weights to `.keras` file, positions to `.json`
- `load_state()` — Restore from disk if files exist

Allows training to resume where it left off.

---

## How to Modify It

### Experiment 1: Change Reward Structure

Edit `config.py`:

```python
REWARD_FOOD = 2.0        # Make food more valuable
REWARD_LIVING = -0.05    # Higher living cost = shorter paths preferred
REWARD_WALL = -0.5       # Harsher wall penalty
```

Rerun training and note changes in learning speed.

### Experiment 2: Change Exploration Strategy

Edit `config.py`:

```python
EPSILON_START = 0.5      # Start with 50% random (less exploring)
EPSILON_DECAY = 0.99     # Faster decay to exploitation
```

**Prediction:** Agent will converge faster but might get stuck in local optima.

### Experiment 3: Bigger Network

Edit `model.py`:

```python
def build_model():
    model = tf.keras.Sequential([
        tf.keras.Input(shape=(STATE_SIZE,)),
        tf.keras.layers.Dense(64, activation='relu'),  # Bigger
        tf.keras.layers.Dense(32, activation='relu'),  # Bigger
        tf.keras.layers.Dense(NUM_ACTIONS, activation='linear')
    ])
    # ... rest same ...
```

**Prediction:** More expressive, but slower training and risk of overfitting on this tiny domain.

### Experiment 4: Larger Grid

Edit `config.py`:

```python
GRID_SIZE = 10  # 10x10 instead of 5x5
```

Then in `config.py`, update `STATE_SIZE`:

```python
STATE_SIZE = GRID_SIZE * GRID_SIZE + 4  # Now 100 + 4 = 104
```

**Prediction:** Much harder problem; may need more training or bigger network.

### Experiment 5: Add a Second Poison

Edit `environment.py`, add global:

```python
poison2_pos = None
```

Update `reset_world()`, `get_state()`, `step()` to handle it.

---

## Rebuilding From Scratch

If you want to fully own this codebase, rebuild it from memory using this checklist:

### Phase 1: Bare Environment (No Neural Net)

- [ ] Create `config.py` with grid size, action list, reward values.
- [ ] Create `environment.py`:
  - [ ] `reset_world()` — random, non-overlapping positions
  - [ ] `get_state()` — flatten grid + 4-direction vision
  - [ ] `step(action_idx)` — move, compute reward, check terminal
- [ ] Write tests for all three functions.
- [ ] Test with random action selection loop (no learning).

### Phase 2: Add Neural Network

- [ ] Create `model.py`:
  - [ ] `build_model()` — INPUT(29) → Dense32(relu) → Dense16(relu) → OUTPUT(5)
  - [ ] Compile with Adam optimizer and MSE loss.
- [ ] Test that model takes state and outputs Q-values.

### Phase 3: Basic Training Loop

- [ ] Create `train.py`:
  - [ ] Initialize model and world.
  - [ ] For N episodes:
    - [ ] Reset world.
    - [ ] For M steps:
      - [ ] Epsilon-greedy action selection.
      - [ ] Take action, get reward.
      - [ ] Compute Bellman target.
      - [ ] Train network on (state, targets).
    - [ ] Decay epsilon.

### Phase 4: Persistence & Polish

- [ ] Create `persistence.py`:
  - [ ] `save_state()` — model + world positions.
  - [ ] `load_state()` — restore if files exist.
- [ ] Add progress printing (episodes, reward moving average).
- [ ] Add checkpoint saving.

### Phase 5: Tests

- [ ] Write unit tests in `test_*.py`.
- [ ] Verify core functions work as expected.
- [ ] Run end-to-end training for 100 episodes.

---

## Next Improvements

### Immediate (Low Effort, High Impact)

1. **Replace global state with a class:**
   ```python
   class HoneyEnvironment:
       def __init__(self, grid_size):
           self.grid_size = grid_size
           self.agent_pos = None
           self.food_pos = None
           self.poison_pos = None
       
       def reset_world(self):
           # ...
       
       def get_state(self):
           # ...
   ```
   Eliminates global state bugs.

2. **Add logging to CSV:**
   ```python
   import csv
   with open('training_log.csv', 'w') as f:
       writer = csv.writer(f)
       writer.writerow(['episode', 'reward', 'steps', 'epsilon'])
       for episode, reward, steps, epsilon in ...:
           writer.writerow([...])
   ```
   Plot reward over time with matplotlib.

3. **Add command-line arguments:**
   ```python
   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument('--episodes', type=int, default=100000)
   parser.add_argument('--grid-size', type=int, default=5)
   args = parser.parse_args()
   ```

### Intermediate (Moderate Effort)

4. **Experience Replay Buffer:**
   - Store the last N transitions (state, action, reward, next_state).
   - Sample random batches for training (instead of online updates).
   - **Benefit:** More stable learning, reuse data.

5. **Target Network:**
   - Maintain two models: online (learns) and target (computes future reward).
   - Update target network every K steps.
   - **Benefit:** Reduces oscillations in target computation.

6. **Dueling Architecture:**
   - Split network into value stream (V) and advantage stream (A).
   - Q = V + (A - mean(A))
   - **Benefit:** More stable learning on large action spaces.

### Advanced (High Effort)

7. **Policy Gradient Methods (Actor-Critic):**
   - Learn policy π(action|state) directly (not via Q-values).
   - **Benefit:** Natural for continuous actions, handles non-stationary environments.

8. **Multi-Agent:**
   - Two agents competing for food.
   - **Benefit:** Game theory, emergent behavior.

9. **Vision Encoding:**
   - Instead of grid encoding, use image (5×5 RGB grid).
   - Use convolutional layers to process.
   - **Benefit:** Scales to larger images, more realistic perception.

10. **Curriculum Learning:**
    - Start with easy (close food), gradually make harder.
    - **Benefit:** Faster learning, avoids local optima.

---

## Debugging & Tips

### The Agent Isn't Learning

**Signs:** Episode reward stays near -0.01 (random behavior).

**Diagnostics:**
1. Check that `model.predict()` output varies.
2. Print Q-values: `q_values = model.predict(state); print(q_values[0])`
3. Check reward structure: `print(reward)` after each step.
4. Verify state changes: `print(np.sum(state))` between steps.

**Fixes:**
- Increase `LEARNING_RATE` (0.001 → 0.01).
- Decrease `EPSILON_DECAY` (0.995 → 0.99) for more exploration.
- Check that rewards are non-zero and diverse.

### Training Is Too Slow

**Cause:** Online learning (one sample per step) is slow.

**Fixes:**
1. Use replay buffer (batch training).
2. Reduce `MAX_STEPS_PER_EPISODE` (but don't nerf agent).
3. Reduce network size (fewer hidden units).
4. Reduce `EPISODES` for testing.

### Reward Is Very Negative

**Sign:** Moving around randomly without finding food.

**Causes:**
1. `REWARD_LIVING` too harsh.
2. Grid too large, food too hard to find.
3. Epsilon not decaying properly (still exploring too much).

**Fix:** Print world state and visually inspect positions.

### Agent Gets Stuck in Loops

**Sign:** Always moves in the same direction repeatedly.

**Cause:** Exploitation without enough prior exploration.

**Fix:**
- Increase `EPSILON_START` (1.0 → higher? already max).
- Increase `MAX_STEPS_PER_EPISODE` (200 → 500) to allow more discovery.
- Add `REWARD_REPETITION` penalty for repeating actions.

---

## Summary

You now have a clean, modular, well-tested Q-learning agent. Use it to:

1. **Learn**: Read each module in order (environment → model → train).
2. **Experiment**: Tweak config values and observe effects.
3. **Extend**: Add replay buffer, target network, new rewards, etc.
4. **Rebuild**: Code from scratch using the checklist to solidify understanding.

This is a multi-year project—there's no rush. Enjoy the journey! 🐝
