# Honey Agent Learning Guide

This guide is built for the modular implementation started from `main.py`.

## 1) Mental Model

The agent is a small Deep Q-Learning setup:

- Environment: a `GRID_SIZE x GRID_SIZE` grid.
- State: flattened grid + 4-cell local vision (north/south/west/east).
- Actions: up, down, left, right, stay.
- Reward:
  - food: `+1.0`
  - poison: `-1.0`
  - wall hit: `-0.2` and end episode
  - living step: `-0.01`
- Policy: epsilon-greedy over predicted Q-values.

Q-learning update used in code:

$$
Q(s,a) \leftarrow r + \gamma \max_{a'} Q(s',a')
$$

For terminal states (`done=True`), target is just:

$$
Q(s,a) \leftarrow r
$$

## 2) File Walkthrough (Modular)

- Config constants:
  - Define experiment behavior (`EPISODES`, `GAMMA`, `EPSILON_*`, etc.).
- Model:
  - `build_model()` creates a 2-hidden-layer MLP that outputs one Q-value per action.
- World state:
  - Global variables hold `agent_pos`, `food_pos`, `poison_pos`.
- Environment functions:
  - `reset_world()`, `get_state()`, `step(action_idx)`.
- Persistence:
  - `save_state()` and `load_state()` for training resume.
- Training:
  - `train(episodes=EPISODES)` runs online Q-learning and periodic checkpointing.

## 3) Unit Tests You Can Run

Added file: `test_honey.py`

Run:

```bash
python -m unittest -v
```

What these tests validate:

- `reset_world` keeps entities in-bounds and non-overlapping.
- `get_state` shape and encoding semantics.
- `step` reward/done behavior for wall, food, poison.
- Model output dimension matches action space.

## 4) Learn It in 4 Phases

1. Environment only (no neural net)
- Temporarily replace action selection with random actions.
- Log transitions `(s, a, r, s', done)`.

2. Tabular Q-learning baseline
- Replace model with a dict or array Q-table for tiny grids.
- Compare learning speed vs neural version.

3. Current neural online update
- Restore model and single-step `fit` updates.
- Plot reward moving average over episodes.

4. Upgrade architecture
- Add replay buffer.
- Add target network.
- Add evaluation episodes (epsilon=0).

## 5) Rebuild-From-Scratch Checklist

- Create constants and action list.
- Implement `reset_world`, `get_state`, `step`.
- Write tests first for those three functions.
- Add simple random-policy loop.
- Add model and epsilon-greedy action selection.
- Add Bellman target update.
- Add saving/loading.
- Add progress/metrics printing.

If you can complete those steps without looking at the file, you fully own this codebase.

## 6) Immediate Next Improvements

- Add deterministic seeding for reproducibility.
- Add CSV logging of episode reward.
- Move environment logic into a class (reduces global-state bugs).
- Add replay memory and target network for more stable learning.
