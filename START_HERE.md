# Honey Agent Setup Overview

Status: fully operational for Windows and Ubuntu.

## What You Have

Core modules:
- config.py
- environment.py
- model.py
- train.py
- persistence.py
- main.py

Support files:
- test_honey.py
- README.md
- QUICK_START.md
- AGENT_LEARNING_GUIDE.md
- run_windows.ps1
- run_ubuntu.sh

## Fast Start

Windows PowerShell:

```powershell
.\run_windows.ps1 -Episodes 100
```

Ubuntu:

```bash
bash ./run_ubuntu.sh --episodes 100
```

## Manual Commands

After activating your virtual environment:

```bash
python -m pip install -r requirements.txt
python -m unittest test_honey -v
python main.py --episodes 100
python main.py --episodes 5000 --quiet
```

## Learning Path

1. Read QUICK_START.md
2. Read README.md sections on environment, model, and training loop
3. Run tests in test_honey.py
4. Change values in config.py and retrain

## Debug Checklist

1. Verify dependencies:
   - `python -m pip show tensorflow numpy`
2. Verify imports:
   - `python -c "import config, environment, model, train"`
3. Run a minimal train:
   - `python main.py --episodes 1`

## Cross-Platform Notes

- Keep using `python main.py` as the main entry point.
- The same codebase and saved model files work on both OSes.
- Windows-only popup notifications are automatically skipped on Ubuntu.
- GPU is optional and depends on local TensorFlow environment support.

## Where to Go Next

- Start training: QUICK_START.md
- Deep explanations: README.md
- Study-focused notes: AGENT_LEARNING_GUIDE.md
- Legacy compatibility: honey-Legacy.py
