"""Path utilities for training data and storage."""

import os
from typing import Optional
import config


def get_data_dir(algorithm: Optional[config.QLearningAlgorithmType] = None) -> str:
    """Get the data directory for a given Q-learning algorithm.
    
    Args:
        algorithm: Q-learning algorithm type (defaults to config.Q_LEARNING_ALGORITHM)
        
    Returns:
        Directory path for data storage
    """
    algo = algorithm if algorithm is not None else config.Q_LEARNING_ALGORITHM
    if algo == config.QLearningAlgorithmType.UPGRADED:
        return config.DATA_DIR_UPGRADED
    return config.DATA_DIR_LEGACY


def get_q_table_path(player: int, algorithm: Optional[config.QLearningAlgorithmType] = None) -> str:
    """Get Q-table file path for a player and algorithm.
    
    Args:
        player: Player ID (config.PLAYER_X or config.PLAYER_O)
        algorithm: Q-learning algorithm type (defaults to config.Q_LEARNING_ALGORITHM)
        
    Returns:
        Full path to the Q-table JSON file
    """
    data_dir = get_data_dir(algorithm)
    suffix = "X" if player == config.PLAYER_X else "O"
    return os.path.join(data_dir, f"q_{suffix}.json")


def get_results_path(player: int, algorithm: Optional[config.QLearningAlgorithmType] = None) -> str:
    """Get results statistics file path for a player and algorithm.
    
    Args:
        player: Player ID (config.PLAYER_X or config.PLAYER_O)
        algorithm: Q-learning algorithm type (defaults to config.Q_LEARNING_ALGORITHM)
        
    Returns:
        Full path to the results TXT file
    """
    data_dir = get_data_dir(algorithm)
    suffix = "X" if player == config.PLAYER_X else "O"
    return os.path.join(data_dir, f"wyniki_{suffix}.txt")
