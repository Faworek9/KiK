"""Q-learning agent for tic-tac-toe."""

import random
import config
from game.board import Board, available_moves, to_state_key
from typing import Optional, Dict, List, Tuple


class QLearningAgent:
    """Q-learning agent for tic-tac-toe."""
    
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
        """Choose a move using epsilon-greedy policy.
        
        Corresponds to ruchAI() in original code.
        
        Args:
            board: Current board state
            available_moves_list: List of available moves (optional, will compute if None)
            
        Returns:
            Chosen move position
        """
        if available_moves_list is None:
            available_moves_list = available_moves(board)
        
        state_key = self.state_to_key(board)
        
        # If state not in Q-table, choose random move
        if state_key not in self.q_table:
            return random.choice(available_moves_list)
        
        # Epsilon-greedy: explore with probability epsilon
        if random.random() < self.epsilon:
            return random.choice(available_moves_list)
        
        # Exploit: choose best move from Q-table
        return self.get_best_move(state_key, available_moves_list)
    
    def get_best_move(self, state_key: str, available_moves_list: List[int]) -> int:
        """Get the best move for a state from Q-table.
        
        Corresponds to najlep() in original code.
        
        Args:
            state_key: State key in Q-table
            available_moves_list: List of available moves
            
        Returns:
            Move with highest Q-value
        """
        state_q = self.q_table[state_key]
        
        best_value = -float('inf')
        best_move = None
        
        for move in available_moves_list:
            move_str = str(move)
            if move_str in state_q:
                if state_q[move_str] > best_value:
                    best_value = state_q[move_str]
                    best_move = move
            elif best_move is None:
                # Move not in Q-table, use as fallback
                best_move = move
        
        # If no moves in Q-table, choose random
        if best_move is None:
            return random.choice(available_moves_list)
        
        return best_move
    
    def update_q_value(self, state_key: str, move: int, reward: float):
        """Update Q-value for a state-action pair.
        
        Corresponds to zamQ() in original code.
        
        Args:
            state_key: State key in Q-table
            move: Move that was taken
            reward: Reward received
        """
        move_str = str(move)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        
        if move_str not in self.q_table[state_key]:
            self.q_table[state_key][move_str] = 0.0
        
        self.q_table[state_key][move_str] = round(
            self.q_table[state_key][move_str] + reward, 2
        )
    
    def update_from_history(self, history: List[Tuple[int, str]], reward: float, gamma: float):
        """Update Q-values from game history with discounting.
        
        Corresponds to nag() and nagW() in original code.
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
        
        Corresponds to the zamQ(Q, stan, str(trans(dan)), 0) call in original code.
        
        Args:
            board: Current board state
            move: Move that was taken
        """
        state_key = self.state_to_key(board)
        self.update_q_value(state_key, move, 0.0)
