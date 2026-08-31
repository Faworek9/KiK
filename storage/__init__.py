"""Storage module for tic-tac-toe."""

from storage.q_table_storage import load_q_table, save_q_table
from storage.paths import get_data_dir, get_q_table_path, get_results_path

__all__ = [
    "load_q_table",
    "save_q_table",
    "get_data_dir",
    "get_q_table_path",
    "get_results_path",
]
