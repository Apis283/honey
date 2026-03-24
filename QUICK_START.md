# Quick Start Guide for New Learners

Welcome to the Honey Agent project! This guide gets you up and running in 5 minutes.

## What You Have

A complete, modular Deep Q-Learning agent that learns to navigate a grid, find food, and avoid poison.

## Your First Run (5 Minutes)

### Fastest Option: One Command Per OS

Windows (PowerShell):

```powershell
.\run_windows.ps1 -Episodes 100
```

If script execution is blocked by policy, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_windows.ps1 -Episodes 100
```

Ubuntu:

```bash
bash ./run_ubuntu.sh 100
```

Optional (once):

```bash
chmod +x ./run_ubuntu.sh
./run_ubuntu.sh --episodes 100
```

These scripts create `.venv` if needed, install dependencies, then train.

### Step 0: Create and Activate a Virtual Environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Ubuntu:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Step 1: Train for 100 Episodes (Test Run)

```bash
python main.py --episodes 100
```

**Expected output:**
```
Starting training for 100 episodes...
Episode 0 | Epsilon: 1.000
New world → Agent@[2, 1] | Food@[4, 4] | Poison@[1, 1]
[...progress messages...]
Training Summary:
  Episodes: 100/100
  Time: 45.3 seconds
  Final epsilon: 0.605
  Status: Completed
```

### Step 2: Look at the Code Structure

```
honey/
├── config.py          ← All hyperparameters (grid size, learning rate, etc.)
├── environment.py     ← World mechanics (agent moves, gets state)
├── model.py          ← Neural network (learns Q-values)
├── train.py          ← Training loop (main learning algorithm)
├── persistence.py    ← Save/load trained model
├── main.py           ← Entry point to run training
├── test_honey.py     ← Unit tests
├── README.md         ← Full documentation (READ THIS NEXT!)
└── QUICK_START.md    ← This file
```

### Step 3: Understand the Minimum

Read these in order (15 minutes total):

1. **config.py** — Skim the constants and comments.
2. **README.md → "How the Honey Agent Works"** — 5 min read.
3. **environment.py → Comments** — How the world works.

### Step 4: Run Tests

```bash
python -m unittest test_honey -v
```

You'll see 7 tests that verify agent mechanics work.

### Step 5: Train Longer (Optional)

```bash
python main.py --episodes 10000
```

This takes ~10 minutes. Watch the reward moving average increase (learning!).

Optional scripted runs:

- Windows: `.\run_windows.ps1 -Episodes 10000 -Quiet`
- Ubuntu: `bash ./run_ubuntu.sh --episodes 10000 --quiet`

Script help:

- Windows: `.\run_windows.ps1 -Help`
- Ubuntu: `bash ./run_ubuntu.sh --help`

---

## Next Steps

### 🎯 To Understand the Code Deeply

1. Read [README.md](README.md) fully.
2. Read [AGENT_LEARNING_GUIDE.md](AGENT_LEARNING_GUIDE.md).
3. Run code snippets from README (Learning section).
4. Modify `config.py` values and observe effects.

### 🧪 To Experiment

**Experiment 1: Make food more valuable**
- Edit `config.py`: `REWARD_FOOD = 2.0`
- Run: `python main.py --episodes 500`
- Do you learn faster?

**Experiment 2: Make the grid bigger**
- Edit `config.py`: `GRID_SIZE = 10`
- Run: `python main.py --episodes 1000`
- Much harder? Add more hidden units?

**Experiment 3: Reduce exploration**
- Edit `config.py`: `EPSILON_DECAY = 0.99` (was 0.995)
- Does the agent converge faster?

### 🏗️ To Rebuild From Scratch

Follow [README.md → "Rebuilding From Scratch"](README.md#rebuilding-from-scratch).

This is the best way to truly own the codebase.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'tensorflow'"

Run:
```bash
python -m pip install tensorflow
```

### "No such file or directory: agent_model.keras"

That's normal on first run. The model is created fresh.

### Training is very slow

Add `--quiet` flag to reduce printing overhead:
```bash
python main.py --episodes 10000 --quiet
```

### Nothing is changing (reward stays at -0.01)

The agent is just exploring randomly. This is normal at first. After ~1,000 episodes of training, you should see improvement. If not after 5,000 episodes:

1. Check that reward is not all -0.01 (run `test_honey` to verify step function works).
2. Try increasing `LEARNING_RATE` in `config.py` (0.001 → 0.01).
3. Try decreasing `EPSILON_DECAY` to explore more (0.995 → 0.99).

---

## File Purpose Reference

| File | Purpose |
|------|---------|
| `config.py` | Constants: grid size, learning rates, reward values |
| `environment.py` | World model: positions, state encoding, reward |
| `model.py` | Neural network: build and getter functions |
| `train.py` | Q-learning algorithm: main training loop |
| `persistence.py` | Save/load: keep progress between sessions |
| `main.py` | Entry point: CLI to run training |
| `test_honey.py` | Unit tests: verify environment and model work |
| `README.md` | Full documentation with theory and examples |
| `AGENT_LEARNING_GUIDE.md` | Study guide with rebuild checklist |

---

## Common Questions

**Q: How long does 100,000 episodes take?**  
A: ~30-45 minutes on a modern CPU.

**Q: Should I use the GPU?**  
A: Not required for this small grid, but you can use one. On Windows, official TensorFlow GPU support is via **WSL2 (Ubuntu)**.

Quick setup:

```powershell
# In an elevated PowerShell
wsl --install
```

Then inside Ubuntu (WSL):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
python main.py --episodes 1000 --quiet
```

When GPU is active, startup now prints:

```text
TensorFlow device: GPU (... detected)
```

**Q: Can I keep the old `honey-Legacy.py`?**  
A: Yes, but treat it as legacy-only. Use `python main.py` as the supported way to run training.

**Q: How do I plot learning curves?**  
A: Add to `train.py`:
```python
import matplotlib.pyplot as plt
plt.plot(episode_rewards)
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.savefig('reward_curve.png')
```

**Q: Can I make the agent learn multiple behaviors?**  
A: Yes! Add new entities/rewards in `config.py` and `environment.py`. See README "Next Improvements."

---

## You're Ready!

Go train your agent, experiment boldly, and enjoy the learning journey. 🐝

Questions? Check [README.md](README.md) for full explanations.
