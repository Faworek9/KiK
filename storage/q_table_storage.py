import os
import json
from typing import Dict


def load_q_table(path: str) -> Dict:
    """Load Q-table from JSON file.
    
    Args:
        path: Path to JSON file
        
    Returns:
        Q-table dictionary, or empty dict if file not found
    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_q_table(path: str, q_table: Dict):
    """Save Q-table to JSON file.
    
    Args:
        path: Path to JSON file
        q_table: Q-table dictionary to save
    """
    dir_name = os.path.dirname(os.path.abspath(path))
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(q_table, f)
