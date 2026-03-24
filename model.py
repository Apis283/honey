"""
Model module: Neural network Q-learning function approximator.
"""

import tensorflow as tf
from config import STATE_SIZE, NUM_ACTIONS, LEARNING_RATE

# Global model instance
model = None
_tf_devices_configured = False


def configure_tensorflow_devices(verbose=True):
    """
    Configure TensorFlow devices and report whether GPU is available.

    Returns:
        bool: True if at least one GPU is available, else False
    """
    global _tf_devices_configured

    gpus = tf.config.list_physical_devices('GPU')

    # Memory growth avoids TensorFlow grabbing all VRAM at startup.
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:
            # Safe to continue; TensorFlow may already be initialized.
            pass

    _tf_devices_configured = True

    if verbose:
        if gpus:
            print(f"TensorFlow device: GPU ({len(gpus)} detected)")
        else:
            print("TensorFlow device: CPU (no GPU detected)")

    return len(gpus) > 0


def build_model():
    """
    Create a neural network for Q-learning.
    
    Architecture:
    - Input: STATE_SIZE neurons (25 grid cells + 4 vision cells)
    - Hidden 1: 32 neurons with ReLU activation
    - Hidden 2: 16 neurons with ReLU activation
    - Output: NUM_ACTIONS neurons with linear activation (Q-values for each action)
    
    The model learns Q(state, action) values via MSE loss.
    
    Returns:
        tf.keras.Model: Compiled sequential model
    """
    model = tf.keras.Sequential([
        tf.keras.Input(shape=(STATE_SIZE,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(NUM_ACTIONS, activation='linear')  # Q-values
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='mse'  # Mean squared error for Bellman target
    )
    
    return model


def initialize_model():
    """Initialize or load the global model instance."""
    global model

    if not _tf_devices_configured:
        configure_tensorflow_devices(verbose=True)

    model = build_model()


def get_model():
    """Return the global model instance."""
    return model
