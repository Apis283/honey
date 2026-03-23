"""
Training module: Main Q-learning training loop.
"""

import os
import time
import random
import numpy as np
from config import (
    EPISODES, MAX_STEPS_PER_EPISODE, EPSILON_START, EPSILON_END, 
    EPSILON_DECAY, GAMMA, PROGRESS_PRINT_EVERY, CHECKPOINT_EVERY, NUM_ACTIONS
)
from model import get_model, initialize_model
import environment
import persistence


def train(episodes=EPISODES, verbose=True):
    """
    Run the main Q-learning training loop.
    
    Args:
        episodes (int): Number of episodes to train for
        verbose (bool): Whether to print progress
    
    Returns:
        dict: Training summary with keys:
            - 'completed': bool, whether training finished or was interrupted
            - 'episodes_ran': int, actual number of episodes completed
            - 'epsilon_final': float, final exploration rate
            - 'elapsed_seconds': float, total training time
    """
    
    # Initialize
    initialize_model()
    persistence.load_state()
    
    model = get_model()
    epsilon = EPSILON_START
    start_time = time.time()
    episode_rewards = []
    
    completed = False
    last_episode = -1
    
    try:
        for episode in range(episodes):
            if verbose and episode % 50 == 0:
                print(f"\nEpisode {episode} | Epsilon: {epsilon:.3f}")
            
            # Reset world for fresh episode (skip first to use loaded state)
            if episode > 0:
                environment.reset_world()
            
            state = environment.get_state()
            total_reward = 0
            step_count = 0
            
            # Inner loop: steps within episode
            for step_num in range(MAX_STEPS_PER_EPISODE):
                step_count += 1
                
                # === EPSILON-GREEDY ACTION SELECTION ===
                if random.random() < epsilon:
                    # Explore: random action
                    action = random.randint(0, NUM_ACTIONS - 1)
                else:
                    # Exploit: best known action via Q-values
                    q_values = model.predict(state, verbose=0)[0]
                    action = np.argmax(q_values)
                
                # === TAKE ACTION ===
                reward, done = environment.step(action)
                total_reward += reward
                
                # === OBSERVE NEXT STATE ===
                next_state = environment.get_state()
                
                # === COMPUTE BELLMAN TARGET ===
                if done:
                    # Terminal state: target is just the immediate reward
                    target = reward
                else:
                    # Non-terminal: reward + discounted future reward
                    next_q_values = model.predict(next_state, verbose=0)[0]
                    future_reward = np.max(next_q_values)
                    target = reward + GAMMA * future_reward
                
                # === UPDATE Q-VALUE ===
                # Only update the Q-value for the action taken
                targets = model.predict(state, verbose=0)
                targets[0][action] = target
                
                # Train on this single step (online learning)
                model.fit(state, targets, epochs=1, verbose=0)
                
                state = next_state
                
                if done:
                    break
            
            # === END-OF-EPISODE BOOKKEEPING ===
            epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)
            last_episode = episode
            episode_rewards.append(total_reward)
            
            # Print episode results
            if verbose and episode % 20 == 0:
                print(f"Episode {episode} | Reward: {total_reward:.2f} | Steps: {step_count}")
            
            # Print moving average
            if verbose and (episode + 1) % 50 == 0:
                recent_rewards = episode_rewards[-50:]
                avg_recent = sum(recent_rewards) / len(recent_rewards)
                print(f"  → Average reward (last {len(recent_rewards)} episodes): {avg_recent:.3f}")
            
            # Print heartbeat (progress indicator)
            if verbose and episode % PROGRESS_PRINT_EVERY == 0:
                elapsed = time.time() - start_time
                episodes_done = episode + 1
                avg_sec_per_ep = elapsed / episodes_done
                eta_sec = max(0, (episodes - episodes_done) * avg_sec_per_ep)
                print(f"  → Heartbeat | {episodes_done}/{episodes} episodes | "
                      f"Elapsed: {elapsed:.1f}s | ETA: {eta_sec:.1f}s")
            
            # Checkpoint (periodic save)
            if episode % CHECKPOINT_EVERY == 0:
                persistence.save_state()
        
        completed = True
    
    except KeyboardInterrupt:
        if verbose:
            print("\n[Training interrupted]")
    
    finally:
        # Always save before exit
        persistence.save_state()
    
    elapsed_total = time.time() - start_time
    
    return {
        'completed': completed,
        'episodes_ran': last_episode + 1,
        'epsilon_final': epsilon,
        'elapsed_seconds': elapsed_total
    }


def notify_completion(message):
    """Show training completion notification (terminal bell + Windows popup)."""
    print("\a", end="")  # Terminal bell
    print(message)
    
    # Windows popup notification
    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, message, "Honey Agent Training", 0x40)
        except Exception:
            pass
