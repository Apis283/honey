#!/usr/bin/env bash
set -euo pipefail

EPISODES="100"
QUIET="false"
SKIP_INSTALL="false"

usage() {
  echo "Usage: bash ./run_ubuntu.sh [--episodes N|-e N] [--quiet|-q] [--skip-install]"
  echo "Example: bash ./run_ubuntu.sh --episodes 1000 --quiet"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --episodes|-e)
      if [[ $# -lt 2 ]]; then
        echo "Error: --episodes requires a value"
        usage
        exit 1
      fi
      EPISODES="$2"
      shift 2
      ;;
    --quiet|-q)
      QUIET="true"
      shift
      ;;
    --skip-install)
      SKIP_INSTALL="true"
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      if [[ "$1" =~ ^[0-9]+$ ]]; then
        EPISODES="$1"
        shift
      else
        echo "Error: unknown argument '$1'"
        usage
        exit 1
      fi
      ;;
  esac
done

if ! [[ "$EPISODES" =~ ^[0-9]+$ ]] || [[ "$EPISODES" -lt 1 ]]; then
  echo "Error: episodes must be a positive integer"
  exit 1
fi

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  if command -v python3 >/dev/null 2>&1; then
    python3 -m venv .venv
  elif command -v python >/dev/null 2>&1; then
    python -m venv .venv
  else
    echo "Error: python3/python not found on PATH"
    exit 1
  fi
fi

PYTHON_CMD=".venv/bin/python"

if [ "$SKIP_INSTALL" = "false" ]; then
  "$PYTHON_CMD" -m pip install --upgrade pip
  "$PYTHON_CMD" -m pip install -r requirements.txt
fi

if [ "$QUIET" = "true" ]; then
  "$PYTHON_CMD" main.py --episodes "$EPISODES" --quiet
else
  "$PYTHON_CMD" main.py --episodes "$EPISODES"
fi
