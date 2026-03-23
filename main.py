#!/usr/bin/env python3
"""
Main entry point for training the Honey Agent.

Usage:
  python main.py                    # Train with default config (100k episodes)
  python main.py --episodes 1000    # Train for 1000 episodes
"""

import sys
import argparse
from train import train, notify_completion
from config import EPISODES


def main():
    parser = argparse.ArgumentParser(
        description="Train the Honey Agent using Deep Q-Learning"
    )
    parser.add_argument(
        '--episodes',
        type=int,
        default=EPISODES,
        help=f'Number of episodes to train (default: {EPISODES})'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress printing'
    )
    
    args = parser.parse_args()
    
    print(f"Starting training for {args.episodes} episodes...")
    
    result = train(episodes=args.episodes, verbose=not args.quiet)
    
    message = (
        f"Training Summary:\n"
        f"  Episodes: {result['episodes_ran']}/{args.episodes}\n"
        f"  Time: {result['elapsed_seconds']:.1f} seconds\n"
        f"  Final epsilon: {result['epsilon_final']:.3f}\n"
        f"  Status: {'Completed' if result['completed'] else 'Interrupted'}"
    )
    
    notify_completion(message)
    
    return 0 if result['completed'] else 1


if __name__ == '__main__':
    sys.exit(main())
