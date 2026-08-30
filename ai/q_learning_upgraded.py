"""Upgraded Q-learning agent for tic-tac-toe with D4 board symmetry reduction."""

import random
from typing import Optional, Dict, List, Tuple
import config
from game.board import Board, available_moves, to_state_key

# 8 D4 dihedral group symmetries of 3x3 board (permutations of positions 0..8)
SYMMETRIES: Tuple[Tuple[int, ...], ...] = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8),  # Identity
    (2, 5, 8, 1, 4, 7, 0, 3, 6),  # Rot 90 cw
    (8, 7, 6, 5, 4, 3, 2, 1, 0),  # Rot 180
    (6, 3, 0, 7, 4, 1, 8, 5, 2),  # Rot 270 cw
    (2, 1, 0, 5, 4, 3, 8, 7, 6),  # Flip Horizontal (left-right)
    (6, 7, 8, 3, 4, 5, 0, 1, 2),  # Flip Vertical (up-down)
    (0, 3, 6, 1, 4, 7, 2, 5, 8),  # Transpose main diagonal
    (8, 5, 2, 7, 4, 1, 6, 3, 0),  # Transpose anti-diagonal
)


def transform_state(state_key: str, p: Tuple[int, ...]) -> str:
    """Transform a 9-character board state string using permutation p."""
    chars = ['0'] * 9
    for old_pos in range(9):
        chars[p[old_pos]] = state_key[old_pos]
    return "".join(chars)


def get_canonical_state_action(state_key: str, move: int) -> Tuple[str, int]:
    """Find canonical (state_key, move) pair under D4 symmetry group.
    
    1. Finds all symmetries that minimize the transformed state string.
    2. Among those, picks the symmetry that minimizes the transformed move index.
    
    Returns:
        (canonical_state_key, canonical_move)
    """
    best_state: Optional[str] = None
    best_move: Optional[int] = None
    
    for p in SYMMETRIES:
        trans_state = transform_state(state_key, p)
        trans_move = p[move]
        
        if best_state is None or trans_state < best_state:
            best_state = trans_state
            best_move = trans_move
        elif trans_state == best_state:
            if best_move is None or trans_move < best_move:
                best_move = trans_move
                
    assert best_state is not None and best_move is not None
    return best_state, best_move


class UpgradedQLearningAgent:
    """Upgraded Q-learning agent with board symmetry reduction (D4 group)."""
    
    def __init__(self, epsilon: float = config.INITIAL_EPSILON):
        """Initialize Q-learning agent.
        
        Args:
            epsilon: Exploration rate (0-1)
        """
        self.q_table: Dict[str, Dict[str, float]] = {}
        self.epsilon = epsilon
    
    def state_to_key(self, board: Board) -> str:
        """Convert board to string key for Q-table.
        
        Args:
            board: Current board state
            
        Returns:
            String key for Q-table
        """
        return to_state_key(board)
    
    def choose_move(self, board: Board, available_moves_list: Optional[List[int]] = None) -> int:
        """Choose a move using epsilon-greedy policy with canonical symmetry mapping.
        
        Args:
            board: Current board state
            available_moves_list: List of available moves (optional, will compute if None)
            
        Returns:
            Chosen move position
        """
        if available_moves_list is None:
            available_moves_list = available_moves(board)
        
        # Epsilon-greedy: explore with probability epsilon
        if random.random() < self.epsilon:
            return random.choice(available_moves_list)
        
        state_key = self.state_to_key(board)
        return self.get_best_move(state_key, available_moves_list)
    
    def get_best_move(self, state_key: str, available_moves_list: List[int]) -> int:
        """Get the best move for a state from Q-table using symmetry mapping.
        
        Args:
            state_key: State key in Q-table
            available_moves_list: List of available moves
            
        Returns:
            Move with highest Q-value (ties broken randomly)
        """
        best_value = -float('inf')
        best_moves: List[int] = []
        
        for move in available_moves_list:
            canon_state, canon_move = get_canonical_state_action(state_key, move)
            move_str = str(canon_move)
            
            if canon_state in self.q_table and move_str in self.q_table[canon_state]:
                val = self.q_table[canon_state][move_str]
                if val > best_value:
                    best_value = val
                    best_moves = [move]
                elif val == best_value:
                    best_moves.append(move)
        
        if not best_moves:
            return random.choice(available_moves_list)
        
        return random.choice(best_moves)
    
    def update_q_value(self, state_key: str, move: int, reward: float):
        """Update Q-value for a state-action pair using canonical symmetry.
        
        Args:
            state_key: State key in Q-table
            move: Move that was taken
            reward: Reward received
        """
        canon_state, canon_move = get_canonical_state_action(state_key, move)
        move_str = str(canon_move)
        
        if canon_state not in self.q_table:
            self.q_table[canon_state] = {}
        
        if move_str not in self.q_table[canon_state]:
            self.q_table[canon_state][move_str] = 0.0
        
        self.q_table[canon_state][move_str] = round(
            self.q_table[canon_state][move_str] + reward, 2
        )
    
    def update_from_history(self, history: List[Tuple[int, str]], reward: float, gamma: float):
        """Update Q-values from game history with discounting and symmetry reduction.
        
        History is already reversed before calling this function.
        
        Args:
            history: List of (move, state_key) tuples, reversed (most recent first)
            reward: Final reward
            gamma: Discount factor
        """
        for y, (move, state_key) in enumerate(history):
            discounted_reward = reward * (gamma ** y)
            self.update_q_value(state_key, move, discounted_reward)
    
    def decay_epsilon(self, decay: float = config.EPSILON_DECAY, min_epsilon: float = config.MIN_EPSILON):
        """Decay epsilon for less exploration over time.
        
        Args:
            decay: Amount to decay epsilon
            min_epsilon: Minimum epsilon value
        """
        if self.epsilon > min_epsilon:
            self.epsilon = round(self.epsilon - decay, 2)
    
    def set_epsilon(self, epsilon: float):
        """Set epsilon to a specific value.
        
        Args:
            epsilon: New epsilon value
        """
        self.epsilon = epsilon
    
    def get_q_table(self) -> Dict[str, Dict[str, float]]:
        """Get the Q-table (for storage).
        
        Returns:
            Copy of Q-table with epsilon included
        """
        result = self.q_table.copy()
        result["E"] = self.epsilon
        return result
    
    def set_q_table(self, q_table: Dict[str, Dict[str, float]]):
        """Set the Q-table (for loading).
        
        Args:
            q_table: Q-table to load (may include "E" for epsilon)
        """
        self.q_table = q_table.copy()
        
        # Extract epsilon if present
        if "E" in self.q_table:
            self.epsilon = self.q_table["E"]
            del self.q_table["E"]
        else:
            self.epsilon = config.INITIAL_EPSILON
    
    def record_move(self, board: Board, move: int):
        """Record a move with zero reward (for exploration).
        
        Args:
            board: Current board state
            move: Move that was taken
        """
        state_key = self.state_to_key(board)
        self.update_q_value(state_key, move, 0.0)


# Alias for backward compatibility / flexibility
QLearningAgent = UpgradedQLearningAgent
