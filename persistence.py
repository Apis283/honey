"""
Persistence module: Save and load agent training state across sessions.
"""

import os
import json
import tensorflow as tf
from model import get_model
import environment


def save_state():
    """
    Save the current agent state to disk.
    
    Saves:
    - agent_model.keras: The trained neural network
    - world_state.json: Agent/food/poison positions (for reproducibility)
    """
    model = get_model()
    if model is None:
        print("Warning: Model not initialized; skipping save.")
        return
    
    model.save('agent_model.keras')
    
    with open('world_state.json', 'w') as f:
        json.dump({
            'agent_pos': environment.agent_pos,
            'food_pos': environment.food_pos,
            'poison_pos': environment.poison_pos
        }, f, indent=2)
    
    print("Saved agent model & world state.")


def load_state():
    """
    Load previously saved agent state from disk if available.
    
    If model file exists, load it.
    If world state file exists, restore positions.
    If neither exist, initialize a fresh world.
    """
    model = get_model()
    
    # Try to load model
    if os.path.exists('agent_model.keras'):
        from model import model as global_model
        import model as model_module
        loaded_model = tf.keras.models.load_model('agent_model.keras')
        model_module.model = loaded_model
        print("Loaded existing model.")
    
    # Try to load world state
    if os.path.exists('world_state.json'):
        with open('world_state.json') as f:
            data = json.load(f)
            environment.agent_pos = data['agent_pos']
            environment.food_pos = data['food_pos']
            environment.poison_pos = data['poison_pos']
        print("Loaded existing world state.")
    else:
        # Fresh start
        environment.reset_world()
