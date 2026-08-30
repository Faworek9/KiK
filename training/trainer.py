"""Trainer for tic-tac-toe Q-learning."""

from dataclasses import dataclass, field
import random
import config
from game.board import create_empty_board, available_moves, to_state_key
from game.game import Game
from game.rules import get_game_result
from ai.move_finder_minimax import StrategicMoveFinder
from ai.move_finder_hybrid import HybridStrategicMoveFinder
from ai.move_finder_legacy import LegacyStrategicMoveFinder
from ai.q_learning import QLearningAgent
from storage.q_table_storage import load_q_table, save_q_table


@dataclass
class TrainingStats:
    """Statistics for training."""
    wins: int = 0
    losses: int = 0
    draws: int = 0
    
    def record_win(self):
        """Record a win."""
        self.wins += 1
    
    def record_loss(self):
        """Record a loss."""
        self.losses += 1
    
    def record_draw(self):
        """Record a draw."""
        self.draws += 1
    
    def reset(self):
        """Reset all statistics."""
        self.wins = 0
        self.losses = 0
        self.draws = 0
    
    def total_games(self) -> int:
        """Get total number of games played."""
        return self.wins + self.losses + self.draws


class Trainer:
    """Trainer for tic-tac-toe with configurable strategies."""
    
    def __init__(self):
        """Initialize trainer with strategies from config."""
        self.stats = TrainingStats()
        self.q_agent = QLearningAgent(epsilon=config.INITIAL_EPSILON)
        
        # Create strategic finders based on algorithm selection
        if config.STRATEGIC_ALGORITHM == config.StrategicAlgorithmType.MINIMAX:
            self.strategic_finder_x = StrategicMoveFinder(config.PLAYER_X)
            self.strategic_finder_o = StrategicMoveFinder(config.PLAYER_O)
        elif config.STRATEGIC_ALGORITHM == config.StrategicAlgorithmType.HYBRID:
            self.strategic_finder_x = HybridStrategicMoveFinder(config.PLAYER_X)
            self.strategic_finder_o = HybridStrategicMoveFinder(config.PLAYER_O)
        else:  # LEGACY
            self.strategic_finder_x = LegacyStrategicMoveFinder(config.PLAYER_X)
            self.strategic_finder_o = LegacyStrategicMoveFinder(config.PLAYER_O)
        
        # Determine which player uses Q-learning
        self.q_learning_player = None
        if config.PLAYER_X_STRATEGY == config.StrategyType.Q_LEARNING:
            self.q_learning_player = config.PLAYER_X
        elif config.PLAYER_O_STRATEGY == config.StrategyType.Q_LEARNING:
            self.q_learning_player = config.PLAYER_O
        
        # Set file paths based on Q-learning player
        if self.q_learning_player == config.PLAYER_X:
            self.q_table_path = config.Q_TABLE_X_PATH
            self.results_path = config.RESULTS_X_PATH
        else:
            self.q_table_path = config.Q_TABLE_O_PATH
            self.results_path = config.RESULTS_O_PATH
        
        # Load existing Q-table if available
        self._load_q_table()
    
    def _load_q_table(self):
        """Load Q-table from file."""
        q_table = load_q_table(self.q_table_path)
        if q_table:
            self.q_agent.set_q_table(q_table)
    
    def _save_q_table(self):
        """Save Q-table to file."""
        q_table = self.q_agent.get_q_table()
        save_q_table(self.q_table_path, q_table)
    
    def _save_stats(self):
        """Save statistics to file."""
        total = self.stats.total_games()
        if total == 0:
            return
        
        loss_pct = (self.stats.losses / total) * 100
        draw_pct = (self.stats.draws / total) * 100
        win_pct = (self.stats.wins / total) * 100
        
        with open(self.results_path, 'a') as f:
            f.write(f"porazki: {loss_pct:.1f}%    remisy: {draw_pct:.1f}%     wygrane: {win_pct:.1f}%\n")
    
    def _create_player(self, player: int, strategy: config.StrategyType):
        """Create a player function based on strategy type.
        
        Args:
            player: PLAYER_X or PLAYER_O
            strategy: StrategyType to use
            
        Returns:
            Player function that takes board and returns move
        """
        if strategy == config.StrategyType.Q_LEARNING:
            def player(board):
                return self.q_agent.choose_move(board, available_moves(board))
            return player
        elif strategy == config.StrategyType.STRATEGIC:
            finder = self.strategic_finder_x if player == config.PLAYER_X else self.strategic_finder_o
            def player(board):
                return finder.choose_move(board)
            return player
        else:  # RANDOM
            def player(board):
                return random.choice(available_moves(board))
            return player
    
    def _play_game(self):
        """Play a single game and update Q-table."""
        # If no Q-learning player, just play without updating
        if self.q_learning_player is None:
            return
        
        # Create players based on config
        player_x = self._create_player(config.PLAYER_X, config.PLAYER_X_STRATEGY)
        player_o = self._create_player(config.PLAYER_O, config.PLAYER_O_STRATEGY)
        
        game = Game(player_x, player_o)
        result = game.play()
        history = game.get_history()
        
        # Determine reward based on result
        if result.winner == self.q_learning_player:
            reward = 1.0
            self.stats.record_win()
        elif result.winner is not None:
            reward = -1.0
            self.stats.record_loss()
        else:
            reward = 1.0  # Draw is positive
            self.stats.record_draw()
        
        # Update Q-table from history
        history_tuples = []
        for move, state in zip(history.moves, history.states):
            history_tuples.append((move, state))
        
        history_tuples.reverse()
        
        gamma = config.GAMMA_POSITIVE if reward > 0 else config.GAMMA_NEGATIVE
        self.q_agent.update_from_history(history_tuples, reward, gamma)
    
    def train(self, number_of_games: int = config.GAMES_COUNT):
        """Train the Q-learning agent.
        
        Args:
            number_of_games: Number of games to play
        """
        for game_num in range(1, number_of_games + 1):
            self._play_game()
            
            # Save progress periodically
            if game_num % config.SAVE_INTERVAL == 0:
                # Decay epsilon
                self.q_agent.decay_epsilon()
                
                # Save stats and Q-table
                self._save_stats()
                self._save_q_table()
                
                # Reset stats for next interval
                self.stats.reset()
        
        # Final save
        self._save_q_table()
